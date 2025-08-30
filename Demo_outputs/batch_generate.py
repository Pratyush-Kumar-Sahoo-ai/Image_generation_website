import argparse
import csv
import hashlib
import os
import sys
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter, Retry


def stable_seed_from_text(text: str) -> int:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(digest[:12], 16)


def build_session(timeout: float) -> requests.Session:
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.request = _wrap_with_timeout(session.request, timeout)
    return session


def _wrap_with_timeout(func, timeout):
    def wrapped(method, url, **kwargs):
        kwargs.setdefault("timeout", timeout)
        return func(method, url, **kwargs)
    return wrapped


def save_png(content: bytes, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate two images per prompt via local Lumina API")
    parser.add_argument("csv_path", type=str, help="Path to CSV with columns: prompt_id,prompt")
    parser.add_argument("output_dir", type=str, help="Directory to save generated images")
    parser.add_argument("--api", type=str, default="http://localhost:8000/generate", help="Generation API endpoint URL")
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--scale", type=float, default=4.0)
    parser.add_argument("--timeout", type=float, default=600.0, help="Request timeout in seconds")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of rows processed")
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    out_dir = Path(args.output_dir)

    if not csv_path.exists():
        print(f"CSV not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    session = build_session(args.timeout)

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not {"prompt_id", "prompt"}.issubset(set(reader.fieldnames or [])):
            print("CSV must contain columns: prompt_id,prompt", file=sys.stderr)
            sys.exit(1)

        processed = 0
        for row in reader:
            if args.limit is not None and processed >= args.limit:
                break
            prompt_id = str(row["prompt_id"]).strip()
            prompt = str(row["prompt"]).strip()
            if not prompt_id or not prompt:
                continue

            base_seed = stable_seed_from_text(f"{prompt_id}|{prompt}")
            for i in range(2):
                payload = {
                    "prompt": prompt,
                    "height": args.height,
                    "width": args.width,
                    "guidance_scale": args.scale,
                    "num_inference_steps": args.steps,
                    "seed": (base_seed + i) % (2**31 - 1),
                }
                try:
                    resp = session.post(args.api, json=payload)
                    resp.raise_for_status()
                except requests.RequestException as e:
                    print(f"[ERROR] prompt_id={prompt_id} idx={i} request failed: {e}", file=sys.stderr)
                    continue

                filename = f"{prompt_id}_{i+1}.png"
                save_png(resp.content, out_dir / filename)
            processed += 1

    print("Done.")


if __name__ == "__main__":
    main() 