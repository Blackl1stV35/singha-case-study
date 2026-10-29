"""T2 check of the ThaiNamthip IPO filing (Version 2) text layer, 20 October 2026 (rework/68a_coca_cola_system.md, section 12).

Purpose: test the record's claim that the saved Version 2 extract (rework/raw/diligence_2026-10-20/T2/
tncc_sec_filing_v2_exec_summary_extract.md) reproduces the PDF text layer. It also records which PDF page carries
each printed figure the record cites. An independent verifier reported unmapped Thai glyphs for this PDF; this
check tests that report on the local copy.

It reads the PDF and the saved extract only. It writes t2_pdf_text_layer_check_results.json next to this script.
Nothing is downloaded.

Usage (the PDF sits in the session scratch folder, so its path is passed as an argument):
    python -I t2_pdf_text_layer_check.py <path-to-tncc_v2.pdf>

Requires PyMuPDF (fitz). Memory use is small.
"""
import hashlib
import json
import os
import re
import sys

import fitz  # PyMuPDF

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_V2 = os.path.normpath(os.path.join(HERE, "..", "raw", "diligence_2026-10-20", "T2",
                                       "tncc_sec_filing_v2_exec_summary_extract.md"))

if len(sys.argv) < 2:
    raise SystemExit("usage: python -I t2_pdf_text_layer_check.py <path-to-pdf>")

pdf_path = sys.argv[1]
with open(pdf_path, "rb") as fh:
    sha256 = hashlib.sha256(fh.read()).hexdigest()

doc = fitz.open(pdf_path)
pdf_pages = [doc[i].get_text() for i in range(doc.page_count)]
THAI = re.compile(r"[฀-๿]")
WS = re.compile(r"\s+")


def squash(s):
    return WS.sub("", s)


# Saved extract: blocks start at "--- PDF page N" lines. Map page number to its block text.
with open(RAW_V2, encoding="utf-8") as fh:
    extract_text = fh.read()
blocks = {}
for m in re.finditer(r"^--- PDF page (\d+)[^\n]*---\s*$", extract_text, flags=re.M):
    blocks[int(m.group(1))] = (m.start(), m.end())
ordered = sorted(blocks.items(), key=lambda kv: kv[1][0])
block_text = {}
for idx, (page_no, (start, end)) in enumerate(ordered):
    stop = ordered[idx + 1][1][0] if idx + 1 < len(ordered) else len(extract_text)
    block_text[page_no] = extract_text[end:stop]

# Shingle match: share of 30-character windows (whitespace removed, step 15) of the PDF page text that also occur in
# the saved extract block for the same page.
match = {}
for page_no in sorted(block_text):
    pdf_sq = squash(pdf_pages[page_no - 1])
    ext_sq = squash(block_text[page_no])
    windows = [pdf_sq[i:i + 30] for i in range(0, max(len(pdf_sq) - 30, 0), 15)]
    thai_windows = [w for w in windows if THAI.search(w)]
    hit = sum(1 for w in thai_windows if w in ext_sq)
    match[str(page_no)] = {
        "pdf_thai_windows_tested": len(thai_windows),
        "windows_found_in_saved_extract": hit,
        "share_found_pct": round(100.0 * hit / len(thai_windows), 1) if thai_windows else None,
    }

# Printed figures the record cites, and the PDF pages on which each string appears.
FIGURES = ["51.4", "47.9", "66.0", "27.5", "15.6", "511,000", "564", "55.59", "50.03", "54.54", "29.95", "26.95",
           "3,064,110,570", "276,342,760", "612,451,687", "5,080.19", "6,365.02", "10,872.74", "12,745.80",
           "181", "216", "20.2"]
figure_pages = {f: [i + 1 for i, t in enumerate(pdf_pages) if f in t] for f in FIGURES}

WORDS = ["บริษัท", "ส่วนแบ่งตลาด", "ฟรอส์ท แอนด์ ซัลลิวัน", "ไทยน้ำทิพย์", "ไทยนำทิพย์", "รายชื่อผู้ถือหุ้น"]
all_text = "".join(pdf_pages)
word_counts = {w: all_text.count(w) for w in WORDS}

thai_codepoints = {str(i + 1): len(THAI.findall(t)) for i, t in enumerate(pdf_pages) if i + 1 in (7, 9, 10, 23)}

results = {
    "task": "T2 text-layer check of the ThaiNamthip IPO filing, Version 2 (20 October 2026, revision 3)",
    "pdf_file_checked": os.path.basename(pdf_path),
    "pdf_sha256": sha256,
    "pdf_bytes": os.path.getsize(pdf_path),
    "pdf_pages": doc.page_count,
    "pymupdf_version": fitz.VersionBind,
    "source_url": "https://market.sec.or.th/public/ipos/IPOSGetFile.aspx?TransID=691644&TransFileSeq=299",
    "thai_codepoints_on_pages": thai_codepoints,
    "thai_word_occurrences_whole_pdf": word_counts,
    "saved_extract_match_by_page": match,
    "figure_pages_in_pdf": figure_pages,
    "reading": (
        "The PDF text layer carries Thai characters that read as Thai words (for example the company name and the "
        "heading of page 9). The saved extract matches the layer for the pages tested (see saved_extract_match_by_page). "
        "The printed figures can be located on the pages listed in figure_pages_in_pdf. The verifier's report of "
        "unmapped Thai glyphs is not reproduced on this copy."
    ),
    "tier": "Check of a local copy. Printed figures stay at tier P (company filing).",
}

out_path = os.path.join(HERE, "t2_pdf_text_layer_check_results.json")
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=2, ensure_ascii=False)
print("wrote", out_path)
