import os, time
from core.engine import Engine
from core.logger import log, safe

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL\033[0m: ").strip()
    if not url: return
    depth = input("  \033[1;36mDepth (1-5, default 3)\033[0m: ").strip() or "3"
    url = e.clean_url(url)
    dom = e.domain(url)
    out = os.path.join("output", "deep_crawl", dom.replace(".","_"))
    os.makedirs(out, exist_ok=True)
    log(f"DEEP CRAWL depth={depth}: {url}", "INFO")
    t = time.time()
    e.clone_page(url, out, dom, 0, int(depth), True)
    e.print_stats(t)
