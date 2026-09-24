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
    out = os.path.join("output", "fonts", dom.replace(".","_"))
    os.makedirs(out, exist_ok=True)
    log(f"FONT GRAB: {url}", "INFO")
    r = e.download(url)
    if not r: return
    soup = BeautifulSoup(r.text, "html.parser")
    font_urls = set()
    # CSS files se fonts nikalo
    for link in soup.find_all("link", rel=lambda x: x and "stylesheet" in str(x)):
        href = link.get("href")
        if not href: continue
        cr = e.download(urljoin(url, href))
        if cr:
            for u in re.findall(r'url\(["\']?(.*?)["\']?\)', cr.text):
                if any(ext in u for ext in [".woff",".woff2",".ttf",".otf",".eot"]):
                    font_urls.add(urljoin(urljoin(url, href), u))
    # Preload fonts
    for t in soup.find_all("link", rel=lambda x: x and "preload" in str(x)):
        if t.get("as") == "font":
            font_urls.add(urljoin(url, t.get("href","")))
    count = 0
    for fu in font_urls:
        fr = e.download(fu)
        if fr:
            name = fu.split("/")[-1].split("?")[0] or f"font_{count}"
            e.save(fr.content, os.path.join(out, name), True)
            log(f"Font: {name}", "OK")
            count += 1
    log(f"Total fonts: {count}", "OK")
