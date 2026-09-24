import os, time
from core.engine import Engine
from core.logger import log, safe

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mPage URL\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    dom = e.domain(url)
    out = os.path.join("output", "single_page", dom.replace(".","_"))
    os.makedirs(out, exist_ok=True)
    log(f"SINGLE PAGE: {url}", "INFO")
    t = time.time()
    e.clone_page(url, out, dom, 0, 0, True)  # depth=0 = sirf ek page
    e.print_stats(t)
