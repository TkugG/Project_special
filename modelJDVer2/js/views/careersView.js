/**
 * Careers View: Comprehensive IT Career Exploration & Roadmaps
 * Design: Modern White Theme with Accent Pink & Rich Visual Hierarchy (SkillMatch IT)
 */
window.CareersView = {
    currentCategory: 'all',
    searchQuery: '',

    categories: [
        { id: 'all', label: 'ทุกสายงาน (All)', iconClass: 'fa-solid fa-layer-group' },
        { id: 'curriculum', label: 'สายงานไอทีหลัก (Core Tracks)', iconClass: 'fa-solid fa-graduation-cap' },
        { id: 'dev', label: 'Software & Web', iconClass: 'fa-solid fa-code' },
        { id: 'infra', label: 'Network & Cloud', iconClass: 'fa-solid fa-server' },
        { id: 'design', label: 'Design & Multimedia', iconClass: 'fa-solid fa-palette' },
        { id: 'mgmt', label: 'Management & Data', iconClass: 'fa-solid fa-chart-line' }
    ],

    roleDetails: [
        // --- 1. นักพัฒนาซอฟต์แวร์ ---
        {
            id: '8.6',
            title: 'นักพัฒนาซอฟต์แวร์ (Software Developer / Engineer)',
            en_title: 'Software Developer / Engineer',
            cat: 'curriculum',
            category_group: 'dev',
            icon: 'fa-solid fa-code',
            gradient: 'from-emerald-500 to-teal-600',
            bgLight: 'bg-emerald-50 text-emerald-700 border-emerald-200',
            exp: 'Entry-Level / เด็กจบใหม่ (0-2 ปี)',
            skills: ['python', 'java', 'c#', '.net', 'javascript', 'typescript', 'react', 'node.js', 'sql', 'rest api', 'git', 'docker'],
            desc: 'ออกแบบ เขียนโปรแกรม พัฒนาเว็บเซอร์วิส ไมโครเซอร์วิส และแอปพลิเคชันบนแพลตฟอร์มต่างๆ ตามมาตรฐานวิศวกรรมซอฟต์แวร์',
            highlights: ['Web & API Services', 'Backend Architecture', 'Clean Code & OOP']
        },

        // --- 2. นักออกแบบและพัฒนาเว็บไซต์ ---
        {
            id: '8.7',
            title: 'นักออกแบบและพัฒนาเว็บไซต์ (Web Designer & Developer)',
            en_title: 'Web Designer & Developer',
            cat: 'curriculum',
            category_group: 'dev',
            icon: 'fa-solid fa-laptop-code',
            gradient: 'from-pink-500 to-rose-600',
            bgLight: 'bg-rose-50 text-rose-700 border-rose-200',
            exp: 'Entry-Level / เด็กจบใหม่ (0-1 ปี)',
            skills: ['html5', 'css3', 'javascript', 'responsive web design', 'tailwind', 'bootstrap', 'wordpress', 'php', 'mysql', 'rest api'],
            desc: 'ออกแบบและจัดทำเว็บไซต์ เว็บแอปพลิเคชันที่รองรับการแสดงผลทุกอุปกรณ์ (Responsive) และพัฒนาระบบจัดการเนื้อหา (CMS)',
            highlights: ['Responsive UI', 'WordPress & CMS', 'Frontend Integration']
        },

        // --- 3. ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์ ---
        {
            id: '8.2',
            title: 'ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์ (Network Administrator / Engineer)',
            en_title: 'Network Administrator / Engineer',
            cat: 'curriculum',
            category_group: 'infra',
            icon: 'fa-solid fa-network-wired',
            gradient: 'from-blue-500 to-cyan-600',
            bgLight: 'bg-blue-50 text-blue-700 border-blue-200',
            exp: 'Entry-Level / เด็กจบใหม่ (0-2 ปี)',
            skills: ['tcp/ip', 'cisco', 'routing', 'switching', 'firewall', 'vpn', 'dns', 'dhcp', 'linux server', 'windows server', 'network security'],
            desc: 'ออกแบบ ติดตั้ง กำหนดค่า และบริหารจัดการระบบเครือข่ายคอมพิวเตอร์ ความมั่นคงปลอดภัย และเครื่องแม่ข่าย (Server)',
            highlights: ['Cisco & Routing', 'Firewall & VPN', 'Server Management']
        },

        // --- 4. เจ้าหน้าที่คอมพิวเตอร์ ---
        {
            id: '8.1',
            title: 'เจ้าหน้าที่คอมพิวเตอร์ (Computer Officer / IT Support)',
            en_title: 'Computer Officer / IT Support',
            cat: 'curriculum',
            category_group: 'infra',
            icon: 'fa-solid fa-headset',
            gradient: 'from-amber-500 to-orange-600',
            bgLight: 'bg-amber-50 text-amber-800 border-amber-200',
            exp: 'Entry-Level / เด็กจบใหม่ (0-1 ปี)',
            skills: ['windows', 'linux', 'hardware', 'troubleshooting', 'basic networking', 'helpdesk', 'active directory', 'backup', 'ms office'],
            desc: 'ติดตั้ง บำรุงรักษา แก้ไขปัญหาฮาร์ดแวร์ ซอฟต์แวร์ และให้บริการสนับสนุนงานเทคโนโลยีสารสนเทศแก่ผู้ใช้งานในองค์กร',
            highlights: ['Hardware Repair', 'Helpdesk Support', 'System Maintenance']
        },

        // --- 5. นักพัฒนาและออกแบบสื่อผสม ---
        {
            id: '8.3',
            title: 'นักพัฒนาและออกแบบสื่อผสม (Multimedia Designer & Developer)',
            en_title: 'Multimedia Designer & Developer',
            cat: 'curriculum',
            category_group: 'design',
            icon: 'fa-solid fa-palette',
            gradient: 'from-purple-500 to-violet-600',
            bgLight: 'bg-purple-50 text-purple-700 border-purple-200',
            exp: 'Entry-Level / เด็กจบใหม่ (0-2 ปี)',
            skills: ['ui/ux', 'figma', 'adobe xd', 'photoshop', 'illustrator', 'premiere pro', 'after effects', '3d animation', 'unity', 'html/css'],
            desc: 'ออกแบบและพัฒนาสื่อดิจิทัล สื่อมัลติมีเดีย ภาพกราฟิก แอนิเมชัน วิดีโอ ตัวต้นแบบส่วนต่อประสานผู้ใช้ (UI/UX) และเกม',
            highlights: ['UI/UX & Figma', 'Motion Graphics', 'Interactive Media & Games']
        },

        // --- 6. นักวิเคราะห์และออกแบบระบบงาน ---
        {
            id: '8.5',
            title: 'นักวิเคราะห์และออกแบบระบบงาน (System Analyst / Business Analyst)',
            en_title: 'System Analyst / Business Analyst',
            cat: 'curriculum',
            category_group: 'mgmt',
            icon: 'fa-solid fa-chart-pie',
            gradient: 'from-indigo-500 to-blue-600',
            bgLight: 'bg-indigo-50 text-indigo-700 border-indigo-200',
            exp: 'Entry-Level / เด็กจบใหม่ (0-2 ปี)',
            skills: ['system analysis', 'business analysis', 'uml', 'use case', 'dfd', 'er diagram', 'database design', 'sql', 'requirement gathering', 'wireframing'],
            desc: 'รวบรวมและวิเคราะห์ความต้องการทางธุรกิจ ออกแบบผังกระบวนการ สถาปัตยกรรมระบบ ฐานข้อมูล และจัดทำข้อกำหนดระบบ (SRS)',
            highlights: ['Requirement Gathering', 'UML / DFD / ERD', 'SRS Documentation']
        },

        // --- 7. นักจัดการโครงการสารสนเทศ ---
        {
            id: '8.4',
            title: 'นักจัดการโครงการสารสนเทศ (IT Project Manager / Coordinator)',
            en_title: 'IT Project Manager / Coordinator',
            cat: 'curriculum',
            category_group: 'mgmt',
            icon: 'fa-solid fa-diagram-project',
            gradient: 'from-orange-500 to-red-600',
            bgLight: 'bg-orange-50 text-orange-700 border-orange-200',
            exp: 'Entry-Level / เด็กจบใหม่ (0-2 ปี)',
            skills: ['agile', 'scrum', 'jira', 'project management', 'trello', 'communication', 'risk management', 'sdlc', 'budgeting'],
            desc: 'วางแผน ประสานงาน บริหารจัดการทรัพยากร ติดตามความก้าวหน้า และควบคุมคุณภาพการส่งมอบโครงการซอฟต์แวร์',
            highlights: ['Agile / Scrum', 'Jira Project Tracking', 'Team Coordination']
        },

        // --- 8. ผู้เชี่ยวชาญด้านเทคโนโลยีสารสนเทศ ---
        {
            id: '8.8',
            title: 'ผู้เชี่ยวชาญด้านเทคโนโลยีสารสนเทศ (Specialized IT Professional)',
            en_title: 'Specialized IT Professional',
            cat: 'curriculum',
            category_group: 'mgmt',
            icon: 'fa-solid fa-brain',
            gradient: 'from-fuchsia-500 to-pink-600',
            bgLight: 'bg-fuchsia-50 text-fuchsia-700 border-fuchsia-200',
            exp: 'Entry-Level / มีประสบการณ์ (1-3 ปี)',
            skills: ['machine learning', 'deep learning', 'nlp', 'cybersecurity', 'cloud architecture', 'big data', 'data science', 'python'],
            desc: 'งานเฉพาะทางด้านเทคโนโลยีขั้นสูง เช่น ปัญญาประดิษฐ์ (AI), วิทยาการข้อมูล (Data Science), หรือความมั่นคงปลอดภัยไซเบอร์',
            highlights: ['AI & Machine Learning', 'Cybersecurity SOC', 'Cloud Architecture']
        }
    ],

    render() {
        return `
        <div class="space-y-8 view-transition-in">
            <!-- Header Hero Banner -->
            <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm border-t-4 border-t-rose-500 space-y-5">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <span class="text-xs font-black tracking-wider uppercase text-rose-700 bg-rose-50 border border-rose-200 px-3 py-1 rounded-xl inline-flex items-center gap-1.5 shadow-2xs">
                            <i class="fa-solid fa-compass text-rose-500"></i> สำรวจเส้นทางอาชีพไอที
                        </span>
                        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2 flex items-center gap-2.5">
                            <i class="fa-solid fa-briefcase text-rose-600"></i> IT Career Explorer & Roadmaps
                        </h2>
                        <p class="text-xs sm:text-sm text-slate-500 font-medium mt-1">
                            ค้นพบโอกาส บทบาทหน้าที่ความรับผิดชอบ และชุดทักษะสำคัญของแต่ละสายงานในอุตสาหกรรมเทคโนโลยี
                        </p>
                    </div>

                    <!-- Quick Stats Pill -->
                    <div class="flex items-center gap-2 bg-slate-50 p-2 rounded-2xl border border-slate-200 shrink-0">
                        <div class="px-3 py-1 text-center">
                            <div class="text-lg font-black text-rose-600 font-english">${this.roleDetails.length}</div>
                            <div class="text-[10px] font-bold text-slate-400">สายงานหลัก</div>
                        </div>
                        <div class="w-px h-8 bg-slate-200"></div>
                        <div class="px-3 py-1 text-center">
                            <div class="text-lg font-black text-slate-800 font-english">100%</div>
                            <div class="text-[10px] font-bold text-slate-400">ตลาดงานไทย</div>
                        </div>
                    </div>
                </div>

                <!-- Search & Filters -->
                <div class="space-y-3 pt-1">
                    <div class="relative">
                        <input type="text" id="careerSearchInput"
                            placeholder="พิมพ์ค้นหาสายงานหรือทักษะ... (เช่น เว็บไซต์, Python, React, Cisco, Figma, SA)"
                            value="${ApiClient.escapeHTML(this.searchQuery)}"
                            oninput="CareersView.onSearchChange(this.value)"
                            class="w-full p-3.5 pl-11 text-sm border border-slate-300 rounded-2xl focus:ring-2 focus:ring-rose-500/30 focus:border-rose-500 outline-none bg-white shadow-2xs transition placeholder:text-slate-400">
                        <span class="absolute left-4 top-4 text-slate-400">
                            <i class="fa-solid fa-magnifying-glass"></i>
                        </span>
                    </div>

                    <!-- Category Tabs -->
                    <div class="flex items-center gap-2 overflow-x-auto pb-1 text-xs">
                        ${this.categories.map(cat => `
                            <button onclick="CareersView.setCategory('${cat.id}')"
                                class="px-4 py-2.5 rounded-2xl font-bold transition-all shrink-0 cursor-pointer flex items-center gap-2 ${this.currentCategory === cat.id ? 'glow-btn-pink shadow-md' : 'bg-white hover:bg-rose-50 hover:text-rose-700 text-slate-700 border border-slate-200'}">
                                <i class="${cat.iconClass}"></i>
                                <span>${cat.label}</span>
                            </button>
                        `).join('')}
                    </div>
                </div>
            </div>

            <!-- Career Cards Grid (Modern Rich Cards) -->
            <div id="careerGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
                <!-- Dynamically rendered -->
            </div>
        </div>
        `;
    },

    onMount() {
        this.renderCards();
    },

    setCategory(catId) {
        this.currentCategory = catId;
        const app = document.getElementById('router-view');
        if (app) app.innerHTML = this.render();
        this.renderCards();
    },

    onSearchChange(val) {
        this.searchQuery = val.trim().toLowerCase();
        this.renderCards();
    },

    getFilteredRoles() {
        return this.roleDetails.filter(role => {
            // #5: แก้ไข — 'curriculum' tab ต้องตรวจ role.cat ด้วย ไม่ใช่แค่ short-circuit true
            const matchesCat = this.currentCategory === 'all' ||
                (this.currentCategory === 'curriculum' && role.cat === 'curriculum') ||
                role.category_group === this.currentCategory;
            const matchesQuery = !this.searchQuery ||
                role.title.toLowerCase().includes(this.searchQuery) ||
                role.desc.toLowerCase().includes(this.searchQuery) ||
                role.skills.some(s => s.toLowerCase().includes(this.searchQuery)) ||
                (role.highlights && role.highlights.some(h => h.toLowerCase().includes(this.searchQuery)));
            return matchesCat && matchesQuery;
        });
    },

    renderCards() {
        const grid = document.getElementById("careerGrid");
        if (!grid) return;

        const roles = this.getFilteredRoles();

        if (roles.length === 0) {
            grid.innerHTML = `
                <div class="col-span-full glass-card p-12 rounded-3xl text-center text-slate-500 space-y-3">
                    <div class="text-4xl text-slate-300">
                        <i class="fa-solid fa-magnifying-glass"></i>
                    </div>
                    <div class="font-bold text-base text-slate-700">ไม่พบสายงานที่ตรงกับคำค้นหา</div>
                    <div class="text-xs text-slate-400">ลองค้นหาด้วยคำอื่น เช่น เว็บไซต์, Python, React, Cisco, Figma, UI/UX</div>
                </div>`;
            return;
        }

        grid.innerHTML = roles.map(role => `
            <div class="glass-card rounded-3xl p-6 shadow-sm hover-lift border border-slate-200/90 flex flex-col justify-between space-y-5 transition-all">
                
                <!-- Card Top Header -->
                <div class="space-y-4">
                    <div class="flex items-start gap-3.5">
                        <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr ${role.gradient} flex items-center justify-center text-white text-xl shadow-md shrink-0">
                            <i class="${role.icon}"></i>
                        </div>
                        <div class="flex-1 min-w-0">
                            <h3 class="font-black text-base md:text-lg text-slate-900 leading-snug">${ApiClient.escapeHTML(role.title)}</h3>
                            <div class="flex items-center gap-2 mt-1 flex-wrap">
                                <span class="inline-flex items-center gap-1.5 text-[10px] font-extrabold ${role.bgLight} border px-2 py-0.5 rounded-lg shadow-2xs">
                                    <i class="fa-solid fa-briefcase text-[10px]"></i> ${ApiClient.escapeHTML(role.exp)}
                                </span>
                                <span class="text-[10px] font-bold text-slate-400 font-english">${role.skills.length} Core Skills</span>
                            </div>
                        </div>
                    </div>

                    <!-- Role Description -->
                    <p class="text-xs text-slate-600 font-medium leading-relaxed bg-slate-50/70 p-3.5 rounded-2xl border border-slate-100">
                        ${ApiClient.escapeHTML(role.desc)}
                    </p>

                    <!-- Key Focus Areas / Highlights -->
                    ${role.highlights ? `
                    <div class="flex items-center gap-1.5 flex-wrap">
                        <span class="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider mr-1">จุดเด่นงาน:</span>
                        ${role.highlights.map(h => `
                            <span class="text-[10px] font-bold bg-white text-slate-700 px-2 py-0.5 rounded-md border border-slate-200 shadow-2xs">${ApiClient.escapeHTML(h)}</span>
                        `).join('')}
                    </div>
                    ` : ''}

                    <!-- Core Skills Badges -->
                    <div class="space-y-2 pt-1">
                        <div class="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider flex items-center justify-between">
                            <span>ทักษะสำคัญประจำสายงาน:</span>
                        </div>
                        <div class="flex flex-wrap gap-1.5 max-h-24 overflow-y-auto p-0.5">
                            ${role.skills.map(s => `
                                <span class="text-[11px] font-bold bg-white text-slate-800 px-2.5 py-1 rounded-xl border border-slate-200 shadow-2xs hover:border-rose-300 transition-colors">${ApiClient.escapeHTML(s)}</span>
                            `).join('')}
                        </div>
                    </div>
                </div>

                <!-- Card Action Footer -->
                <div class="pt-4 border-t border-slate-100 flex items-center justify-between gap-3">
                    <button
                        data-role-title="${ApiClient.escapeHTML(role.title)}"
                        data-role-skills="${ApiClient.escapeHTML(JSON.stringify(role.skills))}"
                        onclick="CareersView.selectForMatch(this.dataset.roleTitle, JSON.parse(this.dataset.roleSkills))"
                        class="w-full glow-btn-pink text-xs font-black py-3 px-4 rounded-2xl transition cursor-pointer flex items-center justify-center gap-2 shadow-sm active:scale-95">
                        <i class="fa-solid fa-crosshairs"></i>
                        <span>นำสายงานและทักษะนี้ไปค้นหางาน</span>
                    </button>
                </div>

            </div>
        `).join('');
    },

    selectForMatch(roleTitle, suggestedSkills) {
        AppState.setRole(roleTitle);
        if (suggestedSkills && suggestedSkills.length > 0) {
            suggestedSkills.forEach(s => AppState.addSkill(s));
        }
        window.location.hash = '#/matcher';
        Swal.fire({
            icon: 'success',
            title: `เลือกสายงานเรียบร้อย`,
            text: `ระบบนำเข้าสายงานและทักษะแนะนำสำหรับ "${roleTitle}" ไปยังแบบฟอร์มแล้วครับ`,
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 2500,
            timerProgressBar: true,
            customClass: { popup: 'rounded-2xl shadow-xl text-sm border border-rose-100' }
        });
    }
};
