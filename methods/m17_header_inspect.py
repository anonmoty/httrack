from core.engine import Engine
from core.logger import log, safe
from core.colors import C

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    log(f"HEADERS: {url}", "INFO")
    r = e.download(url)
    if not r: return
    print(f"\n  {C.BO}{'Header':<35} Value{C.E}")
    print(f"  {C.GR}{'─'*65}{C.E}")
    for k, v in r.headers.items():
        c = C.Y if k.lower() in ["server","x-powered-by"] else C.G
        print(f"  {c}{k:<35} {v}{C.E}")
    print(f"\n  {C.BO}Security Check:{C.E}")
    sec = {"Strict-Transport-Security":"HSTS","X-Frame-Options":"Clickjack",
           "X-Content-Type-Options":"MIME","Content-Security-Policy":"CSP",
           "X-XSS-Protection":"XSS","Referrer-Policy":"Referrer"}
    for h, n in sec.items():
        if h in r.headers: log(f"{n}: ✓ Present", "OK")
        else: log(f"{n}: ✗ MISSING", "ERR")
