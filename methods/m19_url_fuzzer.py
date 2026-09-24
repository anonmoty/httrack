from core.engine import Engine
from core.logger import log, safe

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL (example.com)\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    log(f"URL FUZZER: {url}", "INFO")
    paths = ["/admin","/login","/wp-admin","/wp-login.php","/dashboard",
             "/api","/api/v1","/api/v2","/graphql","/.env","/.git",
             "/.git/config","/config","/backup","/db","/database",
             "/phpmyadmin","/server-status","/robots.txt","/sitemap.xml",
             "/.htaccess","/web.config","/console","/debug","/test",
             "/staging","/dev","/temp","/tmp","/uploads","/files",
             "/images","/assets","/static","/media","/downloads",
             "/.well-known","/xmlrpc.php","/wp-config.php","/readme.html",
             "/cgi-bin","/shell","/cmd","/manager","/jmx-console"]
    found = 0
    for p in paths:
        r = e.download(f"{url}{p}", timeout=8, retries=1)
        if r and r.status_code in [200, 301, 302, 403]:
            c = "\033[1;31m" if r.status_code == 403 else "\033[1;32m"
            log(f"  {c}[{r.status_code}] {url}{p}\033[0m", "FIND")
            found += 1
    log(f"Found {found} paths", "OK")
