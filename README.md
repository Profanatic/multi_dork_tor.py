# multi_dork_tor.py
OSINT tool for performing anonymous dork-based queries via **Tor**, using **Startpage** or **Yandex** as the search engine.

# Tor Dork Search

An OSINT tool for performing anonymous dork-based queries via **Tor**, using **Startpage** or **Yandex** as the search engine.

> 🛡️ Designed for cybersecurity researchers and analysts focused on privacy-preserving reconnaissance.

---

## ⚙️ Requirements

- Python 3.8 or newer
- Tor running on port 9050 (e.g., `sudo systemctl tor start`)
- Linux/WSL/macOS (recommended)

---

## 🚀 Installation

### 1. Clone the repository

git clone https://github.com/multi_dork_tor.py/tor-dork-search.git

cd multi_dork_tor.py

python3 -m venv venv

source venv/bin/activate

pip3 install --break-system-packages -r requirements.txt

Usage

1. Create a dork file:

echo 'site:example.com intitle:"admin login"' > dorks.txt

python3 multi_dork_tor.py -d dorks.txt --engine yandex -o results.txt

Or

python3 multi_dork_tor.py -d dorks.txt --engine startpage -o results.txt

🛡️ Notes

This script routes traffic through the Tor network.

Startpage and Yandex are less aggressive with CAPTCHA and block detection.

Respect each search engine's terms of service.

