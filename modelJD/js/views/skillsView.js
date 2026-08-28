/**
 * Skills View: Comprehensive IT Skill Vocabulary & Categorized Taxonomy
 * Design: Modern White Theme with Accent Pink (SkillMatch IT)
 */
window.SkillsView = {
    searchQuery: '',
    selectedCategory: 'all',

    categories: [
        { id: 'all', label: 'ทั้งหมด (All)', iconClass: 'fa-solid fa-globe' },
        { id: 'lang', label: 'Programming', iconClass: 'fa-solid fa-code' },
        { id: 'web', label: 'Web & Frameworks', iconClass: 'fa-solid fa-laptop-code' },
        { id: 'db', label: 'Databases', iconClass: 'fa-solid fa-database' },
        { id: 'cloud', label: 'Cloud & DevOps', iconClass: 'fa-solid fa-cloud' },
        { id: 'data', label: 'Data & Analytics', iconClass: 'fa-solid fa-chart-line' },
        { id: 'sec', label: 'Cybersecurity', iconClass: 'fa-solid fa-shield-halved' },
        { id: 'test', label: 'QA & Testing', iconClass: 'fa-solid fa-vial-circle-check' }
    ],

    categorizeSkill(skill) {
        const s = skill.toLowerCase();
        if (['python', 'java', 'c#', 'c++', 'c', 'javascript', 'typescript', 'php', 'ruby', 'go', 'golang', 'rust', 'scala', 'kotlin', 'swift', 'dart', 'r', 'html', 'css', 'sass', 'bash', 'shell', 'powershell', 'sql', 'pl/sql'].includes(s)) return 'lang';
        if (s.includes('react') || s.includes('vue') || s.includes('angular') || s.includes('next') || s.includes('node') || s.includes('express') || s.includes('django') || s.includes('flask') || s.includes('fastapi') || s.includes('spring') || s.includes('.net') || s.includes('asp.net') || s.includes('laravel') || s.includes('tailwind') || s.includes('bootstrap')) return 'web';
        if (s.includes('sql') || s.includes('mongo') || s.includes('redis') || s.includes('oracle') || s.includes('postgres') || s.includes('mysql') || s.includes('database') || s.includes('cassandra') || s.includes('dynamodb') || s.includes('elasticsearch')) return 'db';
        if (s.includes('aws') || s.includes('azure') || s.includes('gcp') || s.includes('cloud') || s.includes('docker') || s.includes('kubernetes') || s.includes('terraform') || s.includes('ansible') || s.includes('jenkins') || s.includes('ci/cd') || s.includes('linux') || s.includes('git')) return 'cloud';
        if (s.includes('machine learning') || s.includes('deep learning') || s.includes('nlp') || s.includes('tensorflow') || s.includes('pytorch') || s.includes('scikit') || s.includes('pandas') || s.includes('numpy') || s.includes('data') || s.includes('analytics') || s.includes('power bi') || s.includes('tableau')) return 'data';
        if (s.includes('security') || s.includes('firewall') || s.includes('hacker') || s.includes('penetration') || s.includes('nmap') || s.includes('burp') || s.includes('siem') || s.includes('soc') || s.includes('network') || s.includes('cisco') || s.includes('vpn')) return 'sec';
        if (s.includes('test') || s.includes('selenium') || s.includes('cypress') || s.includes('playwright') || s.includes('postman') || s.includes('qa') || s.includes('junit') || s.includes('pytest') || s.includes('jest')) return 'test';
        return 'other';
    },

    render() {
        return `
        <div class="space-y-6 view-transition-in">
            <!-- Header Banner -->
            <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm border-t-4 border-t-rose-500 space-y-4">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <span class="text-xs font-black tracking-wider uppercase text-rose-700 bg-rose-50 border border-rose-200 px-3 py-1 rounded-xl inline-flex items-center gap-1.5 shadow-2xs">
                            <i class="fa-solid fa-layer-group text-rose-500"></i> คลังคำศัพท์ทักษะมาตรฐาน
                        </span>
                        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2 flex items-center gap-2.5">
                            <i class="fa-solid fa-laptop-code text-rose-600"></i> IT Skills Taxonomy (${AppState.allSkills.length || '1,600+'} ทักษะ)
                        </h2>
                        <p class="text-xs sm:text-sm text-slate-500 font-medium mt-1">
                            ค้นหาและคลิกเพื่อเพิ่มทักษะที่คุณมีลงในตะกร้าประมวลผล (Basket) ได้ทันที
                        </p>
                    </div>
                    <div class="flex items-center gap-2">
                        <button onclick="window.location.hash = '#/matcher'"
                            class="glow-btn-pink px-4 py-2.5 rounded-2xl text-xs font-black flex items-center gap-2 cursor-pointer shadow-md">
                            <i class="fa-solid fa-crosshairs"></i>
                            <span>ไปยังหน้าค้นหางาน (${AppState.userSkills.length} ทักษะที่เลือก)</span>
                        </button>
                    </div>
                </div>

                <!-- Search Input with Accent Pink Focus -->
                <div class="relative pt-2">
                    <input type="text" id="skillSearchInput"
                        placeholder="พิมพ์ค้นหาทักษะไอทีที่ต้องการ... (เช่น Docker, PostgreSQL, React, C#)"
                        value="${ApiClient.escapeHTML(this.searchQuery)}"
                        oninput="SkillsView.onSearchChange(this.value)"
                        class="w-full p-3.5 pl-11 text-sm border border-slate-300 rounded-2xl focus:ring-2 focus:ring-rose-500/30 focus:border-rose-500 outline-none bg-white shadow-2xs transition placeholder:text-slate-400">
                    <span class="absolute left-4 top-5.5 text-slate-400">
                        <i class="fa-solid fa-magnifying-glass"></i>
                    </span>
                </div>

                <!-- Category Filters (Clean White & Pink Active) -->
                <div class="flex items-center gap-2 overflow-x-auto pb-2 pt-1 text-xs">
                    ${this.categories.map(cat => `
                        <button onclick="SkillsView.setCategory('${cat.id}')"
                            class="px-4 py-2.5 rounded-2xl font-bold transition-all shrink-0 cursor-pointer flex items-center gap-2 ${this.selectedCategory === cat.id ? 'glow-btn-pink shadow-md' : 'bg-white hover:bg-rose-50 hover:text-rose-700 text-slate-700 border border-slate-200'}">
                            <i class="${cat.iconClass}"></i>
                            <span>${cat.label}</span>
                        </button>
                    `).join('')}
                </div>
            </div>

            <!-- Skills Grid Card -->
            <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm space-y-4">
                <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                    <div class="text-xs font-extrabold text-slate-700 flex items-center gap-2">
                        <i class="fa-solid fa-circle-dot text-rose-500"></i>
                        <span>รายการทักษะที่พร้อมเลือก:</span>
                        <span id="skillResultCount" class="text-rose-600 font-black">0</span>
                    </div>
                    <div class="text-xs text-slate-400 font-medium hidden sm:block">คลิกที่ป้ายทักษะเพื่อเพิ่ม/ลบจากตะกร้า</div>
                </div>

                <div id="skillsPillsContainer" class="flex flex-wrap gap-2.5 max-h-[500px] overflow-y-auto p-1">
                    <!-- Dynamically populated -->
                </div>
            </div>
        </div>
        `;
    },

    onMount() {
        this.renderPills();
        AppState.subscribe('skills', () => this.renderPills());
    },

    setCategory(catId) {
        this.selectedCategory = catId;
        const app = document.getElementById('router-view');
        if (app) app.innerHTML = this.render();
        this.renderPills();
    },

    onSearchChange(val) {
        this.searchQuery = val.trim().toLowerCase();
        this.renderPills();
    },

    getFilteredSkills() {
        return AppState.allSkills.filter(skill => {
            const matchesQuery = !this.searchQuery || skill.toLowerCase().includes(this.searchQuery);
            if (!matchesQuery) return false;

            if (this.selectedCategory === 'all') return true;
            return this.categorizeSkill(skill) === this.selectedCategory;
        });
    },

    renderPills() {
        const container = document.getElementById("skillsPillsContainer");
        const countSpan = document.getElementById("skillResultCount");
        if (!container) return;

        const skills = this.getFilteredSkills();
        if (countSpan) countSpan.innerText = `${skills.length} ทักษะ`;

        if (skills.length === 0) {
            container.innerHTML = `
                <div class="w-full text-center py-10 text-slate-400 text-sm">
                    <i class="fa-solid fa-magnifying-glass mr-1"></i> ไม่พบทักษะที่ตรงกับเงื่อนไขการค้นหา
                </div>`;
            return;
        }

        container.innerHTML = skills.slice(0, 300).map(skill => {
            const isSelected = AppState.userSkills.includes(skill.toLowerCase());
            return `
                <button onclick="SkillsView.toggleSkill('${skill.replace(/'/g, "\\'")}')"
                    class="skill-chip px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-1.5 ${isSelected ? 'glow-btn-pink ring-2 ring-rose-300 shadow-sm' : 'bg-white hover:bg-rose-50 text-slate-700 hover:text-rose-900 border border-slate-200'}">
                    <i class="${isSelected ? 'fa-solid fa-check' : 'fa-solid fa-plus'} text-[11px]"></i>
                    <span>${ApiClient.escapeHTML(skill)}</span>
                </button>
            `;
        }).join('');
    },

    toggleSkill(skill) {
        const clean = skill.trim().toLowerCase();
        if (AppState.userSkills.includes(clean)) {
            const idx = AppState.userSkills.indexOf(clean);
            AppState.removeSkill(idx);
        } else {
            AppState.addSkill(clean);
        }
    }
};
