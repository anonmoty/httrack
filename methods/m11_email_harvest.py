import re
from core.engine import Engine
from core.logger import log, safe

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    log(f"EMAIL HARVEST: {url}", "INFO")
    r = e.download(url)
    if not r: return
    emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', r.text))
    # mailto: links bhi
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, "html.parser")
    for a in soup.find_all("a", href=True):
        if a["href"].startswith("mailto:"):
            emails.add(a["href"].replace("mailto:","").split("?")[0])
    if emails:
        print(f"\n  \033[1;32mFound {len(emails)} emails:\033[0m")
        for em in sorted(emails): print(f"    📧 {em}")
        with open("output/emails.txt", "w") as f:
            for em in emails: f.write(em+"\n")
        log("Saved: output/emails.txt", "OK")
    else:
        log("No emails found", "WARN")
