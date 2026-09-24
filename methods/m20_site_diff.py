import os
from core.engine import Engine
from core.logger import log, safe

@safe
def run():
    e = Engine()
    url1 = input("  \033[1;36mURL 1\033[0m: ").strip()
    url2 = input("  \033[1;36mURL 2\033[0m: ").strip()
    if not url1 or not url2: return
    url1, url2 = e.clean_url(url1), e.clean_url(url2)
    log(f"COMPARING: {url1} vs {url2}", "INFO")
    r1 = e.download(url1)
    r2 = e.download(url2)
    if not r1 or not r2:
        log("Failed to download one or both", "ERR"); return
    t1, t2 = r1.text, r2.text
    print(f"\n  \033[1;32mComparison Results:\033[0m")
    print(f"    URL 1 size: {len(t1)} chars")
    print(f"    URL 2 size: {len(t2)} chars")
    print(f"    Size diff : {abs(len(t1)-len(t2))} chars")
    # Line by line compare
    l1 = set(t1.splitlines())
    l2 = set(t2.splitlines())
    only1 = l1 - l2
    only2 = l2 - l1
    common = l1 & l2
    print(f"    Common lines  : {len(common)}")
    print(f"    Only in URL 1 : {len(only1)}")
    print(f"    Only in URL 2 : {len(only2)}")
    similarity = len(common) / max(len(l1|l2), 1) * 100
    print(f"    Similarity    : {similarity:.1f}%")
    # Status & headers
    print(f"\n    Status 1: {r1.status_code} | Status 2: {r2.status_code}")
    s1 = r1.headers.get("Server","?")
    s2 = r2.headers.get("Server","?")
    print(f"    Server 1: {s1} | Server 2: {s2}")
    with open("output/diff_report.txt","w") as f:
        f.write(f"URL1: {url1}\nURL2: {url2}\nSimilarity: {similarity:.1f}%\n")
        f.write(f"\nOnly in URL1 ({len(only1)}):\n")
        for l in list(only1)[:50]: f.write(f"  {l}\n")
        f.write(f"\nOnly in URL2 ({len(only2)}):\n")
        for l in list(only2)[:50]: f.write(f"  {l}\n")
    log("Saved: output/diff_report.txt", "OK")
