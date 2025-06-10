import pytesseract
from pathlib import Path

CAPTCHA_DIR = Path('captchas')
WHITELIST = '0123456789'


def ocr_image(path: Path) -> str:
    config = f'--psm 7 -c tessedit_char_whitelist={WHITELIST}'
    text = pytesseract.image_to_string(str(path), lang='eng', config=config)
    digits = ''.join(ch for ch in text if ch in WHITELIST)
    return digits


def main():
    results = {}
    for file in sorted(CAPTCHA_DIR.glob('*.gif')):
        digits = ocr_image(file)
        results[file.name] = digits
        print(f'{file.name}: {digits}')

    out_path = Path('out.txt')
    with open(out_path, 'w', encoding='utf-8') as f:
        for name, digits in results.items():
            f.write(f'{name}\t{digits}\n')
    print(f'written results to {out_path}')


if __name__ == '__main__':
    main()
