#!/usr/bin/env python3
"""
Tor Dork Search - Perform dork-based OSINT queries via Tor using Startpage and Yandex
Compatible with: requests==2.31.0, urllib3==1.26.18, chardet==4.0.0
"""

import requests
import random
import time
import argparse
import os
from tqdm import tqdm
from urllib.parse import unquote
import socks
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Set, Optional
import re

# Configuration
TOR_PROXY = "socks5h://127.0.0.1:9050"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
MAX_RETRIES = 5
MIN_DELAY = 10
MAX_DELAY = 15
MAX_WORKERS = 2
TIMEOUT = 30

def configure_tor():
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket

def check_tor() -> bool:
    try:
        s = get_session()
        r = s.get("https://check.torproject.org/api/ip", timeout=TIMEOUT)
        return '"IsTor":true' in r.text
    except:
        return False

def get_session() -> requests.Session:
    s = requests.Session()
    s.proxies = {"http": TOR_PROXY, "https": TOR_PROXY}
    s.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive"
    })
    return s

def search_startpage(query: str, session: requests.Session) -> Optional[str]:
    url = f"https://www.startpage.com/sp/search?q={requests.utils.quote(query)}"
    return fetch(session, url)

def search_yandex(query: str, session: requests.Session) -> Optional[str]:
    url = f"https://yandex.com/search/?text={requests.utils.quote(query)}"
    return fetch(session, url)

def fetch(session: requests.Session, url: str) -> Optional[str]:
    try:
        r = session.get(url, timeout=TIMEOUT)
        if r.status_code == 429:
            tqdm.write(f"⚠️ 429 Too Many Requests: {url}")
            return None
        r.raise_for_status()
        return r.text
    except Exception as e:
        tqdm.write(f"❌ Request error at {url}: {e}")
        return None

def extract_links(html: str) -> List[str]:
    links = set()
    if not html:
        return []
    for match in re.finditer(r'<a[^>]+href="(https?://[^"]+)"', html):
        url = unquote(match.group(1))
        if not any(b in url for b in ['startpage.', 'yandex.', 'webcache.', 'google.', 'bing.']):
            links.add(url)
    return sorted(links)

def process_dork(dork: str, session: requests.Session, engine: str) -> Set[str]:
    links = set()
    for _ in range(MAX_RETRIES):
        html = search_startpage(dork, session) if engine == "startpage" else search_yandex(dork, session)
        if html:
            found = extract_links(html)
            if found:
                links.update(found)
                break
        time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
    if links:
        tqdm.write(f"✔️ {len(links)} links found for: {dork[:60]}")
    else:
        tqdm.write(f"❌ No results for: {dork[:60]}")
    return links

def main():
    parser = argparse.ArgumentParser(description="Dork-based OSINT search via Tor using Startpage or Yandex")
    parser.add_argument("-d", "--dorks", required=True, help="Path to dorks file")
    parser.add_argument("-o", "--output", default="results.txt", help="Output file path")
    parser.add_argument("--engine", choices=["startpage", "yandex"], default="startpage", help="Search engine to use")
    parser.add_argument("-j", "--workers", type=int, default=MAX_WORKERS, help="Number of concurrent threads")
    args = parser.parse_args()

    if not os.path.isfile(args.dorks):
        print(f"❌ File not found: {args.dorks}")
        return

    with open(args.dorks, "r", encoding="utf-8") as f:
        dorks = [line.strip() for line in f if line.strip()]

    if not dorks:
        print("❌ No valid dorks found.")
        return

    try:
        configure_tor()
        if not check_tor():
            print("❌ Tor is not running on port 9050.")
            return
        print("✔️ Tor connection verified")
    except Exception as e:
        print(f"❌ Tor setup error: {e}")
        return

    session = get_session()
    all_links = set()

    print(f"\n🔍 Starting search using {args.engine} for {len(dorks)} dorks...\n")

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(process_dork, dork, session, args.engine): dork
            for dork in dorks
        }
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing"):
            try:
                links = future.result()
                all_links.update(links)
            except Exception as e:
                tqdm.write(f"⚠️ Unexpected error: {e}")

    with open(args.output, "w", encoding="utf-8") as f_out:
        for link in sorted(all_links):
            f_out.write(link + "\n")

    print(f"\n✅ Done. {len(all_links)} unique links saved to: {args.output}")

if __name__ == "__main__":
    main()

