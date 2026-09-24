# core/engine.py
# ============================================
#   HTTrackX Core Engine v5.0
#   Ye engine sab methods use karte hain
#   HTML+CSS+JS+IMG+Fonts+Media+LinkFix
# ============================================

import os, re, time, mimetypes
import requests
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup
from core.colors import C
from core.logger import log

class Engine:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                      "image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        })
        self.done = set()
        self.count = {"html":0,"css":0,"js":0,"img":0,"font":0,"media":0,"other":0,"fail":0}

    def clean_url(self, url):
        url = url.strip().strip("/")
        if not url.startswith(("http://","https://")):
            url = "https://" + url
        return url

    def domain(self, url):
        m = re.search(r'https?://([^/:]+)', url)
        return m.group(1) if m else url

    def safe_path(self, url_path):
        p = url_path.strip("/").split("?")[0].split("#")[0]
        p = re.sub(r'[<>:"|?*]', '_', p)
        if not p: return "index.html"
        if p.endswith("/"): p += "index.html"
        if "." not in p.split("/")[-1]: p += "/index.html"
        return unquote(p)

    def download(self, url, timeout=15, retries=3):
        """Download with retry + proper encoding"""
        for i in range(retries):
            try:
                r = self.s.get(url, timeout=timeout, allow_redirects=True)
                r.raise_for_status()
                return r
            except requests.exceptions.Timeout:
                if i < retries-1: time.sleep(1); continue
            except requests.exceptions.HTTPError:
                return None
            except requests.exceptions.ConnectionError:
                if i < retries-1: time.sleep(2); continue
            except: return None
        return None

    def save(self, content, path, binary=False):
        """Save file properly"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            if binary:
                with open(path, "wb") as f: f.write(content)
            else:
                if isinstance(content, bytes):
                    try: text = content.decode("utf-8")
                    except: text = content.decode("latin-1", errors="ignore")
                else: text = str(content)
                with open(path, "w", encoding="utf-8", errors="ignore") as f: f.write(text)
            return True
        except: return False

    def detect_type(self, resp, url):
        """Content type detect from headers + URL"""
        ct = resp.headers.get("Content-Type","").lower()
        if "html" in ct or "xhtml" in ct: return "html"
        if "css" in ct: return "css"
        if "javascript" in ct or "ecmascript" in ct: return "js"
        if any(x in ct for x in ["image/","svg"]): return "img"
        if any(x in ct for x in ["font/","woff","ttf","otf"]): return "font"
        if any(x in ct for x in ["video/","audio/","octet-stream"]): return "media"
        # URL extension fallback
        ext = urlparse(url).path.lower().split(".")[-1] if "." in urlparse(url).path else ""
        if ext in ("css",): return "css"
        if ext in ("js","mjs"): return "js"
        if ext in ("png","jpg","jpeg","gif","webp","svg","ico","bmp","avif","tiff"): return "img"
        if ext in ("woff","woff2","ttf","otf","eot"): return "font"
        if ext in ("mp4","mp3","webm","ogg","avi","mov","wav","flac"): return "media"
        if ext in ("html","htm","php","asp","jsp") or not ext: return "html"
        return "other"

    def progress(self, current, total, label=""):
        pct = int((current/max(total,1))*100)
        bar = "█"*int(25*pct/100) + "░"*(25-int(25*pct/100))
        print(f"\r  {C.M}[{bar}] {pct}% ({current}/{total}) {label}{C.E}    ", end="", flush=True)

    # ============ MAIN CLONE METHOD ============

    def clone_page(self, url, out_dir, dom, depth=0, max_depth=1, clone_assets=True):
        """Ek page clone karo with ALL assets"""
        if depth > max_depth or url in self.done:
            return
        if dom not in urlparse(url).netloc:
            return

        self.done.add(url)
        log(f"Page: {url}", "DL")

        resp = self.download(url)
        if not resp:
            log(f"Failed: {url}", "ERR")
            self.count["fail"] += 1
            return

        ctype = self.detect_type(resp, url)
        if ctype != "html":
            return

        html = resp.text
        self.count["html"] += 1

        try: soup = BeautifulSoup(html, "lxml")
        except: soup = BeautifulSoup(html, "html.parser")

        if clone_assets:
            assets = self._collect_assets(soup, url)
            total = len(assets)

            for i, (atype, aurl, tag, attr) in enumerate(assets, 1):
                if aurl in self.done or aurl.startswith("data:"):
                    continue
                self.done.add(aurl)
                self.progress(i, total, atype.upper())

                r = self.download(aurl, timeout=10, retries=2)
                if not r:
                    self.count["fail"] += 1
                    continue

                rtype = self.detect_type(r, aurl)
                p = urlparse(aurl)
                local = self.safe_path(p.path)
                full = os.path.join(out_dir, local)
                binary = rtype in ("img","font","media","other")

                if self.save(r.content if binary else r.text, full, binary):
                    self.count[rtype] = self.count.get(rtype, 0) + 1
                    if tag and attr:
                        rel = os.path.relpath(full, out_dir).replace("\\","/")
                        tag[attr] = rel

                # CSS ke andar url() bhi download karo
                if rtype == "css":
                    self._parse_css_urls(r.text, aurl, out_dir, dom)

                time.sleep(0.08)
            print()

        # Links rewrite
        for a in soup.find_all("a", href=True):
            h = a["href"]
            if h.startswith(("http://","https://")) and dom in h:
                a["href"] = self.safe_path(urlparse(h).path)

        # Save HTML
        p = urlparse(url)
        hp = self.safe_path(p.path)
        self.save(str(soup), os.path.join(out_dir, hp))
        log(f"Saved: {hp}", "OK")

        # Sub pages crawl
        if depth < max_depth:
            subs = []
            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"]).split("#")[0].split("?")[0]
                if dom in urlparse(link).netloc and link not in self.done:
                    subs.append(link)
            for s in subs[:30]:
                self.clone_page(s, out_dir, dom, depth+1, max_depth, clone_assets)

    def _collect_assets(self, soup, base_url):
        """Saare assets collect karo HTML se"""
        assets = []

        # CSS
        for t in soup.find_all("link", rel=lambda x: x and "stylesheet" in str(x)):
            h = t.get("href")
            if h: assets.append(("css", urljoin(base_url, h), t, "href"))

        # JS
        for t in soup.find_all("script", src=True):
            assets.append(("js", urljoin(base_url, t["src"]), t, "src"))

        # Images
        for t in soup.find_all("img"):
            for attr in ["src", "data-src", "data-lazy-src"]:
                v = t.get(attr)
                if v and not v.startswith("data:"):
                    assets.append(("img", urljoin(base_url, v), t, attr))
            ss = t.get("srcset","")
            for part in ss.split(","):
                u = part.strip().split(" ")[0]
                if u and not u.startswith("data:"):
                    assets.append(("img", urljoin(base_url, u), None, None))

        # Favicon
        for t in soup.find_all("link", rel=lambda x: x and "icon" in str(x)):
            h = t.get("href")
            if h: assets.append(("img", urljoin(base_url, h), t, "href"))

        # OG Image
        for t in soup.find_all("meta", attrs={"property":"og:image"}):
            c = t.get("content")
            if c: assets.append(("img", urljoin(base_url, c), t, "content"))

        # Video/Audio
        for t in soup.find_all(["video","audio","source"], src=True):
            assets.append(("media", urljoin(base_url, t["src"]), t, "src"))
        for t in soup.find_all("video", poster=True):
            assets.append(("img", urljoin(base_url, t["poster"]), t, "poster"))

        # Background images from style
        for t in soup.find_all(style=True):
            for u in re.findall(r'url\(["\']?(.*?)["\']?\)', t["style"]):
                if u and not u.startswith("data:"):
                    assets.append(("img", urljoin(base_url, u), None, None))

        # Fonts from <link> preload
        for t in soup.find_all("link", rel=lambda x: x and "preload" in str(x)):
            if t.get("as") == "font":
                h = t.get("href")
                if h: assets.append(("font", urljoin(base_url, h), t, "href"))

        return assets

    def _parse_css_urls(self, css_text, css_url, out_dir, dom):
        """CSS ke andar url() references download karo"""
        for u in re.findall(r'url\(["\']?(.*?)["\']?\)', css_text):
            if u.startswith(("data:","#","//fonts")): continue
            full = urljoin(css_url, u)
            if full in self.done or dom not in urlparse(full).netloc: continue
            self.done.add(full)
            r = self.download(full, timeout=8, retries=2)
            if r:
                local = self.safe_path(urlparse(full).path)
                self.save(r.content, os.path.join(out_dir, local), True)
                rt = self.detect_type(r, full)
                self.count[rt] = self.count.get(rt, 0) + 1

    def print_stats(self, start_time):
        """Final stats dikhao"""
        elapsed = time.time() - start_time
        total = sum(self.count.values())
        print(f"\n  {C.GR}{'═'*55}{C.E}")
        print(f"  {C.BO}{C.G}✅ COMPLETE!{C.E}")
        print(f"  {C.GR}{'─'*55}{C.E}")
        print(f"  {C.CY}📄 HTML  : {self.count['html']}{C.E}")
        print(f"  {C.CY}🎨 CSS   : {self.count['css']}{C.E}")
        print(f"  {C.CY}⚡ JS    : {self.count['js']}{C.E}")
        print(f"  {C.CY}🖼️  IMG   : {self.count['img']}{C.E}")
        print(f"  {C.CY}🔤 Fonts : {self.count['font']}{C.E}")
        print(f"  {C.CY}🎬 Media : {self.count['media']}{C.E}")
        print(f"  {C.CY}📦 Other : {self.count['other']}{C.E}")
        print(f"  {C.R}❌ Failed: {self.count['fail']}{C.E}")
        print(f"  {C.GR}{'─'*55}{C.E}")
        print(f"  {C.G}📊 Total : {total} files{C.E}")
        print(f"  {C.G}⏱️  Time  : {elapsed:.1f}s{C.E}")
        print(f"  {C.GR}{'═'*55}{C.E}\n")
