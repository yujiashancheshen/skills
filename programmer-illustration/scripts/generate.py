#!/usr/bin/env python3
"""自包含的文生图脚本（技能自带，克隆即用）。

用法：
    python generate.py --prompt "完整提示词" --ratio 16:9 \
        --style 科技插画风 --title 实时风控决策引擎
    # 出图默认落在「当前工作目录」，文件名为「风格-标题.png」；
    # 也可用 --out 指定文件名或绝对路径。

配置：
    复制 config.example.json 为 config.json（与本脚本同级的技能根目录），
    把 active 设成要用的通道，再给那一家填上真实 key。结构为：
        { "active": "openai", "providers": { "openai": { "api_key", "base_url", "model" }, ... } }
    config.json 已被 .gitignore 忽略，不会上传。

支持通道：openai | gemini | doubao | qwen。
仅依赖标准库 + requests。
新增通道：写 generate_xxx(cfg, prompt, ratio) -> bytes，并注册进 PROVIDERS。
"""
import argparse
import base64
import json
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("缺少依赖：请先执行 `pip install requests`")

# 路径相对脚本自身定位，无论在哪个工作目录调用都能找到配置。
SKILL_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = SKILL_DIR / "config.json"

# 各通道内置默认值。base_url：doubao 给公开官方地址；openai/gemini/qwen 走网关，须在 config 填。
# model：默认填的是本环境验证可用的版本，换别的网关/官方时按其支持的模型名改即可。
DEFAULT_PROVIDERS = {
    "openai": {"base_url": "", "model": "gpt-image-2"},
    "gemini": {"base_url": "", "model": "gemini-3.1-flash-image-preview"},
    "doubao": {"base_url": "https://ark.cn-beijing.volces.com/api/v3/images/generations",
               "model": "doubao-seedream-5-0-260128"},
    "qwen": {"base_url": "", "model": "qwen-image-2.0"},
}


def load_config():
    """读取 config.json，返回 (active, providers)。文件不存在时仅用内置默认。"""
    user = {}
    if CONFIG_PATH.exists():
        try:
            user = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            sys.exit(f"config.json 格式错误：{e}")
    active = user.get("active", "openai")
    user_providers = user.get("providers", {})
    # 合并：内置默认 < config.json 里各通道的非空字段
    merged = {}
    for name, defaults in DEFAULT_PROVIDERS.items():
        cfg = dict(defaults)
        cfg.update({k: v for k, v in user_providers.get(name, {}).items() if v not in (None, "")})
        merged[name] = cfg
    return active, merged


ACTIVE, PROVIDER_CFG = load_config()


def require(cfg: dict, provider: str, *keys: str) -> tuple:
    """取出 cfg 里的必填项，缺失则给出指向 config.json 的清晰报错。"""
    values = []
    for key in keys:
        val = cfg.get(key)
        if not val:
            sys.exit(f"缺少配置 providers.{provider}.{key}："
                     f"请在 {CONFIG_PATH} 里填写（参考同目录 config.example.json）")
        values.append(val)
    return tuple(values)


# ---------------------------------------------------------------------------
# 通道：gemini（gemini-3.1-flash-image-preview，OpenAI 兼容 chat/completions 网关）
# 排版/多元素一致性强，中文渲染也不错。
# 走 OpenAI 兼容网关（你的代理服务 / OpenRouter 等）的 chat 接口：
# messages + modalities=["text","image"]，图片以裸 base64 放在
# choices[0].message.content 里 type=image_url 的项。
# 注意：这不是 Google 官方原生 API（官方是 generativelanguage 的
# :generateContent + contents/parts 结构）；要直连 Google 官方需改写本函数。
# base_url 直接写到 .../chat/completions；比例靠 prompt 内文字约束（接口不收 ratio 参数）。
# ---------------------------------------------------------------------------
def generate_gemini(cfg: dict, prompt: str, ratio: str) -> bytes:
    key, base = require(cfg, "gemini", "api_key", "base_url")
    url = base.strip()
    if not url.endswith("/chat/completions"):
        url = url.rstrip("/") + "/chat/completions"
    model = cfg["model"].strip()
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["text", "image"],
    }
    r = requests.post(url, headers={"Authorization": f"Bearer {key}",
                                    "Content-Type": "application/json"},
                      json=body, timeout=1000)
    if r.status_code != 200:
        sys.exit(f"Gemini 出图失败 {r.status_code}: {r.text[:500]}")
    data = r.json()
    content = data.get("choices", [{}])[0].get("message", {}).get("content")
    parts = content if isinstance(content, list) else [content]
    for part in parts:
        if isinstance(part, dict) and part.get("type") == "image_url":
            u = (part.get("image_url") or {}).get("url", "")
            if u:
                if u.startswith("data:"):
                    u = u.split(",", 1)[-1]
                return base64.b64decode(u)
    sys.exit(f"Gemini 返回里没有图片数据：{json.dumps(data)[:500]}")


# ---------------------------------------------------------------------------
# 通道：openai（gpt-image-2，OpenAI 兼容 images/generations 网关）
# 生态成熟；中文文字渲染偶尔会糊，纯中文技术图慎用。
# ---------------------------------------------------------------------------
# gpt-image 无真正的 16:9，最接近的是 1536x1024（3:2），故 16:9 也映射到它。
_OPENAI_SIZE = {"16:9": "1536x1024", "3:2": "1536x1024", "1:1": "1024x1024", "9:16": "1024x1536"}


def generate_openai(cfg: dict, prompt: str, ratio: str) -> bytes:
    key, base = require(cfg, "openai", "api_key", "base_url")
    base = base.rstrip("/")
    model = cfg["model"]
    body = {"model": model, "prompt": prompt, "size": _OPENAI_SIZE.get(ratio, "1536x1024"), "n": 1}
    r = requests.post(f"{base}/images/generations",
                      headers={"Authorization": f"Bearer {key}"}, json=body, timeout=1000)
    if r.status_code != 200:
        sys.exit(f"OpenAI 出图失败 {r.status_code}: {r.text[:500]}")
    item = r.json()["data"][0]
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    if item.get("url"):
        return requests.get(item["url"], timeout=120).content
    sys.exit("OpenAI 返回里没有图片数据")


# ---------------------------------------------------------------------------
# 通道：qwen（qwen-image-2.0，DashScope multimodal-generation）
# 中文文字渲染稳；同步返回。接口只给图片的临时 OSS 链接（约 7 天过期），
# 脚本已即时把链接内容下载成本地字节落盘，本地文件不受链接过期影响；
# 该接口不提供 base64，故下载是唯一取图方式。
# base_url 写到完整的 .../multimodal-generation/generation 端点。
# ---------------------------------------------------------------------------
_QWEN_SIZE = {"16:9": "1664*928", "3:2": "1584*1056", "1:1": "1328*1328", "9:16": "928*1664"}


def generate_qwen(cfg: dict, prompt: str, ratio: str) -> bytes:
    key, base = require(cfg, "qwen", "api_key", "base_url")
    url = base.strip()
    model = cfg["model"].strip()
    body = {
        "model": model,
        "input": {"messages": [{"role": "user", "content": [{"text": prompt}]}]},
        "parameters": {"size": _QWEN_SIZE.get(ratio, "1664*928"), "n": 1,
                       "prompt_extend": True, "watermark": False},
    }
    r = requests.post(url, headers={"Authorization": f"Bearer {key}",
                                    "Content-Type": "application/json"},
                      json=body, timeout=1000)
    if r.status_code != 200:
        sys.exit(f"千问出图失败 {r.status_code}: {r.text[:500]}")
    data = r.json()
    try:
        content = data["output"]["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        sys.exit(f"千问返回结构异常：{json.dumps(data)[:500]}")
    for part in content:
        if isinstance(part, dict) and part.get("image"):
            return requests.get(part["image"], timeout=120).content
    sys.exit(f"千问返回里没有图片数据：{json.dumps(data)[:500]}")


# ---------------------------------------------------------------------------
# 通道：doubao（doubao-seedream-5-0-260128，火山方舟 Ark images/generations）
# 中文文字渲染稳；seedream 5.0 要求出图 >= 3686400 像素，故尺寸偏大。
# base_url 直接写到 .../images/generations，只需一个 api_key。
# ---------------------------------------------------------------------------
_DOUBAO_SIZE = {"16:9": "2560x1440", "3:2": "2400x1600", "1:1": "2048x2048", "9:16": "1440x2560"}


def generate_doubao(cfg: dict, prompt: str, ratio: str) -> bytes:
    (key,) = require(cfg, "doubao", "api_key")
    url = cfg["base_url"].strip()
    if not url.endswith("/images/generations"):
        url = url.rstrip("/") + "/images/generations"
    model = cfg["model"].strip()
    body = {"model": model, "prompt": prompt,
            "size": _DOUBAO_SIZE.get(ratio, "2560x1440"),
            "response_format": "url", "n": 1, "watermark": False}
    r = requests.post(url, headers={"Authorization": f"Bearer {key}",
                                    "Content-Type": "application/json"},
                      json=body, timeout=1000)
    if r.status_code != 200:
        sys.exit(f"豆包出图失败 {r.status_code}: {r.text[:500]}")
    item = r.json()["data"][0]
    if item.get("url"):
        return requests.get(item["url"], timeout=120).content
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    sys.exit(f"豆包返回里没有图片数据：{json.dumps(r.json())[:500]}")


PROVIDERS = {
    "openai": generate_openai,
    "gemini": generate_gemini,
    "doubao": generate_doubao,
    "qwen": generate_qwen,
}


def _safe_name(text: str) -> str:
    """把风格/标题清理成可做文件名的片段：去掉非法字符、压缩空白、限长。"""
    cleaned = re.sub(r'[\\/:*?"<>|\r\n\t]+', "", text).strip()
    cleaned = re.sub(r"\s+", "", cleaned)
    return cleaned[:40]


def resolve_out(out_arg: str, style: str, title: str) -> Path:
    """决定输出路径：
    --out 绝对路径 → 原样；--out 相对路径 → 相对当前工作目录；
    --out 为空 → 当前工作目录下「风格-标题.png」，重名自动加序号。
    """
    if out_arg:
        p = Path(out_arg)
        return p if p.is_absolute() else (Path.cwd() / p)

    parts = [_safe_name(style), _safe_name(title)]
    stem = "-".join(p for p in parts if p) or "img"
    candidate = Path.cwd() / f"{stem}.png"
    seq = 2
    while candidate.exists():
        candidate = Path.cwd() / f"{stem}-{seq}.png"
        seq += 1
    return candidate


def main():
    ap = argparse.ArgumentParser(description="文生好看的图 - 自包含出图脚本")
    ap.add_argument("--prompt", required=True, help="填好的完整提示词")
    ap.add_argument("--ratio", default="16:9", help="比例，如 16:9 / 3:2 / 1:1 / 9:16")
    ap.add_argument("--style", default="", help="风格中文名（用于拼输出文件名，如 科技插画风）")
    ap.add_argument("--title", default="", help="图的主标题（用于拼输出文件名）")
    ap.add_argument("--out", default="", help="输出文件名或路径（默认落在当前工作目录）")
    ap.add_argument("--provider", default=ACTIVE,
                    help="openai | gemini | doubao | qwen，默认读 config 的 active")
    args = ap.parse_args()

    provider = args.provider.lower()
    fn = PROVIDERS.get(provider)
    if not fn:
        sys.exit(f"未知 provider: {args.provider}，可选 {list(PROVIDERS)}")
    cfg = PROVIDER_CFG[provider]

    out = resolve_out(args.out, args.style, args.title)
    print(f"[generate] provider={provider} ratio={args.ratio} -> {out}")
    img = fn(cfg, args.prompt, args.ratio)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(img)
    print(f"[generate] 完成，已写入 {out} ({len(img)} bytes)")


if __name__ == "__main__":
    main()
