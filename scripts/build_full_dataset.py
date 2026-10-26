#!/usr/bin/env python3
"""
Generator script to compile all 18 TKA English Reading Modules from CBT Erlangga into server/data/modules.json,
server/data/vocabulary.json, server/data/reading_guide.json, and server/data/stats.json.
"""

import json
import os
import re

os.makedirs('server/data', exist_ok=True)

def word_count(text):
    return len(re.findall(r'\b\w+\b', text))

def est_reading_time(words):
    mins = max(1, round(words / 130))
    return f"{mins} min read"

# Load raw passages
with open('raw_passages.json', 'r', encoding='utf-8') as f:
    raw_passages = json.load(f)

modules = []

# =========================================================================
# 1. Job Application Letter
# =========================================================================
mod_1 = {
    "id": "module-1",
    "package": "Paket 1",
    "packageNum": 1,
    "qRange": "Soal 1 - 5",
    "titleEn": "Job Application Letter: Social Media Officer",
    "titleId": "Surat Lamaran Kerja: Social Media Officer",
    "genre": "Business Correspondence",
    "genreBadge": "Formal Letter",
    "level": "B1 - Intermediate",
    "summaryEn": "A formal job application letter by Putra Ramshiditya applying for the position of Social Media Officer at PT Citra Diraja, showcasing his experience boosting engagement by 35% and his creative portfolio.",
    "summaryId": "Surat lamaran kerja resmi oleh Putra Ramshiditya yang melamar posisi Social Media Officer di PT Citra Diraja, memaparkan pengalamannya meningkatkan engagement sebesar 35% dan portofolio kreatifnya.",
    "hasImage": False,
    "image": None,
    "imageCaptionEn": "",
    "imageCaptionId": "",
    "paragraphs": [
        {
            "id": 1,
            "type": "meta",
            "en": "Putra Ramshiditya\nJl. Ontoseno No. 17\nBantul, Yogyakarta 55711\n+62 817342 | ramshi.putra17@mail.com\n\nJuly 1",
            "idTranslation": "Putra Ramshiditya\nJl. Ontoseno No. 17\nBantul, Yogyakarta 55711\n+62 817342 | ramshi.putra17@mail.com\n\n1 Juli",
            "keyWords": ["Applicant", "Contact Information", "Date"]
        },
        {
            "id": 2,
            "type": "meta",
            "en": "Hiring Manager\nPT Citra Diraja\nJl. Pangeran Antasari No. 45\nJakarta Selatan 12410\n\nDear Hiring Manager,",
            "idTranslation": "Manajer Perekrutan\nPT Citra Diraja\nJl. Pangeran Antasari No. 45\nJakarta Selatan 12410\n\nKepada Manajer Perekrutan yang terhormat,",
            "keyWords": ["Hiring Manager", "Salutation"]
        },
        {
            "id": 3,
            "type": "paragraph",
            "en": "I am writing to express my interest in the Social Media Officer position at PT Citra Diraja, as advertised on your official careers page. With a strong background in digital content creation, audience engagement strategies, and a proven passion for storytelling, I am eager to contribute to your company's growing digital footprint.",
            "idTranslation": "Saya menulis surat ini untuk menyatakan ketertarikan saya terhadap posisi Social Media Officer di PT Citra Diraja, sebagaimana diiklankan pada laman karier resmi perusahaan Anda. Berbekal latar belakang yang solid dalam pembuatan konten digital, strategi interaksi audiens, serta antusiasme yang terbukti dalam storytelling (penceritaan), saya bersemangat untuk berkontribusi pada jejak digital perusahaan Anda yang kian berkembang.",
            "keyWords": ["express my interest", "Social Media Officer", "audience engagement", "digital footprint"]
        },
        {
            "id": 4,
            "type": "paragraph",
            "en": "I gained valuable experience managing social media campaigns during my university years and my previous internship. I spearheaded creative content on Instagram and TikTok, which boosted follower engagement by 35% over a six-month period. I am proficient in utilizing analytic tools, designing eye-catching graphics, and crafting compelling copy tailored to diverse demographics.",
            "idTranslation": "Saya memperoleh pengalaman berharga dalam mengelola kampanye media sosial selama masa perkuliahan dan magang terdahulu. Saya memimpin pembuatan konten kreatif di Instagram dan TikTok, yang berhasil mendongkrak keterlibatan pengikut (engagement) sebesar 35% selama rentang enam bulan. Saya mahir mengoperasikan perangkat analitik, merancang grafis yang memikat, dan menyusun teks copywriting persuasif yang disesuaikan dengan berbagai target demografi.",
            "keyWords": ["valuable experience", "spearheaded", "boosted", "proficient", "compelling copy"]
        },
        {
            "id": 5,
            "type": "paragraph",
            "en": "PT Citra Diraja's innovative campaigns have consistently impressed me, and I would be thrilled to bring my creative energy, adaptability, and deep understanding of digital pop culture to your talented marketing team.",
            "idTranslation": "Kampanye-kampanye inovatif PT Citra Diraja senantiasa memukau saya, dan saya akan sangat bangga dapat menyumbangkan energi kreatif, kemampuan beradaptasi, serta pemahaman mendalam tentang tren budaya pop digital ke dalam tim pemasaran Anda yang berbakat.",
            "keyWords": ["innovative", "consistently", "thrilled", "adaptability", "pop culture"]
        },
        {
            "id": 6,
            "type": "paragraph",
            "en": "I have attached my CV and samples of my social media content for your review. Thank you for your time and consideration. I look forward to the possibility of discussing how my skills and experience align with your company's vision.\n\nSincerely,\nPutra Ramshiditya",
            "idTranslation": "Bersama ini saya lampirkan daftar riwayat hidup (CV) dan contoh karya konten media sosial saya untuk bahan pertimbangan Anda. Terima kasih atas waktu dan perhatian yang Anda luangkan. Saya sangat menantikan kesempatan untuk mendiskusikan bagaimana keahlian dan pengalaman saya selaras dengan visi perusahaan Anda.\n\nHormat saya,\nPutra Ramshiditya",
            "keyWords": ["attached", "consideration", "look forward to", "align with"]
        }
    ],
    "vocabulary": [
        {"word": "express my interest", "phonetic": "/ɪkˈspres maɪ ˈɪntrəst/", "pos": "phrase", "defEn": "To formally state one's desire or intention to apply for a role.", "defId": "Menyatakan minat/ketertarikan secara resmi pada suatu lowongan kerja.", "example": "I am writing to express my interest in the content strategist position."},
        {"word": "spearheaded", "phonetic": "/ˈspɪəhedɪd/", "pos": "verb", "defEn": "To lead an organized activity, project, or movement.", "defId": "Memelopori atau memimpin jalannya suatu proyek atau kampanye.", "example": "He spearheaded the company's transition to paperless workflow."},
        {"word": "engagement", "phonetic": "/ɪnˈɡeɪdʒmənt/", "pos": "noun", "defEn": "The degree of attention, curiosity, or active participation from followers.", "defId": "Keterlibatan atau tingkat interaksi (likes, comments, shares) audiens media sosial.", "example": "Interactive polls significantly improved overall user engagement."},
        {"word": "proficient", "phonetic": "/prəˈfɪʃnt/", "pos": "adjective", "defEn": "Competent or skilled in doing or using something.", "defId": "Mahir, cakap, atau menguasai suatu bidang atau keahlian.", "example": "She is proficient in Adobe Photoshop and video editing tools."},
        {"word": "compelling", "phonetic": "/kəmˈpelɪŋ/", "pos": "adjective", "defEn": "Evoking interest, attention, or conviction powerfully.", "defId": "Memikat, menarik perhatian, atau sangat meyakinkan.", "example": "A compelling headline convinces readers to continue exploring the article."},
        {"word": "attached", "phonetic": "/əˈtætʃt/", "pos": "verb / adjective", "defEn": "Joined, enclosed, or sent together with a document.", "defId": "Dilampirkan bersama surat atau pesan elektronik.", "example": "I have attached the signed agreement for your records."}
    ],
    "grammarPoints": [
        {
            "topic": "Present Continuous for Letter Stance",
            "formula": "Subject (I) + am writing + to-infinitive",
            "explanationEn": "A standard opening formula in formal correspondence to declare the communicative intent right from the first sentence.",
            "explanationId": "Pola baku pembuka surat resmi untuk mengutarakan maksud komunikasi secara santun dan jelas sejak kalimat pertama.",
            "examples": ["I am writing to express my interest in the position...", "I am writing to inquire about the scholarship requirements..."]
        },
        {
            "topic": "Present Perfect for Recent Achievements & Enclosures",
            "formula": "Subject + have/has + Past Participle (V3)",
            "explanationEn": "Used to describe completed actions that directly impact the current interaction, such as enclosing documents or noting brand impressions.",
            "explanationId": "Digunakan untuk menyatakan tindakan tuntas yang berkaitan langsung dengan kondisi saat ini, misalnya melampirkan berkas.",
            "examples": ["I have attached my CV and samples of my work.", "Your campaigns have consistently impressed me."]
        }
    ],
    "genericStructure": [
        {"part": "Sender & Date", "partId": "Identitas Pengirim & Tanggal", "descriptionEn": "Applicant's contact details and dispatch date.", "descriptionId": "Data kontak pelamar dan tanggal surat dikirim.", "excerpt": "Putra Ramshiditya... July 1"},
        {"part": "Salutation & Recipient", "partId": "Salam Pembuka & Penerima", "descriptionEn": "Formal greeting directed to the hiring authority.", "descriptionId": "Salam resmi kepada pihak HR / perekrut.", "excerpt": "Hiring Manager... Dear Hiring Manager,"},
        {"part": "Statement of Purpose", "partId": "Tujuan Penulisan Surat", "descriptionEn": "Explicit mention of the target position and source of information.", "descriptionId": "Penyebutan posisi yang diincar dan media lowongan.", "excerpt": "I am writing to express my interest in the Social Media Officer position..."},
        {"part": "Evidence & Qualifications", "partId": "Kualifikasi & Bukti Prestasi", "descriptionEn": "Measurable track record, past roles, and practical software competence.", "descriptionId": "Bukti terukur (angka 35%), pengalaman magang, dan penguasaan alat kerja.", "excerpt": "I spearheaded creative content... boosted follower engagement by 35%..."},
        {"part": "Enclosures & Sign-off", "partId": "Lampiran & Salam Penutup", "descriptionEn": "Mention of CV attachments and professional sign-off.", "descriptionId": "Keterangan lampiran berkas dan penutup formal.", "excerpt": "I have attached my CV... Sincerely, Putra Ramshiditya"}
    ],
    "tkaStrategies": [
        {
            "topic": "Menemukan Posisi yang Dilamar (Identifying Job Role)",
            "strategyEn": "Quickly scan the opening sentence right after 'express my interest in...'. In CBT questions, distractors often include unrelated departments or applicant's previous roles.",
            "strategyId": "Cermati kalimat pertama setelah frasa 'express my interest in...'. Pada CBT, pengecoh sering menyertakan nama divisi perusahaan atau pekerjaan magang lama pelamar.",
            "cbtKeyInsight": "Soal CBT No. 1 menanyakan posisi yang dilamar. Kunci jawaban D (Social Media Officer) dapat langsung ditemukan di kalimat pembuka tanpa perlu membaca seluruh surat."
        },
        {
            "topic": "Menganalisis Dokumen Lampiran (Enclosures Analysis)",
            "strategyEn": "Check the closing paragraph for verbs like 'attached', 'enclosed', or 'included'. Note exactly which documents are mentioned.",
            "strategyId": "Periksa paragraf terakhir untuk menemukan kata kunci 'attached' atau 'enclosed'. Perhatikan secara cermat jenis dokumen yang dilampirkan.",
            "cbtKeyInsight": "Pada Soal CBT No. 3 (Multiple answers), Putra melampirkan Curriculum Vitae (CV) dan 'samples of my social media content' (portofolio konten)."
        }
    ]
}

# =========================================================================
# 2. Office Memorandum
# =========================================================================
mod_2 = {
    "id": "module-2",
    "package": "Paket 1",
    "packageNum": 1,
    "qRange": "Soal 6 - 10",
    "titleEn": "Office Memorandum: Responsible Supply Consumption",
    "titleId": "Memorandum Kantor: Penggunaan Perlengkapan Kantor Secara Bijak",
    "genre": "Administrative Memorandum",
    "genreBadge": "Office Memo",
    "level": "B1 - Intermediate",
    "summaryEn": "An internal workplace memo issued by the Office Management Division urging staff to consume stationery and printing supplies conscientiously to reduce company waste and support green sustainability.",
    "summaryId": "Memo internal kantor dari Divisi Manajemen Kantor yang menginstruksikan seluruh staf agar menghemat kertas dan perlengkapan cetak demi mengurangi limbah operasional dan mendukung keberlanjutan ramah lingkungan.",
    "hasImage": False,
    "image": None,
    "imageCaptionEn": "",
    "imageCaptionId": "",
    "paragraphs": [
        {
            "id": 1,
            "type": "meta",
            "en": "Memorandum\n\nTo : All Employees\nFrom : Office Management Division\nDate : July 2\nSubject : Let's Use Our Office Supplies Wisely",
            "idTranslation": "Memorandum (Memo Kantor)\n\nKepada : Seluruh Karyawan\nDari : Divisi Manajemen Kantor\nTanggal : 2 Juli\nPerihal : Mari Gunakan Perlengkapan Kantor Kita Secara Bijak",
            "keyWords": ["Memorandum", "Subject", "Office Supplies"]
        },
        {
            "id": 2,
            "type": "paragraph",
            "en": "Hi everyone, just a quick note following the recent supply delivery (PO-2025-1189). We would like to gently remind everyone to be mindful when using office supplies.",
            "idTranslation": "Halo rekan-rekan, ini catatan singkat menindaklanjuti pengiriman perlengkapan kantor baru-baru ini (PO-2025-1189). Kami ingin dengan ramah mengingatkan semua orang agar lebih cermat dan hemat saat menggunakan perlengkapan kantor.",
            "keyWords": ["supply delivery", "gently remind", "mindful"]
        },
        {
            "id": 3,
            "type": "paragraph",
            "en": "Over the past month, we have observed a significant increase in the consumption of printing paper, ink cartridges, and sticky notes. In several instances, full reams of paper were opened and left unused near printers, and colored printing was utilized for non-essential internal draft documents.",
            "idTranslation": "Selama bulan lalu, kami mencatat peningkatan signifikan dalam konsumsi kertas cetak, kartrid tinta, dan kertas memo tempel (sticky notes). Dalam beberapa kesempatan, satu rim kertas utuh dibuka dan ditinggalkan berserakan di samping mesin cetak, serta pencetakan berwarna digunakan untuk draf dokumen internal yang bersifat tidak mendesak.",
            "keyWords": ["significant increase", "consumption", "reams of paper", "non-essential"]
        },
        {
            "id": 4,
            "type": "paragraph",
            "en": "To ensure resources remain available for all teams and to support our company's green sustainability initiative, please observe the following guidelines:\n1. Preview all documents digitally before printing to avoid misprints.\n2. Utilize black-and-white double-sided printing for internal notes and drafts.\n3. Reserve color printing exclusively for client presentations and formal external reports.\n4. Return unused pens, notebooks, and folders to the central supply cabinet in Room 204 so colleagues may access them.",
            "idTranslation": "Untuk menjamin pasokan tetap tersedia bagi seluruh tim dan mendukung inisiatif kelestarian hijau perusahaan kita, mohon patuhi pedoman berikut:\n1. Tinjau semua dokumen di layar komputer sebelum mencetak guna menghindari salah cetak.\n2. Terapkan cetak hitam-putih bolak-balik untuk draf dan catatan internal.\n3. Khususkan cetak berwarna hanya untuk materi presentasi klien dan laporan resmi eksternal.\n4. Kembalikan pulpen, buku catatan, dan map yang berlebih ke lemari pasokan pusat di Ruang 204 agar dapat dimanfaatkan oleh rekan lain.",
            "keyWords": ["sustainability initiative", "guidelines", "double-sided", "exclusively"]
        },
        {
            "id": 5,
            "type": "paragraph",
            "en": "We believe that small, conscious actions create a substantial collective impact. Your cooperation in minimizing office waste is greatly appreciated.\n\nBest regards,\nOffice Management Division",
            "idTranslation": "Kami meyakini bahwa tindakan kecil yang dilakukan secara sadar akan membawa pengaruh kolektif yang luar biasa. Kerja sama Anda dalam meminimalkan pemborosan kantor sangat dihargai.\n\nSalam hangat,\nDivisi Manajemen Kantor",
            "keyWords": ["conscious actions", "substantial", "collective impact", "minimizing waste"]
        }
    ],
    "vocabulary": [
        {"word": "mindful", "phonetic": "/ˈmaɪndfl/", "pos": "adjective", "defEn": "Conscious or aware of something; attentive to avoid waste.", "defId": "Cermat, penuh perhatian, dan tidak ceroboh.", "example": "Be mindful of power consumption when leaving the office."},
        {"word": "consumption", "phonetic": "/kənˈsʌmpʃn/", "pos": "noun", "defEn": "The using up of a resource, good, or service.", "defId": "Konsumsi atau volume pemakaian suatu barang.", "example": "Fuel consumption decreased after adopting hybrid vehicles."},
        {"word": "reams", "phonetic": "/riːmz/", "pos": "noun (plural)", "defEn": "Standard bundles of paper, typically 500 sheets each.", "defId": "Rim kertas (paket berisi 500 lembar).", "example": "He unpacked three reams of paper into the photocopier tray."},
        {"word": "exclusively", "phonetic": "/ɪkˈskluːsɪvli/", "pos": "adverb", "defEn": "Solely; not admitting of something else.", "defId": "Secara khusus atau semata-mata hanya untuk tujuan tertentu.", "example": "This entrance is used exclusively by authorized personnel."},
        {"word": "substantial", "phonetic": "/səbˈstænʃl/", "pos": "adjective", "defEn": "Of considerable importance, value, or size.", "defId": "Besar, substansial, atau berdampak nyata.", "example": "The company reported a substantial increase in quarterly productivity."}
    ],
    "grammarPoints": [
        {
            "topic": "Imperative Verbs in Procedural Guidelines",
            "formula": "Base Verb + Object / Prepositional Phrase",
            "explanationEn": "Used in official workplace directives to provide direct and actionable instructions without sounding aggressive.",
            "explanationId": "Kalimat perintah santun dengan kata kerja dasar di awal kalimat untuk memberikan instruksi operasional yang tegas.",
            "examples": ["Preview all documents digitally before printing.", "Utilize black-and-white printing.", "Return unused pens..."]
        },
        {
            "topic": "Fact vs Opinion Distinction in Reading",
            "formula": "Facts = Verifiable data, records; Opinions = Subjective beliefs ('we believe...')",
            "explanationEn": "TKA questions evaluate whether students can differentiate between observable facts and managerial philosophies.",
            "explanationId": "Soal TKA menguji ketelitian siswa dalam membedakan data faktual terverifikasi dengan pandangan/opini subjektif.",
            "examples": ["Fact: Full reams of paper were left near printers.", "Opinion: We believe that small actions create a substantial collective impact."]
        }
    ],
    "genericStructure": [
        {"part": "Memo Heading", "partId": "Kepala Memo", "descriptionEn": "Contains To, From, Date, and Subject lines.", "descriptionId": "Memuat Kepada, Dari, Tanggal, dan Perihal memo.", "excerpt": "Memorandum... To: All Employees..."},
        {"part": "Problem & Observations", "partId": "Latar Masalah & Pengamatan", "descriptionEn": "Details recent observations of wasteful practices.", "descriptionId": "Penjabaran pemborosan kertas dan tinta di kantor.", "excerpt": "We have observed a significant increase in the consumption..."},
        {"part": "Directive Policies", "partId": "Instruksi Kebijakan", "descriptionEn": "Four clear, numbered guidelines for eco-friendly printing.", "descriptionId": "Empat butir panduan mencetak hemat dan berbagi fasilitas.", "excerpt": "1. Preview... 2. Utilize black-and-white... 3. Reserve color..."},
        {"part": "Closing Call to Cooperation", "partId": "Harapan Kerja Sama", "descriptionEn": "Appreciative remark reinforcing mutual responsibility.", "descriptionId": "Apresiasi manajemen dan dorongan tanggung jawab bersama.", "excerpt": "Your cooperation in minimizing office waste is greatly appreciated."}
    ],
    "tkaStrategies": [
        {
            "topic": "Menganalisis Perilaku yang Tidak Sesuai (Non-aligned Behaviors)",
            "strategyEn": "Locate restrictive adverbs like 'exclusively' and negative guidelines. Color-printing internal drafts explicitly contradicts rule #3.",
            "strategyId": "Cari kata larangan atau pembatas seperti 'exclusively'. Mencetak draf internal dengan tinta berwarna langsung bertentangan dengan aturan nomor 3.",
            "cbtKeyInsight": "Soal CBT No. 6 membidik perilaku pegawai yang melanggar. Pilihan B (mencetak draf internal warna) adalah tindakan yang dilarang."
        },
        {
            "topic": "Membedakan Fakta dan Opini (Categorization Test)",
            "strategyEn": "Statements with 'I think', 'we believe', or 'in my opinion' must be categorized as Opinion. Concrete events like supply arrivals are Facts.",
            "strategyId": "Pernyataan yang memuat kata 'We believe' wajib digolongkan sebagai Opini. Pernyataan dengan nomor PO atau pengiriman fisik adalah Fakta.",
            "cbtKeyInsight": "Pada Soal CBT No. 9, butir A adalah Opinion karena mengandung keyakinan moral, sedangkan butir B dan C merupakan Fact tentang kejadian nyata."
        }
    ]
}

# =========================================================================
# 3. Fat in Balanced Diet
# =========================================================================
mod_3 = {
    "id": "module-3",
    "package": "Paket 1",
    "packageNum": 1,
    "qRange": "Soal 11 - 15",
    "titleEn": "Health & Nutrition: Fat in a Balanced Diet",
    "titleId": "Kesehatan & Nutrisi: Lemak dalam Pola Makan Seimbang",
    "genre": "Nutritional Science & Data",
    "genreBadge": "Health Science",
    "level": "B2 - Upper Intermediate",
    "summaryEn": "A scientific reading passage paired with a nutritional data table explaining the roles of saturated and unsaturated fats, safe daily intake limits for different ages, and heart health risks.",
    "summaryId": "Bacaan sains dan tabel gizi yang menjelaskan perbedaan lemak jenuh dan tak jenuh, ambang batas konsumsi harian berdasarkan kelompok usia, serta risiko penyakit jantung.",
    "hasImage": True,
    "image": "/images/image(7398).png",
    "imageCaptionEn": "Table: Recommended Daily Fat and Saturated Fat Limits by Age and Gender",
    "imageCaptionId": "Tabel: Batas Anjuran Konsumsi Lemak Harian Berdasarkan Usia dan Jenis Kelamin",
    "paragraphs": [
        {
            "id": 1,
            "type": "heading",
            "en": "Fat in Balanced Diet",
            "idTranslation": "Lemak dalam Pola Makan Seimbang",
            "keyWords": ["Balanced Diet", "Nutrition"]
        },
        {
            "id": 2,
            "type": "paragraph",
            "en": "Your diet must contain some fat, but you must be careful about the kind and quantity of fat you consume. Saturated and unsaturated fats are the two main kinds of fat. The risk of heart disease will get higher when blood cholesterol levels increase due to an extreme consumption of saturated fat.",
            "idTranslation": "Pola makan harian Anda harus mengandung sejumlah lemak, tetapi Anda harus cermat memperhatikan jenis dan jumlah lemak yang dikonsumsi. Lemak jenuh (saturated fat) dan lemak tak jenuh (unsaturated fat) adalah dua jenis lemak utama. Risiko penyakit jantung akan meningkat saat kadar kolesterol dalam darah melonjak akibat konsumsi lemak jenuh yang berlebihan.",
            "keyWords": ["quantity", "saturated fat", "unsaturated fat", "cholesterol", "heart disease"]
        },
        {
            "id": 3,
            "type": "paragraph",
            "en": "Men need to consume a maximum of 30 grams of saturated fat per day on average, and women need less than 20 grams of saturated fat per day on average. Those under the age of 11 must have less saturated fat than adults, while kids under the age of 5 have to avoid a low-fat diet. For healthy growth, young children need dietary fats as a concentrated source of energy and fat-soluble vitamins.",
            "idTranslation": "Pria dewasa disarankan mengonsumsi rata-rata maksimal 30 gram lemak jenuh per hari, dan wanita membutuhkan rata-rata kurang dari 20 gram lemak jenuh per hari. Anak-anak di bawah usia 11 tahun harus mengonsumsi lebih sedikit lemak jenuh dibandingkan orang dewasa, sedangkan balita di bawah usia 5 tahun justru harus menghindari diet rendah lemak. Demi pertumbuhan yang sehat, anak-anak membutuhkan lemak makanan sebagai sumber energi padat dan pelarut vitamin yang larut dalam lemak.",
            "keyWords": ["saturated fat", "maximum", "average", "low-fat diet", "fat-soluble vitamins"]
        },
        {
            "id": 4,
            "type": "paragraph",
            "en": "Nutritionists strongly recommend replacing saturated fats—commonly found in fatty meats, butter, palm oil, and processed pastries—with unsaturated fats. Foods rich in unsaturated fats include oily fish (such as salmon and mackerel), nuts, seeds, avocados, and vegetable oils like olive oil. These healthy fats assist in maintaining balanced cholesterol levels and safeguarding cardiovascular wellness.",
            "idTranslation": "Para pakar nutrisi sangat menyarankan untuk mengganti lemak jenuh—yang jamak dijumpai pada daging berlemak, mentega, minyak sawit, dan kue olahan—dengan lemak tak jenuh. Makanan yang kaya akan lemak tak jenuh meliputi ikan berminyak (seperti salmon dan makerel), kacang-kacangan, biji-bijian, alpukat, serta minyak nabati seperti minyak zaitun. Lemak sehat ini membantu menjaga kestabilan kolesterol dan memelihara kebugaran pembuluh darah serta jantung.",
            "keyWords": ["replacing", "unsaturated fats", "cardiovascular wellness", "oily fish"]
        }
    ],
    "vocabulary": [
        {"word": "saturated fat", "phonetic": "/ˈsætʃəreɪtɪd fæt/", "pos": "noun", "defEn": "A type of fat containing a high proportion of fatty acid molecules without double bonds, associated with high cholesterol.", "defId": "Lemak jenuh; jenis lemak padat yang jika berlebih dapat memicu naiknya kolesterol jahat.", "example": "Butter and fatty cuts of beef are high in saturated fat."},
        {"word": "unsaturated fat", "phonetic": "/ʌnˈsætʃəreɪtɪd fæt/", "pos": "noun", "defEn": "A fat containing unsaturated fatty acids, typically liquid at room temperature and beneficial for cardiovascular health.", "defId": "Lemak tak jenuh; lemak nabati/ikan sehat yang membantu melindungi jantung.", "example": "Olive oil and avocados provide heart-healthy unsaturated fats."},
        {"word": "cholesterol", "phonetic": "/kəˈlestərɒl/", "pos": "noun", "defEn": "A compound of the sterol type found in most body tissues, high levels of which can narrow arteries.", "defId": "Kolesterol; senyawa lemak dalam darah yang kadarnya harus terkontrol.", "example": "Excessive intake of trans fats leads to elevated bad cholesterol levels."},
        {"word": "cardiovascular", "phonetic": "/ˌkɑːdiəʊˈvæskjələ(r)/", "pos": "adjective", "defEn": "Relating to the heart and blood vessels.", "defId": "Kardiovaskular; berkaitan dengan jantung dan pembuluh darah.", "example": "Regular aerobic exercise improves cardiovascular endurance."},
        {"word": "fat-soluble", "phonetic": "/fæt ˈsɒljəbl/", "pos": "adjective", "defEn": "Capable of dissolving in fats and oils (e.g., vitamins A, D, E, K).", "defId": "Larut dalam lemak (seperti vitamin A, D, E, dan K).", "example": "Vitamins A and D are fat-soluble, requiring dietary fat for absorption."}
    ],
    "grammarPoints": [
        {
            "topic": "Modals of Obligation & Prohibition (Must, Have to, Need to)",
            "formula": "Subject + must / have to / need to + Base Verb",
            "explanationEn": "Used in scientific and medical texts to state health requirements and strict nutritional limits.",
            "explanationId": "Penggunaan modal auxiliaries untuk menyatakan keharusan medis dan pembatasan asupan gizi.",
            "examples": ["Your diet must contain some fat.", "Men need to consume a maximum of 30g.", "Kids under 5 have to avoid a low-fat diet."]
        },
        {
            "topic": "Cause and Effect Conjunctions (Due to, As a result)",
            "formula": "Effect + due to + Noun Phrase",
            "explanationEn": "Expresses biological relationships where dietary habits trigger specific health outcomes.",
            "explanationId": "Menghubungkan pola sebab-akibat medis antara asupan makanan dan respons fisiologis tubuh.",
            "examples": ["Cholesterol levels increase due to an extreme consumption of saturated fat."]
        }
    ],
    "genericStructure": [
        {"part": "Identification & General Classification", "partId": "Klasifikasi Umum", "descriptionEn": "Introduces dietary fat and classifies it into saturated and unsaturated types.", "descriptionId": "Mengenalkan lemak pangan dan mengklasifikasikannya ke dalam dua golongan.", "excerpt": "Your diet must contain some fat... Saturated and unsaturated fats are the two main kinds..."},
        {"part": "Daily Limits & Age Demographics", "partId": "Ambang Batas Menurut Demografi", "descriptionEn": "Specific quantitative metrics for adult men, women, and young children.", "descriptionId": "Angka batas harian pria (30g), wanita (20g), dan larangan diet rendah lemak balita.", "excerpt": "Men need to consume a maximum of 30 grams... kids under 5 have to avoid..."},
        {"part": "Nutritional Recommendations", "partId": "Rekomendasi Menu Sehat", "descriptionEn": "Practical food substitutions to replace bad fats with heart-protective foods.", "descriptionId": "Panduan mengganti minyak jenuh dengan ikan berminyak, alpukat, dan minyak zaitun.", "excerpt": "Nutritionists strongly recommend replacing saturated fats... with oily fish, nuts..."}
    ],
    "tkaStrategies": [
        {
            "topic": "Membaca Angka & Pengecoh Kelompok Usia (Demographic Detail Questions)",
            "strategyEn": "Pay close attention to exceptions. While older children and adults must restrict saturated fats, children under 5 must NOT be put on a low-fat diet because they need energy for brain growth.",
            "strategyId": "Cermati pengecualian pada teks. Orang dewasa dibatasi konsumsi lemaknya, tetapi balita di bawah 5 tahun TIDAK boleh diet rendah lemak karena butuh energi tumbuh kembang.",
            "cbtKeyInsight": "Soal CBT No. 11 dan 14 menanyakan kebenaran data usia: anak balita (under 5) harus menghindari diet rendah lemak (avoid a low-fat diet)."
        },
        {
            "topic": "Membaca Tabel Gizi Terpadu (Integrating Text & Table Data)",
            "strategyEn": "Correlate table figures with text statements. The text states men need <30g and women <20g; verify products against these daily benchmark values.",
            "strategyId": "Cocokkan angka pada tabel dengan pernyataan pada teks. Angka batas 30g untuk pria dan 20g untuk wanita menjadi acuan evaluasi produk makanan.",
            "cbtKeyInsight": "Soal CBT No. 12 menguji kesimpulan kandungan produk berdasarkan tabel nilai gizi pendamping (image 7398)."
        }
    ]
}

# =========================================================================
# 4. Nurse Assistant Internship
# =========================================================================
mod_4 = {
    "id": "module-4",
    "package": "Paket 1",
    "packageNum": 1,
    "qRange": "Soal 16 - 20",
    "titleEn": "Vocational Recount: Nurse Assistant Internship Experience",
    "titleId": "Teks Recount Kejuruan: Pengalaman Magang Asisten Perawat",
    "genre": "Vocational Healthcare Recount",
    "genreBadge": "Vocational Recount",
    "level": "B1 - Intermediate",
    "summaryEn": "A personal recount by Sinta, a vocational nursing assistant student from Semarang, narrating her three-month clinical rotation at Sehati Hospital through nurseries, outpatient clinics, and inpatient wards.",
    "summaryId": "Teks pengalaman pribadi (recount) oleh Sinta, siswi SMK Asisten Keperawatan di Semarang, yang mengisahkan rotasi klinis magang selama tiga bulan di RS Sehati di berbagai bangsal perawatan.",
    "hasImage": False,
    "image": None,
    "imageCaptionEn": "",
    "imageCaptionId": "",
    "paragraphs": [
        {
            "id": 1,
            "type": "heading",
            "en": "My Internship Experience as a Nurse Assistant",
            "idTranslation": "Pengalaman Magang Saya sebagai Asisten Perawat",
            "keyWords": ["Internship", "Nurse Assistant"]
        },
        {
            "id": 2,
            "type": "paragraph",
            "en": "Hello. My name is Sinta. I am majoring in Nursing Assistant at Semarang Health Vocational School. I would like to share my experience completing an internship at Sehati Hospital in Semarang from February 20th to May 20th. Five of my friends and I completed our internship there. Before I even started my internship, I already predicted that the experience would be exciting but challenging and wearying at the same time. At Sehati Hospital, we interned and learned in various places, including the nursery, the outpatient ward, the inpatient ward, the operating room, and the emergency room. After about two and a half weeks, we moved to a different room or division.",
            "idTranslation": "Halo. Nama saya Sinta. Saya mengambil jurusan Asisten Keperawatan di SMK Kesehatan Semarang. Saya ingin berbagi pengalaman saat menjalani magang di Rumah Sakit Sehati Semarang dari tanggal 20 Februari hingga 20 Mei. Lima orang teman saya dan saya menyelesaikan magang di sana. Sebelum magang dimulai, saya sudah menduga bahwa pengalaman ini akan sangat seru namun menantang dan melelahkan pada saat yang sama. Di RS Sehati, kami magang dan belajar di berbagai unit, meliputi ruang bayi (nursery), bangsal rawat jalan, bangsal rawat inap, ruang operasi, dan instalasi gawat darurat (IGD). Setelah sekitar dua setengah minggu, kami berpindah ke ruangan atau divisi yang berbeda.",
            "keyWords": ["majoring in", "internship", "predict", "wearying", "rotations", "outpatient", "inpatient"]
        },
        {
            "id": 3,
            "type": "paragraph",
            "en": "At first, I was assigned to the nursery, where I learned from senior nurses how to correctly and carefully bathe babies, prepare formula, wash bottles, change diapers, and educate new mothers on breastfeeding. Next, in the third week, when I was in the outpatient ward, I communicated directly with many patients. My duties included checking vital signs, assisting with medical record-keeping, collecting laboratory results, and preparing the doctor's office.",
            "idTranslation": "Awalnya, saya ditugaskan di ruang perawatan bayi (nursery), tempat saya menimba ilmu dari perawat senior tentang cara memandikan bayi dengan benar dan hati-hati, meracik susu formula, mencuci botol susu, mengganti popok, serta mengedukasi ibu-ibu baru mengenai pemberian ASI. Selanjutnya, pada minggu ketiga saat bertugas di bangsal rawat jalan, saya berinteraksi langsung dengan banyak pasien. Tugas saya mencakup memeriksa tanda-tanda vital (tensi, nadi, suhu), membantu pencatatan rekam medis, mengambil hasil laboratorium, dan merapikan ruang periksa dokter.",
            "keyWords": ["assigned to", "nursery", "breastfeeding", "vital signs", "medical record-keeping"]
        },
        {
            "id": 4,
            "type": "paragraph",
            "en": "After around two and a half weeks in the outpatient ward, I interned in the inpatient ward where I learned deeper bedside manners. I monitored patient IV drips, assisted bedridden patients with meals, and observed how professional nurses managed post-operative care. I loved it when patients smiled and expressed genuine gratitude when feeling better. This hands-on clinical exposure solidified my ambition to become a registered nurse in the future.",
            "idTranslation": "Setelah sekitar dua setengah minggu di bangsal rawat jalan, saya melanjutkan magang di bangsal rawat inap di mana saya belajar lebih mendalam mengenai etika pelayanan di samping tempat tidur pasien (bedside manners). Saya memantau tetesan infus pasien, menyuapi pasien yang tirah baring, dan mengamati bagaimana perawat profesional menangani perawatan pasca-operasi. Saya sangat bahagia ketika pasien tersenyum dan mengungkapkan rasa terima kasih yang tulus saat kondisi mereka membaik. Pengalaman klinis langsung ini semakin memantapkan tekad saya untuk menjadi perawat profesional berlisensi di masa depan.",
            "keyWords": ["bedside manners", "IV drips", "bedridden", "post-operative", "genuine gratitude"]
        }
    ],
    "vocabulary": [
        {"word": "wearying", "phonetic": "/ˈwɪəriɪŋ/", "pos": "adjective", "defEn": "Causing one to feel tired, exhausted, or drained.", "defId": "Melelahkan atau menguras tenaga secara fisik dan mental.", "example": "A twelve-hour hospital shift can be demanding and wearying."},
        {"word": "vital signs", "phonetic": "/ˌvaɪtl ˈsaɪnz/", "pos": "noun (plural)", "defEn": "Clinical measurements (pulse rate, temperature, respiration rate, and blood pressure) indicating state of essential bodily functions.", "defId": "Tanda-tanda vital tubuh (tekanan darah, denyut nadi, suhu badan).", "example": "The nursing assistant recorded the patient's vital signs before the physician arrived."},
        {"word": "outpatient ward", "phonetic": "/ˈaʊtpeɪʃnt wɔːd/", "pos": "noun", "defEn": "The hospital department providing medical care without an overnight stay.", "defId": "Bangsal rawat jalan (pasien periksa tanpa menginap).", "example": "The outpatient ward operates from morning until evening on weekdays."},
        {"word": "inpatient ward", "phonetic": "/ˈɪnpeɪʃnt wɔːd/", "pos": "noun", "defEn": "Hospital section where patients are admitted and monitored overnight or longer.", "defId": "Bangsal rawat inap (pasien tinggal dan bermalam di rumah sakit).", "example": "Family visits are allowed during scheduled hours in the inpatient ward."},
        {"word": "bedridden", "phonetic": "/ˈbedrɪdn/", "pos": "adjective", "defEn": "Confined to bed by sickness or old age.", "defId": "Tirah baring; tidak mampu bangun dari ranjang karena sakit.", "example": "Special care is essential for bedridden patients to avoid pressure sores."}
    ],
    "grammarPoints": [
        {
            "topic": "Simple Past for Completed Recount Events",
            "formula": "Subject + Verb 2 (assigned, communicated, loved, solidified)",
            "explanationEn": "Used as the primary tense in Recount texts to sequence chronological events that took place in past clinical rotations.",
            "explanationId": "Tense utama dalam teks recount untuk menceritakan runtutan kegiatan magang yang telah selesai di masa lampau.",
            "examples": ["I was assigned to the nursery.", "I communicated directly with many patients.", "We completed our internship there."]
        },
        {
            "topic": "Time Duration & Date Connectors",
            "formula": "From [Date 1] to [Date 2] / For [Duration]",
            "explanationEn": "Pinpoints the exact time frame of experiences, frequently evaluated in TKA detail questions.",
            "explanationId": "Penanda rentang waktu yang menentukan lamanya kegiatan magang berlangsung.",
            "examples": ["From February 20th to May 20th (3 full months).", "After around two and a half weeks..."]
        }
    ],
    "genericStructure": [
        {"part": "Orientation", "partId": "Orientasi Awal", "descriptionEn": "Introduces Sinta, her vocational major, hospital venue, total duration, and companions.", "descriptionId": "Mengenalkan Sinta, sekolah kejuruan, lokasi RS Sehati, durasi, dan teman magangnya.", "excerpt": "Hello. My name is Sinta. I am majoring in Nursing Assistant... February 20th to May 20th..."},
        {"part": "Series of Clinical Events", "partId": "Rangkaian Pengalaman Klinis", "descriptionEn": "Chronological description of duties across nursery, outpatient, and inpatient units.", "descriptionId": "Uraian tugas mulai dari merawat bayi, mengukur tensi, hingga memantau infus pasien.", "excerpt": "At first, I was assigned to the nursery... Next, in the third week... in the inpatient ward..."},
        {"part": "Reorientation & Personal Reflection", "partId": "Reorientasi & Refleksi", "descriptionEn": "Emotional takeaway, patient gratitude, and career goal confirmation.", "descriptionId": "Kesan emosional rasa syukur pasien dan peneguhan cita-cita menjadi perawat.", "excerpt": "This hands-on clinical exposure solidified my ambition to become a registered nurse."}
    ],
    "tkaStrategies": [
        {
            "topic": "Menghitung Durasi Waktu (Calculating Date Spans)",
            "strategyEn": "Count months between dates carefully: February 20th to May 20th = precisely 3 full months (approx. 90 days). Avoid choosing options that say 'six months' or 'one year'.",
            "strategyId": "Hitung rentang tanggal secara presisi: 20 Februari sampai 20 Mei adalah tepat 3 bulan. Hindari memilih opsi 6 bulan atau 1 bulan.",
            "cbtKeyInsight": "Soal CBT No. 20 menanyakan durasi magang Sinta. Jawaban yang tepat adalah 3 bulan (February 20 to May 20)."
        },
        {
            "topic": "Membedakan Tugas Antar-Ruangan (Specific Task Matching)",
            "strategyEn": "Differentiate duties by ward: Nursery = bathing babies & breastfeeding education; Outpatient = vital signs & medical records; Inpatient = IV drips & bedside meals.",
            "strategyId": "Petakan tugas berdasarkan unit: Nursery = memandikan bayi; Rawat Jalan = tanda vital & rekam medis; Rawat Inap = cek infus & mendampingi makan.",
            "cbtKeyInsight": "Soal CBT No. 17 menguji tanggung jawab Sinta saat berada di rawat jalan (outpatient ward)."
        }
    ]
}

# =========================================================================
# 5. The Beauty of Bougainvillea
# =========================================================================
mod_5 = {
    "id": "module-5",
    "package": "Paket 1",
    "packageNum": 1,
    "qRange": "Soal 21 - 25",
    "titleEn": "Botanical Report: The Beauty of Bougainvillea",
    "titleId": "Laporan Botani: Keindahan Bunga Bougenvil",
    "genre": "Biological Report Text",
    "genreBadge": "Botanical Report",
    "level": "B1 - Intermediate",
    "summaryEn": "An informative scientific report describing the biological anatomy of the Bougainvillea (Paper Flower), clarifying that the vibrant colorful structures are modified leaf bracts rather than actual flower petals.",
    "summaryId": "Teks laporan ilmiah botani yang mendeskripsikan morfologi tanaman Bougenvil (Bunga Kertas), meluruskan kesalahpahaman umum bahwa kelopak berwarna-warni sebenarnya adalah daun pemikat (braktea).",
    "hasImage": False,
    "image": None,
    "imageCaptionEn": "",
    "imageCaptionId": "",
    "paragraphs": [
        {
            "id": 1,
            "type": "heading",
            "en": "The Beauty of Bougainvillea",
            "idTranslation": "Keindahan Bunga Bougenvil",
            "keyWords": ["Bougainvillea", "Ornamental Plant"]
        },
        {
            "id": 2,
            "type": "paragraph",
            "en": "Bougainvillea is an ornamental plant that is well known in various regions of Indonesia. The actual flower of this plant is very small and right in the middle of the petals. However, people often consider the brightly colored petals as the flower itself because they are more eye-catching. Planting this flower is relatively easy, one of the methods being stem cuttings.",
            "idTranslation": "Bougenvil adalah tanaman hias yang sangat populer dan dikenal luas di berbagai wilayah Indonesia. Bunga sejati dari tanaman ini sebenarnya berukuran sangat mungil dan terletak tepat di tengah-tengah kelopak. Akan tetapi, masyarakat kerap menganggap kelopak berwarna cerah tersebut sebagai bunganya sendiri karena tampak jauh lebih memikat pandangan. Menanam bunga ini tergolong cukup mudah, salah satu teknik yang lazim digunakan adalah stek batang.",
            "keyWords": ["ornamental plant", "actual flower", "eye-catching", "stem cuttings"]
        },
        {
            "id": 3,
            "type": "paragraph",
            "en": "This plant is also called Paper Flower because its flowers are as smooth and thin as paper. Bougainvillea generally grows upright and has a relatively small shape. Its leaves are dark green, oval-shaped, and not sharply pointed at the tip. The beauty of this plant lies in its brightly colored petals which have several color variations depending on the type.",
            "idTranslation": "Tanaman ini juga kerap dijuluki Bunga Kertas lantaran seludang bunganya bertekstur halus dan setipis lembaran kertas. Bougenvil pada umumnya tumbuh tegak dengan perawakan rimbun. Daunnya berwarna hijau tua, berbentuk oval (bulat telur), dan tidak runcing tajam di ujungnya. Daya pikat utama tanaman ini terletak pada selubung bunganya yang berwarna semarak dengan aneka ragam corak bergantung pada varietasnya.",
            "keyWords": ["Paper Flower", "upright", "dark green", "oval-shaped", "variations"]
        },
        {
            "id": 4,
            "type": "paragraph",
            "en": "The trunk and branches are surrounded by thorns. Bougainvillea can grow more than 10 meters tall. The leaves are large, slightly pointed, and grow densely around the branches. Bougainvillea originates from South America, but over time, it has spread widely to tropical regions such as Indonesia because it has high adaptability, is drought-tolerant, and requires optimal sunlight. It can grow almost in every season, which makes it possible to enjoy its beauty throughout the year.",
            "idTranslation": "Batang dan dahan tanaman ini dipersenjatai oleh duri-duri tajam. Bougenvil mampu merambat dan tumbuh menjulang hingga lebih dari 10 meter. Daunnya tumbuh lebat menyelimuti cabang-cabang ranting. Bougenvil sejatinya berasal dari kawasan Amerika Selatan, namun seiring waktu, tanaman ini telah tersebar luas ke wilayah tropis seperti Indonesia berkat daya adaptasinya yang tinggi, tahan terhadap cuaca kering/kekeringan, serta memerlukan paparan sinar matahari penuh. Ia sanggup berbunga di hampir setiap musim, memungkinkan siapa pun menikmati keindahannya sepanjang tahun.",
            "keyWords": ["thorns", "South America", "tropical regions", "drought-tolerant", "throughout the year"]
        }
    ],
    "vocabulary": [
        {"word": "ornamental plant", "phonetic": "/ˌɔːnəˈmentl plɑːnt/", "pos": "noun", "defEn": "A plant grown for decorative and aesthetic purposes rather than for food or timber.", "defId": "Tanaman hias yang dibudidayakan untuk mempercantik taman atau pekarangan.", "example": "Bougainvillea and orchids are cherished ornamental plants across Southeast Asia."},
        {"word": "stem cuttings", "phonetic": "/stem ˈkʌtɪŋz/", "pos": "noun (plural)", "defEn": "A piece of plant stem used for vegetative propagation.", "defId": "Stek batang; cara memperbanyak tanaman secara vegetatif dengan memotong ranting.", "example": "Propagating bougainvillea via stem cuttings ensures rapid root development."},
        {"word": "drought-tolerant", "phonetic": "/draʊt ˈtɒlərənt/", "pos": "adjective", "defEn": "Able to survive periods of dry weather with minimal water.", "defId": "Tahan kekeringan; sanggup hidup dengan pasokan air yang sedikit.", "example": "Cacti and bougainvillea are famously drought-tolerant species."},
        {"word": "thorns", "phonetic": "/θɔːnz/", "pos": "noun (plural)", "defEn": "Stiff, sharp-pointed woody projections on a plant stem.", "defId": "Duri tajam yang tumbuh pada batang atau dahan tanaman.", "example": "Gardeners must wear thick gloves to prune bougainvillea branches covered in thorns."},
        {"word": "adaptability", "phonetic": "/əˌdæptəˈbɪləti/", "pos": "noun", "defEn": "The quality of being able to adjust to new conditions.", "defId": "Kemampuan adaptasi atau daya penyesuaian diri terhadap lingkungan baru.", "example": "The plant's high adaptability allowed it to thrive across equatorial zones."}
    ],
    "grammarPoints": [
        {
            "topic": "Simple Present Tense for General Biological Truths",
            "formula": "Subject + Verb 1 (-s/-es) / to be (is, are)",
            "explanationEn": "Used in botanical scientific reports to describe permanent characteristics, physical appearance, and growth behaviors.",
            "explanationId": "Digunakan dalam teks report ilmiah untuk memaparkan karakteristik fisik dan perilaku alami flora secara faktual.",
            "examples": ["Bougainvillea is an ornamental plant.", "The trunk and branches are surrounded by thorns.", "It requires optimal sunlight."]
        },
        {
            "topic": "Simile and Descriptive Comparisons",
            "formula": "as + Adjective + as + Noun",
            "explanationEn": "Used to vividly convey tactile properties to readers.",
            "explanationId": "Kiasan perbandingan 'as... as' untuk melukiskan kelembutan kelopak seperti kertas.",
            "examples": ["Its flowers are as smooth and thin as paper."]
        }
    ],
    "genericStructure": [
        {"part": "General Classification", "partId": "Klasifikasi Umum", "descriptionEn": "Introduces Bougainvillea as an ornamental species and clarifies the true flower vs petal confusion.", "descriptionId": "Mengenalkan Bougenvil sebagai tanaman hias dan posisi bunga mungil yang sebenarnya.", "excerpt": "Bougainvillea is an ornamental plant... The actual flower is very small and right in the middle..."},
        {"part": "Physical Description & Anatomy", "partId": "Deskripsi Morfologi Fisik", "descriptionEn": "Leaf shape, trunk height, thorns, and color variations.", "descriptionId": "Bentuk daun oval, duri pada dahan, tinggi hingga 10 meter, dan variasi warna.", "excerpt": "Its leaves are dark green, oval-shaped... The trunk and branches are surrounded by thorns..."},
        {"part": "Origin, Habitat & Climate Adaptations", "partId": "Asal-Usul & Daya Tahan Tropis", "descriptionEn": "South American origin and drought-resistant resilience in tropical sunlight.", "descriptionId": "Berasal dari Amerika Selatan dan ketahanan luar biasa terhadap terik matahari tropis.", "excerpt": "Bougainvillea originates from South America... drought-tolerant, and requires optimal sunlight."}
    ],
    "tkaStrategies": [
        {
            "topic": "Mengidentifikasi Bagian Bunga Sejati (Actual Flower vs Bracts)",
            "strategyEn": "Look out for comprehension questions regarding what is mistaken for the flower. The colorful parts are modified leaves/bracts, while the real flower is tiny and located at the center.",
            "strategyId": "Waspadai pertanyaan jebakan mengenai bunga sejati. Bagian berwarna cerah adalah kelopak/daun pelindung semu, sedangkan bunga aslinya berukuran sangat kecil di tengah.",
            "cbtKeyInsight": "Soal CBT No. 24 dan 25 menegaskan bahwa masyarakat sering salah mengira kelopak warna-warni sebagai bunga, padahal bunga aslinya kecil di tengah."
        },
        {
            "topic": "Karakteristik Daun (Morphological Traits)",
            "strategyEn": "Scan for adjective sequences: 'dark green', 'oval-shaped', and 'not sharply pointed'.",
            "strategyId": "Cari kombinasi kata sifat bentuk daun: hijau gelap (dark green), bulat telur (oval), dan tidak berujung runcing tajam.",
            "cbtKeyInsight": "Soal CBT No. 23 menanyakan bentuk daun Bougenvil: oval-shaped (berbentuk oval/bulat telur)."
        }
    ]
}

# =========================================================================
# 6. Bandung Techno Park
# =========================================================================
mod_6 = {
    "id": "module-6",
    "package": "Paket 1",
    "packageNum": 1,
    "qRange": "Soal 26 - 30",
    "titleEn": "Technological Innovation: Bandung Techno Park (BTP)",
    "titleId": "Inovasi Teknologi: Bandung Techno Park (BTP)",
    "genre": "Technical & Innovation Report",
    "genreBadge": "Technology Hub",
    "level": "B2 - Upper Intermediate",
    "summaryEn": "An informative overview of Bandung Techno Park (BTP), Indonesia's premier 50-hectare research hub housing additive manufacturing 3D-printers, advanced materials labs, and high-security life sciences wings.",
    "summaryId": "Ulasan informatif mengenai Bandung Techno Park (BTP), kawasan riset teknologi seluas 50 hektar di Indonesia yang memiliki fasilitas pencetakan 3D manufaktur aditif, lab material maju, dan lab vaksin.",
    "hasImage": False,
    "image": None,
    "imageCaptionEn": "",
    "imageCaptionId": "",
    "paragraphs": [
        {
            "id": 1,
            "type": "heading",
            "en": "Bandung Techno Park",
            "idTranslation": "Bandung Techno Park (BTP)",
            "keyWords": ["Bandung Techno Park", "Innovation Hub"]
        },
        {
            "id": 2,
            "type": "paragraph",
            "en": "Bandung Techno Park (BTP) is one of Indonesia’s most important places for new technology and innovation. It contains around 20 structures designed to support research and development, and it occupies about 50 hectares of land. Many technology companies and new start-ups choose BTP as their base because of its modern facilities.",
            "idTranslation": "Bandung Techno Park (BTP) merupakan salah satu pusat terpenting di Indonesia untuk pengembangan teknologi mutakhir dan inovasi. Kawasan ini memiliki sekitar 20 bangunan yang dirancang khusus guna mendukung penelitian dan pengembangan (R&D), serta menempati lahan seluas kurang lebih 50 hektar. Banyak perusahaan teknologi dan perintis usaha (start-up) baru memilih BTP sebagai markas operasi berkat fasilitasnya yang modern.",
            "keyWords": ["research and development", "occupies", "start-ups", "modern facilities"]
        },
        {
            "id": 3,
            "type": "paragraph",
            "en": "One important area is the advanced materials laboratory, which stores and provides special tools for studying materials in great detail. This lab has equipment like powerful microscopes that can see things almost at the atomic level. As a result, researchers have made significant progress in developing new semiconductors and nanomaterials.",
            "idTranslation": "Salah satu area krusial adalah laboratorium material maju (advanced materials laboratory), yang menyimpan dan menyediakan peralatan khusus untuk menganalisis material secara mendalam. Lab ini dilengkapi instrumen seperti mikroskop berkekuatan tinggi yang sanggup mengamati objek hingga tingkat atom. Alhasil, para peneliti telah mencatatkan kemajuan berarti dalam mengembangkan semikonduktor baru dan material berskala nano (nanomaterials).",
            "keyWords": ["advanced materials", "atomic level", "semiconductors", "nanomaterials"]
        },
        {
            "id": 4,
            "type": "paragraph",
            "en": "Next to it is the additive manufacturing center, which has large 3D printers that can make parts from plastics and metals. This enables companies to create and test new designs more quickly. For example, the center has made special medical implants that fit a patient’s body exactly. The life sciences research wing has high-security laboratories where scientists work on new medicines and study infectious diseases. These labs contributed significantly to the development of vaccines during the COVID-19 epidemic. The integration testing center allows different technologies such as smart city systems, renewable energy, and AI software to be tested together.",
            "idTranslation": "Di sebelahnya terdapat pusat manufaktur aditif (additive manufacturing center), yang diperkuat mesin cetak 3D berskala besar yang mampu membuat komponen dari bahan plastik maupun logam. Hal ini memungkinkan perusahaan merancang dan menguji purwarupa baru dengan jauh lebih gesit. Sebagai contoh, pusat ini telah memproduksi implan medis khusus yang sangat presisi dengan anatomi tubuh pasien. Sayap riset ilmu hayati (life sciences) memiliki laboratorium berkeamanan tinggi tempat para ilmuwan meneliti obat-obatan baru dan virus penyakit menular. Lab-lab ini berkontribusi nyata pada pengembangan vaksin selama pandemi COVID-19. Selain itu, pusat uji integrasi memfasilitasi pengujian gabungan berbagai teknologi seperti sistem kota cerdas (smart city), energi terbarukan, dan peranti lunak kecerdasan buatan (AI).",
            "keyWords": ["additive manufacturing", "3D printers", "medical implants", "life sciences", "vaccines", "smart city"]
        },
        {
            "id": 5,
            "type": "paragraph",
            "en": "BTP also supports green technology through the renewable energy testing facility. Here, companies can test solar panels, wind energy systems, and batteries in different conditions. For data work, the data analytics center has very fast computers that help researchers in areas like climate studies and artificial intelligence. One of BTP’s strengths is that it is open for collaboration with universities to private companies all through straightforward and manageable administration and agreements. All BTP facilities follow ISO 9001:2015 standards, which means their work is high quality and trusted worldwide.",
            "idTranslation": "BTP juga mengusung teknologi hijau melalui fasilitas pengujian energi terbarukan. Di sini, perusahaan dapat menguji panel surya, sistem tenaga angin, dan performa baterai di berbagai kondisi cuaca. Untuk pengolahan data, pusat analitik data dilengkapi superkomputer berkecepatan tinggi yang mendukung periset di bidang iklim dan kecerdasan buatan. Salah satu keunggulan utama BTP adalah keterbukaannya dalam menjalin kolaborasi, mulai dari perguruan tinggi hingga korporasi swasta melalui prosedur administrasi dan kemitraan yang transparan. Seluruh fasilitas BTP menerapkan sertifikasi standar ISO 9001:2015, yang menjamin hasil kerja bermutu tinggi serta diakui secara internasional.",
            "keyWords": ["renewable energy", "data analytics", "collaboration", "ISO 9001:2015", "trusted worldwide"]
        }
    ],
    "vocabulary": [
        {"word": "additive manufacturing", "phonetic": "/ˈædətɪv ˌmænjuˈfæktʃərɪŋ/", "pos": "noun", "defEn": "The industrial production name for 3D printing, building 3D objects by adding layer upon layer.", "defId": "Manufaktur aditif; teknik produksi pencetakan 3D dengan menumpuk lapisan material lapis demi lapis.", "example": "Additive manufacturing reduces material wastage compared to traditional CNC cutting."},
        {"word": "semiconductors", "phonetic": "/ˌsemikənˈdʌktəz/", "pos": "noun (plural)", "defEn": "Solid substances with electrical conductivity between that of a conductor and an insulator, vital for microchips.", "defId": "Semikonduktor; bahan inti pembuatan mikrocip komputer dan elektronik modern.", "example": "BTP researchers work on advanced silicon semiconductors for sensor devices."},
        {"word": "implants", "phonetic": "/ˈɪmplɑːnts/", "pos": "noun (plural)", "defEn": "Artificial medical devices manufactured to replace, support, or enhance a biological structure.", "defId": "Implan medis; peranti buatan yang dipasang di dalam tubuh pasien.", "example": "Custom titanium medical implants can be printed within hours at BTP."},
        {"word": "collaboration", "phonetic": "/kəˌlæbəˈreɪʃn/", "pos": "noun", "defEn": "The action of working with someone to produce or create something.", "defId": "Kolaborasi atau kerja sama strategis antara berbagai lembaga.", "example": "BTP fosters strong collaboration between academia and high-tech startups."},
        {"word": "infectious diseases", "phonetic": "/ɪnˈfekʃəs dɪˈziːzɪz/", "pos": "noun (plural)", "defEn": "Illnesses caused by pathogenic microorganisms like bacteria, viruses, parasites, or fungi.", "defId": "Penyakit menular yang disebabkan oleh patogen/virus.", "example": "The biocontainment wing studies infectious diseases to design responsive vaccines."}
    ],
    "grammarPoints": [
        {
            "topic": "Passive Voice in Technical Descriptions",
            "formula": "Object + to be (is/are/were) + Past Participle (V3)",
            "explanationEn": "Used in technical writing when the focus is on the facility, machinery, or process rather than on the human operator.",
            "explanationId": "Kalimat pasif dalam wacana teknis untuk menitikberatkan pada teknologi, laboratorium, dan hasil uji daripada operator manusianya.",
            "examples": ["It contains around 20 structures designed to support research.", "Special medical implants are made.", "Technologies can be tested together."]
        },
        {
            "topic": "Defining Relative Clauses with 'Which' & 'Where'",
            "formula": "Noun + which (things/facilities) / where (locations) + Clause",
            "explanationEn": "Provides essential descriptive details about the specific functions of various laboratories and tech divisions.",
            "explanationId": "Klausa relatif pembatas untuk memerinci fungsi spesifik dari masing-masing gedung laboratorium.",
            "examples": ["...the additive manufacturing center, which has large 3D printers...", "...high-security laboratories where scientists work on new medicines..."]
        }
    ],
    "genericStructure": [
        {"part": "General Identification", "partId": "Identifikasi Umum", "descriptionEn": "Size (50 hectares), building count (20 structures), and core mission as Indonesia's tech park.", "descriptionId": "Luas wilayah 50 ha, jumlah gedung (20), dan peran sentralnya bagi inovasi teknologi.", "excerpt": "Bandung Techno Park (BTP) is one of Indonesia’s most important places... occupies about 50 hectares..."},
        {"part": "Specialized Laboratories Breakdown", "partId": "Rincian Laboratorium & Fasilitas", "descriptionEn": "Details advanced materials lab, 3D printing center, and life sciences vaccine research.", "descriptionId": "Pusat cetak 3D untuk implan medis, riset material nano, dan lab vaksin penyakit menular.", "excerpt": "One important area is the advanced materials laboratory... Next to it is additive manufacturing..."},
        {"part": "Sustainability & Institutional Strengths", "partId": "Keberlanjutan & Keunggulan Institusi", "descriptionEn": "Green energy testing, ISO 9001:2015 compliance, and open academic-corporate partnership.", "descriptionId": "Uji panel surya, standar mutu ISO 9001:2015, dan kemitraan riset kampus-swasta.", "excerpt": "BTP also supports green technology... All BTP facilities follow ISO 9001:2015 standards..."}
    ],
    "tkaStrategies": [
        {
            "topic": "Menjodohkan Fasilitas dengan Fungsinya (Facility-Function Matching)",
            "strategyEn": "Keep a mental map: Advanced Materials = powerful microscopes & semiconductors; Additive Manufacturing = 3D printers & medical implants; Life Sciences = vaccines & infectious diseases; Integration Center = smart city & AI.",
            "strategyId": "Pahami pemetaan fasilitas: Material Maju = mikroskop & semikonduktor; Manufaktur Aditif = printer 3D & implan medis; Ilmu Hayati = vaksin; Pusat Integrasi = smart city & AI.",
            "cbtKeyInsight": "Soal CBT No. 26 dan 27 meminta mencocokkan fasilitas BTP dengan fungsi kerjanya secara presisi."
        },
        {
            "topic": "Tujuan Utama Pendirian BTP (Main Purpose Analysis)",
            "strategyEn": "Focus on paragraph 1: BTP is founded to serve as a comprehensive national base for R&D, commercial innovation, and startup incubation.",
            "strategyId": "Fokus pada paragraf 1: BTP dirikan sebagai wadah terpadu penelitian, inovasi teknologi baru, dan inkubasi perusahaan rintisan.",
            "cbtKeyInsight": "Soal CBT No. 29 menanyakan tujuan utama BTP: menjadi pusat inovasi teknologi dan riset terpadu di Indonesia."
        }
    ]
}

modules.extend([mod_1, mod_2, mod_3, mod_4, mod_5, mod_6])
print(f"Loaded {len(modules)} modules (Paket 1 complete).")
