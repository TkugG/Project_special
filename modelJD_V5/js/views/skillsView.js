/**
 * Skills View: Comprehensive IT Skill Vocabulary & Categorized Taxonomy
 * Design: Modern White Theme with Accent Pink (SkillMatch IT)
 */
window.SkillsView = {
    searchQuery: '',
    selectedCategory: 'all',
    _unsubSkills: null, // เก็บ unsubscribe fn เพื่อป้องกัน subscriber สะสมทุก route change

    categories: [
        { id: 'all', label: 'ทั้งหมด (All)', iconClass: 'fa-solid fa-layer-group' },
        { id: 'dev', label: 'Software & Web', iconClass: 'fa-solid fa-code' },
        { id: 'infra', label: 'Systems & Network', iconClass: 'fa-solid fa-server' },
        { id: 'data', label: 'Data & AI', iconClass: 'fa-solid fa-chart-line' },
        { id: 'design', label: 'UI/UX & Media', iconClass: 'fa-solid fa-palette' },
        { id: 'mgmt', label: 'Management & Analysis', iconClass: 'fa-solid fa-diagram-project' },
        { id: 'sec', label: 'Cybersecurity', iconClass: 'fa-solid fa-shield-halved' },
        { id: 'test', label: 'QA & Testing', iconClass: 'fa-solid fa-vial-circle-check' }
    ],

    categorizeSkill(skill) {
        const s = skill.toLowerCase().trim();
        // UI/UX & Multimedia
        if (/(\b(ui|ux|figma|adobe|photoshop|illustrator|premiere|after effects|animation|wirefram|prototyp|graphic|video|blender|game|unity|motion|visual effects|design system|user flow|user research|product design)\b)/i.test(s) ||
            s.includes('ui/ux') || s.includes('wireframe') || s.includes('prototype') || s.includes('photoshop') || s.includes('illustrator') || s.includes('figma') || s.includes('adobe') || s.includes('animation') || s.includes('motion')) {
            return 'design';
        }
        // Data & AI
        if (/(\b(machine learning|deep learning|nlp|tensorflow|pytorch|scikit|pandas|numpy|data|analytics|power bi|tableau|big data|spark|etl|dashboard|reporting|excel)\b)/i.test(s) ||
            s.includes('data') || s.includes('analytics') || s.includes('learning') || s.includes('bi')) {
            return 'data';
        }
        // Cybersecurity
        if (/(\b(security|firewall|soc|siem|penetration|vulnerability|incident|cissp|ceh|cisco|vpn|devsecops|antivirus|access control|palo alto|fortinet|wireshark|ids|ips)\b)/i.test(s) ||
            s.includes('security') || s.includes('firewall') || s.includes('vpn') || s.includes('soc') || s.includes('siem')) {
            return 'sec';
        }
        // Systems, Cloud & Network (Infra & Support)
        if (/(\b(cloud|aws|azure|gcp|docker|kubernetes|k8s|terraform|ansible|jenkins|ci\/cd|cicd|linux|git|devops|server|active directory|network|routing|switching|dhcp|dns|tcp\/ip|hardware|troubleshooting|helpdesk|backup|windows|cctv|virtualization|vmware|prtg|subnetting|vlan|lan|printer|remote support|ticketing|inventory|customer service|ms office|office 365|powerpoint|clone|ghost)\b)/i.test(s) ||
            s.includes('network') || s.includes('server') || s.includes('troubleshooting') || s.includes('hardware') || s.includes('cloud') || s.includes('docker') || s.includes('kubernetes') || s.includes('linux') || s.includes('helpdesk')) {
            return 'infra';
        }
        // QA & Testing
        if (/(\b(test|selenium|cypress|playwright|postman|qa|junit|pytest|jest|load testing|uat)\b)/i.test(s) ||
            s.includes('test') || s.includes('selenium') || s.includes('qa') || s.includes('postman')) {
            return 'test';
        }
        // Management, Business & System Analysis
        if (/(\b(agile|scrum|jira|trello|project management|sdlc|uml|use case|requirement|business analysis|system analysis|communication|budgeting|risk|coordination|presentation|negotiation|kanban|user story|dfd|er diagram|srs|system architecture|business process|process|project planning|roadmap|stakeholder|vendor|facilitation|documentation|time management|problem solving|market research|continuous improvement|erp)\b)/i.test(s) ||
            s.includes('project') || s.includes('analysis') || s.includes('agile') || s.includes('scrum') || s.includes('jira') || s.includes('management') || s.includes('communication') || s.includes('uml') || s.includes('requirement')) {
            return 'mgmt';
        }
        // Programming & Web Development
        return 'dev';
    },

    render() {
        return `
        <div class="space-y-6 view-transition-in">
            <!-- Header Banner -->
            <div class="glass-card rounded-2xl sm:rounded-3xl p-4 sm:p-6 shadow-sm border-t-4 border-t-rose-500 space-y-4">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div>
                        <h2 class="text-lg sm:text-xl font-black text-slate-900 flex items-center gap-2">
                            <i class="fa-solid fa-layer-group text-rose-600"></i>
                            <span>คลังทักษะไอที</span>
                        </h2>
                        <p class="text-xs text-slate-400 mt-0.5">
                            คลิกเลือกทักษะที่คุณมีเพื่อนำไปค้นหาตำแหน่งงานจริงในตลาด
                        </p>
                    </div>
                    <div class="flex items-center gap-2 self-start sm:self-auto">
                        <button onclick="window.location.hash = '#/matcher'"
                            class="glow-btn-pink px-3.5 py-2 rounded-xl text-xs font-bold flex items-center gap-1.5 cursor-pointer shadow-sm">
                            <i class="fa-solid fa-crosshairs text-[11px]"></i>
                            <span>กลับหน้าค้นหางาน (${AppState.userSkills.length})</span>
                        </button>
                    </div>
                </div>

                <!-- Search Input -->
                <div class="relative pt-1">
                    <input type="text" id="skillSearchInput"
                        placeholder="พิมพ์ค้นหาทักษะ... (เช่น Docker, React, SQL)"
                        value="${ApiClient.escapeHTML(this.searchQuery)}"
                        oninput="SkillsView.onSearchChange(this.value)"
                        class="w-full py-2.5 px-3 pl-9 text-xs sm:text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-rose-500/20 focus:border-rose-500 outline-none bg-white shadow-2xs transition placeholder:text-slate-400">
                    <span class="absolute left-3 top-4 text-slate-400 text-xs">
                        <i class="fa-solid fa-magnifying-glass"></i>
                    </span>
                </div>

                <!-- Category Filters -->
                <div class="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs">
                    ${this.categories.map(cat => `
                        <button onclick="SkillsView.setCategory('${cat.id}')"
                            class="px-3 py-1.5 rounded-xl font-semibold transition-all shrink-0 cursor-pointer flex items-center gap-1.5 text-xs ${this.selectedCategory === cat.id ? 'glow-btn-pink shadow-xs' : 'bg-white hover:bg-rose-50 hover:text-rose-700 text-slate-700 border border-slate-200'}">
                            <i class="${cat.iconClass} text-[11px]"></i>
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
                        <span>รายการทักษะที่ตลาดต้องการ</span>
                        <span id="skillResultCount" class="text-rose-600 font-bold hidden"></span>
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
        // #3: Teardown listener เก่าก่อนเพิ่มใหม่ — ป้องกัน subscriber สะสมทุกครั้งที่ navigate มาหน้านี้
        if (this._unsubSkills) {
            this._unsubSkills();
            this._unsubSkills = null;
        }
        this.renderPills();
        this._unsubSkills = AppState.subscribe('skills', () => this.renderPills());
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
        if (countSpan) {
            if (this.searchQuery) {
                countSpan.innerText = `(พบ ${skills.length} รายการ)`;
                countSpan.classList.remove('hidden');
            } else {
                countSpan.innerText = '';
                countSpan.classList.add('hidden');
            }
        }

        if (skills.length === 0) {
            container.innerHTML = `
                <div class="w-full text-center py-10 text-slate-400 text-sm">
                    <i class="fa-solid fa-magnifying-glass mr-1"></i> ไม่พบทักษะที่ตรงกับเงื่อนไขการค้นหา
                </div>`;
            return;
        }

        // Render all matching market skills (216 clean skills)
        container.innerHTML = skills.map(skill => {
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
