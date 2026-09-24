import os, datetime
from core.colors import C

def log(msg, lvl="INFO"):
    os.makedirs("output", exist_ok=True)
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    with open("output/httrackx.log", "a") as f:
        f.write(f"[{ts}][{lvl}] {msg}\n")
    ic = {"ERR": f"{C.R}[✗]", "WARN": f"{C.Y}[!]", "OK": f"{C.G}[✓]",
          "DL": f"{C.M}[↓]", "INFO": f"{C.CY}[*]", "FIND": f"{C.O}[+]"}
    print(f"  {ic.get(lvl, f'{C.CY}[*]')} {msg}{C.E}")

def safe(func):
    def wrap(*a, **kw):
        try: return func(*a, **kw)
        except KeyboardInterrupt: log("Cancelled", "WARN")
        except Exception as e: log(f"Bug: {e}", "ERR")
    return wrap
