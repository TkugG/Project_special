/**
 * Matcher View: Clean, Mobile-First IT Skill & Job Matcher
 * Design: Modern White Theme with Accent Pink (SkillMatch IT)
 */
window.MatcherView = {
    render() {
        return `
        <div class="space-y-6 view-transition-in">
            <!-- SKILL MATCHING CARD -->
            <div class="glass-card rounded-2xl sm:rounded-3xl p-4 sm:p-6 md:p-8 shadow-sm space-y-4 sm:space-y-5 border-t-4 border-t-rose-500">

                <!-- Header & Quick Demo Presets -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
                    <div>
                        <h2 class="text-lg sm:text-xl font-black text-slate-900 flex items-center gap-2">
                            <i class="fa-solid fa-bullseye text-rose-500"></i>
                            <span>ค้นหาตำแหน่งงานตามทักษะ</span>
                        </h2>
                        <p class="text-xs text-slate-400 mt-0.5">เลือกหรือพิมพ์ทักษะเพื่อดูสายงานและตำแหน่งที่เหมาะสม</p>
                    </div>

                    <!-- Quick Demo Presets for Mobile & Live Defense -->
                    <div class="flex items-center gap-1.5 flex-wrap">
                        <span class="text-[11px] font-bold text-slate-400 mr-0.5">ตัวอย่าง:</span>
                        <button type="button" onclick="MatcherView.fillPreset('web')"
                            class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-rose-50 hover:text-rose-700 text-slate-700 text-xs font-semibold border border-slate-200 active:scale-95 transition cursor-pointer">
                            💻 Web
                        </button>
                        <button type="button" onclick="MatcherView.fillPreset('network')"
                            class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-rose-50 hover:text-rose-700 text-slate-700 text-xs font-semibold border border-slate-200 active:scale-95 transition cursor-pointer">
                            ⚙️ Network
                        </button>
                        <button type="button" onclick="MatcherView.fillPreset('design')"
                            class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-rose-50 hover:text-rose-700 text-slate-700 text-xs font-semibold border border-slate-200 active:scale-95 transition cursor-pointer">
                            🎨 UI/UX
                        </button>
                        <button type="button" onclick="MatcherView.fillPreset('data')"
                            class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-rose-50 hover:text-rose-700 text-slate-700 text-xs font-semibold border border-slate-200 active:scale-95 transition cursor-pointer">
                            📊 Data/AI
                        </button>
                        <button type="button" onclick="MatcherView.fillPreset('random')"
                            class="px-2.5 py-1 rounded-lg bg-rose-50 hover:bg-rose-100 text-rose-700 text-xs font-semibold border border-rose-200 active:scale-95 transition cursor-pointer">
                            🎲 สุ่ม
                        </button>
                    </div>
                </div>

                <!-- FIELD 1: Target Career Role (Filter Selector Dropdown) -->
                <div class="space-y-1.5">
                    <div class="flex justify-between items-center text-xs">
                        <label for="roleSelect" class="font-bold text-slate-700 flex items-center gap-1.5">
                            <i class="fa-solid fa-briefcase text-slate-400"></i>
                            <span>สายงานที่สนใจ (ตัวกรองเป้าหมาย)</span>
                            <span class="text-slate-400 font-normal">(ไม่บังคับ)</span>
                        </label>
                        ${AppState.selectedRole ? `
                            <button type="button" onclick="MatcherView.selectRole('')" class="text-rose-600 hover:underline text-[11px] font-semibold cursor-pointer">
                                <i class="fa-solid fa-xmark mr-0.5"></i> ล้างตัวเลือก
                            </button>
                        ` : ''}
                    </div>
                    <div class="relative">
                        <select id="roleSelect"
                            onchange="MatcherView.selectRole(this.value)"
                            class="w-full py-2.5 px-3 pl-9 pr-8 text-xs sm:text-sm font-semibold text-slate-900 border border-slate-200 rounded-xl focus:ring-2 focus:ring-rose-500/20 focus:border-rose-500 outline-none bg-slate-50/60 focus:bg-white transition cursor-pointer appearance-none">
                            <option value="">-- ให้ระบบวิเคราะห์อัตโนมัติ (แนะนำทุกสายงาน) --</option>
                            <option value="8.1" ${AppState.selectedRole === '8.1' ? 'selected' : ''}>Track 8.1: เจ้าหน้าที่คอมพิวเตอร์ (Computer Officer / IT Support)</option>
                            <option value="8.2" ${AppState.selectedRole === '8.2' ? 'selected' : ''}>Track 8.2: ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์ (Network Administrator / Engineer)</option>
                            <option value="8.3" ${AppState.selectedRole === '8.3' ? 'selected' : ''}>Track 8.3: นักพัฒนาและออกแบบสื่อผสม (Multimedia Designer & Developer)</option>
                            <option value="8.4" ${AppState.selectedRole === '8.4' ? 'selected' : ''}>Track 8.4: นักจัดการโครงการสารสนเทศ (IT Project Manager / Coordinator)</option>
                            <option value="8.5" ${AppState.selectedRole === '8.5' ? 'selected' : ''}>Track 8.5: นักวิเคราะห์และออกแบบระบบงาน (System Analyst / Business Analyst)</option>
                            <option value="8.6" ${AppState.selectedRole === '8.6' ? 'selected' : ''}>Track 8.6: นักพัฒนาซอฟต์แวร์ (Software Developer / Engineer)</option>
                            <option value="8.7" ${AppState.selectedRole === '8.7' ? 'selected' : ''}>Track 8.7: นักออกแบบและพัฒนาเว็บไซต์ (Web Designer & Developer)</option>
                            <option value="8.8" ${AppState.selectedRole === '8.8' ? 'selected' : ''}>Track 8.8: ผู้เชี่ยวชาญด้านเทคโนโลยีสารสนเทศ (Specialized IT / AI / Cloud)</option>
                        </select>
                        <span class="absolute left-3 top-3 text-slate-400 text-xs pointer-events-none">
                            <i class="fa-solid fa-filter text-rose-500"></i>
                        </span>
                        <span class="absolute right-3 top-3.5 text-slate-400 text-xs pointer-events-none">
                            <i class="fa-solid fa-chevron-down text-[10px]"></i>
                        </span>
                    </div>
                </div>

                <!-- FIELD 2: Skills Basket -->
                <div class="space-y-2 pt-1">
                    <div class="flex justify-between items-center text-xs">
                        <label class="font-bold text-slate-900 text-sm flex items-center gap-1.5">
                            <i class="fa-solid fa-laptop-code text-rose-500"></i>
                            <span>ทักษะของคุณ</span>
                            <span class="text-rose-500 font-bold">*</span>
                        </label>
                        <div class="flex items-center gap-2">
                            <span id="skillCountBadge" class="text-xs font-bold text-rose-700 bg-rose-50 border border-rose-200 px-2.5 py-0.5 rounded-full">
                                ${AppState.userSkills.length} ทักษะ
                            </span>
                            <button onclick="MatcherView.clearAllSkills()" class="text-slate-400 hover:text-rose-600 text-xs font-semibold cursor-pointer">
                                ล้างทั้งหมด
                            </button>
                        </div>
                    </div>

                    <!-- Selected Skills Display Box -->
                    <div id="skillsTagBox"
                        class="flex flex-wrap gap-1.5 min-h-[56px] max-h-[150px] overflow-y-auto p-2.5 bg-slate-50/70 rounded-xl border border-slate-200 items-center">
                    </div>

                    <!-- Skill Search Input + Add Button -->
                    <div class="relative">
                        <div class="flex gap-1.5">
                            <div class="relative flex-1">
                                <input type="text" id="skillSearchInput"
                                    placeholder="พิมพ์ทักษะ... (เช่น Python, React, SQL, Docker)"
                                    autocomplete="off"
                                    onkeydown="MatcherView.handleInputKeydown(event)"
                                    oninput="MatcherView.onSkillSearchInput(this.value)"
                                    class="w-full py-2.5 px-3 pl-9 text-xs sm:text-sm font-semibold text-slate-900 border border-slate-300 rounded-xl focus:ring-2 focus:ring-rose-500/20 focus:border-rose-500 outline-none bg-white shadow-2xs transition placeholder:font-normal placeholder:text-slate-400">
                                <span class="absolute left-3 top-3 text-slate-400 text-xs">
                                    <i class="fa-solid fa-plus"></i>
                                </span>
                            </div>
                            <button type="button" onclick="MatcherView.addFromInput()"
                                class="glow-btn-pink px-4 sm:px-5 py-2.5 rounded-xl font-bold text-xs sm:text-sm flex items-center gap-1 cursor-pointer shrink-0">
                                <span>เพิ่ม</span>
                            </button>
                        </div>

                        <!-- Dropdown Suggestions -->
                        <div id="suggestionsDropdown"
                            class="hidden absolute z-30 left-0 right-0 top-full mt-1 bg-white rounded-xl shadow-lg border border-slate-200 max-h-52 overflow-y-auto p-1.5 space-y-0.5">
                        </div>
                    </div>

                    <!-- Popular Quick Skill Tags -->
                    <div class="pt-1">
                        <div class="text-[11px] font-semibold text-slate-400 mb-1.5">ทักษะยอดนิยม:</div>
                        <div class="flex flex-wrap gap-1 text-xs">
                            ${this.renderQuickSkillButtons()}
                        </div>
                    </div>
                </div>

                <!-- SUBMIT BUTTON -->
                <div class="pt-2">
                    <button id="submitBtn" onclick="MatcherView.handleRecommend()"
                        class="w-full glow-btn-pink py-3 sm:py-3.5 rounded-xl font-bold text-sm sm:text-base flex items-center justify-center gap-2 cursor-pointer shadow-md transition active:scale-95">
                        <i class="fa-solid fa-magnifying-glass text-sm"></i>
                        <span>ค้นหาตำแหน่งงาน</span>
                    </button>
                </div>

            </div>

            <!-- RESULTS CONTAINER -->
            <div id="resultsWrapper">
                ${this.renderInitialEmptyState()}
            </div>
        </div>
        `;
    },

    renderQuickSkillButtons() {
        const quickSkills = [
            "python", "javascript", "react", "html5", "css3", "sql", "node.js", ".net", "c#", "docker", "git", "figma", "linux", "cisco"
        ];
        return quickSkills.map(s => `
            <button onclick="MatcherView.addQuickSkill('${s}')"
                class="px-2 py-0.5 rounded-lg bg-slate-100 hover:bg-rose-50 hover:text-rose-700 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer flex items-center gap-1">
                <i class="fa-solid fa-plus text-[9px] text-rose-400"></i> ${s}
            </button>
        `).join('');
    },

    renderInitialEmptyState() {
        return `
        <div class="text-center py-8 px-4 text-slate-400 space-y-2">
            <div class="w-12 h-12 mx-auto rounded-2xl bg-rose-50 text-rose-500 flex items-center justify-center text-xl shadow-2xs">
                <i class="fa-solid fa-crosshairs"></i>
            </div>
            <p class="text-xs sm:text-sm font-semibold text-slate-600">
                เลือกทักษะด้านบน แล้วกด <span class="text-rose-600 font-bold">"ค้นหาตำแหน่งงาน"</span>
            </p>
            <p class="text-[11px] text-slate-400">
                ระบบจะวิเคราะห์สายงานที่เหมาะสมพร้อมแนะนำตำแหน่งงานทันที
            </p>
        </div>
        `;
    },

    _unsubSkills: null,

    onMount() {
        if (this._unsubSkills) {
            this._unsubSkills();
            this._unsubSkills = null;
        }
        this._unsubSkills = AppState.subscribe('skills', () => {
            this.renderTags();
        });

        this.renderTags();

        if (AppState.recommendations) {
            this.renderResults(AppState.recommendations);
        }
    },

    renderTags() {
        const box = document.getElementById('skillsTagBox');
        const countBadge = document.getElementById('skillCountBadge');
        if (!box) return;

        if (AppState.userSkills.length === 0) {
            box.innerHTML = `
                <div class="w-full text-center py-2 text-slate-400 text-xs flex items-center justify-center gap-1.5">
                    <i class="fa-solid fa-tags text-slate-300"></i>
                    <span>ยังไม่ได้เลือกทักษะ (คลิกปุ่มตัวอย่างหรือพิมพ์ค้นหาด้านล่าง)</span>
                </div>
            `;
            if (countBadge) countBadge.innerText = `0 ทักษะ`;
            return;
        }

        box.innerHTML = AppState.userSkills.map((skill, idx) => `
            <span class="inline-flex items-center gap-1 bg-white text-rose-800 border border-rose-200 px-2.5 py-1 rounded-lg font-semibold text-xs shadow-2xs transition-all hover:border-rose-300 animate__animated animate__fadeIn">
                <span>${ApiClient.escapeHTML(skill)}</span>
                <button type="button" onclick="MatcherView.removeSkill(${idx})" class="text-rose-400 hover:text-rose-700 ml-0.5 cursor-pointer focus:outline-none">
                    <i class="fa-solid fa-xmark text-[10px]"></i>
                </button>
            </span>
        `).join('');

        if (countBadge) {
            countBadge.innerText = `${AppState.userSkills.length} ทักษะ`;
        }
    },

    clearAllSkills() {
        AppState.clearSkills();
        this.renderTags();
        const resultsWrapper = document.getElementById('resultsWrapper');
        if (resultsWrapper) {
            resultsWrapper.innerHTML = this.renderInitialEmptyState();
        }
        AppState.setResults(null);
    },

    clearSkills() {
        this.clearAllSkills();
    },

    selectRole(roleVal) {
        let matchedId = (roleVal || '').trim();
        if (matchedId && AppState.curriculumRoles) {
            const found = AppState.curriculumRoles.find(r => r.id === matchedId || r.title === matchedId || matchedId.includes(r.id));
            if (found) matchedId = found.id;
        }
        AppState.setRole(matchedId);
        const select = document.getElementById('roleSelect');
        if (select) select.value = matchedId;
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
        if (!val) return;

        // รองรับการพิมพ์หลายทักษะคั่นด้วยจุลภาค เช่น "python, docker, sql"
        const tokens = val.split(/[,;\n]+/).map(t => t.trim()).filter(Boolean);
        const validSkills = AppState.allSkills || [];
        let addedCount = 0;
        let invalidTokens = [];

        for (const token of tokens) {
            const tLower = token.toLowerCase();
            const exactMatch = validSkills.find(s => s.toLowerCase() === tLower);
            if (exactMatch) {
                if (AppState.addSkill(exactMatch)) addedCount++;
            } else {
                const partialMatches = validSkills.filter(s =>
                    s.toLowerCase().includes(tLower) && !AppState.userSkills.includes(s.toLowerCase())
                );
                if (partialMatches.length > 0) {
                    if (AppState.addSkill(partialMatches[0])) addedCount++;
                } else {
                    invalidTokens.push(token);
                }
            }
        }

        if (invalidTokens.length > 0) {
            Swal.fire({
                icon: 'warning',
                title: 'ไม่พบทักษะในระบบ',
                text: `คำว่า "${invalidTokens.join(', ')}" ไม่ใช่ทักษะไอทีในคลังข้อมูล กรุณาเลือกทักษะที่ถูกต้องครับ`,
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3500,
                timerProgressBar: true,
                customClass: { popup: 'rounded-xl shadow-lg text-xs' }
            });
        }

        if (addedCount > 0) {
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
        ).slice(0, 8);

        if (matches.length === 0) {
            dropdown.innerHTML = `
                <div class="p-2.5 text-xs text-slate-400 text-center">
                    ไม่พบทักษะที่ตรงกับ "${ApiClient.escapeHTML(query)}"
                </div>
            `;
            dropdown.classList.remove('hidden');
            return;
        }

        dropdown.innerHTML = matches.map(m => `
            <div onclick="MatcherView.selectSuggestedSkill('${ApiClient.escapeHTML(m)}')"
                class="px-3 py-2 hover:bg-rose-50 rounded-lg cursor-pointer flex items-center justify-between text-xs transition">
                <span class="font-semibold text-slate-800">${ApiClient.escapeHTML(m)}</span>
                <span class="text-[10px] font-bold text-rose-600 bg-rose-100/70 px-1.5 py-0.5 rounded">+ เพิ่ม</span>
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

    fillPreset(type) {
        let skills = [];
        let role = '';
        if (type === 'web') {
            skills = ['html5', 'css3', 'javascript', 'react', 'tailwind', 'git'];
            role = 'นักออกแบบและพัฒนาเว็บไซต์ (Web Designer & Developer)';
        } else if (type === 'network') {
            skills = ['cisco', 'tcp/ip', 'routing', 'switching', 'firewall', 'linux'];
            role = 'ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์ (Network Administrator / Engineer)';
        } else if (type === 'design') {
            skills = ['figma', 'ui/ux', 'photoshop', 'illustrator', 'premiere pro', 'after effects'];
            role = 'นักพัฒนาและออกแบบสื่อผสม (Multimedia Designer & Developer)';
        } else if (type === 'data') {
            skills = ['python', 'sql', 'machine learning', 'pandas', 'data analysis'];
            role = 'ผู้เชี่ยวชาญด้านเทคโนโลยีสารสนเทศ (Specialized IT Professional)';
        } else {
            this.fillSampleSkills();
            return;
        }
        this.selectRole(role);
        AppState.setUserSkills(skills);
        this.renderTags();
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
                skills: ["ui/ux", "figma", "photoshop", "illustrator", "premiere pro", "3d animation", "unity"]
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
                text: 'กรุณาเพิ่มทักษะที่คุณมีอย่างน้อย 1 ทักษะครับ',
                confirmButtonText: 'ตกลง',
                confirmButtonColor: '#e11d48',
                customClass: { popup: 'rounded-2xl p-5 shadow-xl', confirmButton: 'glow-btn-pink rounded-xl px-5 py-2 font-bold text-xs' }
            });
            return;
        }

        const btn = document.getElementById('submitBtn');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin text-sm"></i> <span>กำลังวิเคราะห์...</span>`;
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
                text: err.message || 'ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้',
                confirmButtonColor: '#e11d48'
            });
        } finally {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = `<i class="fa-solid fa-magnifying-glass text-sm"></i> <span>ค้นหาตำแหน่งงาน</span>`;
            }
        }
    },

    renderResults(data) {
        const resultsWrapper = document.getElementById('resultsWrapper');
        if (!resultsWrapper) return;

        if (!data || data.status === 'error') {
            resultsWrapper.innerHTML = `
                <div class="glass-card p-6 rounded-2xl text-center space-y-2">
                    <i class="fa-solid fa-triangle-exclamation text-2xl text-amber-500"></i>
                    <h3 class="text-base font-bold text-slate-800">ไม่พบผลลัพธ์ที่ตรงกัน</h3>
                    <p class="text-xs text-slate-500">${ApiClient.escapeHTML(data?.message || 'กรุณาลองเพิ่มทักษะอื่นๆ หรือเลือกสายงานใหม่ครับ')}</p>
                </div>
            `;
            return;
        }

        const targetAnalysis = data.target_career_analysis;
        const skillMatches = data.skill_matched_recommendations || [];

        let html = '';

        // SECTION 1: TARGET CAREER
        if (targetAnalysis) {
            const roleTheme = JobComponents.getRoleTheme(targetAnalysis.target_role_id);
            const targetStatus = JobComponents.getReadinessStatus(targetAnalysis.skill_readiness);

            html += `
            <div class="relative bg-white border-2 ${roleTheme.cardBorder} p-4 sm:p-5 rounded-2xl sm:rounded-3xl shadow-sm space-y-3.5 mb-6 animate__animated animate__fadeInDown overflow-hidden transition-all ${roleTheme.cardBg}">
                <!-- Top Accent Gradient Bar -->
                <div class="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r ${roleTheme.gradient}"></div>

                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div class="flex items-start gap-3">
                        <!-- Role Icon Avatar (matching Careers View) -->
                        <div class="w-11 h-11 sm:w-12 sm:h-12 rounded-2xl bg-gradient-to-tr ${roleTheme.gradient} flex items-center justify-center text-white text-lg sm:text-xl shadow-md shrink-0">
                            <i class="${roleTheme.icon}"></i>
                        </div>
                        <div>
                            <div class="flex flex-wrap items-center gap-1.5">
                                <span class="text-[11px] font-extrabold ${roleTheme.badgeBg} px-2.5 py-0.5 rounded-lg inline-flex items-center gap-1.5 border">
                                    <span>Track ${targetAnalysis.target_role_id}</span>
                                    <span class="opacity-40">|</span>
                                    <span>${roleTheme.tagLabel}</span>
                                </span>
                                <span class="text-[10px] font-bold text-slate-500 bg-white/90 border border-slate-200 px-2 py-0.5 rounded-md shadow-2xs">
                                    ${AppState.selectedRole ? '<i class="fa-solid fa-filter text-rose-500 mr-0.5"></i> เป้าหมายที่คุณเลือก' : '<i class="fa-solid fa-wand-magic-sparkles text-amber-500 mr-0.5"></i> AI วิเคราะห์อัตโนมัติ'}
                                </span>
                            </div>
                            <h3 class="text-base sm:text-xl font-black text-slate-900 mt-1">
                                ${ApiClient.escapeHTML(targetAnalysis.target_role_title)}
                            </h3>
                            <p class="text-[11px] text-slate-500 font-english mt-0.5">
                                ${ApiClient.escapeHTML(targetAnalysis.target_role_en || '')}
                            </p>
                        </div>
                    </div>
                    <div class="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center gap-1.5 self-stretch sm:self-auto pt-2 sm:pt-0 border-t sm:border-t-0 border-slate-100">
                        <span class="text-xs font-black ${targetStatus.badgeBg} px-3 py-1 rounded-xl border flex items-center gap-1.5 shadow-2xs">
                            <i class="${targetStatus.iconClass}"></i>
                            <span>ความพร้อม ${targetAnalysis.skill_readiness}%</span>
                        </span>
                        <span class="text-[11px] font-bold ${targetStatus.textColor}">
                            สถานะ: ${targetStatus.text}
                        </span>
                    </div>
                </div>

                <!-- Progress Bar -->
                <div class="space-y-1">
                    <div class="flex justify-between text-[11px] font-semibold text-slate-500">
                        <span>ความพร้อมของทักษะแกนหลักประจำสายงาน (Core Competencies)</span>
                        <span class="font-bold text-slate-700">${targetAnalysis.matched_skills.length} / ${targetAnalysis.total_skills_count} ทักษะ</span>
                    </div>
                    <div class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden p-0.5 border border-slate-200/60">
                        <div class="${roleTheme.barGradient} h-full rounded-full transition-all duration-800 shadow-xs" style="width: 0%" data-progress-bar data-target-width="${targetAnalysis.skill_readiness}%"></div>
                    </div>
                </div>

                <!-- Matched vs Missing Core Skills -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs pt-1">
                    <div class="bg-emerald-50/80 p-3.5 rounded-2xl border border-emerald-200/90 space-y-2">
                        <div class="font-bold text-emerald-950 flex items-center justify-between text-xs">
                            <span class="flex items-center gap-1.5">
                                <i class="fa-solid fa-circle-check text-emerald-600"></i>
                                <span>ทักษะแกนที่คุณมี (${targetAnalysis.matched_skills.length})</span>
                            </span>
                            <span class="text-[10px] bg-emerald-200/70 text-emerald-900 font-bold px-2 py-0.5 rounded-full">พร้อมแล้ว</span>
                        </div>
                        <div class="flex flex-wrap gap-1.5">
                            ${targetAnalysis.matched_skills.length > 0
                                ? targetAnalysis.matched_skills.map(s => `<span class="bg-white text-emerald-950 px-2.5 py-1 rounded-lg border border-emerald-200 font-bold text-[11px] shadow-2xs">${ApiClient.escapeHTML(s)}</span>`).join('')
                                : '<span class="text-slate-400 text-[11px] italic py-0.5">ยังไม่มีทักษะแกนหลักที่ตรงกัน</span>'}
                        </div>
                    </div>

                    <div class="bg-rose-50/80 p-3.5 rounded-2xl border border-rose-200/90 space-y-2">
                        <div class="font-bold text-rose-950 flex items-center justify-between text-xs">
                            <span class="flex items-center gap-1.5">
                                <i class="fa-solid fa-lightbulb text-rose-600"></i>
                                <span>ทักษะแกนที่ควรศึกษาเพิ่ม (${targetAnalysis.missing_skills.length})</span>
                            </span>
                            <span class="text-[10px] bg-rose-200/70 text-rose-900 font-bold px-2 py-0.5 rounded-full">Skill Gap</span>
                        </div>
                        <div class="flex flex-wrap gap-1.5">
                            ${targetAnalysis.missing_skills.length > 0
                                ? targetAnalysis.missing_skills.map(s => `<span class="bg-white text-rose-950 px-2.5 py-1 rounded-lg border border-rose-200 font-semibold text-[11px] shadow-2xs">${ApiClient.escapeHTML(s)}</span>`).join('')
                                : '<span class="text-emerald-700 font-bold text-[11px]">🎉 ยอดเยี่ยม! คุณมีทักษะครบถ้วนตามเกณฑ์</span>'}
                        </div>
                    </div>
                </div>
            </div>
            `;
        }

        // SECTION 2: JOB MATCHES
        html += `
        <div class="space-y-3 animate__animated animate__fadeInUp">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 px-1">
                <div>
                    <h3 class="text-base sm:text-lg font-black text-slate-900 flex items-center gap-1.5">
                        <i class="fa-solid fa-building text-rose-500"></i>
                        <span>ประกาศรับสมัครงานจริงในตลาด (${skillMatches.length})</span>
                    </h3>
                    <p class="text-xs text-slate-400">ตำแหน่งงานที่มีทักษะตรงกับคุณมากที่สุด</p>
                </div>
            </div>
        `;

        html += skillMatches.map((job, index) => {
            let gaugeColor = "bg-gradient-to-r from-rose-500 to-pink-500";
            if (job.score < 50) {
                gaugeColor = "bg-gradient-to-r from-amber-400 to-orange-500";
            } else if (job.score < 80) {
                gaugeColor = "bg-gradient-to-r from-pink-500 to-rose-600";
            }

            return `
            <div class="glass-card hover-lift p-4 sm:p-5 rounded-2xl sm:rounded-3xl space-y-3" style="animation-delay: ${index * 0.05}s">
                
                <!-- Title & Match Score Header -->
                <div class="flex items-start justify-between gap-2">
                    <div class="space-y-1">
                        <div class="flex items-center gap-2 flex-wrap">
                            <span class="w-6 h-6 rounded-lg bg-gradient-to-tr from-rose-500 to-pink-600 text-white font-bold text-xs inline-flex items-center justify-center shrink-0">${index + 1}</span>
                            <h4 class="text-base sm:text-lg font-bold text-slate-900 leading-snug">${ApiClient.escapeHTML(job.title)}</h4>
                        </div>
                        <div class="flex flex-wrap items-center gap-1.5 text-xs text-slate-500 pl-8">
                            <span class="font-medium">${ApiClient.escapeHTML(job.company || "องค์กรไอที")}</span>
                            <span>•</span>
                            <span>${ApiClient.escapeHTML(job.province || "กรุงเทพฯ")}</span>
                        </div>
                    </div>

                    <!-- Single, Clean Match Score -->
                    <div class="flex flex-col items-end shrink-0 bg-slate-50 px-3 py-1 rounded-xl border border-slate-200 text-right">
                        <span class="text-[10px] text-slate-400 font-bold uppercase">ตรงกัน</span>
                        <span class="text-lg font-black text-rose-600 font-english">${job.score}%</span>
                    </div>
                </div>

                <!-- Progress Bar -->
                <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                    <div class="${gaugeColor} h-full rounded-full transition-all duration-800" style="width: 0%" data-progress-bar data-target-width="${job.score}%"></div>
                </div>

                <!-- Matched & Missing Skills -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                    <div class="bg-emerald-50/50 p-2.5 rounded-xl border border-emerald-200/70 space-y-1">
                        <span class="font-bold text-emerald-950 text-[11px] flex items-center gap-1">
                            <i class="fa-solid fa-check text-emerald-600 text-[10px]"></i> ทักษะที่ตรง (${job.matched_skills.length})
                        </span>
                        <div class="flex flex-wrap gap-1">
                            ${job.matched_skills.length > 0
                                ? job.matched_skills.map(s => `<span class="bg-white text-emerald-950 px-2 py-0.5 rounded border border-emerald-200 text-[11px] font-medium">${ApiClient.escapeHTML(s)}</span>`).join('')
                                : '<span class="text-slate-400 text-[11px]">-</span>'}
                        </div>
                    </div>

                    <div class="bg-rose-50/50 p-2.5 rounded-xl border border-rose-200/70 space-y-1">
                        <span class="font-bold text-rose-950 text-[11px] flex items-center gap-1">
                            <i class="fa-solid fa-lightbulb text-rose-600 text-[10px]"></i> ควรฝึกเพิ่ม (${job.missing_skills.length})
                        </span>
                        <div class="flex flex-wrap gap-1">
                            ${job.missing_skills.length > 0
                                ? job.missing_skills.map(s => `<span class="bg-white text-rose-950 px-2 py-0.5 rounded border border-rose-200 text-[11px] font-medium">${ApiClient.escapeHTML(s)}</span>`).join('')
                                : '<span class="text-emerald-700 font-bold text-[11px]">ครบถ้วน</span>'}
                        </div>
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
