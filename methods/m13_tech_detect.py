from core.engine import Engine
from core.logger import log, safe

@safe
def run():
    e = Engine()
    url = input("  \033[1;36mTarget URL\033[0m: ").strip()
    if not url: return
    url = e.clean_url(url)
    log(f"TECH DETECT: {url}", "INFO")
    r = e.download(url)
    if not r: return
    h = r.text.lower()
    hdr = r.headers
    techs = []
    checks = {
        "WordPress": ["wp-content","wp-includes","wordpress"],
        "Joomla": ["joomla","/media/jui/"],
        "Drupal": ["drupal","sites/default/files"],
        "Shopify": ["shopify","cdn.shopify.com"],
        "Wix": ["wix.com","wixstatic"],
        "Squarespace": ["squarespace"],
        "React": ["react","__next","_next/"],
        "Angular": ["ng-app","angular"],
        "Vue.js": ["vue","v-bind","v-model"],
        "jQuery": ["jquery"],
        "Bootstrap": ["bootstrap"],
        "Tailwind": ["tailwind"],
        "Laravel": ["laravel","csrf-token"],
        "Django": ["csrfmiddlewaretoken","django"],
        "PHP": ["php"],
        "ASP.NET": ["asp.net","__viewstate"],
    }
    for name, keywords in checks.items():
        if any(k in h for k in keywords): techs.append(name)
    if "server" in hdr: techs.append(f"Server: {hdr['server']}")
    if "x-powered-by" in hdr: techs.append(f"Powered: {hdr['x-powered-by']}")
    print(f"\n  \033[1;32mDetected Technologies:\033[0m")
    for t in sorted(set(techs)): print(f"    🔧 {t}")
