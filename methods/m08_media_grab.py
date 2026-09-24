import os
from core.engine import Engine
from core.logger import log, safe
from bs4 import BeautifulSoup
from urllib.parse import urljoin

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    dom = e.domain(url)
    out = os.path.join("output", "media", dom.replace(".","_"))
    os.makedirs(out, exist_ok=True)
    log(f"MEDIA GRAB: {url}", "INFO")
    r = e.download(url)
    if not r: return
    soup = BeautifulSoup(r.text, "html.parser")
    media = set()
    for t in soup.find_all(["video","audio","source"], src=True):
        media.add(urljoin(url, t["src"]))
    for t in soup.find_all("a", href=True):
        h = t["href"].lower()
        if any(h.endswith(x) for x in [".mp4",".mp3",".webm",".ogg",".avi",".mov",".wav"]):
            media.add(urljoin(url, t["href"]))
    count = 0
    for mu in media:
        mr = e.download(mu, timeout=30)
        if mr:
            name = mu.split("/")[-1].split("?")[0] or f"media_{count}"
            e.save(mr.content, os.path.join(out, name), True)
            log(f"Media: {name} ({len(mr.content)//1024}KB)", "OK")
            count += 1
    log(f"Total media: {count}", "OK")
