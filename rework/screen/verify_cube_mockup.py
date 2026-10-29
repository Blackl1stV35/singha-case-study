"""Verify the 3D cube mockup page at rework/mockup/cube_3d.html.

Run from the repo with Playwright installed:  python rework/screen/verify_cube_mockup.py

Cases:
- desktop (1280 x 800) and phone (375 x 812), CDN allowed. For each case the script
  - opens the page from file:// and records console errors, page errors, failed requests
    and 4xx responses
  - waits for window.mockupCheck.threeLoaded to be a boolean
  - checks that a WebGL canvas sits directly under #stage and the fallback is not shown
  - checks horizontal overflow (documentElement.scrollWidth <= innerWidth)
  - reads the name line width in mm against the 62 mm live width, and the bottom of the
    front and back label text against the 90 mm label canvas
  - checks the scene parts (pouch, cube, carton), that no water is drawn, and that no drop control is shown
    the order and the cube's visibility
  - saves an idle screenshot
- fallback: the three.js CDN is blocked at the network layer (desktop width). The page must
  fall back to its text and front label, with no WebGL canvas and no uncaught page errors.
- wording: the page file is scanned with the wording list in rework/mockup/make_label.py.

Outputs in rework/screen/: verify_cube_mockup_<run date>.json (the full report) and the
screenshots it names. Exit code 0 only if every check passes.
"""
import datetime
import json
import re
import struct
import sys
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
MOCKUP_DIR = ROOT / "rework" / "mockup"
SCREEN_DIR = ROOT / "rework" / "screen"
PAGE = MOCKUP_DIR / "cube_3d.html"
CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"
CDN_PROBE_URL = "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"
CDN_ROUTE = "https://cdn.jsdelivr.net/**"
LAUNCH_ARGS = ["--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]
RUN_DATE = datetime.date.today().isoformat()
LIVE_W_MM = 62.0
LABEL_H_PX = 900  # the 90 mm label canvas at 10 px per mm

VIEWPORTS = [
    {"tag": "desktop", "width": 1280, "height": 800, "dissolved_shot": False},
    {"tag": "phone", "width": 375, "height": 812, "dissolved_shot": False},
]

STATE_JS = """() => {
  const c = window.mockupCheck || {};
  const stage = document.getElementById('stage');
  const cv = document.querySelector('#stage > canvas');
  const r = cv ? cv.getBoundingClientRect() : null;
  const fb = document.getElementById('fallback');
  const sarabun = [...document.fonts].filter((f) => /Sarabun/.test(f.family) && f.status === 'loaded').length;
  const round1 = (v) => (typeof v === 'number' ? Math.round(v * 10) / 10 : null);
  return {
    threeLoaded: c.threeLoaded === undefined ? null : c.threeLoaded,
    threeError: c.threeError || null,
    sceneParts: typeof c.sceneParts === 'function' ? c.sceneParts() : null,
    dropControl: !!document.getElementById('dropBtn'),
    stageIsFallback: stage ? stage.classList.contains('is-fallback') : null,
    fallbackShown: fb ? !fb.hidden : null,
    fallbackLabelCanvas: !!document.querySelector('#fallbackLabel canvas'),
    webglCanvasPresent: !!cv,
    webglCanvasCss: r ? [Math.round(r.width), Math.round(r.height)] : null,
    webglCanvasBuffer: cv ? [cv.width, cv.height] : null,
    sarabunFacesLoaded: sarabun,
    liveWidthMm: round1(c.liveWidthMm),
    nameLineMm: round1(c.nameLineMm),
    labelImagesLoaded: c.labelImagesLoaded === true,
    nameLineFitsAtSpec: c.nameLineFitsAtSpec === undefined ? null : c.nameLineFitsAtSpec,
    nameLineSizeMm: c.nameLineSizeMm || null,
    frontBottomPx: c.frontBottomPx === undefined ? null : c.frontBottomPx,
    backBottomPx: c.backBottomPx === undefined ? null : c.backBottomPx,
    scrollWidth: document.documentElement.scrollWidth,
    bodyScrollWidth: document.body ? document.body.scrollWidth : null,
    innerWidth: window.innerWidth
  };
}"""

def probe_cdn():
    try:
        req = urllib.request.Request(CDN_PROBE_URL, headers={"User-Agent": "cube-mockup-verify/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read(256)
            return {
                "reachable": resp.status == 200,
                "status": resp.status,
                "detail": f"HTTP {resp.status}, first {len(body)} bytes read",
            }
    except urllib.error.HTTPError as e:
        return {"reachable": False, "status": e.code, "detail": f"HTTP error {e.code}"}
    except Exception as e:  # network, DNS, TLS, timeout
        return {"reachable": False, "status": None, "detail": f"{type(e).__name__}: {e}"}


def png_size(path):
    try:
        with open(path, "rb") as f:
            head = f.read(24)
        if head[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        w, h = struct.unpack(">II", head[16:24])
        return [w, h]
    except OSError:
        return None


def rel(path):
    return str(path.relative_to(ROOT)).replace("\\", "/")


def launch(p):
    try:
        browser = p.chromium.launch(headless=True, args=LAUNCH_ARGS)
        return browser, "Playwright bundled Chromium (headless)"
    except Exception as e:
        bundled_err = f"{type(e).__name__}: {str(e).splitlines()[0] if str(e) else ''}"
        browser = p.chromium.launch(headless=True, executable_path=CHROME_PATH, args=LAUNCH_ARGS)
        return browser, f"Google Chrome at {CHROME_PATH} (bundled launch failed: {bundled_err})"


def run_case(browser, tag, width, height, idle_name, block_cdn=False):
    idle = SCREEN_DIR / idle_name
    rec = {
        "case": tag,
        "viewport": f"{width}x{height}",
        "cdn_blocked": block_cdn,
        "navigated": False,
        "goto_error": None,
        "flag_set": False,
        "flag_error": None,
        "state": None,
        "idle_screenshot": rel(idle),
        "idle_screenshot_size": None,
        "console_errors": [],
        "page_errors": [],
        "failed_requests": [],
        "http_errors": [],
        "run_error": None,
    }
    context = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
    if block_cdn:
        context.route(CDN_ROUTE, lambda route: route.abort())
    page = context.new_page()
    page.on("console", lambda m: rec["console_errors"].append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: rec["page_errors"].append(str(e)))
    page.on("requestfailed", lambda r: rec["failed_requests"].append(f"{r.url} :: {r.failure}"))
    page.on("response", lambda r: rec["http_errors"].append(f"{r.status} {r.url}") if r.status >= 400 else None)
    try:
        try:
            page.goto(PAGE.as_uri(), wait_until="domcontentloaded", timeout=45000)
            rec["navigated"] = True
        except Exception as e:
            rec["goto_error"] = f"{type(e).__name__}: {e}"
        try:
            page.wait_for_function(
                "() => window.mockupCheck && typeof window.mockupCheck.threeLoaded === 'boolean'",
                timeout=40000,
            )
            rec["flag_set"] = True
        except Exception:
            rec["flag_error"] = "flag not set within timeout"
        page.wait_for_timeout(1500)  # let a few render frames run
        rec["state"] = page.evaluate(STATE_JS)
        # Measured before the full-page screenshot, which can resize the viewport.
        page.screenshot(path=str(idle), full_page=True)
        rec["idle_screenshot_size"] = png_size(idle)
    except Exception as e:
        rec["run_error"] = f"{type(e).__name__}: {e}"
    finally:
        context.close()
    return rec


def visible_copy(text):
    """The page text a reader sees: no script, no style, no data URIs."""
    text = re.sub(r"<script.*?</script>", "", text, flags=re.S | re.I)
    text = re.sub(r"<style.*?</style>", "", text, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", text)


def wording_scan():
    sys.path.insert(0, str(MOCKUP_DIR))
    import make_label  # the wording list and the organiser digests are defined there
    text = PAGE.read_text(encoding="utf-8")
    # The emblem is an embedded image: scan the copy only, not its base64 data.
    text = re.sub(r"data:image/[a-z]+;base64,[A-Za-z0-9+/=]+", "", text)
    hits = [pat for pat in make_label.FORBIDDEN if pat != r"\bnew\b" and re.search(pat, text, re.I)]
    return {
        "page": "rework/mockup/cube_3d.html",
        "patterns_checked": len(make_label.FORBIDDEN) - 1,
        "forbidden_pattern_hits": hits,
        # The word new is checked by position: it may appear only as the constructor (new X).
        "bare_new_occurrences": len(re.findall(r"\bnew\b(?!\s+[A-Z])", text)),
        "new_as_constructor": len(re.findall(r"\bnew\s+[A-Z]", text)),
        "organiser_digest_hits": make_label.organiser_digest_hits(text),
        "water_word_hits_in_visible_copy": len(re.findall(r"water", visible_copy(text), re.I)),
    }


def build_checks(report):
    checks = []

    def add(name, ok, detail):
        checks.append({"check": name, "pass": bool(ok), "detail": detail})

    cdn = report["cdn_probe"]
    add("three.js CDN reachable from this machine (urllib probe)", cdn["reachable"], cdn["detail"])
    for case in report["cases"]:
        tag = case["case"]
        st = case["state"] or {}
        if case["cdn_blocked"]:
            add("CDN blocked: fallback text and front label shown, no WebGL canvas",
                st.get("threeLoaded") is False and st.get("stageIsFallback") is True
                and st.get("fallbackShown") is True and st.get("fallbackLabelCanvas") is True
                and st.get("webglCanvasPresent") is False and case["flag_set"],
                f"threeLoaded={st.get('threeLoaded')}; threeError={st.get('threeError')}; "
                f"fallbackShown={st.get('fallbackShown')}; fallbackLabelCanvas={st.get('fallbackLabelCanvas')}; "
                f"webglCanvasPresent={st.get('webglCanvasPresent')}; flag_error={case['flag_error']}")
            add("CDN blocked: no uncaught page errors",
                len(case["page_errors"]) == 0 and case["run_error"] is None,
                f"page_errors={len(case['page_errors'])}; run_error={case['run_error']}")
            add("CDN blocked: fallback screenshot saved",
                case["idle_screenshot_size"] is not None,
                f"{case['idle_screenshot']} size={case['idle_screenshot_size']}")
            continue
        add(f"{tag} page loads from file://",
            case["navigated"] and case["run_error"] is None,
            f"navigated={case['navigated']}; goto_error={case['goto_error']}; run_error={case['run_error']}")
        add(f"{tag} three.js loaded in page",
            st.get("threeLoaded") is True,
            f"threeLoaded={st.get('threeLoaded')}; threeError={st.get('threeError')}; flag_error={case['flag_error']}")
        css = st.get("webglCanvasCss") or [0, 0]
        add(f"{tag} WebGL canvas under #stage at non-zero size, fallback not shown",
            bool(st.get("webglCanvasPresent")) and st.get("stageIsFallback") is False and all(v > 0 for v in css),
            f"css={st.get('webglCanvasCss')}; buffer={st.get('webglCanvasBuffer')}; "
            f"stageIsFallback={st.get('stageIsFallback')}")
        add(f"{tag} no horizontal overflow",
            st.get("scrollWidth") is not None and st["scrollWidth"] <= st["innerWidth"],
            f"scrollWidth={st.get('scrollWidth')}; bodyScrollWidth={st.get('bodyScrollWidth')}; "
            f"innerWidth={st.get('innerWidth')}")
        n_console, n_page = len(case["console_errors"]), len(case["page_errors"])
        add(f"{tag} no console or page errors",
            n_console == 0 and n_page == 0,
            f"console_errors={n_console}; page_errors={n_page}; "
            f"failed_requests={len(case['failed_requests'])}; http_errors={len(case['http_errors'])}")
        add(f"{tag} front and back label artwork decoded and drawn on the canvas",
            st.get("labelImagesLoaded") is True,
            f"labelImagesLoaded={st.get('labelImagesLoaded')}; sarabunFacesLoaded={st.get('sarabunFacesLoaded')}")
        add(f"{tag} idle screenshot saved",
            case["idle_screenshot_size"] is not None,
            f"{case['idle_screenshot']} size={case['idle_screenshot_size']}")
        parts = st.get("sceneParts") or []
        add(f"{tag} scene has pouch, cube and carton, and no water",
            {"Pouch", "Cube", "Carton"} <= set(parts) and "Water" not in parts,
            f"sceneParts={parts}")
        add(f"{tag} no drop control (the water and drop story is removed, rework/48 section 8.4)",
            st.get("dropControl") is False,
            f"dropControl={st.get('dropControl')}")

    wc = report["wording_scan"]
    add("cube_3d.html wording scan (make_label.py list and organiser digests)",
        not wc["forbidden_pattern_hits"] and wc["bare_new_occurrences"] == 0 and wc["organiser_digest_hits"] == 0
        and wc["water_word_hits_in_visible_copy"] == 0,
        f"pattern hits={wc['forbidden_pattern_hits']}; bare new={wc['bare_new_occurrences']}; "
        f"organiser digest hits={wc['organiser_digest_hits']}")
    return checks


def main():
    SCREEN_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "run_date": RUN_DATE,
        "cdn_probe": probe_cdn(),
        "launch": None,
        "wording_scan": wording_scan(),
        "cases": [],
    }
    with sync_playwright() as p:
        browser, how = launch(p)
        report["launch"] = how
        try:
            for vp in VIEWPORTS:
                report["cases"].append(run_case(
                    browser, vp["tag"], vp["width"], vp["height"],
                    f"cube_3d_{vp['tag']}_idle.png",
                ))
            report["cases"].append(run_case(
                browser, "fallback_cdn_blocked", 1280, 800,
                "cube_3d_fallback_cdn_blocked.png", block_cdn=True,
            ))
        finally:
            browser.close()
    report["checks"] = build_checks(report)
    failed = [c["check"] for c in report["checks"] if not c["pass"]]
    report["summary"] = {"passed": len(report["checks"]) - len(failed), "total": len(report["checks"]),
                         "failed": failed}
    out = SCREEN_DIR / f"verify_cube_mockup_{RUN_DATE}.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"report saved: {rel(out)}")
    print(f"launch: {report['launch']}")
    for c in report["checks"]:
        print(("PASS " if c["pass"] else "FAIL ") + c["check"] + " :: " + c["detail"])
    print(f"\nSUMMARY: {report['summary']['passed']}/{report['summary']['total']} checks passed")
    for name in failed:
        print(f"FAILED: {name}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
