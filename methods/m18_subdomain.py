import socket
from core.engine import Engine
from core.logger import log, safe

@safe
def run():
    e = Engine()
    dom = input("  \033[1;36mDomain (example.com)\033[0m: ").strip()
    if not dom: return
    dom = dom.replace("http://","").replace("https://","").split("/")[0]
    log(f"SUBDOMAIN SCAN: {dom}", "INFO")
    subs = ["www","mail","ftp","admin","blog","dev","api","test","staging",
            "app","shop","m","cdn","portal","dashboard","login","webmail",
            "support","docs","status","demo","beta","alpha","mobile",
            "secure","vpn","ns1","ns2","mx","smtp","pop","imap","cpanel",
            "whm","webdisk","autodiscover","sip","lync","remote"]
    found = 0
    for s in subs:
        try:
            ip = socket.gethostbyname(f"{s}.{dom}")
            log(f"  {s}.{dom} → {ip}", "FIND")
            found += 1
        except: pass
    log(f"Found {found} subdomains", "OK")
