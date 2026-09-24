from core.engine import Engine
from core.logger import log, safe

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    log(f"ROBOTS.TXT: {url}", "INFO")
    r = e.download(f"{url}/robots.txt")
    if not r or r.status_code != 200:
        log("robots.txt not found", "WARN"); return
    print(f"\n  \033[1;36m{'─'*50}\033[0m")
    print(r.text)
    print(f"  \033[1;36m{'─'*50}\033[0m")
    # Disallowed paths nikalo
    disallowed = [l.split(":")[1].strip() for l in r.text.splitlines() if l.lower().startswith("disallow:") and ":" in l]
    if disallowed:
        print(f"\n  \033[1;33mHidden/Disallowed Paths:\033[0m")
        for d in disallowed:
            if d: print(f"    🚫 {url}{d}")
