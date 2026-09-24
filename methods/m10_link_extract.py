from core.engine import Engine
from core.logger import log, safe
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    dom = e.domain(url)
    log(f"LINK EXTRACT: {url}", "INFO")
    r = e.download(url)
    if not r: return
    soup = BeautifulSoup(r.text, "html.parser")
    internal, external = set(), set()
    for a in soup.find_all("a", href=True):
        link = urljoin(url, a["href"]).split("#")[0]
        if dom in urlparse(link).netloc: internal.add(link)
        elif link.startswith("http"): external.add(link)
    print(f"\n  \033[1;32mInternal Links ({len(internal)}):\033[0m")
    for l in sorted(internal): print(f"    {l}")
    print(f"\n  \033[1;33mExternal Links ({len(external)}):\033[0m")
    for l in sorted(external): print(f"    {l}")
    # Save to file
    with open("output/links.txt", "w") as f:
        f.write("=== INTERNAL ===\n")
        for l in internal: f.write(l+"\n")
        f.write("\n=== EXTERNAL ===\n")
        for l in external: f.write(l+"\n")
    log("Saved: output/links.txt", "OK")
