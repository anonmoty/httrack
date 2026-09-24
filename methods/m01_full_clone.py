import os, time
from core.engine import Engine
from core.logger import log, safe

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL (example.com)\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    dom = e.domain(url)
    out = os.path.join("output", "full_clone", dom.replace(".","_"))
    os.makedirs(out, exist_ok=True)
    log(f"FULL CLONE: {url}", "INFO")
    t = time.time()
    e.clone_page(url, out, dom, 0, 1, True)
    e.print_stats(t)
    log(f"Saved: {out}/", "OK")
