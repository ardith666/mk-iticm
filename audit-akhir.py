#!/usr/bin/env python3
"""audit-akhir.py — GATE WAJIB sebelum worksheet dianggap selesai.

Satu perintah, satu exit code. Kalau exit != 0, worksheet BELUM selesai
walaupun semua file sudah dibuat.

    python3 audit-akhir.py /path/ke/mk

Exit 0 = semua cek lolos, boleh serah terima.
Exit 1 = ada cek gagal, perbaiki dulu lalu jalankan ulang.

Daftar cek diambil dari bagian "Audit Konsistensi (fase 5)" di SKILL.md
dan dari pelajaran rebuild slow-logic IT104.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Karakter non-Latin yang tidak boleh ada di dokumen .md
CJK = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\u0400-\u04ff\uac00-\ud7af\u0600-\u06ff]")


class Audit:
    def __init__(self, project: Path):
        self.p = project
        self.rows = []

    def cek(self, nama, temuan, ok=""):
        n = len(temuan)
        if n:
            msg = f"{n} temuan: " + "; ".join(str(t)[:60] for t in temuan[:3])
        else:
            msg = ok or "bersih"
        self.rows.append((nama, "FAIL" if n else "PASS", msg))
        return n

    def rel(self, f):
        try:
            return str(f.relative_to(self.p))
        except ValueError:
            return str(f)

    def files(self, pattern):
        return [f for f in self.p.rglob(pattern) if f.is_file()]

    def report(self):
        lebar = max(len(r[0]) for r in self.rows)
        gagal = sum(1 for r in self.rows if r[1] == "FAIL")
        print()
        print("=" * 78)
        print(f"AUDIT AKHIR — {self.p}")
        print("=" * 78)
        for nama, status, msg in self.rows:
            print(f"[{status}] {nama.ljust(lebar)}  {msg}")
        print("-" * 78)
        if gagal:
            print(f"RESULT: GAGAL — {gagal} cek belum lolos. Worksheet BELUM selesai.")
            print("Perbaiki temuan di atas, lalu jalankan ulang:")
            print(f"  python3 {Path(__file__).name} {self.p}")
            return 1
        print("RESULT: LOLOS — semua cek hijau. Boleh serah terima.")
        return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    P = Path(argv[1]).expanduser().resolve()
    if not P.is_dir():
        print(f"bukan folder: {P}")
        return 1
    a = Audit(P)

    # ── 1. Penamaan ─────────────────────────────────────────
    a.cek("1. file ber-underscore (selain .git)",
          [a.rel(f) for f in a.files("*_*") if ".git" not in f.parts])
    a.cek("2. file sampah (~$* / .DS_Store)",
          [a.rel(f) for f in a.files("~$*") + a.files(".DS_Store")])
    a.cek("3. istilah lama 'jobsheet'", [a.rel(f) for f in a.files("*jobsheet*")])
    a.cek("4. folder kosong",
          [a.rel(d) for d in P.rglob("*") if d.is_dir() and not any(d.iterdir())])

    # ── 2. Pemisahan dosen vs mahasiswa ─────────────────────
    a.cek("5. .md di dalam folder NN/ (harus 0)",
          [a.rel(f) for f in P.rglob("*.md")
           if f.parent.name.isdigit() or (f.parent.parent.name.isdigit() and f.parent.name in
                                           ("bacaan", "praktikum", "latihan", "contoh-kode", "diagram"))])

    sb = P / "siap-bagikan"
    if sb.is_dir():
        leak = [a.rel(f) for f in sb.rglob("*") if f.is_file()
                and ("kunci" in f.name.lower() or "kisi" in f.name.lower()
                     or f.suffix == ".md")]
        a.cek("6. kebocoran di siap-bagikan/ (kunci/kisi/.md)", leak)

        extra = [d.name for d in sb.iterdir() if d.is_dir() and d.name != "pertemuan"]
        a.cek("7. subfolder tambahan di siap-bagikan/ (harus 0)", extra)

        # tiap folder pertemuan harus punya deck pdf-nya sendiri
        tanpa_deck = []
        folders = sorted(d for d in (sb / "pertemuan").glob("*") if d.is_dir())
        for d in folders:
            if not any(re.match(r"^p\d\d-.*\.pdf$", f.name) for f in d.iterdir()):
                tanpa_deck.append(a.rel(d))
        a.cek("8. folder pertemuan tanpa deck pdf", tanpa_deck,
              f"{len(folders)} folder, semua punya deck pdf")
    else:
        a.cek("6-8. siap-bagikan/", ["folder siap-bagikan/ tidak ada"])

    # rubrik internal tidak boleh di penugasan.md di akar
    bocor_rubrik = [a.rel(f) for f in P.rglob("penugasan.md") if "RAHASIA" in f.read_text(encoding="utf-8", errors="ignore")]
    a.cek("9. rubrik RAHASIA di penugasan.md", bocor_rubrik)

    # ── 3. Bahasa ───────────────────────────────────────────
    nonlatin = []
    for f in P.rglob("*.md"):
        bad = CJK.findall(f.read_text(encoding="utf-8", errors="ignore"))
        if bad:
            nonlatin.append(f"{a.rel(f)}: {''.join(sorted(set(bad))[:6])}")
    a.cek("10. karakter non-Latin di .md", nonlatin)

    # ── 4. Deck ─────────────────────────────────────────────
    pptx = sorted(P.glob("pptx/p*.pptx"))
    pdf = sorted((P / "pptx" / "pdf").glob("*.pdf")) if (P / "pptx" / "pdf").is_dir() else []
    a.cek("11. jumlah deck pptx == pdf export",
          [f"{len(pptx)} pptx vs {len(pdf)} pdf"] if len(pptx) != len(pdf) else [],
          f"{len(pptx)} deck, {len(pdf)} pdf, parity")

    mmd = sorted((P / "pptx" / "diagram").glob("*.mmd")) if (P / "pptx" / "diagram").is_dir() else []
    png = sorted((P / "pptx" / "diagram").glob("*.png")) if (P / "pptx" / "diagram").is_dir() else []
    a.cek("12. pasangan diagram mmd+png",
          [f"{len(mmd)} mmd vs {len(png)} png"] if len(mmd) != len(png) else [],
          f"{len(mmd)} pasangan lengkap")

    # ── 5. Kode contoh ──────────────────────────────────────
    gagal = []
    php = [f for f in P.rglob("*.php")]
    for f in php:
        with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False, encoding="utf-8") as tf:
            tf.write(f.read_text(encoding="utf-8", errors="ignore"))
            tmp = tf.name
        r = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
        Path(tmp).unlink(missing_ok=True)
        if r.returncode != 0:
            gagal.append(f"{a.rel(f)}: {r.stderr.strip()[:60]}")
    a.cek("13. php -l semua contoh kode", gagal, f"{len(php)} file lolos")

    # ── 6. Operasional ───────────────────────────────────────
    gb = P / "operasional" / "lms" / "gradebook.csv"
    if gb.is_file():
        try:
            rows = [r for r in csv.DictReader(gb.open(encoding="utf-8"))
                    if r.get("Komponen", "").strip().upper() != "TOTAL"]
            total = sum(int(r["Bobot"].strip().rstrip("%")) for r in rows)
            a.cek("14. bobot gradebook = 100%",
                  [f"total {total}%"] if total != 100 else [], f"{len(rows)} komponen, {total}%")
        except Exception as e:
            a.cek("14. bobot gradebook = 100%", [f"gagal baca: {e}"])
    else:
        a.cek("14. bobot gradebook = 100%", ["gradebook.csv tidak ada"])

    moodle = sorted((P / "operasional" / "lms").glob("*.xml")) if (P / "operasional" / "lms").is_dir() else []
    if moodle:
        err = []
        for x in moodle:
            try:
                ET.parse(x)
            except Exception as e:
                err.append(f"{a.rel(x)}: {e}")
        a.cek("15. XML Moodle parse", err, f"{len(moodle)} file parse OK")
    else:
        a.cek("15. XML Moodle parse", ["tidak ada .xml di operasional/lms/"])

    # ── 7. Dokumen wajib ────────────────────────────────────
    wajib = {
        "README root": P / "README.md",
        "indeks pembahasan": P / "pembahasan" / "README.md",
        "panduan pengumpulan": P / "pembahasan" / "panduan-pengumpulan.md",
        "KNOWLEDGE": P / "knowledge" / "KNOWLEDGE.md",
        "history": P / "knowledge" / "history.md",
        "spec desain": P / "knowledge" / "specs",
        "RPS": P / "RPS",
        "draft deck": P / "pptx" / "draft",
    }
    hilang = [nama for nama, path in wajib.items() if not path.exists()]
    a.cek("16. dokumen wajib ada", hilang, f"{len(wajib)} dokumen/folder ada")

    return a.report()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
