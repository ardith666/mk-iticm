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

### Isi skill ini

```
mk-iticm/
├── SKILL.md          # dokumen ini
└── audit-akhir.py    # GATE wajib — 16 cek, exit 0 = boleh serah terima
```

`audit-akhir.py` butuh `php` di PATH (untuk `php -l`). Cek yang butuh `pandoc`
atau `soffice` sengaja tidak dimasukkan karena keduanya sudah tervalidasi
dari pipeline `build-dokumen.py`.

## Core Pattern — 6 Phases with Gates

| Phase | Output | Gate (do not advance on fail) |
|---|---|---|
| 0. Desain | `knowledge/specs/YYYY-MM-DD-<topik>-design.md`: struktur folder, penamaan, cakupan, keputusan yang dikunci user | **User menyetujui desain** sebelum ada file produksi. Jangan mulai bikin deck sebelum ini |
| 1. Ekstraksi RPS | `knowledge/` (KNOWLEDGE.md, history.md, README.md): identitas MK, CPMK→Sub-CPMK→pertemuan map, peta 16 pertemuan, 4 tugas + rubrik, batasan tiap tugas | RPS dibaca penuh; tiap artefak refs Sub-CPMK; **angka RPS dicatat apa adanya** (lihat Pitfalls A) |
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

### A Angka "bobot" di RPS ada dua jenis, jangan dicampur
RPS SmartDos memuat minimal dua tabel berbeda yang sama-sama menyebut "Bobot (%)":
1. **Bobot penilaian** = bobot komponen nilai mata kuliah (UTS/UAS/tugas).
2. **Rubrik penilaian analitik** = bobot **kriteria penilaian satu tugas/proyek**.

Contoh nyata (IF022): angka **30/40/15/15** ternyata adalah rubrik *Proyek Akhir*
(Kualitas Analisis 30 · Kebenaran Implementasi 40 · Kreativitas 15 · Presentasi 15),
**bukan** bobot nilai MK. Salah baca ini bikin P00 menampilkan bobot yang salah.
**Aturan:** saat ekstraksi, catat **judul tabel** di KNOWLEDGE.md, bukan cuma angkanya.
Kalau RPS tidak memuat bobot nilai MK → pakai nilai relatif + "dapat disesuaikan".

### B Bobot RPS tidak selalu jumlah 100
Bobot pertemuan IF022 = 98% (2% tidak dirinci). **Jangan dipaksa jadi 100** —
cukup tulis apa adanya + catatan "sisanya dapat disesuaikan" (anti-fabrikasi).

### C RPS bisa berformat `.docx` dengan `altChunk` (MHT)
Beberapa file RPS SmartDos tidak menyimpan teks di `word/document.xml`; isinya ada di
`word/afchunk.mht` (MIME HTML, biasanya `quoted-printable`). Gejalanya: ekstraksi
`<w:p>` mengembalikan **0 paragraf** padahal file 32 KB.
**Cara cek cepat:** `unzip -l file.docx` → kalau ada `afchunk.mht`, baca part itu
(bukan `document.xml`).

### Batasan tugas dari RPS wajib masuk artefak
RPS_IF022 menyebut batasan konkret: graf A* 10 simpul, studi kasus 10 aturan inferensi,
dataset nyata (iris/credit scoring) untuk KNN, kelompok 3–4 orang untuk Proyek Akhir.
**Batasan ini wajib muncul di LKP, penugasan, dan slide** — jangan disederhanakan jadi
"seperti contoh".

## Struktur Universal Folder (wajib semua MK)

```
<MK>/
├── README.md # ringkasan MK utk manusia
├── RPS/ # docx SmartDos-obe (1 file)
├── knowledge/ # INTERNAL — tidak untuk mahasiswa
│ ├── KNOWLEDGE.md
│ ├── README.md
│ ├── history.md
│ ├── specs/ # design doc rebuild (opsional tapi berguna)
│ └── scripts/ # tooling build & QC (WAJIB)
│ ├── deck_build.py build-deck.py
│ ├── build-dokumen.py # md → docx → pdf
│ └── cek-lint.sh # php -l + run + cek parity
├── pptx/ # SARANA PRESENTASI
│ ├── draft/draft-p00.md # sumber narasi (markdown)
│ ├── p00-pengantar-kontrak-kuliah.pptx
│ ├── p01- .pptx p16- .pptx
│ ├── pdf/ # export PDF tiap deck (wajib)
│ └── diagram/ # source .drawio/.mmd + PNG
├── pembahasan/ # ISI PRAKTIK & TUGAS — per Pertemuan
│ ├── README.md # indeks: PXX → file apa saja (satu titik masuk)
│ └── p00-kontrak-kuliah/ p16-uas/ # satu folder per pertemuan
│ ├── materi.md # sumber kerja (bacaan)
│ ├── lembar-kerja-praktikum.md # sumber kerja (praktikum)
│ ├── soal.md # sumber kerja (latihan)
│ ├── penugasan.md + .pdf # tugas yang dinilai
│ ├── kunci/ # INTERNAL — kunci jawaban (md + pdf)
│ │ ├── kunci-jawaban.md
│ │ └── kunci-jawaban.pdf
│ └── 06/ # NOMOR PERTEMUAN — untuk mahasiswa
│ ├── bacaan/ materi.pdf
│ ├── praktikum/ lembar-kerja-praktikum.pdf
│ ├── latihan/ soal.pdf
│ ├── contoh-kode/ pXX-slug.php
│ └── diagram/ pXX-NN.png
├── operasional/ # OPERASIONAL & ADMIN — tidak untuk mahasiswa
│ ├── soal-ujian/ # bank soal + kunci + kisi-kisi (uts/uas)
│ ├── administrasi/ # kalender-semester, upload-checklist
│ └── lms/ # moodle-bank-soal.xml, gradebook.xlsx
├── siap-bagikan/ # SALINAN semua berkas mahasiswa (siap kirim)
│ └── pertemuan/pXX-*/ # SATU folder per pertemuan = cukup share 1 folder
│ ├── pXX-slug.pdf # deck slide (dari pptx/pdf/)
│ ├── materi.pdf # bacaan
│ ├── lembar-kerja-praktikum.pdf
│ ├── soal.pdf
│ ├── penugasan.pdf # hanya bila ada tugas formal
│ ├── pXX-*.php / .html # contoh kode
│ └── pXX-NN.png # diagram
└── README.md
```

> [!important] Satu Folder = Satu Pertemuan (2026-09-27, atas permintaan user)
> Dosen cukup **share satu folder per pertemuan** — tidak ada lagi
> `siap-bagiankan/slide-deck/` terpisah. PDF deck digabung ke
> `siap-bagikan/pertemuan/pXX-slug/pXX-slug.pdf` karena **nama stem deck
> sudah sama dengan nama folder pertemuan**, jadi tidak perlu tabel pemetaan.
>
> | Yang dibagikan | Letak |
> |---|---|
> | Deck slide | `pertemuan/pXX-slug/pXX-slug.pdf` |
> | Bacaan, praktikum, latihan | `pertemuan/pXX-slug/*.pdf` |
> | Contoh kode, diagram | `pertemuan/pXX-slug/*.php`, `*.png` |
> | Penugasan | `pertemuan/pXX-slug/penugasan.pdf` |
>
> Penugasan **tidak** masuk bila hanya berisi rubrik internal (mis. showcase P16)
> — taruh di `pembahasan/pXX-*/kunci/` supaya skrip otomatis tidak menyalinnya.
>
> Di `siap-bagiankan.py`, tiap rule punya mode penentuan folder pertemuan:
> `meeting` (ambil komponen path ke-2, untuk isi `pembahasan/`) dan
> `bydeck` (ambil stem nama berkas, untuk PDF deck). Both rule wajib menunjuk
> ke `DEST/pertemuan/`, tidak boleh membuat subfolder sendiri.

> [!important] Tiga Folder Tunggal (2026-09-26)
> Top level cuma **empat**: `pptx/` (presentasi), `pembahasan/` (isi praktik),
> `operasional/` (ujian + admin), `knowledge/` (internal + scripts).
> - `bank-soal/` + `ops/` digabung jadi **`operasional/`** — semuanya non-ajar,
> lalu dikelompokkan lagi jadi 3 subfolder (`soal-ujian/`, `administrasi/`, `lms/`).
> - `scripts/` pindah ke **`knowledge/scripts/`** — tooling adalah knowledge.
> - Isi praktik (`jobsheet`/LKP, `contoh-kode`, `penugasan`, `studi-kasus`) **tidak**
> punya folder top-level sendiri: semuanya di dalam `pembahasan/pXX-*/`.

> [!warning] Aturan Pemisahan Dosen vs Mahasiswa (2026-09-26)
> `pembahasan/pXX-*/` dipecah menjadi **3 tingkat** supaya aman saat dibagikan:
>
> | Letak | Isi | Boleh ke mahasiswa? |
> |---|---|---|
> | akar folder `pXX-*/` | semua `.md` (sumber kerja dosen) + `penugasan.pdf` | `.md` tidak |
> | `kunci/` | `kunci-jawaban.md` + `.pdf` (bertanda RAHASIA DOSEN) | **tidak boleh** |
> | `NN/` (nomor pertemuan) | `bacaan/` `praktikum/` `latihan/` (PDF) + `contoh-kode/` (.php) + `diagram/` (.png) | ya |
>
> - Folder berbagi **bernomor** (`p06` → `06`), konsisten dengan nama foldernya.
> - Isi folder `NN/` **tidak boleh ada `.md`** — hanya PDF/PHP/PNG, siap kirim apa adanya.
> - PDF untuk `.md` di akar diarahkan ke `NN/<sub>/` sesuai jenis (bacaan/praktikum/
> latihan), bukan di sebelah `.md`. Ini ditangani `build-dokumen.py` (`pdf_target()`).
> **Pengecualian:** `penugasan.md` PDF-nya tetap di akar folder `pXX-*/` karena
> penugasan memang harus dibagikan ke mahasiswa.
> - `penugasan.md` yang isinya **rubrik internal** (mis. showcase P16 yang
> berlabel RAHASIA DOSEN) **tidak boleh** di akar folder — pindahkan ke
> `pembahasan/pXX-*/kunci/`. Indeks glob `pembahasan/*/penugasan.pdf` hanya
> menyalin yang di akar, jadi rubrik otomatis tidak bocor ke `siap-bagikan/`.
> - Folder `siap-bagikan/` = **salinan** seluruh berkas mahasiswa, dikumpulkan dari
> semua `NN/`. Saat generation selalu cek kebocoran: tidak boleh ada `kunci`,
> `kisi-kisi`, `uts`, `uas`, rubrik, atau `.md`.

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
| Materi | `pembahasan/pXX-slug/materi.md` (akar) + `pXX-slug/NN/bacaan/materi.pdf` |
| **Lembar kerja praktikum** | `pembahasan/pXX-slug/lembar-kerja-praktikum.md` (akar) + `NN/praktikum/*.pdf` (16 buah, termasuk UTS & UAS) |
| Soal | `pembahasan/pXX-slug/soal.md` (akar) + `NN/latihan/soal.pdf` |
| Kunci jawaban | `pembahasan/pXX-slug/kunci/kunci-jawaban.md` + `.pdf` (INTERNAL) |
| Contoh kode | `pembahasan/pXX-slug/NN/contoh-kode/pXX-slug.php` |
| Diagram | `pembahasan/pXX-slug/NN/diagram/pXX-NN.png` + sumber `.mmd`/`.drawio` |
| Penugasan | `pembahasan/pXX-slug/penugasan.md` + `penugasan.pdf` (akar) + `panduan-pengumpulan.md` |
| Bank soal | `operasional/uts.md`, `operasional/uas.md`, `operasional/kisi-kisi-uts.md`, `operasional/kisi-kisi-uas.md` (+ `.pdf`) |
| Operasional | `operasional/kalender-semester.md`, `operasional/upload-checklist.md`, `operasional/moodle-bank-soal.xml`, `operasional/gradebook.xlsx` |
| kode | `pXX-slug.php` / `.html` / `.sql` |

> [!warning] Larangan nama
> **Jangan lagi memakai istilah "jobsheet"** — gunakan **lembar kerja praktikum**
> (singkat: LKP). Larangan juga: campuran casing (`P00_Pengantar_ `),
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
14. **Audit akhir jalan (exit 0)** — `python3 <mk-iticm>/audit-akhir.py <path-mk>`. Lihat "GATE Audit Akhir" di bawah. **Jangan tandai selesai sebelum exit 0.**

## GATE Audit Akhir (wajib, exit code)

> [!danger] Worksheet BELUM selesai sampai `audit-akhir.py` keluar **exit 0**
> Setiap artefak yang ada **tidak** berarti selesai. Yang menentukan selesai
> adalah satu perintah yang bisa dijalankan ulang kapan saja.

```bash
python3 ~/.agents/skills/mk-iticm/audit-akhir.py /path/ke/mk
```

| Exit | Arti | Tindakan |
|---|---|---|
| `0` | Semua cek hijau | Sah serah terima |
| `1` | Ada cek gagal | **Belum selesai.** Perbaiki temuan, jalankan ulang |

### 16 Cek yang Dijalankan

| # | Cek | Menangkap |
|---|---|---|
| 1 | File ber-underscore | `nama_file` melanggar kebab-lowercase |
| 2 | File sampah | `~$*.pptx` (lock Office), `.DS_Store` |
| 3 | Istilah lama `jobsheet` | Harus `lembar kerja praktikum` |
| 4 | Folder kosong | Sisa `rm -rf` atau folder `NN/` tanpa isi |
| 5 | `.md` di folder `NN/` | Sumber dosen bocor ke paket mahasiswa |
| 6 | Kebocoran `siap-bagikan/` | `kunci`, `kisi-kisi`, `.md` ikut tersalin |
| 7 | Subfolder tambahan | `siap-bagiankan/slide-deck/` — harus 1 folder/pertemuan |
| 8 | Folder tanpa deck pdf | Deck tidak ikut, mahasiswa tidak bisa belajar |
| 9 | Rubrik bocor di `penugasan.md` | `RAHASIA DOSEN` di file yang dibagikan |
| 10 | Karakter non-Latin di `.md` | Glitf CJK/Cyrillik dari generator |
| 11 | Parity deck | `pptx/*.pptx` != `pptx/pdf/*.pdf` |
| 12 | Pasangan diagram | `.mmd` tanpa `.png` (atau sebaliknya) |
| 13 | `php -l` semua kode | Contoh kode tidak jalan |
| 14 | Bobot gradebook | Komponen tidak jumlah 100% |
| 15 | XML Moodle parse | Bank soal rusak, tidak bisa import |
| 16 | Dokumen wajib | README, KNOWLEDGE, history, specs, RPS, draft hilang |

### Aturan Pakai

1. Jalankan **setiap selesai satu fase besar** (bukan cuma di akhir).
2. Kalau FAIL, **perbaiki yang disebut** — jangan disabling ceknya.
3. Kalau sebuah cek tidak relevan untuk MK tertentu (mis. tidak ada
 Moodle), **kebaikan dokumentasikan** di `history.md` kenapa dilewati.
 Jangan diam-diam menambahkannya ke daftar skip.
4. Sertakan output audit di `history.md` sebagai bukti serah terima.

## Audit Konsistensi (fase 5, wajib)

> Rincian manual tiap cek ada di bawah. **Yang mengikat adalah
> `audit-akhir.py` sudah automate semuanya** — pakai skrip, bukan
> manual, supaya tidak ada cek yang terlewat.

- **Jangan hapus folder/backup lama sebelum user konfirmasi.** Saat rebuild, backup
 (mis. `backup-v3/`) dihapus **hanya setelah** user menyatakan selesai. Rebuild =
 produksi dari draft; backup = jaring pengaman kalau ada yang tak sengaja terhapus.
- `find . -iname "*_*"` → gak ada file ber-underscore selain `.git`
- `find . -iname "~$*" -o -iname "*.DS_Store"` → kosong
- `find . -iname "*jobsheet*"` → **kosong** (istilah lama, ganti lembar-kerja-praktikum)
- `ls pptx/pdf` == `ls pptx/*.pptx` (count sama, nama konsisten)
- **Cermin:** untuk tiap PXX, isi deck PXX punya pasangan di `pembahasan/pXX-*/` (materi, soal, kunci, kode, LKP)
- **Pemisahan mahasiswa:** tiap `pembahasan/pXX-*/` punya folder bernomor `NN/` (isi mahasiswa) + `kunci/` (rahasia) + `.md` di akar (sumber dosen). Tidak boleh ada `.md` di dalam `NN/`.
- **Tidak ada folder kosong:** bila `pXX-NN/` tidak punya `bacaan`/`praktikum`/`latihan`/`contoh-kode`/`diagram`, hapus foldernya, jangan dibiarkan kosong.
- **Tidak ada folder kosong:** setelah `rm -rf` atau rebuild, pastikan tidak ada direktori kosong tertinggal (audit `find . -type d -empty`).
- **PDF:** tiap `.md` student-facing punya `.pdf` pasangannya
- `test -f penugasan/panduan-pengumpulan.md` dan `test -f pptx/p00-*.pptx` → exit 0
- **Satu folder per pertemuan:** `siap-bagiankan/` hanya berisi `pertemuan/pXX-*/`,
 **tanpa** `slide-deck/` atau subfolder tambahan lain. Tiap folder pertemuan
 harus punya deck PDF-nya sendiri (`pXX-slug.pdf`).
- **Rubrik tidak bocor:** `grep -rl "RAHASIA DOSEN" */penugasan.md` → kosong
 (rubrik internal harus di `kunci/`).
- **Tidak ada karakter non-Latin:** `grep -rlP '[\x{4e00}-\x{9fff}\x{3040}-\x{30ff}]' --include='*.md' .` → kosong.
 Ini wajib dicek setelah long generation run; glitf dari generator sering
 Sisipkan karakter CJK/Cyrillik yang lolos validator.
- Jika gagal: backfill dulu sebelum serah terima.

## Slide Rules (from real failures)
- **Reference first:** dissect a liked reference deck precisely (shape type, radius, fills, fonts, max cards/slide) BEFORE rebuilding. Never ship thin one-bullet decks.
- **Narasi = "cer mengalir, siap dibacakan"** (lihat `pptx-iticm/references/slide-rules.md` 7.9): 5–8 kalimat, pembuka konteks/analogi, isi, angka, penutup transisi. **Dilarang** meta-pembuka "Slide ini menjelaskan tentang ".
- **Tugas OBE 2 tipe:** Tipe A drill (every deck, ungraded) + Tipe B formal (milestone meetings only, full instructions + rubric ref). Exam decks (UTS/UAS) get NO new task slides.
- **Diagrams:** draw.io/mermaid sources + embedded PNGs; tool tutorials (install, setup, export) inside meetings that need them.
- **Logo/branding:** full brand on title + closing only; content slides keep footer label.

## Pelajaran Rebuild slow-logic (2026-09-27, IT104 — 17 deck / 423 slide)

Temuan dari rebuild penuh yang layak jadi aturan umum. Detail teknis ada di
`pptx-iticm/references/slide-rules.md` §14.

1. **Slow-logic untuk S1:** satu pertemuan satu konsep logika. Urut **analogi
 kehidupan sehari-hari → notasi (pseudocode/flowchart) → PHP kecil → trace
 kertas → latihan**. P01–P04 **0 baris PHP** (unplugged). Kode P05–P07
 maksimal 15 baris, naik bertahap. **Trace table kertas wajib sebelum slide
 kode** — mahasiswa harus bisa menghitungnya tanpa laptop.
2. **Mix prodi + role.** Satu MK dipakai beberapa prodi. Tiap deck rotasi
 contoh: Logistik (stok/ongkir), Bisnis Digital (diskon/keranjang),
 Informatika (nilai/login), dan role analis/marketing/dev/konsultan —
 selalu lewat analogi harian, jangan informatika-sentris terus.
3. **Mermaid heavy semua deck.** 2–5 diagram per deck, boleh 2–3 chart dalam
 1 slide. Source `pptx/diagram/pXX-NN.mmd`, PNG 1600px `mmdc -s 3 -b white`.
 Butuh `chrome-headless-shell` — install sekali:
 `npx puppeteer browsers install chrome-headless-shell@stable`.
4. **Format uang `Rp.` titik ribuan** (`Rp. 10.000`) di narasi, mermaid, tabel,
 dan `echo` (`number_format($n, 0, ',', '.')`). **Kecuali pseudocode** —
 di pseudocode angka tetap mentah (`120000`) karena menguji logika, bukan
 format tampilan. Validator kalimat harus mengabaikan titik setelah `Rp.`.
5. **Uji output kode, bukan cuma `php -l`.** Lint hanya cek sintaks. Jalankan
 tiap contoh kode dan **cocokkan output dengan trace yang tertulis di
 materi** — inilah pembuktian angka tidak dikarang.
6. **Divergensi dari RPS dicatat eksplisit** di `KNOWLEDGE.md`, bukan
 diam-diam diganti. Contoh IT104: RPS menyebut P16 UAS tulis 25%,
 implementasi jadi Showcase Proyek Akhir (demo, tanpa soal) 25% dengan
 rubrik sama. Bobot total tetap 100%, dan alasannya ditulis.
7. **Topik proyek dipilih lebih awal** (P09), lalu tiap deck berikutnya punya
 slide "Kaitkan ke Proyekmu" yang memetakan konsep ke fitur wajib proyek
 (tambah/tampil/cari/urut). Ini menyatukan pembelajaran dengan tugas akhir.
8. **Cek karakter non-Latin di EVERY artifact .md** sebelum surrender:
 `re.search(r'[\u4e00-\u9fff\u3040-\u30ff\u0400-\u04ff]', teks)`. Long
 generation run bisa Sisipkan glitf; add this to the final audit list.
9. **Stub script boleh menyalin nama, tapi jangan duplikasi tanpa alasan.**
 Kalau `deck_build.py` diduplikasi jadi `build-dek.py`, hapus yang lama dan
 import via `importlib.util.spec_from_file_location` (nama ber-dash tidak
 bisa di-`import` biasa). Dua file identik = sumber kebenaran ganda.
10. **`siap-bagikan/` = satu folder per pertemuan, tanpa subfolder tambahan.**
 Dosen ingin cukup share **satu folder per pertemuan**. Jadi PDF deck
 (`pptx/pdf/pXX-slug.pdf`) digabung ke `pertemuan/pXX-slug/pXX-slug.pdf`,
 bukan ke `slide-deck/` terpisah. Ide kuncinya: nama stem deck sudah identik
 dengan nama folder pertemuan, jadi cukup `os.path.splitext(base)[0]`.
 Kalau skrip punya rule yang menyalin pattern lebih dalam
 (`pembahasan/*/*/...`), bagian `parts[1]` adalah meeting — tapi untuk
 `pptx/pdf/*.pdf` `parts[1]` = `pdf`, bukan nama pertemuan, dan hasilnya
 `slide-deck/pdf/`. Karena itu tiap rule butuh mode eksplisit:
 `meeting` (ambil path ke-2) vs `bydeck` (ambil stem nama berkas).
 **Semua** rule harus menunjuk ke `DEST/pertemuan/`. Tambahkan
 `slide-deck` ke daftar forbidden saat generate.
11. **Rubrik tidak boleh bocor lewat `penugasan.md`.** Kalau `penugasan.md`
 berisi rubrik berlabel RAHASIA DOSEN (mis. showcase), jangan taruh di akar
 `pembahasan/pXX-*/` karena akan ikut ter-copy ke `siap-bagiankan/`.
 Pindahkan ke `kunci/penugasan-<nama>.md`. Aturan ini menambah satu
 pen ke audit: `grep -ri "RAHASIA" */penugasan.md` → harus kosong.

## Anti-Fabrication (baseline agents invent these)
| Excuse | Reality |
|---|---|
| "Weights % look professional" | NEVER invent grade weights/dates — relative deadlines + configurable weight rows only |
| "One generic deck is fine" | Each deck's content must match its meeting title; audit titles per slide |
| "Tool X is equivalent" | One sanctioned toolchain per worksheet (e.g. Laragon, never mixed with XAMPP) — grep-enforce |
| "Kisi-kisi with student files is fine" | Kisi-kisi + keys stay internal until the exam week |
| "Makin detail angkanya, makin bagus slide-nya" | Nomor di slide harus berasal dari sumber terverifikasi (literatur/dataset) dan dicek ulang dengan kode saat build — bukan dikarang agar terlihat ramai |
| "Output PHP sudah pasti benar karena php -l OK" | Lint hanya sintaks. Jalankan program, cocokkan output dengan trace di materi |
| "Rubrik bisa dihitung ulang sendiri" | Poin bank soal harus **sum** dengan poin di kisi-kisi. Cek aritmetikanya, jangan biarkan jumlah tidak cocok antara naskah, kunci, dan kisi |
| "Placeholder regex selalu benar" | Regex `label\s*\d` menandai frasa sah seperti "label sembilan huruf". Uji regex terhadap vocabulary MK sebelum dipakai |

## Quick Reference
- Proof commands: slide-title dump per deck, `php -l` + run with expected outputs, XML parse + count, PDF pages = slides
- Dokumen: `knowledge/scripts/build-dokumen.py` (md → docx → pdf) untuk semua artefak student-facing
- 4-way parallel split: lembar-kerja-praktikum / bank-soal+blueprints / penugasan+rubrics / studi-kasus — then self-verify counts and spot-check formats
- **Poin bank soal harus jumlah sama dengan kisi-kisi** (IT104: 20 PG × 1 + 5 kasus × 16 = 100)
- **Cek non-Latin di semua .md** setelah long generation run
- Record everything: Todo Aktif in KNOWLEDGE.md, timestamped history entries, root README counts
