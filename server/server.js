const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Load Data
const DATA_DIR = fs.existsSync(path.join(__dirname, 'data'))
  ? path.join(__dirname, 'data')
  : path.join(process.cwd(), 'server', 'data');

const modulesData = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'modules.json'), 'utf-8'));
const vocabData = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'vocabulary.json'), 'utf-8'));
const guideData = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'reading_guide.json'), 'utf-8'));
const statsData = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'stats.json'), 'utf-8'));

// API Routes

// 1. Stats Endpoint
app.get('/api/stats', (req, res) => {
  res.json({
    status: 'success',
    data: statsData
  });
});

// 2. Modules List with Filters
app.get('/api/modules', (req, res) => {
  let results = [...modulesData];
  const { search, package: pkg, genre, level } = req.query;

  if (pkg) {
    const pkgLower = pkg.toLowerCase();
    results = results.filter(m => 
      m.package.toLowerCase().includes(pkgLower) || 
      String(m.packageNum) === pkgLower
    );
  }

  if (genre) {
    const genreLower = genre.toLowerCase();
    results = results.filter(m => 
      m.genre.toLowerCase().includes(genreLower) ||
      m.genreBadge.toLowerCase().includes(genreLower)
    );
  }

  if (level) {
    const levelLower = level.toLowerCase();
    results = results.filter(m => m.level.toLowerCase().includes(levelLower));
  }

  if (search) {
    const query = search.toLowerCase().trim();
    results = results.filter(m => 
      m.titleEn.toLowerCase().includes(query) ||
      m.titleId.toLowerCase().includes(query) ||
      m.summaryEn.toLowerCase().includes(query) ||
      m.summaryId.toLowerCase().includes(query) ||
      m.genre.toLowerCase().includes(query) ||
      m.genreBadge.toLowerCase().includes(query) ||
      m.paragraphs.some(p => p.en.toLowerCase().includes(query) || p.idTranslation.toLowerCase().includes(query)) ||
      m.vocabulary.some(v => v.word.toLowerCase().includes(query) || v.defId.toLowerCase().includes(query))
    );
  }

  // Return list with lightweight metadata for cards
  const listItems = results.map(m => ({
    id: m.id,
    package: m.package,
    packageNum: m.packageNum,
    qRange: m.qRange,
    titleEn: m.titleEn,
    titleId: m.titleId,
    genre: m.genre,
    genreBadge: m.genreBadge,
    level: m.level,
    estimatedReadTime: m.estimatedReadTime,
    wordCount: m.wordCount,
    summaryEn: m.summaryEn,
    summaryId: m.summaryId,
    hasImage: m.hasImage,
    image: m.image,
    keyVocabPreview: m.vocabulary.slice(0, 3).map(v => v.word),
    paragraphsCount: m.paragraphs.length
  }));

  res.json({
    status: 'success',
    count: listItems.length,
    data: listItems
  });
});

// 3. Module Detail by ID
app.get('/api/modules/:id', (req, res) => {
  const mod = modulesData.find(m => m.id === req.params.id);
  if (!mod) {
    return res.status(404).json({
      status: 'error',
      message: `Modul dengan ID '${req.params.id}' tidak ditemukan.`
    });
  }

  // Find adjacent modules for Prev / Next navigation
  const currentIndex = modulesData.findIndex(m => m.id === req.params.id);
  const prevModule = currentIndex > 0 ? {
    id: modulesData[currentIndex - 1].id,
    titleEn: modulesData[currentIndex - 1].titleEn,
    package: modulesData[currentIndex - 1].package
  } : null;
  const nextModule = currentIndex < modulesData.length - 1 ? {
    id: modulesData[currentIndex + 1].id,
    titleEn: modulesData[currentIndex + 1].titleEn,
    package: modulesData[currentIndex + 1].package
  } : null;

  res.json({
    status: 'success',
    data: {
      ...mod,
      navigation: {
        prev: prevModule,
        next: nextModule,
        currentIndex: currentIndex + 1,
        totalModules: modulesData.length
      }
    }
  });
});

// 4. Master Vocabulary List
app.get('/api/vocabulary', (req, res) => {
  let list = [...vocabData];
  const { q, letter, package: pkg } = req.query;

  if (letter) {
    const l = letter.toUpperCase();
    list = list.filter(item => item.word.toUpperCase().startsWith(l));
  }

  if (pkg) {
    const pkgLower = pkg.toLowerCase();
    list = list.filter(item => item.package.toLowerCase().includes(pkgLower));
  }

  if (q) {
    const query = q.toLowerCase().trim();
    list = list.filter(item => 
      item.word.toLowerCase().includes(query) ||
      item.defEn.toLowerCase().includes(query) ||
      item.defId.toLowerCase().includes(query) ||
      item.example.toLowerCase().includes(query)
    );
  }

  res.json({
    status: 'success',
    count: list.length,
    data: list
  });
});

// 5. Reading Strategy Guide
app.get('/api/guide', (req, res) => {
  res.json({
    status: 'success',
    data: guideData
  });
});

// 6. Global Search
app.get('/api/search', (req, res) => {
  const query = (req.query.q || '').toLowerCase().trim();
  if (!query) {
    return res.json({ status: 'success', data: { modules: [], vocabulary: [] } });
  }

  const matchingModules = modulesData.filter(m => 
    m.titleEn.toLowerCase().includes(query) ||
    m.titleId.toLowerCase().includes(query) ||
    m.summaryEn.toLowerCase().includes(query) ||
    m.summaryId.toLowerCase().includes(query) ||
    m.genre.toLowerCase().includes(query) ||
    m.paragraphs.some(p => p.en.toLowerCase().includes(query) || p.idTranslation.toLowerCase().includes(query))
  ).map(m => ({
    id: m.id,
    titleEn: m.titleEn,
    titleId: m.titleId,
    package: m.package,
    genreBadge: m.genreBadge,
    summaryId: m.summaryId
  }));

  const matchingVocab = vocabData.filter(v =>
    v.word.toLowerCase().includes(query) ||
    v.defEn.toLowerCase().includes(query) ||
    v.defId.toLowerCase().includes(query)
  );

  res.json({
    status: 'success',
    data: {
      modules: matchingModules,
      vocabulary: matchingVocab
    }
  });
});

// Serve Static Frontend Assets
const PUBLIC_DIR = fs.existsSync(path.join(__dirname, '..', 'public'))
  ? path.join(__dirname, '..', 'public')
  : path.join(process.cwd(), 'public');

app.use(express.static(PUBLIC_DIR));

// Fallback to index.html for client-side routing
app.use((req, res) => {
  res.sendFile(path.join(PUBLIC_DIR, 'index.html'));
});

// Start Server (only if run directly)
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`=======================================================`);
    console.log(`  TKA English Reading Mastery Web Portal is running!`);
    console.log(`  Local URL: http://localhost:${PORT}`);
    console.log(`  CBT Source: https://cbt.erlanggaonline.co.id/book/details/0054200490.0094`);
    console.log(`  Loaded ${modulesData.length} Modules across 3 CBT Packages`);
    console.log(`=======================================================`);
  });
}

module.exports = app;
