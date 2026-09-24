from core.engine import Engine
from core.logger import log, safe
from bs4 import BeautifulSoup
from urllib.parse import urljoin

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    log(f"FORM FINDER: {url}", "INFO")
    r = e.download(url)
    if not r: return
    soup = BeautifulSoup(r.text, "html.parser")
    forms = soup.find_all("form")
    if not forms:
        log("No forms found", "WARN"); return
    print(f"\n  \033[1;32mFound {len(forms)} forms:\033[0m")
    for i, f in enumerate(forms, 1):
        action = urljoin(url, f.get("action",""))
        method = f.get("method","GET").upper()
        inputs = [inp.get("name","?") for inp in f.find_all("input") if inp.get("name")]
        print(f"\n  \033[1;36mForm #{i}\033[0m")
        print(f"    Action : {action}")
        print(f"    Method : {method}")
        print(f"    Inputs : {', '.join(inputs)}")
