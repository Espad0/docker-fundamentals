"""Download the model's files into a folder.

Used at build time (to bake the model into the image) or at start-up (if the
folder is empty). Pinning MODEL_REVISION means you always get the same files.
"""
import os
import sys

from huggingface_hub import snapshot_download

MODEL_ID = os.getenv("MODEL_ID", "distilbert/distilbert-base-uncased-finetuned-sst-2-english")
MODEL_REVISION = os.getenv("MODEL_REVISION", "714eb0fa89d2f80546fda750413ed43d93601a13")
MODEL_DIR = os.getenv("MODEL_DIR", "/models/sst2")
# The repository holds the same weights in five formats (~1.3 GB). We only need these.
FILES = ["config.json", "model.safetensors", "tokenizer_config.json", "vocab.txt"]


def download(target=MODEL_DIR):
    return snapshot_download(MODEL_ID, revision=MODEL_REVISION, local_dir=target, allow_patterns=FILES)


if __name__ == "__main__":
    print("model files in", download(sys.argv[1] if len(sys.argv) > 1 else MODEL_DIR))
