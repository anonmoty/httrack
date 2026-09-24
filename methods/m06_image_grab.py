import os, re
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
    out = os.path.join("output", "images", dom.replace(".","_"))
    os.makedirs(out, exist_ok=True)
    log(f"IMAGE GRAB: {url}", "INFO")
    r = e.download(url)
    if not r: return
    soup = BeautifulSoup(r.text, "html.parser")
    urls = set()
    for img in soup.find_all("img"):
        for a in ["src","data-src","data-lazy-src"]:
            v = img.get(a)
            if v and not v.startswith("data:"): urls.add(urljoin(url, v))
        for part in img.get("srcset","").split(","):
            u = part.strip().split(" ")[0]
            if u: urls.add(urljoin(url, u))
    for t in soup.find_all(style=True):
        for u in re.findall(r'url\(["\']?(.*?)["\']?\)', t["style"]):
            if not u.startswith("data:"): urls.add(urljoin(url, u))
    count = 0
    for i, iu in enumerate(urls, 1):
        e.progress(i, len(urls), "IMG")
        ir = e.download(iu, timeout=10)
        if ir:
            name = iu.split("/")[-1].split("?")[0] or f"img_{count}.png"
            e.save(ir.content, os.path.join(out, name), True)
            count += 1
    print()
    log(f"Total images: {count}", "OK")
