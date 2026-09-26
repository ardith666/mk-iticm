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
- **dispatching-parallel-agents** — fan out independent workstreams (LKP / bank-soal / penugasan / studi-kasus)

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

## Core Pattern — 6 Phases with Gates

| Phase | Output | Gate (do not advance on fail) |
|---|---|---|
| 0. Desain | `knowledge/specs/YYYY-MM-DD-<topik>-design.md`: struktur folder, penamaan, cakupan, keputusan yang dikunci user | **User menyetujui desain** sebelum ada file produksi. Jangan mulai bikin deck sebelum ini |
| 1. Ekstraksi RPS | `knowledge/` (KNOWLEDGE.md, history.md, README.md): identitas MK, CPMK→Sub-CPMK→pertemuan map, peta 16 pertemuan, 4 tugas + rubrik, batasan tiap tugas | RPS dibaca penuh; tiap artefak refs Sub-CPMK; **angka RPS dicatat apa adanya** (lihat Pitfalls §A) |
| 2. Struktur | Folders per **Struktur Universal** di bawah; `RPS/` + `knowledge/` = INTERNAL (never to students, incl. kisi-kisi); produktivitas di `pptx/` (presentasi) + `pembahasan/pXX-*/` (isi praktik) + `operasional/` (ujian + admin). Tooling di `knowledge/scripts/`. Root `README.md` untuk manusia | Structure written to knowledge before producing; naming follows Konvensi Penamaan (kebab lowercase, nama Indonesia) |
| 3. Produksi | Decks (reference-driven, see below) → runnable code (lint + run, expected outputs in comments) → lembar kerja praktikum → bank-soal + kisi-kisi → penugasan + 4×4 rubrics → studi-kasus (cases distinct from slides) | Counts + execution proofs per batch; **checklist wajib per MK** (see below) |
| 4. Operasional | `operasional/`: semester calendar (DRAFT dates), Moodle XML parsed from uts.md/uas.md (count match), upload checklist, gradebook xlsx (weight row sums 100, formulas verified) | XML parses; question count equals source |
| 5. Serah terima | Root `README.md` (lihat WEB README di bawah), knowledge status, history entry; render proof (export PDFs, pages = slides) | Zero drift: grep banned terms (e.g. old tool names) + **audit penamaan** (see below) |

### Isi Root `README.md` (wajib — bahasa mudah dibaca)

README adalah pintu masuk manusia (dosen). Minimal berisi:

1. **Struktur folder** — pohon + tabel penjelasan tiap folder (isi & untuk siapa),
   termasuk penanda mana yang **tidak** dibagikan ke mahasiswa.
2. **Alur mengajar** — tabel 16 pertemuan: topik, Sub-CPMK, metode, bobot (apa adanya
   dari RPS), plus pola satu siklus per pertemuan (baca materi → kerjakan LKP →
   jalankan kode → latihan soal → tugas) dan daftar tugas + rubrik.
3. **Peta path** — tabel "mau cari apa, di mana": deck, draft, materi, LKP, soal,
   bank soal, kisi-kisi, kalender, Moodle XML, gradebook, KNOWLEDGE, history, specs, scripts.
4. **Cara build** — perintah singkat + syarat tool.
5. **Aturan pembagian** — tabel boleh/tidak boleh dibagikan.

## Pitfalls RPS — jebakan pembacaan (2026-09-26)

### §A Angka "bobot" di RPS ada dua jenis, jangan dicampur
RPS SmartDos memuat minimal dua tabel berbeda yang sama-sama menyebut "Bobot (%)":
1. **Bobot penilaian** = bobot komponen nilai mata kuliah (UTS/UAS/tugas).
2. **Rubrik penilaian analitik** = bobot **kriteria penilaian satu tugas/proyek**.

Contoh nyata (IF022): angka **30/40/15/15** ternyata adalah rubrik *Proyek Akhir*
(Kualitas Analisis 30 · Kebenaran Implementasi 40 · Kreativitas 15 · Presentasi 15),
**bukan** bobot nilai MK. Salah baca ini bikin P00 menampilkan bobot yang salah.
**Aturan:** saat ekstraksi, catat **judul tabel** di KNOWLEDGE.md, bukan cuma angkanya.
Kalau RPS tidak memuat bobot nilai MK → pakai nilai relatif + "dapat disesuaikan".

### §B Bobot RPS tidak selalu jumlah 100
Bobot pertemuan IF022 = 98% (2% tidak dirinci). **Jangan dipaksa jadi 100** —
cukup tulis apa adanya + catatan "sisanya dapat disesuaikan" (anti-fabrikasi).

### §C RPS bisa berformat `.docx` dengan `altChunk` (MHT)
Beberapa file RPS SmartDos tidak menyimpan teks di `word/document.xml`; isinya ada di
`word/afchunk.mht` (MIME HTML, biasanya `quoted-printable`). Gejalanya: ekstraksi
`<w:p>` mengembalikan **0 paragraf** padahal file 32 KB.
**Cara cek cepat:** `unzip -l file.docx` → kalau ada `afchunk.mht`, baca part itu
(bukan `document.xml`).

### §Batasan tugas dari RPS wajib masuk artefak
RPS_IF022 menyebut batasan konkret: graf A* ≥10 simpul, studi kasus ≥10 aturan inferensi,
dataset nyata (iris/credit scoring) untuk KNN, kelompok 3–4 orang untuk Proyek Akhir.
**Batasan ini wajib muncul di LKP, penugasan, dan slide** — jangan disederhanakan jadi
"seperti contoh".

## Struktur Universal Folder (wajib semua MK)

```
<MK>/
├── README.md                     # ringkasan MK utk manusia
├── RPS/                          # docx SmartDos-obe (1 file)
├── knowledge/                    # INTERNAL — tidak untuk mahasiswa
│   ├── KNOWLEDGE.md
│   ├── README.md
│   ├── history.md
│   ├── specs/                    # design doc rebuild (opsional tapi berguna)
│   └── scripts/                  # tooling build & QC (WAJIB)
│       ├── deck_build.py  build-deck.py
│       ├── build-dokumen.py            # md → docx → pdf
│       └── cek-lint.sh                 # php -l + run + cek parity
├── pptx/                         # SARANA PRESENTASI
│   ├── draft/draft-p00.md …      # sumber narasi (markdown)
│   ├── p00-pengantar-kontrak-kuliah.pptx
│   ├── p01-….pptx … p16-….pptx
│   ├── pdf/                      # export PDF tiap deck (wajib)
│   └── diagram/                  # source .drawio/.mmd + PNG
├── pembahasan/                    # ISI PRAKTIK & TUGAS — per Pertemuan
│   ├── README.md                 # indeks: PXX → file apa saja (satu titik masuk)
│   └── p00-kontrak-kuliah/ … p15-…/     # satu folder per pertemuan
│       ├── materi.md                      # versi panjang narasi + pembahasan
│       ├── lembar-kerja-praktikum.md      # langkah praktik bertiming
│       ├── soal.md                        # soal latihan
│       ├── kunci-jawaban.md               # INTERNAL
│       ├── contoh-kode/pXX-slug.php       # runnable
│       ├── penugasan.md                   # tugas formal
│       ├── studi-kasus.md
│       └── diagram/                       # sumber + PNG
├── operasional/                  # OPERASIONAL & ADMIN — tidak untuk mahasiswa
│   ├── uts.md, uas.md                     # bank soal + kunci (INTERNAL)
│   ├── kisi-kisi-uts.md, kisi-kisi-uas.md # pemetaan Sub-CPMK → soal
│   ├── kalender-semester.md
│   ├── upload-checklist.md
│   ├── moodle-bank-soal.xml               # XML Moodle (dari uts.md/uas.md)
│   └── gradebook.xlsx                     # bobot nilai (baris sum 100)
└── README.md
```

> [!important] Tiga Folder Tunggal (2026-09-26)
> Top level cuma **empat**: `pptx/` (presentasi), `pembahasan/` (isi praktik),
> `operasional/` (ujian + admin), `knowledge/` (internal + scripts).
> - `bank-soal/` + `ops/` digabung jadi **`operasional/`** — semuanya non-ajar.
> - `scripts/` pindah ke **`knowledge/scripts/`** — tooling adalah knowledge.
> - Isi praktik (`jobsheet`/LKP, `contoh-kode`, `penugasan`, `studi-kasus`) **tidak**
>   punya folder top-level sendiri: semuanya di dalam `pembahasan/pXX-*/`.

> [!important] Aturan Cermin (Mirror Rule) — diperbarui 2026-09-26
> **PPTX = sarana presentasi. `pembahasan/pXX-*/` = isi praktik & tugas.**
> Isi `pembahasan/pXX-*/` mencerminkan deck PXX secara lengkap: narasi → `materi.md`,
> kode → `contoh-kode/*.php`, soal → `soal.md`, jawaban → `kunci-jawaban.md`,
> tugas → `penugasan.md`, praktik → `lembar-kerja-praktikum.md`, kasus → `studi-kasus.md`,
> diagram → `diagram/`. **Tidak boleh ada materi ajar yang hanya hidup di dalam PPTX** —
> mahasiswa harus bisa belajar & berlatih tanpa membuka satu pun file pptx.

> [!note] Isi vs Struktur
> Yang dibakukan = struktur + penamaan. **Isi wajib mengikuti RPS masing-masing MK** (jumlah pertemuan, topik, jumlah tugas, prodi berbeda). Audit 2026-09-19 menemukan BD tanpa P00/panduan/PDF, KB tanpa panduan — semua karena checklist tidak dijalankan secara konsisten.

## Dua Format: `.md` untuk dosen, `.pdf` untuk mahasiswa

> Diperbarui 2026-09-26 (Kecerdasan Buatan). Setiap dokumen student-facing ditulis
> **dua kali**: `.md` (sumber kerja dosen) dan `.pdf` (file yang dibagikan ke mahasiswa).
> Dosen tidak akan pernah membagikan file `.md` ke mahasiswa.

| Artefak | Format | Catatan |
|---|---|---|
| Deck | `.pptx` + `.pdf` (`pptx/pdf/`) | parity halaman == slide |
| Materi, LKP, soal, kunci, penugasan, studi kasus, bank soal, ops | `.md` **+ `.pdf`** | pdf = file Distributions |
| Contoh kode | `.php` saja | runnable, tidak perlu pdf |
| Gradebook, XML Moodle | `.xlsx` / `.xml` | biner, tidak perlu pdf |

**Pipeline PDF:** `pandoc (md → docx) → soffice --headless (docx → pdf)`.
Terverifikasi jalan tanpa LaTeX; A4 + nomor halaman otomatis dari docx.
Kunci jawaban diberi heading/watermark **"RAHASIA DOSEN"** di PDF-nya.

## Konvensi Penamaan (kebab lowercase, nama Indonesia — tunggal, tanpa variasi)

| Artefak | Format |
|---|---|
| Deck | `p00-pengantar-kontrak-kuliah.pptx`, `p01-pengenalan-ai.pptx`, `p08-uts.pptx`, `p16-uas.pptx` |
| Draft deck | `pptx/draft/draft-pXX.md` |
| PDF export deck | nama sama dengan deck, di `pptx/pdf/` |
| Materi | `pembahasan/pXX-slug/materi.md` + `.pdf` |
| **Lembar kerja praktikum** | `pembahasan/pXX-slug/lembar-kerja-praktikum.md` + `.pdf` (16 buah, termasuk UTS & UAS) |
| Soal | `pembahasan/pXX-slug/soal.md` + `.pdf` |
| Kunci jawaban | `pembahasan/pXX-slug/kunci-jawaban.md` + `.pdf` (INTERNAL) |
| Contoh kode | `pembahasan/pXX-slug/contoh-kode/pXX-slug.php` |
| Penugasan | `pembahasan/pXX-slug/penugasan.md` + `panduan-pengumpulan.md` |
| Studi kasus | `pembahasan/pXX-slug/studi-kasus.md` |
| Bank soal | `operasional/uts.md`, `operasional/uas.md`, `operasional/kisi-kisi-uts.md`, `operasional/kisi-kisi-uas.md` (+ `.pdf`) |
| Operasional | `operasional/kalender-semester.md`, `operasional/upload-checklist.md`, `operasional/moodle-bank-soal.xml`, `operasional/gradebook.xlsx` |
| kode | `pXX-slug.php` / `.html` / `.sql` |

> [!warning] Larangan nama
> **Jangan lagi memakai istilah "jobsheet"** — gunakan **lembar kerja praktikum**
> (singkat: LKP). Larangan juga: campuran casing (`P00_Pengantar_…`),
> underscore sebagai pemisah kata, file sampah (`~$*.pptx`, `.DS_Store`),
> draft tak terpakai.

## Istilah Artefak

| Istilah | Arti | Dipakai di |
|---|---|---|
| **Materi** | Memahami — konsep, angka, pembahasan mendalam, pertanyaan refleksi | `materi.md` |
| **Lembar kerja praktikum (LKP)** | Mengerjakan — langkah bertiming di kelas + kriteria selesai | `lembar-kerja-praktikum.md` |
| **Contoh kode** | Kode referensi runnable | `contoh-kode/*.php` |
| **Soal + kunci** | Berlatih sendiri, kunci untuk cek mandiri | `soal.md`, `kunci-jawaban.md` |
| **Penugasan** | Tugas yang dinilai & dikumpulkan | `penugasan.md` |
| **Studi kasus** | Analisis kasus, tantangan/proyek | `studi-kasus.md` |

## Checklist Wajib per MK (gate fase 3)

1. `P00` kontrak kuliah ada (BD kelewat — mulai dari P01)
2. `penugasan/panduan-pengumpulan.md` ada (BD & KB kelewat)
3. Deck `P01–P16` lengkap sesuai map pertemuan RPS
4. PDF export **semua** deck di `pptx/pdf/` (TL, BD, KB kelewat)
5. `pembahasan/pXX-*/contoh-kode/` runnable (lint + output tercatat)
6. `pembahasan/pXX-*/lembar-kerja-praktikum.md` per pertemuan (16, termasuk UTS & UAS)
7. `pembahasan/pXX-*/soal.md` + `kunci-jawaban.md` per pertemuan; `operasional/uts.md`/`uas.md` + kisi-kisi
8. `pembahasan/pXX-*/penugasan.md` jumlah tugas sesuai RPS MK tsb + `panduan-pengumpulan.md`
9. `pembahasan/pXX-*/studi-kasus.md` per pertemuan
10. **Setiap dokumen student-facing punya `.pdf`** (materi, LKP, soal, kunci, penugasan, studi-kasus, bank soal, ops)
11. `pembahasan/README.md` indeks navigasi + root `README.md` counts
12. `operasional/`: kalender, upload-checklist, moodle XML (parses, count = sumber), gradebook (bobot sum 100)
13. `knowledge/history.md` entry per batch + root README counts
14. Audit penamaan di akhir (grep casing/underscore/sampah) — see Fase 5

## Audit Konsistensi (fase 5, wajib)

- **Jangan hapus folder/backup lama sebelum user konfirmasi.** Saat rebuild, backup
  (mis. `backup-v3/`) dihapus **hanya setelah** user menyatakan selesai. Rebuild =
  produksi dari draft; backup = jaring pengaman kalau ada yang tak sengaja terhapus.
- `find . -iname "*_*"` → gak ada file ber-underscore selain `.git`
- `find . -iname "~$*" -o -iname "*.DS_Store"` → kosong
- `find . -iname "*jobsheet*"` → **kosong** (istilah lama, ganti lembar-kerja-praktikum)
- `ls pptx/pdf` == `ls pptx/*.pptx` (count sama, nama konsisten)
- **Cermin:** untuk tiap PXX, isi deck PXX punya pasangan di `pembahasan/pXX-*/` (materi, soal, kunci, kode, LKP)
- **PDF:** tiap `.md` student-facing punya `.pdf` pasangannya
- `test -f penugasan/panduan-pengumpulan.md` dan `test -f pptx/p00-*.pptx` → exit 0
- Jika gagal: backfill dulu sebelum serah terima.

## Slide Rules (from real failures)
- **Reference first:** dissect a liked reference deck precisely (shape type, radius, fills, fonts, max cards/slide) BEFORE rebuilding. Never ship thin one-bullet decks.
- **Narasi = "cer mengalir, siap dibacakan"** (lihat `pptx-iticm/references/slide-rules.md` §7.9): 5–8 kalimat, pembuka konteks/analogi, isi, angka, penutup transisi. **Dilarang** meta-pembuka "Slide ini menjelaskan tentang…".
- **Tugas OBE 2 tipe:** Tipe A drill (every deck, ungraded) + Tipe B formal (milestone meetings only, full instructions + rubric ref). Exam decks (UTS/UAS) get NO new task slides.
- **Diagrams:** draw.io/mermaid sources + embedded PNGs; tool tutorials (install, setup, export) inside meetings that need them.
- **Logo/branding:** full brand on title + closing only; content slides keep footer label.

## Anti-Fabrication (baseline agents invent these)
| Excuse | Reality |
|---|---|
| "Weights % look professional" | NEVER invent grade weights/dates — relative deadlines + configurable weight rows only |
| "One generic deck is fine" | Each deck's content must match its meeting title; audit titles per slide |
| "Tool X is equivalent" | One sanctioned toolchain per worksheet (e.g. Laragon, never mixed with XAMPP) — grep-enforce |
| "Kisi-kisi with student files is fine" | Kisi-kisi + keys stay internal until the exam week |
| "Makin detail angkanya, makin bagus slide-nya" | Nomor di slide harus berasal dari sumber terverifikasi (literatur/dataset) dan dicek ulang dengan kode saat build — bukan dikarang agar terlihat ramai |

## Quick Reference
- Proof commands: slide-title dump per deck, `php -l` + run with expected outputs, XML parse + count, PDF pages = slides
- Dokumen: `knowledge/scripts/build-dokumen.py` (md → docx → pdf) untuk semua artefak student-facing
- 4-way parallel split: lembar-kerja-praktikum / bank-soal+blueprints / penugasan+rubrics / studi-kasus — then self-verify counts and spot-check formats
- Record everything: Todo Aktif in KNOWLEDGE.md, timestamped history entries, root README counts
