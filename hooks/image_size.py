"""MkDocs hook: give every <img> its real width and height.

The guide's screenshots are lazy-loaded. Without width/height the browser
treats an unloaded image as 0 px tall, so clicking a TREE link scrolls to a
position that moves as images load on the way, and you land mid-page.
Reserving each image's space up front keeps anchor jumps exact.
"""
import os
import re
import struct

IMG = re.compile(r"<img\b[^>]*>")
SRC = re.compile(r'\ssrc="([^"]+)"')


def _png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def on_page_content(html, page, config, files, **kwargs):
    page_dir = os.path.dirname(page.file.src_uri)
    docs_dir = config["docs_dir"]

    def add_size(match):
        tag = match.group(0)
        if " width=" in tag or " height=" in tag:
            return tag
        src = SRC.search(tag)
        if not src or "://" in src.group(1) or not src.group(1).lower().endswith(".png"):
            return tag
        path = os.path.normpath(os.path.join(docs_dir, page_dir, src.group(1)))
        size = os.path.isfile(path) and _png_size(path)
        if not size:
            return tag
        return tag[:-1].rstrip("/").rstrip() + f' width="{size[0]}" height="{size[1]}">'

    return IMG.sub(add_size, html)
