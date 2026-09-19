---
name: mk-iticm
description: Use when building a complete lecturer worksheet for one course from an RPS — slides, reference code, lab sheets, quiz banks, assignments, Moodle package (OBE, CPMK, UTS/UAS, Laragon, draw.io)
---

# MK-ITICM

## Overview
Proven pattern for turning one course RPS into a full teaching worksheet: knowledge base, 16-meeting slide decks, runnable code, labs, quiz banks, assignments with rubrics, and LMS-ready ops files. Distilled from building Algoritma & Pemrograman Dasar (IT104): 17 decks, 353 slides, 100+ product files.

## When to Use
- New course worksheet from an RPS document (any prodi ITICM)
- User says: worksheet matkul, perangkat pembelajaran, RPS jadi bahan ajar
- NOT for: single-slide edits (use pptx-iticm directly), general scripting, non-course projects

## REQUIRED BACKGROUND
- **dev-methodology** — knowledge/ discipline: KNOWLEDGE.md + history.md (append-only, timestamped), Todo Aktif tracking
- **pptx-iticm** — branded decks (dark navy `#1a1a2e`, orange `#e86c00`, Calibri/Consolas)
- **dispatching-parallel-agents** — fan out independent workstreams (jobsheet / bank-soal / penugasan / studi-kasus)

## Instalasi di Mesin Lain

`mk-iticm` adalah **entry point**. Skill ini hanya orkestrasi — tanpa dependensi di
bawah, alur berhenti di phase yang membutuhkannya. Saat setup mesin baru, install
skill ini lalu clone dependensi yang belum ada ke folder skills agent:

| Skill | Repo / Sumber | Install |
|---|---|---|
| `mk-iticm` (ini) | `https://github.com/ardith666/mk-iticm` | `git clone https://github.com/ardith666/mk-iticm ~/.agents/skills/mk-iticm` |
| `pptx-iticm` | `https://github.com/ardith666/pptx-iticm` | `git clone https://github.com/ardith666/pptx-iticm ~/.agents/skills/pptx-iticm` |
| `dev-methodology` | `https://github.com/ardith666/dev-methodology` | `git clone https://github.com/ardith666/dev-methodology ~/.agents/skills/dev-methodology` |
| `dispatching-parallel-agents` | `obra/superpowers` (plugin) | install plugin superpowers, atau clone `https://github.com/obra/superpowers` dan salin `skills/dispatching-parallel-agents/` |

Verifikasi: `pip install python-pptx` (dipakai `pptx-iticm` di phase decks) dan font
Calibri/Consolas harus terpasang sebelum fase Produksi (Phase 3).

## Core Pattern — 5 Phases with Gates
| Phase | Output | Gate (do not advance on fail) |
|---|---|---|
| 1. Ekstraksi RPS | `knowledge/` (KNOWLEDGE.md, history.md, README.md): identitas MK, CPMK→Sub-CPMK→pertemuan map, 16-meeting map, 8-component standard, task types | RPS read in full; every later artifact refs a Sub-CPMK |
| 2. Struktur | Folders per **Struktur Universal** di bawah; `RPS/` + `knowledge/` = INTERNAL (never to students, incl. kisi-kisi); produktivitas di `pptx/`, `contoh-kode/`, `jobsheet/`, `bank-soal/`, `penugasan/`, `studi-kasus/`, `ops/`. Root `README.md` for humans | Structure written to knowledge before producing; naming follows Konvensi Penamaan (kebab lowercase) |
| 3. Produksi | Decks (reference-driven, see below) → runnable code (lint + run, expected outputs in comments) → jobsheet → bank-soal + kisi-kisi → penugasan + 4×4 rubrics → studi-kasus (cases distinct from slides) | Counts + execution proofs per batch; **checklist wajib per MK** (see below) |
| 4. Ops | `ops/`: semester calendar (DRAFT dates), Moodle XML parsed from bank-soal (count match), upload checklist, gradebook xlsx (weight row sums 100, formulas verified) | XML parses; question count equals source |
| 5. Serah terima | Root README counts, knowledge status, history entry; render proof (export PDFs via real PowerPoint, pages = slides) | Zero drift: grep banned terms (e.g. old tool names) + **audit penamaan** (see below) |

## Struktur Universal Folder (wajib semua MK)

```
<MK>/
├── README.md                     # ringkasan MK utk manusia
├── RPS/                          # docx SmartDos-obe (1 file)
├── knowledge/                    # INTERNAL — tidak untuk mahasiswa
│   ├── KNOWLEDGE.md
│   ├── README.md
│   └── history.md
├── pptx/
│   ├── p00-pengantar-kontrak-kuliah.pptx
│   ├── p01-….pptx … p16-….pptx
│   ├── pdf/                      # export PDF tiap deck (wajib)
│   └── diagram/                  # source .drawio (optional)
├── contoh-kode/                  # runnable, sesuai pertemuan
├── jobsheet/                     # jobsheet-pXX-*.md
├── bank-soal/
│   ├── pXX-*.md                  # bank per pertemuan
│   ├── uts.md, uas.md
│   └── kisi-kisi-uts.md, kisi-kisi-uas.md
├── penugasan/
│   ├── panduan-pengumpulan.md    # WAJIB ada
│   └── tugas-N-*.md              # jumlah sesuai RPS MK
├── studi-kasus/
│   └── kasus-pXX-*.md
├── ops/
│   ├── kalender-semester.md
│   ├── upload-checklist.md
│   ├── moodle-bank-soal.xml
│   └── gradebook.xlsx
└── scripts/                      # optional: build_decks/, diagrams/
```

> [!note] Isi vs Struktur
> Yang dibakukan = struktur + penamaan. **Isi wajib mengikuti RPS masing-masing MK** (jumlah pertemuan, topik, jumlah tugas, prodi berbeda). Audit 2026-09-19 menemukan BD tanpa P00/panduan/PDF, KB tanpa panduan — semua karena checklist tidak dijalankan secara konsisten.

## Konvensi Penamaan (kebab lowercase — tunggal, tanpa variasi)

| Artefak | Format |
|---|---|
| Deck | `p00-pengantar-kontrak-kuliah.pptx`, `p01-konsep-dasar-….pptx`, `p08-uts.pptx`, `p16-uas.pptx` |
| PDF export | nama sama dengan deck, di `pptx/pdf/` |
| Jobsheet | `jobsheet-pXX-slug.md` (contoh `jobsheet-p05-variabel-operator.md`) |
| Bank soal | `pXX-slug.md` + `uts.md` / `uas.md` |
| Kisi-kisi | `kisi-kisi-uts.md`, `kisi-kisi-uas.md` (di `bank-soal/`; kunci jawaban tetap di `knowledge/`) |
| Penugasan | `tugas-N-slug.md` + `panduan-pengumpulan.md` |
| Studi kasus | `kasus-pXX-slug.md` |
| ops | `kalender-semester.md`, `upload-checklist.md`, `moodle-bank-soal.xml`, `gradebook.xlsx` |
| kode | `pXX-slug.php` / `.html` / `.sql` |

**Dilarang:** campuran casing (`P00_Pengantar_…`, `P01-Konsep-Dasar-…`, `Tugas01_…`, `01_Nama.md`, `kasus-01-…`), underscore sebagai pemisah kata, file sampah (`~$*.pptx`, `.DS_Store`, draft tak terpakai).

## Checklist Wajib per MK (gate fase 3)

1. `P00` kontrak kuliah ada (BD kelewat — mulai dari P01)
2. `penugasan/panduan-pengumpulan.md` ada (BD & KB kelewat)
3. Deck `P01–P16` lengkap sesuai map pertemuan RPS
4. PDF export **semua** deck di `pptx/pdf/` (TL, BD, KB kelewat)
5. `contoh-kode/` runnable (lint + output tercatat)
6. `jobsheet/` per pertemuan praktikum
7. `bank-soal/` per pertemuan + `uts.md`/`uas.md` + kisi-kisi
8. `penugasan/` jumlah tugas sesuai RPS MK tsb (3 vs 4 tugas = beda RPS, wajar)
9. `studi-kasus/` per pertemuan
10. `ops/`: kalender, upload-checklist, moodle XML (parses, count = sumber), gradebook (bobot sum 100)
11. `knowledge/history.md` entry per batch + root README counts
12. Audit penamaan di akhir (grep casing/underscore/sampah) — see Fase 5

## Audit Konsistensi (fase 5, wajib)

- `find . -iname "*_*"` → gak ada file ber-underscore selain `.git`
- `find . -iname "~$*" -o -iname "*.DS_Store"` → kosong
- `ls pptx/pdf` == `ls pptx/*.pptx` (count sama, nama konsisten)
- `test -f penugasan/panduan-pengumpulan.md` dan `test -f pptx/p00-*.pptx` → exit 0
- Jika gagal: backfill dulu sebelum serah terima.

## Slide Rules (from real failures)
- **Reference first:** dissect a liked reference deck precisely (shape type, radius, fills, fonts, max cards/slide) BEFORE rebuilding. Never ship thin one-bullet decks.
- **Tugas OBE 2 tipe:** Tipe A drill (every deck, ungraded) + Tipe B formal (milestone meetings only, full instructions + rubric ref). Exam decks (UTS/UAS) get NO new task slides.
- **Diagrams:** draw.io sources (`.drawio`, valid XML) + embedded PNGs; tool tutorials (install, setup, export) inside meetings that need them.
- **Logo/branding:** full brand on title + closing only; content slides keep footer label.

## Anti-Fabrication (baseline agents invent these)
| Excuse | Reality |
|---|---|
| "Weights % look professional" | NEVER invent grade weights/dates — relative deadlines + configurable weight rows only |
| "One generic deck is fine" | Each deck's content must match its meeting title; audit titles per slide |
| "Tool X is equivalent" | One sanctioned toolchain per worksheet (e.g. Laragon, never mixed with XAMPP) — grep-enforce |
| "Kisi-kisi with student files is fine" | Kisi-kisi + keys stay internal until the exam week |

## Quick Reference
- Proof commands: slide-title dump per deck, `php -l` + run with expected outputs, XML parse + count, PDF pages = slides
- 4-way parallel split: jobsheet / bank-soal+blueprints / penugasan+rubrics / studi-kasus — then self-verify counts and spot-check formats
- Record everything: Todo Aktif in KNOWLEDGE.md, timestamped history entries, root README counts
