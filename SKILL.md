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
| 2. Struktur | Folders: `RPS/` + `knowledge/` = INTERNAL (never to students, incl. kisi-kisi); `pptx/`, `contoh-kode/`, `jobsheet/`, `bank-soal/`, `penugasan/`, `studi-kasus/`, `ops/` = product. Root `README.md` for humans | Structure written to knowledge before producing |
| 3. Produksi | Decks (reference-driven, see below) → runnable code (lint + run, expected outputs in comments) → jobsheet → bank-soal + kisi-kisi → penugasan + 4×4 rubrics → studi-kasus (cases distinct from slides) | Counts + execution proofs per batch |
| 4. Ops | `ops/`: semester calendar (DRAFT dates), Moodle XML parsed from bank-soal (count match), upload checklist, gradebook xlsx (weight row sums 100, formulas verified) | XML parses; question count equals source |
| 5. Serah terima | Root README counts, knowledge status, history entry; render proof (export PDFs via real PowerPoint, pages = slides) | Zero drift: grep banned terms (e.g. old tool names) |

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
