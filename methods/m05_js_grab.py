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
    out = os.path.join("output", "js_grab", dom.replace(".","_"))
    os.makedirs(out, exist_ok=True)
    log(f"JS GRAB: {url}", "INFO")
    r = e.download(url)
    if not r: return
    soup = BeautifulSoup(r.text, "html.parser")
    count = 0
    for s in soup.find_all("script", src=True):
        js_url = urljoin(url, s["src"])
        jr = e.download(js_url)
        if jr:
            name = js_url.split("/")[-1].split("?")[0] or f"script_{count}.js"
            e.save(jr.text, os.path.join(out, name))
            log(f"Downloaded: {name}", "OK")
            count += 1
    log(f"Total JS files: {count}", "OK")
