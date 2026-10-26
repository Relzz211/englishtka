/**
 * TKA ENGLISH MASTER - Client Application Logic
 * Single Page Application for TKA English Reading Mastery
 */

class TKAApp {
  constructor() {
    this.state = {
      currentView: 'modules',
      modules: [],
      filteredModules: [],
      activeModule: null,
      readingMode: localStorage.getItem('tka_reading_mode') || 'dual',
      fontSizeLevel: parseInt(localStorage.getItem('tka_font_level') || '0', 10),
      filterPackage: 'all',
      filterGenre: 'all',
      searchQuery: '',
      sortOption: 'default',
      bookmarks: JSON.parse(localStorage.getItem('tka_bookmarks') || '[]'),
      theme: localStorage.getItem('tka_theme') || 'dark',
      masterVocab: [],
      filteredVocab: [],
      selectedVocabPkg: 'all',
      selectedAlpha: 'ALL',
      guide: null,
      tts: {
        synth: window.speechSynthesis,
        speaking: false,
        rate: 1.0,
        voice: null
      }
    };

    this.init();
  }

  async init() {
    this.applyTheme(this.state.theme);
    this.updateBookmarkBadge();
    this.initTTSVoices();
    this.initScrollProgress();

    // Fetch initial datasets
    await Promise.all([
      this.fetchStats(),
      this.fetchModules(),
      this.fetchMasterVocab(),
      this.fetchGuide()
    ]);

    // Handle deep link hash
    this.handleRouting();
    window.addEventListener('hashchange', () => this.handleRouting());

    // Close floating tooltip on outside click
    document.addEventListener('click', (e) => {
      const tooltip = document.getElementById('vocabTooltipCard');
      if (tooltip && !tooltip.contains(e.target) && !e.target.classList.contains('vocab-token')) {
        this.hideVocabTooltip();
      }
    });
  }

  /* =========================================================================
     THEME & NAVIGATION
     ========================================================================= */
  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    this.state.theme = theme;
    localStorage.setItem('tka_theme', theme);
    const themeIcon = document.getElementById('themeIcon');
    if (themeIcon) {
      themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
  }

  toggleTheme() {
    const nextTheme = this.state.theme === 'dark' ? 'light' : 'dark';
    this.applyTheme(nextTheme);
  }

  toggleMobileMenu() {
    const nav = document.getElementById('mainNav');
    if (nav) nav.classList.toggle('open');
  }

  showView(viewName, updateHash = true) {
    this.state.currentView = viewName;

    if (updateHash) {
      if (viewName === 'modules') {
        if (window.location.hash) {
          history.pushState(null, '', window.location.pathname + window.location.search);
        }
      } else if (viewName !== 'reader') {
        window.location.hash = viewName;
      }
    }

    // Close mobile nav if open
    const nav = document.getElementById('mainNav');
    if (nav) nav.classList.remove('open');

    // Update main nav buttons
    document.querySelectorAll('.main-nav .nav-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.view === viewName);
    });

    // Hide all view sections
    const sections = ['viewModules', 'viewReader', 'viewVocabulary', 'viewGuide', 'viewBookmarks'];
    sections.forEach(id => {
      const el = document.getElementById(id);
      if (el) el.style.display = 'none';
    });

    // Stop TTS if navigating away from reader
    if (viewName !== 'reader' && this.state.tts.speaking) {
      this.stopTTS();
    }

    // Show active section
    if (viewName === 'modules') {
      document.getElementById('viewModules').style.display = 'block';
    } else if (viewName === 'reader') {
      document.getElementById('viewReader').style.display = 'block';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (viewName === 'vocabulary') {
      document.getElementById('viewVocabulary').style.display = 'block';
      this.renderMasterVocab();
    } else if (viewName === 'guide') {
      document.getElementById('viewGuide').style.display = 'block';
      this.renderGuide();
    } else if (viewName === 'bookmarks') {
      document.getElementById('viewBookmarks').style.display = 'block';
      this.renderBookmarksView();
    }
  }

  handleRouting() {
    const rawHash = (window.location.hash || '').replace(/^#\/?/, '').trim();
    if (rawHash.startsWith('module/')) {
      const moduleId = rawHash.replace('module/', '');
      this.openModule(moduleId, false);
    } else if (rawHash === 'vocabulary') {
      this.showView('vocabulary', false);
    } else if (rawHash === 'guide') {
      this.showView('guide', false);
    } else if (rawHash === 'bookmarks') {
      this.showView('bookmarks', false);
    } else {
      this.showView('modules', false);
    }
  }

  /* =========================================================================
     DATA FETCHING
     ========================================================================= */
  async fetchStats() {
    try {
      const res = await fetch('/api/stats');
      const data = await res.json();
      if (data.status === 'success') {
        const stats = data.data;
        document.getElementById('statModulesCount').textContent = stats.totalModules;
        document.getElementById('statPackagesCount').textContent = stats.totalPackages;
        document.getElementById('statVocabCount').textContent = stats.totalVocabulary + '+';
      }
    } catch (e) {
      console.warn('Stats fetch error:', e);
    }
  }

  async fetchModules() {
    try {
      const res = await fetch('/api/modules');
      const json = await res.json();
      if (json.status === 'success') {
        this.state.modules = json.data;
        this.applyFilters();
      }
    } catch (e) {
      console.error('Modules fetch error:', e);
    }
  }

  async fetchMasterVocab() {
    try {
      const res = await fetch('/api/vocabulary');
      const json = await res.json();
      if (json.status === 'success') {
        this.state.masterVocab = json.data;
        this.state.filteredVocab = json.data;
        this.renderAlphaFilter();
      }
    } catch (e) {
      console.error('Vocab fetch error:', e);
    }
  }

  async fetchGuide() {
    try {
      const res = await fetch('/api/guide');
      const json = await res.json();
      if (json.status === 'success') {
        this.state.guide = json.data;
        document.getElementById('guideMainTitle').textContent = json.data.title;
        document.getElementById('guideMainSubtitle').textContent = json.data.subtitle;
      }
    } catch (e) {
      console.error('Guide fetch error:', e);
    }
  }

  /* =========================================================================
     MODULES LIST & FILTERING
     ========================================================================= */
  applyFilters() {
    let list = [...this.state.modules];

    // Filter Package
    if (this.state.filterPackage !== 'all') {
      list = list.filter(m => String(m.packageNum) === this.state.filterPackage);
    }

    // Filter Genre
    if (this.state.filterGenre !== 'all') {
      const g = this.state.filterGenre.toLowerCase();
      list = list.filter(m => 
        m.genre.toLowerCase().includes(g) || 
        m.genreBadge.toLowerCase().includes(g)
      );
    }

    // Search Query
    if (this.state.searchQuery) {
      const q = this.state.searchQuery.toLowerCase().trim();
      list = list.filter(m =>
        m.titleEn.toLowerCase().includes(q) ||
        m.titleId.toLowerCase().includes(q) ||
        m.summaryEn.toLowerCase().includes(q) ||
        m.summaryId.toLowerCase().includes(q) ||
        m.genreBadge.toLowerCase().includes(q)
      );
    }

    // Sorting
    if (this.state.sortOption === 'time-asc') {
      list.sort((a, b) => parseInt(a.estimatedReadTime) - parseInt(b.estimatedReadTime));
    } else if (this.state.sortOption === 'words-desc') {
      list.sort((a, b) => b.wordCount - a.wordCount);
    } else if (this.state.sortOption === 'title-asc') {
      list.sort((a, b) => a.titleEn.localeCompare(b.titleEn));
    }

    this.state.filteredModules = list;
    this.renderModulesGrid();
  }

  handleSearch(val) {
    this.state.searchQuery = val;
    const clearBtn = document.getElementById('clearSearchBtn');
    if (clearBtn) clearBtn.style.display = val ? 'block' : 'none';
    this.applyFilters();
  }

  clearSearch() {
    const input = document.getElementById('globalSearchInput');
    if (input) input.value = '';
    this.handleSearch('');
  }

  filterByPackage(pkg) {
    this.state.filterPackage = pkg;
    document.querySelectorAll('.package-tabs .pkg-tab').forEach(tab => {
      tab.classList.toggle('active', tab.dataset.pkg === pkg);
    });
    this.applyFilters();
  }

  filterByGenre(genre) {
    this.state.filterGenre = genre;
    document.querySelectorAll('.genre-pills .genre-pill').forEach(pill => {
      pill.classList.toggle('active', pill.dataset.genre === genre);
    });
    this.applyFilters();
  }

  handleSort(val) {
    this.state.sortOption = val;
    this.applyFilters();
  }

  resetFilters() {
    this.state.filterPackage = 'all';
    this.state.filterGenre = 'all';
    this.state.searchQuery = '';
    const input = document.getElementById('globalSearchInput');
    if (input) input.value = '';
    document.getElementById('clearSearchBtn').style.display = 'none';

    document.querySelectorAll('.package-tabs .pkg-tab').forEach(t => t.classList.toggle('active', t.dataset.pkg === 'all'));
    document.querySelectorAll('.genre-pills .genre-pill').forEach(p => p.classList.toggle('active', p.dataset.genre === 'all'));
    this.applyFilters();
  }

  renderModulesGrid() {
    const grid = document.getElementById('modulesGrid');
    const empty = document.getElementById('emptyState');
    const sub = document.getElementById('modulesListSub');

    if (this.state.filteredModules.length === 0) {
      grid.innerHTML = '';
      empty.style.display = 'block';
      if (sub) sub.textContent = 'Tidak ditemukan modul yang sesuai';
      return;
    }

    empty.style.display = 'none';
    if (sub) sub.textContent = `Menampilkan ${this.state.filteredModules.length} materi bacaan`;

    grid.innerHTML = this.state.filteredModules.map(m => {
      const isBookmarked = this.state.bookmarks.includes(m.id);
      return `
        <article class="module-card" onclick="app.openModule('${m.id}')">
          <div>
            <div class="card-top">
              <div class="card-badges">
                <span class="chip-badge chip-pkg">${m.package}</span>
                <span class="chip-badge chip-q">${m.qRange}</span>
                <span class="chip-badge chip-genre">${m.genreBadge}</span>
              </div>
              <button class="card-bookmark-btn ${isBookmarked ? 'active' : ''}" 
                      onclick="event.stopPropagation(); app.toggleBookmark('${m.id}')" 
                      title="${isBookmarked ? 'Hapus bookmark' : 'Simpan bookmark'}">
                ${isBookmarked ? '★' : '☆'}
              </button>
            </div>

            <h3 class="card-title-en">${m.titleEn}</h3>
            <h4 class="card-title-id">${m.titleId}</h4>
            <p class="card-summary">${m.summaryId}</p>

            <div class="card-vocab-tags">
              ${(m.keyVocabPreview || []).map(v => `<span class="vocab-tag">${v}</span>`).join('')}
            </div>
          </div>

          <div class="card-footer">
            <div class="card-meta-info">
              <span>⏱️ ${m.estimatedReadTime}</span>
              <span>📝 ${m.wordCount} kata</span>
              <span>📊 ${m.level}</span>
            </div>
            <div class="card-read-action">
              <span>Mulai Baca</span>
              <span>→</span>
            </div>
          </div>
        </article>
      `;
    }).join('');
  }

  /* =========================================================================
     MODULE READER VIEW
     ========================================================================= */
  async openModule(moduleId, updateHash = true) {
    try {
      if (updateHash) {
        window.location.hash = `module/${moduleId}`;
      }

      // Check if we need to fetch or if we already have it
      let mod = this.state.activeModule && this.state.activeModule.id === moduleId ? this.state.activeModule : null;
      if (!mod) {
        const res = await fetch(`/api/modules/${moduleId}`);
        const json = await res.json();
        if (json.status !== 'success') return;
        mod = json.data;
        this.state.activeModule = mod;
      }

      // Populate Header Metadata
      document.getElementById('readerPkgBadge').textContent = mod.package;
      document.getElementById('readerQBadge').textContent = mod.qRange;
      document.getElementById('readerGenreBadge').textContent = mod.genreBadge;
      document.getElementById('readerTitleEn').textContent = mod.titleEn;
      document.getElementById('readerTitleId').textContent = mod.titleId;
      document.getElementById('readerReadTime').textContent = mod.estimatedReadTime;
      document.getElementById('readerWordCount').textContent = mod.wordCount;
      document.getElementById('readerLevel').textContent = mod.level;
      document.getElementById('readerSummaryEn').textContent = mod.summaryEn;
      document.getElementById('readerSummaryId').textContent = mod.summaryId;

      // Bookmark Button State
      const isBookmarked = this.state.bookmarks.includes(mod.id);
      const bmIcon = document.getElementById('readerBookmarkIcon');
      const bmBtn = document.getElementById('readerBookmarkBtn');
      if (bmIcon) bmIcon.textContent = isBookmarked ? '★' : '☆';
      if (bmBtn) bmBtn.classList.toggle('active', isBookmarked);

      // Diagram Card (Image)
      const diagContainer = document.getElementById('readerDiagramContainer');
      if (mod.hasImage && mod.image) {
        diagContainer.style.display = 'block';
        document.getElementById('readerDiagramImg').src = mod.image;
        document.getElementById('readerDiagramCapEn').textContent = mod.imageCaptionEn || '';
        document.getElementById('readerDiagramCapId').textContent = mod.imageCaptionId || '';
      } else {
        diagContainer.style.display = 'none';
      }

      // Render Text Layout with current mode
      this.renderReaderText();

      // Deepdive Tabs Data
      this.renderDeepdiveData(mod);

      // Navigation Footer
      const navInd = document.getElementById('navIndicator');
      if (navInd) {
        navInd.textContent = `Modul ${mod.navigation.currentIndex} dari ${mod.navigation.totalModules}`;
      }
      const prevBtn = document.getElementById('prevModuleBtn');
      const nextBtn = document.getElementById('nextModuleBtn');
      if (prevBtn) {
        prevBtn.style.visibility = mod.navigation.prev ? 'visible' : 'hidden';
      }
      if (nextBtn) {
        nextBtn.style.visibility = mod.navigation.next ? 'visible' : 'hidden';
      }

      // Show Reader View (without changing hash!)
      this.showView('reader', false);

    } catch (e) {
      console.error('Error opening module:', e);
    }
  }

  closeReader() {
    this.showView('modules', true);
  }

  navigateModule(direction) {
    if (!this.state.activeModule) return;
    const nav = this.state.activeModule.navigation;
    if (direction === 'prev' && nav.prev) {
      this.openModule(nav.prev.id, true);
    } else if (direction === 'next' && nav.next) {
      this.openModule(nav.next.id, true);
    }
  }

  setReadingMode(mode) {
    this.state.readingMode = mode;
    localStorage.setItem('tka_reading_mode', mode);

    document.querySelectorAll('.mode-switcher .mode-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.mode === mode);
    });

    this.renderReaderText();
  }

  renderReaderText() {
    const mod = this.state.activeModule;
    if (!mod) return;

    const layout = document.getElementById('readerContentLayout');
    const mode = this.state.readingMode;

    // Helper to inject interactive vocabulary spans into English text
    const vocabList = mod.vocabulary || [];
    const enrichEnglishText = (text) => {
      let enriched = text;
      vocabList.forEach(v => {
        const escaped = v.word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(`\\b(${escaped})\\b`, 'gi');
        enriched = enriched.replace(regex, (match) => {
          return `<span class="vocab-token" data-word="${v.word.replace(/"/g, '&quot;')}">${match}</span>`;
        });
      });
      return enriched;
    };

    // Attach delegated click listener for vocab tokens
    layout.onclick = (e) => {
      const token = e.target.closest('.vocab-token');
      if (token) {
        const word = token.getAttribute('data-word');
        app.showVocabTooltip(e, word);
      }
    };

    if (mode === 'dual') {
      // DUAL COLUMN (Side-by-side)
      let html = `
        <div class="layout-dual">
          <div class="dual-columns-header">
            <div class="col-header-en">🇬🇧 Teks Bahasa Inggris Asli</div>
            <div class="col-header-id">🇮🇩 Terjemahan Bahasa Indonesia</div>
          </div>
      `;

      mod.paragraphs.forEach((p, idx) => {
        html += `
          <div class="para-pair" id="paraPair-${p.id}" 
               onmouseenter="app.highlightPair(${p.id}, true)" 
               onmouseleave="app.highlightPair(${p.id}, false)">
            <div class="col-en">${enrichEnglishText(p.en)}</div>
            <div class="col-id">${p.idTranslation}</div>
          </div>
        `;
      });

      html += `</div>`;
      layout.innerHTML = html;

    } else if (mode === 'interleaved') {
      // INTERLEAVED (Line-by-line / Accordion block)
      let html = `<div class="layout-interleaved">`;

      mod.paragraphs.forEach(p => {
        html += `
          <div class="interleaved-block">
            <div class="block-en">
              <span class="block-label label-en">English</span>
              <div>${enrichEnglishText(p.en)}</div>
            </div>
            <div class="block-id">
              <span class="block-label label-id">Terjemahan</span>
              <div>${p.idTranslation}</div>
            </div>
          </div>
        `;
      });

      html += `</div>`;
      layout.innerHTML = html;

    } else if (mode === 'en') {
      // ENGLISH ONLY
      let html = `<div class="layout-single">`;
      mod.paragraphs.forEach(p => {
        html += `<div class="single-para">${enrichEnglishText(p.en)}</div>`;
      });
      html += `</div>`;
      layout.innerHTML = html;

    } else if (mode === 'id') {
      // INDONESIAN ONLY
      let html = `<div class="layout-single">`;
      mod.paragraphs.forEach(p => {
        html += `<div class="single-para">${p.idTranslation}</div>`;
      });
      html += `</div>`;
      layout.innerHTML = html;
    }
  }

  highlightPair(id, active) {
    const el = document.getElementById(`paraPair-${id}`);
    if (el) el.classList.toggle('active-highlight', active);
  }

  adjustFontSize(delta) {
    this.state.fontSizeLevel = Math.max(-2, Math.min(3, this.state.fontSizeLevel + delta));
    localStorage.setItem('tka_font_level', this.state.fontSizeLevel);
    const baseSize = 1.0625 + (this.state.fontSizeLevel * 0.125);
    document.documentElement.style.setProperty('--reader-font-size', `${baseSize}rem`);
  }

  /* =========================================================================
     DEEP-DIVE LEARNING TABS
     ========================================================================= */
  setDeepdiveTab(tabName) {
    document.querySelectorAll('.deepdive-tabs .deepdive-tab').forEach(t => {
      t.classList.toggle('active', t.dataset.tab === tabName);
    });

    const panels = ['tabVocabPanel', 'tabGrammarPanel', 'tabStructurePanel', 'tabInsightsPanel'];
    panels.forEach(id => {
      const el = document.getElementById(id);
      if (el) el.style.display = 'none';
    });

    if (tabName === 'vocab') document.getElementById('tabVocabPanel').style.display = 'block';
    if (tabName === 'grammar') document.getElementById('tabGrammarPanel').style.display = 'block';
    if (tabName === 'structure') document.getElementById('tabStructurePanel').style.display = 'block';
    if (tabName === 'insights') document.getElementById('tabInsightsPanel').style.display = 'block';
  }

  renderDeepdiveData(mod) {
    // 1. Vocab Grid
    const vocabGrid = document.getElementById('readerVocabGrid');
    const vocabCount = document.getElementById('deepdiveVocabCount');
    if (vocabCount) vocabCount.textContent = (mod.vocabulary || []).length;

    if (vocabGrid) {
      vocabGrid.innerHTML = (mod.vocabulary || []).map(v => `
        <div class="vocab-item-card">
          <div>
            <div class="vocab-card-header">
              <div>
                <div class="vocab-word-title">${v.word}</div>
                <div class="vocab-meta">
                  <span class="vocab-phonetic">${v.phonetic || ''}</span>
                  <span class="vocab-pos-badge">${v.pos || ''}</span>
                </div>
              </div>
              <button class="speak-icon-btn" onclick="app.speakWord('${v.word}')" title="Dengarkan pengucapan">🔊</button>
            </div>
            <div class="vocab-def-id">🇮🇩 ${v.defId}</div>
            <div class="vocab-def-en">🇬🇧 ${v.defEn}</div>
          </div>
          <div class="vocab-example">"${v.example}"</div>
        </div>
      `).join('');
    }

    // 2. Grammar Points
    const grammarList = document.getElementById('readerGrammarList');
    if (grammarList) {
      grammarList.innerHTML = (mod.grammarPoints || []).map(g => `
        <div class="grammar-card">
          <h4>📐 ${g.topic}</h4>
          ${g.formula ? `<div class="grammar-formula">Pola Rumus: ${g.formula}</div>` : ''}
          <div class="grammar-explanation-id"><strong>Penjelasan:</strong> ${g.explanationId}</div>
          <div class="grammar-explanation-en"><small>${g.explanationEn}</small></div>
          <div class="grammar-examples-box">
            <strong>Contoh dalam Kalimat:</strong>
            ${(g.examples || []).map(ex => `<div>• ${ex}</div>`).join('')}
          </div>
        </div>
      `).join('');
    }

    // 3. Generic Structure
    const structList = document.getElementById('readerStructureList');
    if (structList) {
      structList.innerHTML = (mod.genericStructure || []).map(s => `
        <div class="structure-step">
          <h4>🏛️ ${s.part} <span class="structure-sub">(${s.partId})</span></h4>
          <div class="structure-desc"><strong>Fungsi:</strong> ${s.descriptionId}</div>
          <div class="structure-excerpt"><em>Kutipan Teks:</em> "${s.excerpt}"</div>
        </div>
      `).join('');
    }

    // 4. CBT Reading Insights & Strategies
    const insightsList = document.getElementById('readerInsightsList');
    if (insightsList) {
      insightsList.innerHTML = (mod.tkaStrategies || []).map(ins => `
        <div class="insight-card">
          <h4>💡 ${ins.topic}</h4>
          <div class="insight-strategy-id">${ins.strategyId}</div>
          <div class="insight-cbt-key">
            <strong>Analisis Kunci Soal CBT Erlangga:</strong><br>
            ${ins.cbtKeyInsight}
          </div>
        </div>
      `).join('');
    }
  }

  /* =========================================================================
     INTERACTIVE VOCABULARY TOOLTIP
     ========================================================================= */
  showVocabTooltip(event, word) {
    event.stopPropagation();
    if (!this.state.activeModule) return;

    const v = (this.state.activeModule.vocabulary || []).find(
      item => item.word.toLowerCase() === word.toLowerCase()
    );
    if (!v) return;

    const card = document.getElementById('vocabTooltipCard');
    document.getElementById('tooltipWord').textContent = v.word;
    document.getElementById('tooltipPhonetic').textContent = v.phonetic || '';
    document.getElementById('tooltipPos').textContent = v.pos || '';
    document.getElementById('tooltipDefId').textContent = v.defId;
    document.getElementById('tooltipDefEn').textContent = v.defEn;
    document.getElementById('tooltipExample').textContent = `"${v.example}"`;

    const speakBtn = document.getElementById('tooltipSpeakBtn');
    speakBtn.onclick = () => this.speakWord(v.word);

    // Position tooltip near the clicked element
    const rect = event.target.getBoundingClientRect();
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;

    let top = rect.bottom + scrollTop + 8;
    let left = rect.left + scrollLeft - 60;

    // Boundary checks
    if (left + 330 > window.innerWidth) {
      left = window.innerWidth - 340;
    }
    if (left < 10) left = 10;

    card.style.top = `${top}px`;
    card.style.left = `${left}px`;
    card.style.display = 'block';
  }

  hideVocabTooltip() {
    const card = document.getElementById('vocabTooltipCard');
    if (card) card.style.display = 'none';
  }

  /* =========================================================================
     TEXT-TO-SPEECH (TTS) AUDIO SYNTHESIS
     ========================================================================= */
  initTTSVoices() {
    if (!window.speechSynthesis) return;
    const loadVoices = () => {
      const voices = window.speechSynthesis.getVoices();
      // Look for natural English voice
      const preferred = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha')));
      this.state.tts.voice = preferred || voices.find(v => v.lang.startsWith('en'));
    };

    window.speechSynthesis.onvoiceschanged = loadVoices;
    loadVoices();
  }

  setTTSSpeed(speed) {
    this.state.tts.rate = parseFloat(speed);
    if (this.state.tts.speaking) {
      this.stopTTS();
      this.playTTS();
    }
  }

  toggleTTS() {
    if (this.state.tts.speaking) {
      this.stopTTS();
    } else {
      this.playTTS();
    }
  }

  playTTS() {
    const mod = this.state.activeModule;
    if (!mod || !window.speechSynthesis) return;

    window.speechSynthesis.cancel();

    // Collect all paragraph English text
    const fullText = mod.paragraphs.map(p => p.en).join('. ');
    const utter = new SpeechSynthesisUtterance(fullText);
    utter.rate = this.state.tts.rate || 1.0;
    if (this.state.tts.voice) utter.voice = this.state.tts.voice;

    const playBtn = document.getElementById('ttsPlayBtn');
    const btnText = document.getElementById('ttsBtnText');
    const icon = document.getElementById('ttsIcon');

    utter.onstart = () => {
      this.state.tts.speaking = true;
      if (playBtn) playBtn.classList.add('speaking');
      if (btnText) btnText.textContent = 'Jeda Audio';
      if (icon) icon.textContent = '⏸️';
    };

    utter.onend = () => {
      this.stopTTS();
    };

    utter.onerror = () => {
      this.stopTTS();
    };

    window.speechSynthesis.speak(utter);
  }

  stopTTS() {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    this.state.tts.speaking = false;
    const playBtn = document.getElementById('ttsPlayBtn');
    const btnText = document.getElementById('ttsBtnText');
    const icon = document.getElementById('ttsIcon');

    if (playBtn) playBtn.classList.remove('speaking');
    if (btnText) btnText.textContent = 'Dengarkan Audio';
    if (icon) icon.textContent = '🔊';
  }

  speakWord(word) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(word);
    utter.rate = 0.9;
    if (this.state.tts.voice) utter.voice = this.state.tts.voice;
    window.speechSynthesis.speak(utter);
  }

  /* =========================================================================
     READING PROGRESS TRACKER
     ========================================================================= */
  initScrollProgress() {
    window.addEventListener('scroll', () => {
      if (this.state.currentView !== 'reader') return;
      const winHeight = window.innerHeight;
      const docHeight = document.documentElement.scrollHeight;
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const progress = (scrollTop / (docHeight - winHeight)) * 100;

      const bar = document.getElementById('readingProgressBar');
      if (bar) bar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
    });
  }

  /* =========================================================================
     IMAGE MODAL
     ========================================================================= */
  openImageModal(src) {
    const modal = document.getElementById('imageModal');
    const img = document.getElementById('modalImg');
    if (modal && img) {
      img.src = src;
      modal.style.display = 'flex';
    }
  }

  closeImageModal() {
    const modal = document.getElementById('imageModal');
    if (modal) modal.style.display = 'none';
  }

  /* =========================================================================
     BOOKMARKS SYSTEM
     ========================================================================= */
  toggleBookmark(moduleId) {
    let bms = this.state.bookmarks;
    if (bms.includes(moduleId)) {
      bms = bms.filter(id => id !== moduleId);
    } else {
      bms.push(moduleId);
    }
    this.state.bookmarks = bms;
    localStorage.setItem('tka_bookmarks', JSON.stringify(bms));

    this.updateBookmarkBadge();
    this.renderModulesGrid();

    // If on bookmarks view, re-render
    if (this.state.currentView === 'bookmarks') {
      this.renderBookmarksView();
    }
  }

  toggleCurrentBookmark() {
    if (!this.state.activeModule) return;
    this.toggleBookmark(this.state.activeModule.id);

    const isBookmarked = this.state.bookmarks.includes(this.state.activeModule.id);
    const bmIcon = document.getElementById('readerBookmarkIcon');
    const bmBtn = document.getElementById('readerBookmarkBtn');
    if (bmIcon) bmIcon.textContent = isBookmarked ? '★' : '☆';
    if (bmBtn) bmBtn.classList.toggle('active', isBookmarked);
  }

  updateBookmarkBadge() {
    const badge = document.getElementById('bookmarkCount');
    if (badge) badge.textContent = this.state.bookmarks.length;
  }

  renderBookmarksView() {
    const container = document.getElementById('bookmarksContent');
    if (!container) return;

    const bookmarkedModules = this.state.modules.filter(m => this.state.bookmarks.includes(m.id));

    if (bookmarkedModules.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">⭐</div>
          <h3>Belum ada modul yang tersimpan</h3>
          <p>Klik tombol bintang (☆) pada kartu modul bacaan untuk menyimpannya ke daftar ini.</p>
          <button class="btn btn-primary" onclick="app.showView('modules')">Jelajahi Modul</button>
        </div>
      `;
      return;
    }

    container.innerHTML = `
      <div class="modules-grid">
        ${bookmarkedModules.map(m => `
          <article class="module-card" onclick="app.openModule('${m.id}')">
            <div>
              <div class="card-top">
                <div class="card-badges">
                  <span class="chip-badge chip-pkg">${m.package}</span>
                  <span class="chip-badge chip-genre">${m.genreBadge}</span>
                </div>
                <button class="card-bookmark-btn active" 
                        onclick="event.stopPropagation(); app.toggleBookmark('${m.id}')">★</button>
              </div>
              <h3 class="card-title-en">${m.titleEn}</h3>
              <h4 class="card-title-id">${m.titleId}</h4>
              <p class="card-summary">${m.summaryId}</p>
            </div>
            <div class="card-footer">
              <div class="card-meta-info">
                <span>⏱️ ${m.estimatedReadTime}</span>
                <span>📝 ${m.wordCount} kata</span>
              </div>
              <div class="card-read-action">
                <span>Baca Lagi →</span>
              </div>
            </div>
          </article>
        `).join('')}
      </div>
    `;
  }

  /* =========================================================================
     MASTER VOCABULARY DICTIONARY VIEW
     ========================================================================= */
  renderAlphaFilter() {
    const bar = document.getElementById('alphaFilterBar');
    if (!bar) return;

    const letters = 'ALL,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,Z'.split(',');
    bar.innerHTML = letters.map(l => `
      <button class="alpha-btn ${this.state.selectedAlpha === l ? 'active' : ''}" 
              onclick="app.filterVocabAlpha('${l}')">${l}</button>
    `).join('');
  }

  filterVocabAlpha(letter) {
    this.state.selectedAlpha = letter;
    this.renderAlphaFilter();
    this.applyVocabFilters();
  }

  filterVocabPackage(pkg) {
    this.state.selectedVocabPkg = pkg;
    document.querySelectorAll('#vocabPackageFilter .filter-chip').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.vpkg === pkg);
    });
    this.applyVocabFilters();
  }

  handleVocabSearch(query) {
    this.applyVocabFilters(query);
  }

  applyVocabFilters(searchVal) {
    let list = [...this.state.masterVocab];

    // Package
    if (this.state.selectedVocabPkg !== 'all') {
      const p = this.state.selectedVocabPkg;
      list = list.filter(v => v.package.includes(p));
    }

    // Alphabet
    if (this.state.selectedAlpha !== 'ALL') {
      const alpha = this.state.selectedAlpha;
      list = list.filter(v => v.word.toUpperCase().startsWith(alpha));
    }

    // Query
    const q = (searchVal || document.getElementById('vocabSearchInput')?.value || '').toLowerCase().trim();
    if (q) {
      list = list.filter(v => 
        v.word.toLowerCase().includes(q) ||
        v.defId.toLowerCase().includes(q) ||
        v.defEn.toLowerCase().includes(q) ||
        v.example.toLowerCase().includes(q)
      );
    }

    this.state.filteredVocab = list;
    this.renderMasterVocab();
  }

  renderMasterVocab() {
    const grid = document.getElementById('masterVocabGrid');
    if (!grid) return;

    if (this.state.filteredVocab.length === 0) {
      grid.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1;">
          <div class="empty-icon">🗂️</div>
          <h3>Tidak ada kosakata yang cocok</h3>
          <p>Coba gunakan kata pencarian lain atau pilih huruf abjad yang lain.</p>
        </div>
      `;
      return;
    }

    grid.innerHTML = this.state.filteredVocab.map(v => `
      <div class="vocab-item-card">
        <div>
          <div class="vocab-card-header">
            <div>
              <div class="vocab-word-title">${v.word}</div>
              <div class="vocab-meta">
                <span class="vocab-phonetic">${v.phonetic || ''}</span>
                <span class="vocab-pos-badge">${v.pos || ''}</span>
              </div>
            </div>
            <button class="speak-icon-btn" onclick="app.speakWord('${v.word}')" title="Dengarkan pengucapan">🔊</button>
          </div>
          <div class="vocab-def-id">🇮🇩 ${v.defId}</div>
          <div class="vocab-def-en">🇬🇧 ${v.defEn}</div>
        </div>
        <div>
          <div class="vocab-example">"${v.example}"</div>
          <div style="margin-top: 0.75rem; font-size: 0.75rem; color: var(--primary-light);">
            📖 Modul: <a href="#module/${v.moduleId}" style="color: inherit; text-decoration: underline;">${v.moduleTitle}</a>
          </div>
        </div>
      </div>
    `).join('');
  }

  /* =========================================================================
     TKA READING STRATEGY GUIDE VIEW
     ========================================================================= */
  renderGuide() {
    const container = document.getElementById('guideChaptersContainer');
    if (!container || !this.state.guide) return;

    container.innerHTML = this.state.guide.chapters.map((ch, idx) => `
      <div class="guide-chapter-card ${idx === 0 ? 'expanded' : ''}" id="guideCard-${ch.id}">
        <div class="chapter-header" onclick="app.toggleGuideChapter('${ch.id}')">
          <div class="chapter-title-group">
            <div class="chapter-icon">${ch.icon}</div>
            <div>
              <div class="chapter-title-en">Bab ${ch.number}: ${ch.titleEn}</div>
              <div class="chapter-title-id">${ch.titleId}</div>
            </div>
          </div>
          <div class="chapter-toggle-arrow">▼</div>
        </div>

        <div class="chapter-body">
          <div class="chapter-summary">${ch.summary}</div>
          <div class="chapter-markdown">
            ${this.convertSimpleMarkdown(ch.content)}
          </div>
        </div>
      </div>
    `).join('');
  }

  toggleGuideChapter(id) {
    const card = document.getElementById(`guideCard-${id}`);
    if (card) card.classList.toggle('expanded');
  }

  convertSimpleMarkdown(md) {
    return md
      .replace(/### (.*?)\n/g, '<h3>$1</h3>')
      .replace(/\* \*\*(.*?)\*\*(.*?)\n/g, '<li><strong>$1</strong>$2</li>')
      .replace(/\* (.*?)\n/g, '<li>$1</li>')
      .replace(/<li>/g, '<ul><li>')
      .replace(/<\/li>(?!<li>)/g, '</li></ul>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/> \[!TIP\]\n> (.*?)\n/g, '<div style="background: rgba(16, 185, 129, 0.1); border-left: 3px solid var(--accent-emerald); padding: 0.85rem 1.25rem; border-radius: var(--radius-md); margin: 1rem 0; color: #a7f3d0;">💡 <strong>Trik TKA:</strong> $1</div>');
  }
}

// Global App Instance
const app = new TKAApp();
window.app = app;
