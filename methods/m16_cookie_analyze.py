from core.engine import Engine
from core.logger import log, safe

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    log(f"COOKIE ANALYZE: {url}", "INFO")
    r = e.download(url)
    if not r: return
    cookies = r.cookies
    if not cookies:
        log("No cookies set", "WARN"); return
    print(f"\n  \033[1;32mCookies ({len(cookies)}):\033[0m")
    print(f"  {'Name':<30} {'Value':<30} {'Secure'} {'HttpOnly'}")
    print(f"  {'─'*75}")
    for c in cookies:
        sec = "✓" if c.secure else "✗"
        # httponly check from header
        ho = "✓" if "httponly" in str(c).lower() else "?"
        val = c.value[:25] + "..." if len(c.value) > 25 else c.value
        print(f"  {c.name:<30} {val:<30} {sec:^6} {ho:^8}")
