from core.engine import Engine
from core.logger import log, safe
from bs4 import BeautifulSoup

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    log(f"META EXTRACT: {url}", "INFO")
    r = e.download(url)
    if not r: return
    soup = BeautifulSoup(r.text, "html.parser")
    print(f"\n  \033[1;32mTitle:\033[0m {soup.title.string if soup.title else 'N/A'}")
    print(f"\n  \033[1;32mMeta Tags:\033[0m")
    for m in soup.find_all("meta"):
        name = m.get("name") or m.get("property") or m.get("http-equiv")
        content = m.get("content","")
        if name and content:
            print(f"    {name}: {content[:100]}")
    # OG Tags
    print(f"\n  \033[1;32mOpen Graph:\033[0m")
    for m in soup.find_all("meta", property=True):
        if m["property"].startswith("og:"):
            print(f"    {m['property']}: {m.get('content','')}")
