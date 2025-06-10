import requests
from pathlib import Path
from time import sleep

# --- CONFIG ---
URL = "https://www.utcms.ir/Cap.aspx?id=LoginShowFuelQuota"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.utcms.ir/ShowFuelQuota.aspx"
}

SAVE_DIR = Path("captchas")
SAVE_DIR.mkdir(exist_ok=True)

# --- MAIN FUNCTION ---
def download_captchas(count=100, delay=0.3):
    for i in range(count):
        try:
            response = requests.get(URL, headers=HEADERS)
            if response.status_code == 200:
                filename = SAVE_DIR / f"captcha_{i+1:03}.gif"
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"[✓] Saved {filename}")
            else:
                print(f"[✗] Failed {i+1}: {response.status_code}")
        except Exception as e:
            print(f"[!] Error at {i+1}: {e}")
        
        sleep(delay)  # short delay to avoid overwhelming the server

# --- RUN ---
if __name__ == "__main__":
    download_captchas(count=100)
