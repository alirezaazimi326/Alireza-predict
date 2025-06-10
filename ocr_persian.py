"""Simple OCR helper for captcha digits.

This version uses OpenCV pre-processing to get more reliable
results. Images are converted to grayscale, binarized with Otsu
thresholding and cleaned up slightly before running Tesseract.
The script prints the recognized digits for each image in the
``captchas`` folder and writes them to ``out.txt``.
"""

from pathlib import Path

import cv2
import numpy as np
import pytesseract
from PIL import Image


CAPTCHA_DIR = Path("captchas")
WHITELIST = "0123456789"


def preprocess(path: Path) -> np.ndarray:
    """Load image and return cleaned binary array."""
    img = Image.open(path).convert("L")
    arr = np.array(img)
    # Otsu threshold with inversion so digits are black on white
    _, bw = cv2.threshold(
        arr, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    # remove tiny noise and close small gaps
    kernel = np.ones((3, 3), np.uint8)
    bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel, iterations=1)
    # invert back for Tesseract (black text on white background)
    bw = 255 - bw
    return bw


def ocr_image(path: Path) -> str:
    img = preprocess(path)
    config = f"--psm 7 -c tessedit_char_whitelist={WHITELIST}"
    text = pytesseract.image_to_string(img, lang="eng", config=config)
    digits = "".join(ch for ch in text if ch in WHITELIST)
    # captcha images contain exactly five digits
    return digits[:5]


def main() -> None:
    results = {}
    for file in sorted(CAPTCHA_DIR.glob("*.gif")):
        digits = ocr_image(file)
        results[file.name] = digits
        print(f"{file.name}: {digits}")

    with open("out.txt", "w", encoding="utf-8") as f:
        for name, digits in results.items():
            f.write(f"{name}\t{digits}\n")


if __name__ == "__main__":
    main()

