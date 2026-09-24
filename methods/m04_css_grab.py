import os, re
from core.engine import Engine
from core.logger import log, safe
from bs4 import BeautifulSoup

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    dom = e.domain(url)
    out = os.path.join("output", "css_grab", dom.replace(".","_"))
    os.makedirs(out, exist_ok=True)
    log(f"CSS GRAB: {url}", "INFO")
    r = e.download(url)
    if not r: return
    soup = BeautifulSoup(r.text, "html.parser")
    count = 0
    for link in soup.find_all("link", rel=lambda x: x and "stylesheet" in str(x)):
        href = link.get("href")
        if not href: continue
        from urllib.parse import urljoin
        css_url = urljoin(url, href)
        cr = e.download(css_url)
        if cr:
            name = css_url.split("/")[-1].split("?")[0] or "style.css"
            e.save(cr.text, os.path.join(out, name))
            log(f"Downloaded: {name} ({len(cr.text)} bytes)", "OK")
            count += 1
    # Inline CSS bhi save karo
    for style in soup.find_all("style"):
        if style.string:
            e.save(style.string, os.path.join(out, f"inline_{count}.css"))
            count += 1
    log(f"Total CSS files: {count}", "OK")
