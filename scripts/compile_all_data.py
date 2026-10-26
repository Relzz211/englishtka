#!/usr/bin/env python3
"""
Master compiler script that stitches together all 18 modules, builds the master vocabulary dictionary,
generates the TKA English Reading Strategy Guide, and produces statistical summaries.
"""

import json
import os
import re
import sys

# Ensure current script directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.abspath('.'))

import importlib.util

spec1 = importlib.util.spec_from_file_location("build_full_dataset", "scripts/build_full_dataset.py")
mod1_pkg = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(mod1_pkg)
modules_p1 = mod1_pkg.modules

from modules_p2 import modules_p2
from modules_p3 import modules_p3

all_modules = modules_p1 + modules_p2 + modules_p3
print(f"Total compiled modules: {len(all_modules)}")

# Ensure word count and reading time are accurately formatted
def word_count(text):
    return len(re.findall(r'\b\w+\b', text))

def est_reading_time(words):
    mins = max(1, round(words / 130))
    return f"{mins} min read"

for m in all_modules:
    # Combine all paragraph English text
    full_en = " ".join([p.get('en', '') for p in m.get('paragraphs', [])])
    wc = word_count(full_en)
    m['wordCount'] = wc
    m['estimatedReadTime'] = est_reading_time(wc)

# 1. Save server/data/modules.json
with open('server/data/modules.json', 'w', encoding='utf-8') as f:
    json.dump(all_modules, f, ensure_ascii=False, indent=2)
print("Saved server/data/modules.json")

# 2. Compile Master Vocabulary List
master_vocab = []
seen_words = set()

for m in all_modules:
    for v in m.get('vocabulary', []):
        w_lower = v['word'].lower()
        if w_lower not in seen_words:
            seen_words.add(w_lower)
            master_vocab.append({
                "word": v['word'],
                "phonetic": v.get('phonetic', ''),
                "pos": v.get('pos', ''),
                "defEn": v.get('defEn', ''),
                "defId": v.get('defId', ''),
                "example": v.get('example', ''),
                "moduleId": m['id'],
                "moduleTitle": m['titleEn'],
                "package": m['package']
            })

# Sort alphabetically
master_vocab.sort(key=lambda x: x['word'].lower())

with open('server/data/vocabulary.json', 'w', encoding='utf-8') as f:
    json.dump(master_vocab, f, ensure_ascii=False, indent=2)
print(f"Saved server/data/vocabulary.json ({len(master_vocab)} vocabulary entries)")

# 3. Create Comprehensive TKA English Reading Strategy Guide
reading_guide = {
    "title": "Panduan Komprehensif Menguasai Soal Bacaan TKA Bahasa Inggris",
    "subtitle": "Strategi Jitu, Bedah Pola Soal, dan Trik Pemahaman Bacaan Akademik Tanpa Terjebak",
    "chapters": [
        {
            "id": "ch-1",
            "number": 1,
            "titleEn": "Skimming & Scanning Mastery for TKA Passages",
            "titleId": "Keahlian Skimming & Scanning untuk Membaca Cepat Teks TKA",
            "icon": "⚡",
            "summary": "Teknik membaca cepat untuk menemukan ide pokok dalam 30 detik (Skimming) dan melacak data spesifik seperti angka, tahun, atau nama orang (Scanning) tanpa harus membaca kata per kata.",
            "content": """
### 1. Apa Perbedaan Skimming dan Scanning?
* **Skimming (Membaca Cepat untuk Ide Utama):**
  Tujuan skimming adalah mendapatkan *gambaran umum* (gist) dari teks dalam waktu singkat.
  - Baca judul dan subjudul teks.
  - Baca kalimat pertama dan kalimat terakhir pada setiap paragraf (karena 80% ide pokok berada di sana).
  - Abaikan detail kecil, contoh, atau angka saat skimming pertama.
  - Waktu ideal: 30–45 detik per teks.

* **Scanning (Melacak Informasi Spesifik):**
  Tujuan scanning adalah menemukan *jawaban atas pertanyaan spesifik*, seperti angka tahun, nama lembaga, persentase, atau kata kunci tertentu.
  - Tandai kata kunci pada soal (misalnya: *30 grams*, *PISA 2022*, *Bandung Techno Park*).
  - Gerakkan pandangan mata secara vertikal/zig-zag melintasi teks untuk menemukan kata kunci tersebut.
  - Ketika kata kunci ditemukan, baca 1 kalimat sebelum dan 1 kalimat sesudahnya secara cermat.

> [!TIP]
> **Trik TKA:** Jangan pernah membaca teks secara lambat dari awal sampai akhir sebelum membaca pertanyaan! Baca soal terlebih dahulu untuk menentukan apakah butuh skimming atau scanning.
            """
        },
        {
            "id": "ch-2",
            "number": 2,
            "titleEn": "Identifying Main Ideas & Topic Sentences",
            "titleId": "Menemukan Ide Pokok & Kalimat Topik Setiap Paragraf",
            "icon": "🎯",
            "summary": "Cara jitu mengidentifikasi gagasan utama teks, membedakan topik dengan ide penjelas, serta mengenali letak topic sentence (deduktif di awal vs induktif di akhir).",
            "content": """
### 1. Letak Topic Sentence dalam Teks TKA
Sebagian besar teks ujian TKA (akademik/ilmiah) mengikuti struktur deduktif:
* **Paragraf Pembuka (Deduktif):** Ide utama terletak di kalimat ke-1 atau ke-2.
  *Contoh pada Modul 3:* *"Your diet must contain some fat, but you must be careful about the kind and quantity of fat you consume."* -> Kalimat ini adalah ide pokok paragraf.
* **Paragraf Penutup (Induktif/Kesimpulan):** Ide utama berada di akhir paragraf yang diawali kata transisi seperti *Therefore, Thus, In conclusion, As a result*.

### 2. Jebakan Pilihan Jawaban pada Soal 'Main Idea':
1. **Terlalu Sempit (Too Specific):** Hanya memuat detail kecil dari satu kalimat, bukan keseluruhan teks.
2. **Terlalu Luas (Too General):** Terlalu abstrak dan melampaui cakupan teks yang diberikan.
3. **Salah Informasi (Inaccurate/Contradictory):** Memutarbalikkan fakta teks.
4. **Ide Pokok Sejati (Correct Main Idea):** Memayungi seluruh paragraf dan relevan dengan tujuan penulisan teks.
            """
        },
        {
            "id": "ch-3",
            "number": 3,
            "titleEn": "Decoding Unknown Words using Context Clues",
            "titleId": "Menafsirkan Arti Kata Asing Menggunakan Petunjuk Konteks (Context Clues)",
            "icon": "🔍",
            "summary": "Strategi memecahkan arti kosakata sulit dalam teks bahasa Inggris tanpa kamus dengan menganalisis definisi langsung, sinonim, antonim, dan contoh di sekitarnya.",
            "content": """
### 4 Jenis Petunjuk Konteks (Context Clues) di TKA:
1. **Definisi atau Penjelasan Langsung (Definition / Restatement Clue):**
   Penulis langsung mendefinisikan istilah tersebut menggunakan tanda koma, tanda pisah (—), atau kata *which means*.
   *Contoh:* *"Free-range chicken—which is required in the recipe—is chicken allowed to roam freely..."*
2. **Petunjuk Sinonim (Synonym / Comparison Clue):**
   Kata sulit dipasangkan dengan kata yang lebih umum menggunakan kata hubung *and, or, also called*.
   *Contoh pada Modul 5:* *"This plant is also called Paper Flower because its flowers are as smooth and thin as paper."*
3. **Petunjuk Lawan Kata / Kontras (Antonym / Contrast Clue):**
   Arti kata dapat ditebak melalui kebalikan maknanya dengan kata sinyal: *however, although, whereas, unlike, but*.
   *Contoh pada Modul 7:* *"The tranquil seashore... unlike rowdy and noisy tourist spots."* -> *Tranquil* berarti tenang/damai.
4. **Petunjuk Contoh (Example Clue):**
   Penulis memberikan contoh konkret melalui kata *such as, for example, including*.
   *Contoh pada Modul 3:* *"...unsaturated fat, such as oily fish, avocados, and olive oil."*
            """
        },
        {
            "id": "ch-4",
            "number": 4,
            "titleEn": "Distinguishing Fact vs. Opinion in TKA Questions",
            "titleId": "Membedakan Pernyataan Fakta dan Opini dalam Soal TKA",
            "icon": "⚖️",
            "summary": "Panduan menjawab soal tipe kategorisasi (Categorization Questions) yang menguji kemampuan siswa membedakan fakta objektif terbukti dengan opini subjektif.",
            "content": """
### Ciri Khas Fakta (Fact) vs Opini (Opinion):
* **Fakta (Fact):**
  - Dapat dibuktikan kebenarannya secara objektif melalui data riil, dokumen, atau peristiwa sejarah.
  - Memuat tanggal, angka terukur, nama tempat, nomor surat dinas, hasil riset, atau observasi konkret.
  - Menggunakan kata kerja netral: *occurred, established, delivered (PO-2025-1189), measured, contains 50 hectares*.
  *Contoh TKA:* *"Bandung Techno Park occupies about 50 hectares of land."* (Fakta terverifikasi).

* **Opini (Opinion):**
  - Mengungkapkan perasaan, keyakinan moral, prediksi masa depan, atau penilaian subjektif seseorang/manajemen.
  - Memuat kata sinyal opini: *I think, we believe, it seems, should, might, arguably, best, essential*.
  *Contoh TKA:* *"We believe that small, conscious actions create a substantial collective impact."* (Opini karena diawali 'We believe').
            """
        },
        {
            "id": "ch-5",
            "number": 5,
            "titleEn": "Interpreting Tables, Charts & Visual Data",
            "titleId": "Membaca dan Menginterpretasikan Tabel & Diagram dalam Soal TKA",
            "icon": "📊",
            "summary": "Metode praktis membaca soal gabungan teks + infografis: menganalisis judul tabel/grafik, sumbu X dan Y, persentase dominan, serta korelasi data visual dengan isi paragraf.",
            "content": """
### Langkah Sistematis Membaca Infografis & Tabel:
1. **Baca Judul dan Satuan Data Terlebih Dahulu:**
   Pastikan memahami apakah angka berupa gram (Modul 3), persentase (%) (Modul 16), atau jumlah orang.
2. **Cari Angka Tertinggi (Peak) dan Terendah (Lowest):**
   Soal TKA hampir selalu menanyakan proporsi terbesar (*the largest proportion*) atau nilai batas aman maksimal (*maximum limit*).
3. **Perhatikan Perbandingan Antarkelompok (Demographic Comparison):**
   Contoh: Bandingkan batasan lemak pria dewasa (30g) vs wanita dewasa (20g) vs anak di bawah 5 tahun (tidak boleh diet rendah lemak).
4. **Cocokkan Bukti Visual dengan Opsi Pilihan:**
   Jangan berasumsi tanpa mencocokkan garis batang atau baris tabel secara teliti.
            """
        },
        {
            "id": "ch-6",
            "number": 6,
            "titleEn": "Analyzing Tone, Attitude & Author's Purpose",
            "titleId": "Menganalisis Nada Teks (Tone), Sikap (Attitude), dan Tujuan Penulis",
            "icon": "🧠",
            "summary": "Teknik menentukan maksud komunikatif teks (to inform, to persuade, to instruct, to recount) dan mengidentifikasi nada emosional penulis (objective, encouraging, critical, appreciative).",
            "content": """
### Kata Kunci Menentukan 'Author's Purpose':
* **To Inform / To Describe:** Menjelaskan fenomena ilmiah atau tempat wisata secara objektif (Contoh: *Bougainvillea report, Sanur Beach*).
* **To Persuade / To Convince:** Mengajak pembaca bertindak atau meyakinkan perekrut (Contoh: *Surat Lamaran Kerja, Memo Hemat Kertas*).
* **To Instruct / To Guide:** Memberikan petunjuk bertahap (Contoh: *Resep Orak-Arik Telur, Panduan Menanam Kacang Hijau*).
* **To Entertain / To Impart Moral Values:** Menghibur dan menyampaikan pesan moral (Contoh: *Legenda Cenderawasih, Kisah Amat Mude*).
* **To Share Personal Reflection:** Menceritakan pengalaman masa lalu dan dampaknya pada diri penulis (Contoh: *Magang Rumah Sakit, Liburan Gunung Bromo*).
            """
        }
    ]
}

with open('server/data/reading_guide.json', 'w', encoding='utf-8') as f:
    json.dump(reading_guide, f, ensure_ascii=False, indent=2)
print("Saved server/data/reading_guide.json")

# 4. Save Overall Statistics
total_words = sum([m['wordCount'] for m in all_modules])
stats = {
    "totalModules": len(all_modules),
    "totalPackages": 3,
    "totalWords": total_words,
    "totalVocabulary": len(master_vocab),
    "genresCount": len(set([m['genre'] for m in all_modules])),
    "packages": [
        {"package": "Paket 1", "moduleCount": len(modules_p1), "qRange": "Soal 1 - 30"},
        {"package": "Paket 2", "moduleCount": len(modules_p2), "qRange": "Soal 1 - 30"},
        {"package": "Paket 3", "moduleCount": len(modules_p3), "qRange": "Soal 1 - 30"}
    ]
}

with open('server/data/stats.json', 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)
print("Saved server/data/stats.json")
print("ALL DATASETS COMPILED SUCCESSFULLY!")
