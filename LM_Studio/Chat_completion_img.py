import requests
import base64
import mimetypes
from pathlib import Path
import json

# ---- Config ----
URL = "http://localhost:1234/v1/chat/completions"  # LM Studio server (OpenAI-compatible)
MODEL = "qwen/qwen3-vl-4b"
IMAGE_PATH = "img.png"
QUESTION = "What programming languages are mentioned in this image?"

def encode_image_to_data_uri(path: str) -> str:
    """
    Reads a local image and returns a data: URI suitable for image_url.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {p.resolve()}")

    # Best-effort MIME type (defaults to jpeg if unknown)
    mime, _ = mimetypes.guess_type(p.name)
    if mime is None:
        mime = "image/jpeg"

    b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

image_data_uri = encode_image_to_data_uri(IMAGE_PATH)

payload = {
    "model": MODEL,
    "temperature": 0.7,
    "messages": [
        {"role": "system", "content": "You are a helpful assistant that can see images."},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": QUESTION},
                # Send the image as a data: URI
                {"type": "image_url", "image_url": {"url": image_data_uri}}
            ]
        }
    ]
}

resp = requests.post(URL, json=payload, headers={"Content-Type": "application/json"})
resp.raise_for_status()
data = resp.json()

print("--- Server Response ---")
print(data["choices"][0]["message"]["content"])
