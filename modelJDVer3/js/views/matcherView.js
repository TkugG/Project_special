/**
 * Matcher View: Pure Skill-Based IT Job Recommendation Engine
 * Design: Modern White Theme with Accent Pink (SkillMatch IT - มคอ.2 Curriculum)
 */
window.MatcherView = {
    render() {
        return `
        <div class="space-y-8 view-transition-in">
            <!-- PURE SKILL-BASED SEARCHABLE FORM -->
            <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm space-y-6 border-t-4 border-t-rose-500">

                <div class="border-b border-slate-100 pb-4 flex items-center justify-between flex-wrap gap-3">
                    <div>
                        <div class="flex items-center gap-2.5">
                            <span class="w-9 h-9 rounded-xl bg-rose-100 text-rose-600 flex items-center justify-center font-bold text-sm shadow-2xs">
                                <i class="fa-solid fa-clipboard-list text-base"></i>
                            </span>
                            <h2 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
                                จับคู่ทักษะและสายงานไอที (Skill Matcher)
                            </h2>
                        </div>
                        <p class="text-xs text-slate-500 font-medium mt-1">
                            ระบุทักษะที่คุณมีเพื่อประเมินความพร้อมและค้นหาตำแหน่งงานจริงในตลาดไอทีไทยที่ตรงกับตัวคุณ
                        </p>
                    </div>
                    <button onclick="MatcherView.fillSampleSkills()"
                        class="text-xs glow-btn-secondary px-3.5 py-2 rounded-xl transition font-bold flex items-center gap-2 cursor-pointer shadow-2xs">
                        <i class="fa-solid fa-shuffle text-rose-500"></i>
                        <span>สุ่มตัวอย่างชุดทักษะ</span>
                    </button>
                </div>

                <!-- FIELD 1: Target Career Role -->
                <div class="space-y-2">
                    <div class="flex justify-between items-center text-xs">
                        <label for="roleInput" class="font-bold text-slate-800 text-sm flex items-center gap-2">
                            <i class="fa-solid fa-bullseye text-rose-500"></i>
                            <span>1. สายงานเป้าหมายที่คุณสนใจ</span>
                            <span class="text-slate-400 font-normal text-xs">(ไม่บังคับระบุ)</span>
                        </label>
                        <span class="text-slate-400 font-medium hidden sm:inline">เลือกสายงานเพื่อวิเคราะห์ทักษะที่ต้องพัฒนาเพิ่ม</span>
                    </div>
                    <div class="relative">
                        <input type="text" id="roleInput" list="rolesList"
                            placeholder="พิมพ์หรือเลือกสายงาน... (เช่น นักพัฒนาซอฟต์แวร์, นักออกแบบและพัฒนาเว็บไซต์)"
                            value="${ApiClient.escapeHTML(AppState.selectedRole)}"
                            oninput="AppState.setRole(this.value)"
                            class="w-full p-3.5 pl-10 text-sm font-bold text-slate-900 border border-slate-300 rounded-2xl focus:ring-2 focus:ring-rose-500/30 focus:border-rose-500 outline-none bg-slate-50/50 focus:bg-white shadow-2xs transition placeholder:font-normal placeholder:text-slate-400">
                        <span class="absolute left-3.5 top-4 text-slate-400">
                            <i class="fa-solid fa-briefcase"></i>
                        </span>
                        <datalist id="rolesList"></datalist>
                    </div>

                    <!-- Quick Role Pills -->
                    <div class="flex items-center gap-1.5 flex-wrap pt-1 text-xs">
                        <span class="text-slate-400 font-semibold mr-1">สายงานแนะนำ:</span>
                        <button onclick="MatcherView.selectRole('เจ้าหน้าที่คอมพิวเตอร์ (Computer Officer / IT Support)')"
                            class="px-2.5 py-1 rounded-xl bg-slate-100 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">เจ้าหน้าที่คอมพิวเตอร์</button>
                        <button onclick="MatcherView.selectRole('ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์ (Network Administrator / Engineer)')"
                            class="px-2.5 py-1 rounded-xl bg-slate-100 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">ดูแลระบบเครือข่าย</button>
                        <button onclick="MatcherView.selectRole('นักพัฒนาและออกแบบสื่อผสม (Multimedia Designer & Developer)')"
                            class="px-2.5 py-1 rounded-xl bg-slate-100 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">สื่อผสม & UI/UX</button>
                        <button onclick="MatcherView.selectRole('นักจัดการโครงการสารสนเทศ (IT Project Manager / Coordinator)')"
                            class="px-2.5 py-1 rounded-xl bg-slate-100 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">จัดการโครงการไอที</button>
                        <button onclick="MatcherView.selectRole('นักวิเคราะห์และออกแบบระบบงาน (System Analyst / Business Analyst)')"
                            class="px-2.5 py-1 rounded-xl bg-slate-100 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">นักวิเคราะห์ระบบ</button>
                        <button onclick="MatcherView.selectRole('นักพัฒนาซอฟต์แวร์ (Software Developer / Engineer)')"
                            class="px-2.5 py-1 rounded-xl bg-slate-100 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">นักพัฒนาซอฟต์แวร์</button>
                        <button onclick="MatcherView.selectRole('นักออกแบบและพัฒนาเว็บไซต์ (Web Designer & Developer)')"
                            class="px-2.5 py-1 rounded-xl bg-slate-100 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">พัฒนาเว็บไซต์</button>
                        <button onclick="MatcherView.selectRole('ผู้เชี่ยวชาญด้านเทคโนโลยีสารสนเทศ (Specialized IT Professional)')"
                            class="px-2.5 py-1 rounded-xl bg-slate-100 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">ผู้เชี่ยวชาญไอที</button>
                        <button onclick="MatcherView.selectRole('')"
                            class="px-2 py-1 rounded-xl bg-slate-100 hover:bg-rose-100 hover:text-rose-800 text-slate-400 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">
                            <i class="fa-solid fa-xmark mr-1"></i> ล้างสายงาน
                        </button>
                    </div>
                </div>

                <!-- FIELD 2: Searchable Multi-Select Tag Input -->
                <div class="space-y-3 pt-2">
                    <div class="flex justify-between items-center text-xs">
                        <label class="font-bold text-slate-900 text-sm md:text-base flex items-center gap-2">
                            <i class="fa-solid fa-laptop-code text-rose-500"></i>
                            <span>2. ทักษะของคุณ (Skills Basket)</span>
                            <span class="text-rose-600 font-extrabold">*จำเป็น</span>
                        </label>
                        <div class="flex items-center gap-3">
                            <span id="skillCountBadge"
                                class="text-xs font-black bg-rose-50 text-rose-800 px-3 py-1 rounded-full border border-rose-200 shadow-2xs">
                                <i class="fa-solid fa-layer-group text-rose-600 mr-1"></i> ${AppState.userSkills.length} ทักษะ
                            </span>
                            <button onclick="AppState.clearSkills()"
                                class="text-xs text-rose-600 hover:text-rose-800 font-bold hover:underline cursor-pointer flex items-center gap-1">
                                <i class="fa-solid fa-trash-can"></i> ล้างทั้งหมด
                            </button>
                        </div>
                    </div>

                    <!-- Interactive Tags Display Box -->
                    <div id="skillsTagBox"
                        class="flex flex-wrap gap-2.5 min-h-[90px] max-h-[220px] overflow-y-auto p-4 bg-slate-50/70 rounded-2xl border-2 border-dashed border-slate-200 items-center transition-colors">
                    </div>

                    <!-- Input + Autocomplete Suggestions -->
                    <div class="relative">
                        <div class="flex gap-2">
                            <div class="relative flex-1">
                                <input type="text" id="skillSearchInput"
                                    placeholder="พิมพ์ค้นหาทักษะ... (เช่น Python, HTML5, SQL, Docker, Figma)"
                                    autocomplete="off"
                                    onkeydown="MatcherView.handleInputKeydown(event)"
                                    oninput="MatcherView.onSkillSearchInput(this.value)"
                                    class="w-full p-3.5 pl-10 text-sm font-bold text-slate-900 border border-slate-300 rounded-2xl focus:ring-2 focus:ring-rose-500/30 focus:border-rose-500 outline-none bg-white shadow-2xs transition placeholder:font-normal placeholder:text-slate-400">
                                <span class="absolute left-3.5 top-4 text-slate-400">
                                    <i class="fa-solid fa-magnifying-glass"></i>
                                </span>
                            </div>
                            <button type="button" onclick="MatcherView.addFromInput()"
                                class="glow-btn-pink px-6 py-3.5 rounded-2xl font-bold text-xs sm:text-sm flex items-center gap-2 cursor-pointer shadow-sm">
                                <i class="fa-solid fa-plus"></i>
                                <span>เพิ่ม</span>
                            </button>
                        </div>

                        <!-- Dropdown Suggestions -->
                        <div id="suggestionsDropdown"
                            class="hidden absolute z-30 left-0 right-0 top-full mt-2 bg-white rounded-2xl shadow-xl border border-slate-200 max-h-60 overflow-y-auto p-2 space-y-1">
                        </div>
                    </div>

                    <!-- Common IT Skills Quick Select Buttons -->
                    <div class="pt-2">
                        <div class="flex items-center justify-between text-xs text-slate-500 mb-2 font-medium">
                            <span><i class="fa-solid fa-wand-magic-sparkles text-rose-500 mr-1"></i> แนะนำทักษะยอดนิยม (คลิกเพื่อเพิ่มทันที):</span>
                            <span class="text-slate-400">คลังทักษะไอทีมาตรฐาน 1,600+ คำ</span>
                        </div>
                        <div class="flex flex-wrap gap-1.5 text-xs">
                            ${this.renderQuickSkillButtons()}
                        </div>
                    </div>
                </div>

                <!-- SUBMIT ACTION BUTTON -->
                <div class="pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
                    <div class="text-xs text-slate-500 flex items-center gap-2">
                        <i class="fa-solid fa-circle-info text-rose-500"></i>
                        <span>ระบบใช้โมเดล Calibrated Machine Learning 3 มิติฟีเจอร์</span>
                    </div>
                    <button id="submitBtn" onclick="MatcherView.handleRecommend()"
                        class="w-full sm:w-auto glow-btn-pink px-8 py-3.5 rounded-2xl font-black text-sm tracking-wide flex items-center justify-center gap-2.5 cursor-pointer shadow-md transition-all active:scale-95">
                        <i class="fa-solid fa-magnifying-glass-chart text-base"></i>
                        <span>วิเคราะห์ความพร้อม & ค้นหาตำแหน่งงาน</span>
                    </button>
                </div>

            </div>

            <!-- RESULTS CONTAINER (Dual-Section) -->
            <div id="resultsWrapper">
                <!-- Recommendations will be rendered here dynamically -->
            </div>
        </div>
        `;
    },

    renderQuickSkillButtons() {
        const quickSkills = [
            "python", "javascript", "react", "html5", "css3", "sql", "node.js", "c#", ".net", "java",
            "docker", "git", "figma", "ui/ux", "linux", "cisco", "tcp/ip", "agile", "jira", "uml", "php", "wordpress"
        ];
        return quickSkills.map(s => `
            <button onclick="MatcherView.addQuickSkill('${s}')"
                class="px-2.5 py-1 rounded-xl bg-slate-100 hover:bg-rose-100 hover:text-rose-800 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer flex items-center gap-1">
                <i class="fa-solid fa-plus text-[10px] text-rose-400"></i> ${s}
            </button>
        `).join('');
    },

    onMount() {
        this.renderTags();
        this.populateRolesDatalist();
        // #2: ย้าย global click listener ไปอยู่ใน app.js แล้ว
        // ไม่ลงทะเบียนซ้ำที่นี่เพื่อป้องกัน memory leak ทุก route change

        if (AppState.recommendations) {
            this.renderResults(AppState.recommendations);
        }
    },

    populateRolesDatalist() {
        const datalist = document.getElementById('rolesList');
        if (datalist && AppState.rolesList) {
            datalist.innerHTML = AppState.rolesList.map(r => `<option value="${ApiClient.escapeHTML(r)}">`).join('');
        }
    },

    renderTags() {
        const box = document.getElementById('skillsTagBox');
        const countBadge = document.getElementById('skillCountBadge');
        if (!box) return;

        if (AppState.userSkills.length === 0) {
            box.innerHTML = `
                <div class="w-full text-center py-4 text-slate-400 text-xs flex flex-col items-center justify-center gap-1.5">
                    <i class="fa-solid fa-tags text-2xl text-slate-300"></i>
                    <span>ยังไม่มีทักษะในตะกร้าของคุณ (พิมพ์ค้นหาหรือคลิกปุ่มทักษะด้านล่างเพื่อเพิ่ม)</span>
                </div>
            `;
            if (countBadge) countBadge.innerHTML = `<i class="fa-solid fa-layer-group text-rose-600 mr-1"></i> 0 ทักษะ`;
            return;
        }

        box.innerHTML = AppState.userSkills.map((skill, idx) => `
            <span class="inline-flex items-center gap-1.5 bg-white text-rose-800 border border-rose-200/90 px-3 py-1.5 rounded-xl font-bold text-xs shadow-2xs transition-all hover:border-rose-400 animate__animated animate__fadeIn">
                <i class="fa-solid fa-check text-rose-500 text-[11px]"></i>
                <span>${ApiClient.escapeHTML(skill)}</span>
                <button type="button" onclick="MatcherView.removeSkill(${idx})" class="text-rose-400 hover:text-rose-700 ml-1 cursor-pointer focus:outline-none">
                    <i class="fa-solid fa-xmark text-xs"></i>
                </button>
            </span>
        `).join('');

        if (countBadge) {
            countBadge.innerHTML = `<i class="fa-solid fa-layer-group text-rose-600 mr-1"></i> ${AppState.userSkills.length} ทักษะ`;
        }
    },

    selectRole(roleName) {
        AppState.setRole(roleName);
        const input = document.getElementById('roleInput');
        if (input) input.value = roleName;
    },

    addQuickSkill(skill) {
        AppState.addSkill(skill);
        this.renderTags();
    },

    removeSkill(index) {
        AppState.removeSkill(index);
        this.renderTags();
    },

    addFromInput() {
        const input = document.getElementById('skillSearchInput');
        if (!input) return;
        const val = input.value.trim();
        if (val) {
            AppState.addSkill(val);
            input.value = '';
            this.renderTags();
            const dropdown = document.getElementById('suggestionsDropdown');
            if (dropdown) dropdown.classList.add('hidden');
        }
    },

    handleInputKeydown(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            this.addFromInput();
        }
    },

    onSkillSearchInput(query) {
        const dropdown = document.getElementById('suggestionsDropdown');
        if (!dropdown) return;

        const q = query.trim().toLowerCase();
        if (!q || q.length < 1) {
            dropdown.classList.add('hidden');
            return;
        }

        const matches = (AppState.skillsVocabulary || []).filter(s =>
            s.toLowerCase().includes(q) && !AppState.userSkills.includes(s)
        ).slice(0, 10);

        if (matches.length === 0) {
            dropdown.innerHTML = `
                <div class="p-3 text-xs text-slate-400 text-center flex items-center justify-center gap-2">
                    <i class="fa-solid fa-magnifying-glass text-slate-300"></i>
                    <span>ไม่พบทักษะที่ตรงกับ "${ApiClient.escapeHTML(query)}"</span>
                </div>
            `;
            dropdown.classList.remove('hidden');
            return;
        }

        dropdown.innerHTML = matches.map(m => `
            <div onclick="MatcherView.selectSuggestedSkill('${ApiClient.escapeHTML(m)}')"
                class="px-3.5 py-2.5 hover:bg-rose-50 rounded-xl cursor-pointer flex items-center justify-between text-xs transition">
                <span class="font-bold text-slate-800 flex items-center gap-2">
                    <i class="fa-solid fa-code text-rose-500 text-[11px]"></i>
                    ${ApiClient.escapeHTML(m)}
                </span>
                <span class="text-[10px] font-bold text-rose-600 bg-rose-100/70 px-2 py-0.5 rounded-md">+ เพิ่ม</span>
            </div>
        `).join('');

        dropdown.classList.remove('hidden');
    },

    selectSuggestedSkill(skill) {
        AppState.addSkill(skill);
        this.renderTags();
        const input = document.getElementById('skillSearchInput');
        if (input) input.value = '';
        const dropdown = document.getElementById('suggestionsDropdown');
        if (dropdown) dropdown.classList.add('hidden');
    },

    fillSampleSkills() {
        const samples = [
            {
                role: "นักออกแบบและพัฒนาเว็บไซต์ (Web Designer & Developer)",
                skills: ["html5", "css3", "javascript", "php", "wordpress", "tailwind", "responsive web design", "mysql"]
            },
            {
                role: "นักพัฒนาซอฟต์แวร์ (Software Developer / Engineer)",
                skills: ["python", "fastapi", "react", "sql", "docker", "git", "rest api", "oop"]
            },
            {
                role: "เจ้าหน้าที่คอมพิวเตอร์ (Computer Officer / IT Support)",
                skills: ["windows", "linux", "hardware", "troubleshooting", "basic networking", "helpdesk", "active directory"]
            },
            {
                role: "ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์ (Network Administrator / Engineer)",
                skills: ["cisco", "tcp/ip", "routing", "switching", "firewall", "vpn", "linux server"]
            },
            {
                role: "นักพัฒนาและออกแบบสื่อผสม (Multimedia Designer & Developer)",
                skills: ["ui/ux", "figma", "adobe xd", "photoshop", "illustrator", "html/css", "wireframing"]
            },
            {
                role: "นักวิเคราะห์และออกแบบระบบงาน (System Analyst / Business Analyst)",
                skills: ["system analysis", "uml", "dfd", "er diagram", "sql", "database design", "requirement gathering"]
            }
        ];
        const randomSample = samples[Math.floor(Math.random() * samples.length)];
        this.selectRole(randomSample.role);
        AppState.setUserSkills(randomSample.skills);
        this.renderTags();
    },

    async handleRecommend() {
        if (AppState.userSkills.length === 0 && !AppState.selectedRole) {
            Swal.fire({
                icon: 'warning',
                title: 'กรุณาระบุข้อมูล',
                text: 'โปรดเลือกสายงานเป้าหมายตามหลักสูตร มคอ.2 หรือเพิ่มทักษะที่คุณมีอย่างน้อย 1 ทักษะครับ',
                confirmButtonText: 'ตกลง',
                confirmButtonColor: '#e11d48',
                customClass: { popup: 'rounded-3xl p-6 shadow-xl', confirmButton: 'glow-btn-pink rounded-xl px-6 py-2.5 font-bold text-xs' }
            });
            return;
        }

        const btn = document.getElementById('submitBtn');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin text-base"></i> <span>กำลังวิเคราะห์ด้วย Machine Learning...</span>`;
        }

        try {
            const data = await ApiClient.getRecommendations(AppState.selectedRole, AppState.userSkills);
            AppState.setRecommendations(data);
            this.renderResults(data);

            const resElem = document.getElementById('resultsWrapper');
            if (resElem) {
                resElem.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        } catch (err) {
            console.error(err);
            Swal.fire({
                icon: 'error',
                title: 'เกิดข้อผิดพลาด',
                text: err.message || 'ไม่สามารถเชื่อมต่อกับระบบ AI หลังบ้านได้',
                confirmButtonColor: '#e11d48'
            });
        } finally {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = `<i class="fa-solid fa-magnifying-glass-chart text-base"></i> <span>วิเคราะห์ความพร้อม & ค้นหาตำแหน่งงาน</span>`;
            }
        }
    },

    renderResults(data) {
        const resultsWrapper = document.getElementById('resultsWrapper');
        if (!resultsWrapper) return;

        if (!data || data.status === 'error') {
            resultsWrapper.innerHTML = `
                <div class="glass-card p-8 rounded-3xl text-center space-y-3">
                    <i class="fa-solid fa-triangle-exclamation text-3xl text-amber-500"></i>
                    <h3 class="text-lg font-bold text-slate-800">ไม่พบผลลัพธ์ที่ตรงกัน</h3>
                    <p class="text-xs text-slate-500">${ApiClient.escapeHTML(data?.message || 'กรุณาลองเพิ่มทักษะอื่นๆ หรือเลือกสายงานใหม่ครับ')}</p>
                </div>
            `;
            return;
        }

        const targetAnalysis = data.target_career_analysis;
        const skillMatches = data.skill_matched_recommendations || [];

        let html = '';

        // SECTION 1: TARGET CURRICULUM CAREER ANALYSIS (มคอ.2)
        if (targetAnalysis) {
            let targetGaugeColor = "bg-gradient-to-r from-emerald-500 to-teal-600";
            let targetTextColor = "text-rose-600";
            if (targetAnalysis.score < 50) {
                targetGaugeColor = "bg-gradient-to-r from-amber-400 to-orange-500";
                targetTextColor = "text-amber-600";
            } else if (targetAnalysis.score < 80) {
                targetGaugeColor = "bg-gradient-to-r from-pink-500 to-rose-600";
                targetTextColor = "text-rose-600";
            }

            const targetStatus = JobComponents.getReadinessStatus(targetAnalysis.skill_readiness);

            html += `
            <div class="space-y-3 mb-8 animate__animated animate__fadeInDown">
                <div class="flex items-center justify-between px-1 flex-wrap gap-2">
                    <div>
                        <span class="text-xs font-black tracking-wider uppercase text-rose-700 bg-rose-50 border border-rose-200 px-3 py-1 rounded-xl inline-flex items-center gap-1.5 shadow-2xs">
                            <i class="fa-solid fa-bullseye text-rose-500"></i> ส่วนที่ 1: วิเคราะห์ความพร้อมในสายงานเป้าหมาย (Career Readiness Analysis)
                        </span>
                        <h3 class="text-xl sm:text-2xl font-black text-slate-900 mt-2 flex items-center gap-2 flex-wrap">
                            <i class="fa-solid fa-crosshairs text-rose-600"></i> สายงานเป้าหมาย: 
                            <span class="text-rose-600 font-black">${ApiClient.escapeHTML(targetAnalysis.target_role_title)}</span>
                        </h3>
                        <p class="text-xs text-slate-500 font-medium">ประเมินสมรรถนะเทียบกับทักษะหลักประจำสายงาน พร้อมชี้เป้า Skill Gap เพื่อเตรียมความพร้อมสู่ตลาดงาน</p>
                    </div>
                    <span class="inline-flex items-center gap-1.5 text-xs font-extrabold ${targetStatus.badgeBg} px-3.5 py-1.5 rounded-2xl border shadow-2xs">
                        <i class="${targetStatus.iconClass}"></i> ความพร้อม ${targetAnalysis.skill_readiness}% • ${targetStatus.text}
                    </span>
                </div>

                <!-- Target Career Highlight Card -->
                <div class="glass-card-highlight p-6 md:p-8 rounded-3xl space-y-4">
                    
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                        <div>
                            <div class="flex items-center gap-2 flex-wrap">
                                <h4 class="text-xl font-black text-slate-900">${ApiClient.escapeHTML(targetAnalysis.title)}</h4>
                                <span class="text-xs font-extrabold text-rose-700 bg-rose-100 border border-rose-300 px-2.5 py-0.5 rounded-lg flex items-center gap-1">
                                    <i class="fa-solid fa-bullseye"></i> สายงานเป้าหมาย
                                </span>
                            </div>
                            
                            <div class="flex flex-wrap items-center gap-1.5 mt-2">
                                <span class="inline-flex items-center gap-1.5 text-[11px] font-extrabold bg-white text-slate-700 border border-slate-200 px-2.5 py-0.5 rounded-lg shadow-2xs">
                                    <i class="fa-solid fa-building text-slate-400"></i> ${ApiClient.escapeHTML(targetAnalysis.company || "องค์กรไอทีในไทย")}
                                </span>
                                <span class="inline-flex items-center gap-1.5 text-[11px] font-extrabold bg-white text-slate-700 border border-slate-200 px-2.5 py-0.5 rounded-lg shadow-2xs">
                                    <i class="fa-solid fa-location-dot text-rose-400"></i> ${ApiClient.escapeHTML(targetAnalysis.province || "กรุงเทพมหานคร")}
                                </span>
                            </div>
                        </div>
                        
                        <div class="flex items-center gap-2 shrink-0 self-start sm:self-auto">
                            <div class="flex flex-col items-end ${targetStatus.pillBg} px-4 py-2 rounded-2xl border shadow-2xs">
                                <span class="text-[10px] font-extrabold uppercase tracking-wider">${targetStatus.shortText}</span>
                                <span class="text-lg font-black font-english">${targetAnalysis.skill_readiness}%</span>
                            </div>
                            <div class="bg-white px-4 py-2 rounded-2xl border border-rose-200 shadow-xs text-right">
                                <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">TQF Readiness</div>
                                <span class="text-2xl font-black ${targetTextColor} font-english">${targetAnalysis.skill_readiness}<span class="text-sm text-slate-400 font-normal">%</span></span>
                            </div>
                        </div>
                    </div>

                    <!-- Progress Bar -->
                    <div class="w-full bg-slate-100 rounded-full h-3 overflow-hidden p-0.5 border border-slate-200/80">
                        <div class="${targetGaugeColor} h-full rounded-full transition-all duration-800 ease-out shadow-xs" style="width: 0%" data-progress-bar data-target-width="${targetAnalysis.skill_readiness}%"></div>
                    </div>

                    <!-- Description & Responsibilities -->
                    <div class="bg-white/95 p-4 rounded-2xl border border-slate-200/90 shadow-2xs space-y-2 text-xs">
                        <div class="font-extrabold text-slate-900 flex items-center gap-1.5 text-xs text-rose-700">
                            <i class="fa-solid fa-book-bookmark"></i>
                            <span>คำอธิบายสมรรถนะตามหลักสูตร มคอ.2</span>
                        </div>
                        <p class="text-slate-600 leading-relaxed">${ApiClient.escapeHTML(targetAnalysis.target_role_desc || "")}</p>
                    </div>

                    <!-- Matched Core Skills vs Skill Gap Roadmap -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-1 text-xs">
                        <div class="bg-emerald-50/70 p-5 rounded-2xl border border-emerald-200 space-y-3">
                            <span class="font-bold text-emerald-950 flex items-center gap-2 text-xs">
                                <i class="fa-solid fa-circle-check text-emerald-600"></i>
                                ทักษะที่คุณมีตรงกับหลักสูตร (${targetAnalysis.matched_skills.length}/${targetAnalysis.total_skills_count})
                            </span>
                            <div class="flex flex-wrap gap-1.5">
                                ${targetAnalysis.matched_skills.length > 0
                    ? targetAnalysis.matched_skills.map(s => `<span class="bg-white text-emerald-950 px-2.5 py-1 rounded-lg border border-emerald-300 font-bold text-xs shadow-2xs">${ApiClient.escapeHTML(s)}</span>`).join('')
                    : '<span class="text-slate-400 italic text-xs">ยังไม่มีทักษะแกนหลักที่ตรงกับหลักสูตร</span>'}
                            </div>
                        </div>

                        <div class="bg-rose-50/70 p-5 rounded-2xl border border-rose-200 space-y-3">
                            <span class="font-bold text-rose-950 flex items-center gap-2 text-xs">
                                <i class="fa-solid fa-lightbulb text-rose-600"></i>
                                ทักษะที่ควรศึกษาเพิ่มตาม มคอ.2 (Skill Gap Roadmap) (${targetAnalysis.missing_skills.length})
                            </span>
                            <div class="flex flex-wrap gap-1.5">
                                ${targetAnalysis.missing_skills.length > 0
                    ? targetAnalysis.missing_skills.map(s => `<span class="bg-white text-rose-950 px-2.5 py-1 rounded-lg border border-rose-300 font-bold text-xs shadow-2xs">${ApiClient.escapeHTML(s)}</span>`).join('')
                    : '<span class="text-emerald-800 font-extrabold text-xs flex items-center gap-1.5"><i class="fa-solid fa-star text-amber-500"></i> คุณมีทักษะครอบคลุมสมบูรณ์ตามเกณฑ์หลักสูตร!</span>'}
                            </div>
                        </div>
                    </div>

                    <!-- Footer -->
                    <div class="flex items-center justify-between gap-2 pt-2 border-t border-rose-100/80 flex-wrap">
                        <div class="text-[11px] text-slate-400 font-medium flex items-center gap-1.5">
                            <i class="fa-solid fa-graduation-cap text-rose-500"></i>
                            <span>มาตรฐานสายงานหลักสูตร มคอ.2 สาขา IT</span>
                        </div>
                        <div>
                            <button
                                data-job-title="${ApiClient.escapeHTML(targetAnalysis.title)}"
                                data-missing-skills="${ApiClient.escapeHTML(JSON.stringify(targetAnalysis.missing_skills || []))}"
                                onclick="JobComponents.showPrepGuide(this.dataset.jobTitle, JSON.parse(this.dataset.missingSkills))"
                                class="glow-btn-pink px-4 py-2 rounded-xl text-xs font-extrabold transition-all flex items-center gap-2 cursor-pointer shadow-sm">
                                <i class="fa-solid fa-rocket"></i>
                                <span>ดูแนวทางเตรียมตัว</span>
                            </button>
                        </div>
                    </div>

                </div>
            </div>
            `;
        }

        // SECTION 2: TOP MATCHED THAI JOB RECOMMENDATIONS
        html += `
        <div class="space-y-4 animate__animated animate__fadeInUp">
            <div class="flex items-center justify-between px-1 flex-wrap gap-2">
                <div>
                    <span class="text-xs font-black tracking-wider uppercase text-rose-700 bg-rose-50 border border-rose-200 px-3 py-1 rounded-xl inline-flex items-center gap-1.5 shadow-2xs">
                        <i class="fa-solid fa-award text-rose-500"></i> ส่วนที่ 2: ตำแหน่งงานจริงในไทยที่ตรงกับทักษะ (Top Thai Job Matches)
                    </span>
                    <h3 class="text-xl sm:text-2xl font-black text-slate-900 mt-2 flex items-center gap-2">
                        <i class="fa-solid fa-trophy text-amber-500"></i> อันดับตำแหน่งงานที่เหมาะสมที่สุด (Top 5 Matches)
                    </h3>
                    <p class="text-xs text-slate-500 font-medium">คำนวณด้วย Calibrated Logistic Regression จากประกาศรับสมัครงานจริงในไทย</p>
                </div>
                <span class="text-xs font-extrabold bg-rose-50 text-rose-800 px-3.5 py-1.5 rounded-2xl border border-rose-200 shadow-2xs flex items-center gap-1.5">
                    <i class="fa-solid fa-briefcase"></i> พบ ${skillMatches.length} ตำแหน่งที่แนะนำ
                </span>
            </div>
        `;

        html += skillMatches.map((job, index) => {
            let gaugeColor = "bg-gradient-to-r from-rose-500 to-pink-500";
            let textColor = "text-rose-600";

            if (job.score < 50) {
                gaugeColor = "bg-gradient-to-r from-amber-400 to-orange-500";
                textColor = "text-amber-600";
            } else if (job.score < 80) {
                gaugeColor = "bg-gradient-to-r from-pink-500 to-rose-600";
                textColor = "text-rose-600";
            }

            const totalReq = (job.matched_skills.length + job.missing_skills.length);
            const readiness = totalReq > 0 ? Math.round((job.matched_skills.length / totalReq) * 100) : 0;
            const readinessStatus = JobComponents.getReadinessStatus(readiness);

            return `
            <div class="glass-card hover-lift p-5 md:p-6 rounded-3xl space-y-4" style="animation-delay: ${index * 0.08}s">
                
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div>
                        <div class="flex items-center gap-2.5 flex-wrap">
                            <span class="w-7 h-7 rounded-xl bg-gradient-to-tr from-rose-500 to-pink-600 text-white font-black text-xs inline-flex items-center justify-center shadow-xs">${index + 1}</span>
                            <h4 class="text-lg font-black text-slate-900">${ApiClient.escapeHTML(job.title)}</h4>
                            <span class="text-[11px] font-bold text-rose-700 bg-rose-50 border border-rose-200 px-2 py-0.5 rounded-lg">
                                <i class="fa-solid fa-layer-group text-[10px] text-rose-400 mr-1"></i>${ApiClient.escapeHTML(job.curriculum_role_title || "สายงานไอที")}
                            </span>
                        </div>

                        <div class="flex flex-wrap items-center gap-1.5 mt-2 ml-9">
                            <span class="inline-flex items-center gap-1.5 text-[11px] font-extrabold bg-slate-50 text-slate-700 border border-slate-200 px-2.5 py-0.5 rounded-lg shadow-2xs">
                                <i class="fa-solid fa-building text-slate-400"></i> ${ApiClient.escapeHTML(job.company || "องค์กรไอทีในไทย")}
                            </span>
                            <span class="inline-flex items-center gap-1.5 text-[11px] font-extrabold bg-slate-50 text-slate-700 border border-slate-200 px-2.5 py-0.5 rounded-lg shadow-2xs">
                                <i class="fa-solid fa-location-dot text-rose-400"></i> ${ApiClient.escapeHTML(job.province || "กรุงเทพมหานคร")}
                            </span>
                            <span class="inline-flex items-center gap-1.5 text-[11px] font-extrabold bg-slate-50 text-slate-700 border border-slate-200 px-2.5 py-0.5 rounded-lg shadow-2xs">
                                <i class="fa-solid fa-graduation-cap text-slate-400"></i> ${ApiClient.escapeHTML(job.experience_level || "Entry-Level / เด็กจบใหม่")}
                            </span>
                        </div>
                    </div>
                    
                    <div class="flex items-center gap-2 shrink-0 self-start sm:self-auto">
                        <div class="flex flex-col items-end ${readinessStatus.pillBg} px-3 py-1.5 rounded-2xl border shadow-2xs">
                            <span class="text-[10px] font-extrabold uppercase tracking-wider">${readinessStatus.shortText}</span>
                            <span class="text-base font-black font-english">${readiness}%</span>
                        </div>
                        <div class="flex items-center gap-2 bg-slate-50/80 px-3.5 py-1.5 rounded-2xl border border-slate-200 shadow-2xs">
                            <div class="text-right">
                                <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Match Score</div>
                                <span class="text-2xl font-black ${textColor} font-english">${job.score}<span class="text-sm text-slate-400 font-normal">%</span></span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Progress Bar -->
                <div class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
                    <div class="${gaugeColor} h-full rounded-full transition-all duration-800 ease-out" style="width: 0%" data-progress-bar data-target-width="${job.score}%"></div>
                </div>

                <!-- Responsibilities -->
                <div class="bg-slate-50/80 p-3.5 md:p-4 rounded-2xl border border-slate-200/90 space-y-2 text-xs">
                    <div class="font-extrabold text-slate-900 flex items-center gap-1.5 text-xs text-rose-700">
                        <i class="fa-solid fa-list-check"></i>
                        <span>หน้าที่และความรับผิดชอบหลัก (Responsibilities)</span>
                    </div>
                    <ul class="space-y-1.5 text-slate-600 font-medium pl-1">
                        ${JobComponents.renderResponsibilities(job.responsibilities_list || job.responsibilities)}
                    </ul>
                </div>

                <!-- Matched Skills vs Missing Skills -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-5 pt-1 text-xs">
                    <div class="bg-emerald-50/50 p-4 rounded-2xl border border-emerald-200 space-y-2.5">
                        <span class="font-bold text-emerald-950 flex items-center gap-2 text-xs">
                            <i class="fa-solid fa-circle-check text-emerald-600"></i>
                            ทักษะที่คุณมีตรงกับงานนี้ (${job.matched_skills.length})
                        </span>
                        <div class="flex flex-wrap gap-1.5">
                            ${job.matched_skills.length > 0
                    ? job.matched_skills.map(s => `<span class="bg-white text-emerald-950 px-2.5 py-1 rounded-lg border border-emerald-300 font-bold text-xs shadow-2xs">${ApiClient.escapeHTML(s)}</span>`).join('')
                    : '<span class="text-slate-400 italic text-xs">ยังไม่มีทักษะที่ตรงตัวโดยตรง</span>'}
                        </div>
                    </div>

                    <div class="bg-rose-50/50 p-4 rounded-2xl border border-rose-200 space-y-2.5">
                        <span class="font-bold text-rose-950 flex items-center gap-2 text-xs">
                            <i class="fa-solid fa-lightbulb text-rose-600"></i>
                            ทักษะที่ควรศึกษาเพิ่ม (Skill Gap Roadmap) (${job.missing_skills.length})
                        </span>
                        <div class="flex flex-wrap gap-1.5">
                            ${job.missing_skills.length > 0
                    ? job.missing_skills.map(s => `<span class="bg-white text-rose-950 px-2.5 py-1 rounded-lg border border-rose-300 font-bold text-xs shadow-2xs">${ApiClient.escapeHTML(s)}</span>`).join('')
                    : '<span class="text-emerald-800 font-extrabold text-xs flex items-center gap-1.5"><i class="fa-solid fa-star text-amber-500"></i> คุณสมบัติครบถ้วนทุกทักษะสำหรับตำแหน่งนี้!</span>'}
                        </div>
                    </div>
                </div>

                <!-- Footer -->
                <div class="flex items-center justify-between gap-2 pt-2 border-t border-slate-100 flex-wrap">
                    <div class="text-[11px] text-slate-400 font-medium flex items-center gap-1.5">
                        <i class="fa-solid fa-database text-slate-400"></i>
                        <span>อ้างอิง: ข้อมูลตลาดแรงงานไอทีไทย (Blognone Jobs)</span>
                    </div>
                    <div>
                        <button
                            data-job-title="${ApiClient.escapeHTML(job.title)}"
                            data-missing-skills="${ApiClient.escapeHTML(JSON.stringify(job.missing_skills || []))}"
                            onclick="JobComponents.showPrepGuide(this.dataset.jobTitle, JSON.parse(this.dataset.missingSkills))"
                            class="glow-btn-pink px-4 py-2 rounded-xl text-xs font-extrabold transition-all flex items-center gap-2 cursor-pointer shadow-sm">
                            <i class="fa-solid fa-rocket"></i>
                            <span>ดูแนวทางเตรียมตัว</span>
                        </button>
                    </div>
                </div>

            </div>
            `;
        }).join("");

        html += `</div>`;
        resultsWrapper.innerHTML = html;

        setTimeout(() => {
            const bars = document.querySelectorAll('#resultsWrapper [data-progress-bar]');
            bars.forEach(bar => {
                bar.style.width = bar.getAttribute('data-target-width');
            });
        }, 50);
    }
};
