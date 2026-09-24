import os, time
from core.engine import Engine
from core.logger import log, safe
from bs4 import BeautifulSoup
from urllib.parse import urljoin

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL (example.com)\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    dom = e.domain(url)
    out = os.path.join("output", "sitemap_clone", dom.replace(".","_"))
    os.makedirs(out, exist_ok=True)
    log(f"SITEMAP CRAWL: {url}", "INFO")
    sm_url = f"{url}/sitemap.xml"
    r = e.download(sm_url)
    if not r:
        log("sitemap.xml not found!", "ERR")
        return
    soup = BeautifulSoup(r.text, "lxml")
    urls = [loc.text for loc in soup.find_all("loc")]
    log(f"Found {len(urls)} URLs in sitemap", "FIND")
    t = time.time()
    for i, u in enumerate(urls[:50], 1):  # Max 50 pages
        log(f"[{i}/{len(urls)}] {u}", "DL")
        e.clone_page(u, out, dom, 0, 0, True)
    e.print_stats(t)
