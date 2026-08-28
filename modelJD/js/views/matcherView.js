/**
 * Matcher View: Pure Skill-Based IT Job Recommendation Engine
 * Design: Modern White Theme with Accent Pink (SkillMatch IT)
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
                                แบบฟอร์มระบุทักษะและความสามารถ
                            </h2>
                        </div>
                        <p class="text-xs text-slate-500 font-medium mt-1">
                            ระบุทักษะที่คุณมีเพื่อให้ระบบวิเคราะห์และจับคู่ตำแหน่งงานที่เหมาะสมที่สุดสำหรับคุณ
                        </p>
                    </div>
                    <button onclick="MatcherView.fillSampleSkills()"
                        class="text-xs glow-btn-secondary px-3.5 py-2 rounded-xl transition font-bold flex items-center gap-2 cursor-pointer shadow-2xs">
                        <i class="fa-solid fa-shuffle text-rose-500"></i>
                        <span>สุ่มตัวอย่างชุดทักษะ</span>
                    </button>
                </div>

                <!-- FIELD 1: Target Career Role (Optional) -->
                <div class="space-y-2">
                    <div class="flex justify-between items-center text-xs">
                        <label for="roleInput" class="font-bold text-slate-800 text-sm flex items-center gap-2">
                            <i class="fa-solid fa-bullseye text-rose-500"></i>
                            <span>1. สายงานเป้าหมายที่สนใจ</span>
                            <span class="text-slate-400 font-normal text-xs">(ไม่บังคับระบุ)</span>
                        </label>
                        <span class="text-slate-400 font-medium hidden sm:inline">หากเว้นว่างไว้ ระบบจะค้นหาจากทุกสายงาน</span>
                    </div>
                    <div class="relative">
                        <input type="text" id="roleInput" list="rolesList"
                            placeholder="พิมพ์หรือเลือกสายงาน... (เช่น .NET Developer, Data Scientist, Frontend Developer)"
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
                        <span class="text-slate-400 font-semibold mr-1">สายงานยอดนิยม:</span>
                        <button onclick="MatcherView.selectRole('.NET Developer')"
                            class="px-3 py-1 rounded-xl bg-slate-100/90 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">.NET Developer</button>
                        <button onclick="MatcherView.selectRole('Data Scientist')"
                            class="px-3 py-1 rounded-xl bg-slate-100/90 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">Data Scientist</button>
                        <button onclick="MatcherView.selectRole('Ethical Hacker')"
                            class="px-3 py-1 rounded-xl bg-slate-100/90 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">Ethical Hacker</button>
                        <button onclick="MatcherView.selectRole('Frontend Developer')"
                            class="px-3 py-1 rounded-xl bg-slate-100/90 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">Frontend Developer</button>
                        <button onclick="MatcherView.selectRole('Cloud Engineer')"
                            class="px-3 py-1 rounded-xl bg-slate-100/90 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">Cloud Engineer</button>
                        <button onclick="MatcherView.selectRole('QA Tester')"
                            class="px-3 py-1 rounded-xl bg-slate-100/90 hover:bg-rose-50 hover:text-rose-700 hover:border-rose-300 text-slate-700 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">QA Tester</button>
                        <button onclick="MatcherView.selectRole('')"
                            class="px-2.5 py-1 rounded-xl bg-slate-100/90 hover:bg-rose-100 hover:text-rose-800 text-slate-400 border border-slate-200 transition font-medium text-xs active:scale-95 cursor-pointer">
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

                    <!-- Search & Add Input with Accent Pink Button -->
                    <div class="flex gap-2.5">
                        <div class="relative flex-1">
                            <input type="text" id="addSkillInput" list="skillsDatalist"
                                aria-label="ช่องพิมพ์ค้นหาและเพิ่มทักษะ"
                                placeholder="พิมพ์ค้นหาทักษะ... แล้วกด Enter (เช่น Python, Docker, SQL Server, React)"
                                class="w-full p-3.5 pl-10 text-sm border border-slate-300 rounded-2xl focus:ring-2 focus:ring-rose-500/30 focus:border-rose-500 outline-none bg-white shadow-2xs transition placeholder:text-slate-400">
                            <span class="absolute left-3.5 top-4 text-slate-400">
                                <i class="fa-solid fa-magnifying-glass"></i>
                            </span>
                            <datalist id="skillsDatalist"></datalist>
                        </div>
                        <button onclick="MatcherView.addSkillFromInput()"
                            class="glow-btn-pink active:scale-95 font-bold px-6 py-3.5 rounded-2xl text-sm transition shadow-md flex items-center gap-2 shrink-0 cursor-pointer">
                            <i class="fa-solid fa-plus"></i>
                            <span>เพิ่มทักษะ</span>
                        </button>
                    </div>

                    <!-- Quick Add Popular Skills -->
                    <div class="flex items-center gap-1.5 flex-wrap pt-1 text-xs">
                        <span class="text-slate-400 font-semibold mr-1">ทักษะยอดนิยม:</span>
                        <button onclick="AppState.addSkill('python')" class="px-2.5 py-1 rounded-lg bg-rose-50/70 hover:bg-rose-100 text-rose-900 border border-rose-200 transition font-bold text-xs active:scale-95 cursor-pointer">+ Python</button>
                        <button onclick="AppState.addSkill('sql')" class="px-2.5 py-1 rounded-lg bg-rose-50/70 hover:bg-rose-100 text-rose-900 border border-rose-200 transition font-bold text-xs active:scale-95 cursor-pointer">+ SQL</button>
                        <button onclick="AppState.addSkill('c#')" class="px-2.5 py-1 rounded-lg bg-rose-50/70 hover:bg-rose-100 text-rose-900 border border-rose-200 transition font-bold text-xs active:scale-95 cursor-pointer">+ C#</button>
                        <button onclick="AppState.addSkill('asp.net core')" class="px-2.5 py-1 rounded-lg bg-rose-50/70 hover:bg-rose-100 text-rose-900 border border-rose-200 transition font-bold text-xs active:scale-95 cursor-pointer">+ ASP.NET Core</button>
                        <button onclick="AppState.addSkill('react')" class="px-2.5 py-1 rounded-lg bg-rose-50/70 hover:bg-rose-100 text-rose-900 border border-rose-200 transition font-bold text-xs active:scale-95 cursor-pointer">+ React</button>
                        <button onclick="AppState.addSkill('docker')" class="px-2.5 py-1 rounded-lg bg-rose-50/70 hover:bg-rose-100 text-rose-900 border border-rose-200 transition font-bold text-xs active:scale-95 cursor-pointer">+ Docker</button>
                        <button onclick="AppState.addSkill('linux')" class="px-2.5 py-1 rounded-lg bg-rose-50/70 hover:bg-rose-100 text-rose-900 border border-rose-200 transition font-bold text-xs active:scale-95 cursor-pointer">+ Linux</button>
                        <button onclick="AppState.addSkill('git')" class="px-2.5 py-1 rounded-lg bg-rose-50/70 hover:bg-rose-100 text-rose-900 border border-rose-200 transition font-bold text-xs active:scale-95 cursor-pointer">+ Git</button>
                        <button onclick="AppState.addSkill('scikit-learn')" class="px-2.5 py-1 rounded-lg bg-rose-50/70 hover:bg-rose-100 text-rose-900 border border-rose-200 transition font-bold text-xs active:scale-95 cursor-pointer">+ Scikit-Learn</button>
                    </div>
                </div>

                <!-- ACTION BUTTON: Run Job Matching -->
                <div class="pt-3">
                    <button onclick="MatcherView.runJobMatching()" id="searchBtn"
                        class="w-full glow-btn-pink active:scale-[0.99] font-black py-4 px-6 rounded-2xl transition-all duration-150 flex items-center justify-center gap-2.5 text-base md:text-lg shadow-xl cursor-pointer">
                        <i class="fa-solid fa-magnifying-glass-chart"></i>
                        <span>ค้นหางานที่ใช่สำหรับคุณ</span>
                    </button>
                </div>

            </div>

            <!-- JOB RECOMMENDATION RESULTS AREA -->
            <div id="resultsWrapper" class="space-y-6 pt-2">
                <!-- Rendered dynamically -->
            </div>
        </div>
        `;
    },

    onMount() {
        this.renderSkillTags();
        this.populateDatalists();

        const input = document.getElementById('addSkillInput');
        if (input) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.addSkillFromInput();
                }
            });
        }

        AppState.subscribe('skills', () => {
            this.renderSkillTags();
        });

        if (AppState.latestResults) {
            this.renderResults(AppState.latestResults);
        }
    },

    populateDatalists() {
        const skillsDatalist = document.getElementById("skillsDatalist");
        if (skillsDatalist && AppState.allSkills.length > 0) {
            skillsDatalist.innerHTML = AppState.allSkills.map(s => `<option value="${ApiClient.escapeHTML(s)}">`).join("");
        }

        const rolesList = document.getElementById("rolesList");
        if (rolesList && AppState.allRoles.length > 0) {
            rolesList.innerHTML = AppState.allRoles.map(r => `<option value="${ApiClient.escapeHTML(r)}">`).join("");
        }
    },

    selectRole(roleName) {
        AppState.setRole(roleName);
        const input = document.getElementById("roleInput");
        if (input) input.value = roleName;
    },

    addSkillFromInput() {
        const input = document.getElementById("addSkillInput");
        if (!input) return;
        const val = input.value.trim().toLowerCase();
        if (val) {
            if (AppState.addSkill(val)) {
                input.value = "";
            }
        }
    },

    renderSkillTags() {
        const tagBox = document.getElementById("skillsTagBox");
        const countBadge = document.getElementById("skillCountBadge");
        if (!tagBox) return;

        if (countBadge) countBadge.innerHTML = `<i class="fa-solid fa-layer-group text-rose-600 mr-1"></i> ${AppState.userSkills.length} ทักษะ`;

        if (AppState.userSkills.length === 0) {
            tagBox.innerHTML = `
                <div id="emptySkillsGuide" class="w-full text-center py-4 text-slate-400 text-xs font-medium">
                    <i class="fa-solid fa-arrow-pointer mr-1"></i> ยังไม่มีการเลือกทักษะ &bull; พิมพ์ค้นหาจากคลังทักษะมาตรฐานด้านล่าง หรือคลิกเลือกทักษะยอดนิยม
                </div>`;
            return;
        }

        tagBox.innerHTML = AppState.userSkills.map((skill, index) => `
            <span class="skill-chip animate__animated animate__fadeIn inline-flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-bold bg-white text-rose-950 border border-rose-200 shadow-xs">
                <span>${ApiClient.escapeHTML(skill)}</span>
                <button onclick="AppState.removeSkill(${index})" title="ลบทักษะนี้" aria-label="ลบทักษะ ${ApiClient.escapeHTML(skill)}" class="hover:bg-rose-100 hover:text-rose-600 text-slate-400 rounded-full w-4 h-4 inline-flex items-center justify-center transition-colors text-[10px] cursor-pointer">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </span>
        `).join("");
    },

    fillSampleSkills() {
        const samples = [
            {
                role: "",
                skills: ["c#", "asp.net core", "asp.net mvc", "sql server", "git", "visual studio"]
            },
            {
                role: "",
                skills: ["python", "scikit-learn", "pandas", "sql", "pytorch", "machine learning"]
            },
            {
                role: "Ethical Hacker",
                skills: ["linux", "network security", "bash", "penetration testing", "web application security"]
            },
            {
                role: "Frontend Developer",
                skills: ["react", "typescript", "javascript", "tailwind", "html", "css", "git"]
            }
        ];

        const chosen = samples[Math.floor(Math.random() * samples.length)];
        this.selectRole(chosen.role);
        AppState.setSkills(chosen.skills);
    },

    async runJobMatching() {
        const role = AppState.selectedRole;
        const resultsWrapper = document.getElementById("resultsWrapper");
        const searchBtn = document.getElementById("searchBtn");

        if (!role && AppState.userSkills.length === 0) {
            Swal.fire({
                icon: 'warning',
                title: 'ข้อมูลไม่เพียงพอ',
                text: 'กรุณาระบุทักษะที่คุณมีอย่างน้อย 1 ทักษะ หรือระบุสายงานที่สนใจครับ',
                confirmButtonColor: '#e11d48',
                confirmButtonText: 'ตกลง',
                customClass: { popup: 'rounded-3xl', confirmButton: 'glow-btn-pink rounded-xl px-6 py-2.5 font-bold text-xs' }
            });
            return;
        }

        if (searchBtn) {
            searchBtn.disabled = true;
            searchBtn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin mr-2"></i> กำลังวิเคราะห์ตำแหน่งงาน...`;
            searchBtn.classList.add('opacity-80', 'cursor-not-allowed');
        }

        if (resultsWrapper) {
            resultsWrapper.innerHTML = `
                <div class="flex justify-center items-center py-14 glass-card rounded-3xl">
                    <div class="flex flex-col items-center gap-3">
                        <div class="w-12 h-12 border-4 border-rose-200 border-t-rose-600 rounded-full animate-spin"></div>
                        <p class="text-slate-800 font-extrabold text-sm">กำลังวิเคราะห์ข้อมูลและค้นหางานที่เหมาะสมที่สุด...</p>
                    </div>
                </div>
            `;
        }

        try {
            const data = await ApiClient.getRecommendations(role, AppState.userSkills);
            if (data.status === "success") {
                AppState.setResults(data);
                this.renderResults(data);
                resultsWrapper.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                resultsWrapper.innerHTML = `
                    <div class="bg-rose-50 border border-rose-200 p-6 rounded-3xl text-center space-y-2 animate__animated animate__fadeInUp">
                        <div class="w-12 h-12 bg-rose-100 rounded-full flex items-center justify-center mx-auto mb-2 text-rose-600 text-xl">
                            <i class="fa-solid fa-triangle-exclamation"></i>
                        </div>
                        <div class="font-bold text-base text-rose-900">เกิดข้อผิดพลาด</div>
                        <div class="text-xs text-rose-700">${ApiClient.escapeHTML(data.message)}</div>
                    </div>`;
            }
        } catch (error) {
            console.error("Error:", error);
            Swal.fire({
                icon: 'error',
                title: 'การเชื่อมต่อล้มเหลว',
                text: 'เกิดข้อผิดพลาดในการเชื่อมต่อกับ Server กรุณาตรวจสอบว่าเซิร์ฟเวอร์ทำงานอยู่ครับ',
                confirmButtonColor: '#e11d48',
                confirmButtonText: 'ตกลง'
            });
            if (resultsWrapper) resultsWrapper.innerHTML = '';
        } finally {
            if (searchBtn) {
                searchBtn.disabled = false;
                searchBtn.innerHTML = `<i class="fa-solid fa-magnifying-glass-chart mr-1.5"></i> ค้นหางานที่ใช่สำหรับคุณ`;
                searchBtn.classList.remove('opacity-80', 'cursor-not-allowed');
            }
        }
    },

    renderResults(data) {
        const resultsWrapper = document.getElementById("resultsWrapper");
        if (!resultsWrapper) return;

        const targetAnalysis = data.target_career_analysis;
        const skillMatches = data.skill_matched_recommendations || data.results || [];

        if (!targetAnalysis && (!skillMatches || skillMatches.length === 0)) {
            resultsWrapper.innerHTML = `
                <div class="glass-card p-8 rounded-3xl text-center text-slate-500 shadow-sm animate__animated animate__fadeInUp">
                    <div class="text-3xl mb-2 text-slate-400">
                        <i class="fa-solid fa-magnifying-glass"></i>
                    </div>
                    <p class="font-bold text-base text-slate-700">ไม่พบตำแหน่งงานที่ตรงตามเงื่อนไข</p>
                    <p class="text-xs mt-1 text-slate-400">ลองเพิ่มทักษะหรือปรับสายงานที่เลือกดูอีกครั้งครับ</p>
                </div>`;
            return;
        }

        let html = ``;

        // SECTION 1: TARGET CAREER ANALYSIS
        if (targetAnalysis) {
            let targetGaugeColor = "bg-gradient-to-r from-rose-500 to-pink-500";
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
                            <i class="fa-solid fa-bullseye text-rose-500"></i> ส่วนที่ 1: การวิเคราะห์สายงานเป้าหมาย (Target Career Analysis)
                        </span>
                        <h3 class="text-xl sm:text-2xl font-black text-slate-900 mt-2 flex items-center gap-2">
                            <i class="fa-solid fa-crosshairs text-rose-600"></i> สายงานเป้าหมายที่คุณเลือก: <span class="text-rose-600 font-black">${ApiClient.escapeHTML(targetAnalysis.target_role)}</span>
                        </h3>
                        <p class="text-xs text-slate-500 font-medium">ประเมินความพร้อมและชี้เป้าทักษะที่ต้องศึกษาเพิ่ม (Skill Gap Roadmap) เพื่อเตรียมพร้อมสมัครงานนี้</p>
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
                                    <i class="fa-solid fa-bullseye"></i> ตำแหน่งเป้าหมาย
                                </span>
                            </div>
                            
                            <div class="flex flex-wrap items-center gap-1.5 mt-2">
                                <span class="inline-flex items-center gap-1.5 text-[11px] font-extrabold bg-white text-slate-700 border border-slate-200 px-2.5 py-0.5 rounded-lg shadow-2xs">
                                    <i class="fa-solid fa-graduation-cap text-slate-400"></i> ${ApiClient.escapeHTML(targetAnalysis.experience_level || "Entry-Level / Fresher")}
                                </span>
                                <span class="inline-flex items-center gap-1.5 text-[11px] font-extrabold bg-white text-slate-700 border border-slate-200 px-2.5 py-0.5 rounded-lg shadow-2xs">
                                    <i class="fa-solid fa-clock text-slate-400"></i> ประสบการณ์: ${JobComponents.formatExperienceYears(targetAnalysis.years_of_experience)}
                                </span>
                                ${JobComponents.renderKeywordBadges(targetAnalysis.keywords_list || targetAnalysis.keywords, targetAnalysis.title, targetAnalysis.experience_level)}
                            </div>
                        </div>
                        
                        <div class="flex items-center gap-2 shrink-0 self-start sm:self-auto">
                            <div class="flex flex-col items-end ${targetStatus.pillBg} px-4 py-2 rounded-2xl border shadow-2xs">
                                <span class="text-[10px] font-extrabold uppercase tracking-wider">${targetStatus.shortText}</span>
                                <span class="text-lg font-black font-english">${targetAnalysis.skill_readiness}%</span>
                            </div>
                            <div class="bg-white px-4 py-2 rounded-2xl border border-rose-200 shadow-xs text-right">
                                <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Target Match</div>
                                <span class="text-2xl font-black ${targetTextColor} font-english">${targetAnalysis.score}<span class="text-sm text-slate-400 font-normal">%</span></span>
                            </div>
                        </div>
                    </div>

                    <!-- Progress Bar -->
                    <div class="w-full bg-slate-100 rounded-full h-3 overflow-hidden p-0.5 border border-slate-200/80">
                        <div class="${targetGaugeColor} h-full rounded-full transition-all duration-800 ease-out shadow-xs" style="width: 0%" data-progress-bar data-target-width="${targetAnalysis.score}%"></div>
                    </div>

                    <!-- Responsibilities -->
                    <div class="bg-white/95 p-4 rounded-2xl border border-slate-200/90 shadow-2xs space-y-2 text-xs">
                        <div class="font-extrabold text-slate-900 flex items-center gap-1.5 text-xs text-rose-700">
                            <i class="fa-solid fa-list-check"></i>
                            <span>หน้าที่และความรับผิดชอบหลัก (Responsibilities)</span>
                        </div>
                        <ul class="space-y-1.5 text-slate-600 font-medium pl-1">
                            ${JobComponents.renderResponsibilities(targetAnalysis.responsibilities_list || targetAnalysis.responsibilities)}
                        </ul>
                    </div>

                    <!-- Matched Skills vs Gap Roadmap -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-1 text-xs">
                        <div class="bg-emerald-50/70 p-5 rounded-2xl border border-emerald-200 space-y-3">
                            <span class="font-bold text-emerald-950 flex items-center gap-2 text-xs">
                                <i class="fa-solid fa-circle-check text-emerald-600"></i>
                                ทักษะที่คุณมีตรงกับสายงานเป้าหมายนี้ (${targetAnalysis.matched_skills.length})
                            </span>
                            <div class="flex flex-wrap gap-1.5">
                                ${targetAnalysis.matched_skills.length > 0
                    ? targetAnalysis.matched_skills.map(s => `<span class="bg-white text-emerald-950 px-2.5 py-1 rounded-lg border border-emerald-300 font-bold text-xs shadow-2xs">${ApiClient.escapeHTML(s)}</span>`).join('')
                    : '<span class="text-slate-400 italic text-xs">ยังไม่มีทักษะที่ตรงตัวโดยตรง</span>'}
                            </div>
                        </div>

                        <div class="bg-rose-50/70 p-5 rounded-2xl border border-rose-200 space-y-3">
                            <span class="font-bold text-rose-950 flex items-center gap-2 text-xs">
                                <i class="fa-solid fa-lightbulb text-rose-600"></i>
                                ทักษะที่ควรศึกษาเพิ่ม (Skill Gap Roadmap) (${targetAnalysis.missing_skills.length})
                            </span>
                            <div class="flex flex-wrap gap-1.5">
                                ${targetAnalysis.missing_skills.length > 0
                    ? targetAnalysis.missing_skills.map(s => `<span class="bg-white text-rose-950 px-2.5 py-1 rounded-lg border border-rose-300 font-bold text-xs shadow-2xs">${ApiClient.escapeHTML(s)}</span>`).join('')
                    : '<span class="text-emerald-800 font-extrabold text-xs flex items-center gap-1.5"><i class="fa-solid fa-star text-amber-500"></i> คุณสมบัติครบถ้วนทุกทักษะสำหรับตำแหน่งนี้!</span>'}
                            </div>
                            ${targetAnalysis.missing_skills.length > 0 ? `
                                <div class="pt-1.5 text-[11px] text-rose-700 font-bold flex items-center gap-1.5">
                                    <i class="fa-solid fa-circle-info"></i> แนะนำ: ศึกษาทักษะเหล่านี้เพิ่มเติม เพื่อเพิ่มโอกาสในการได้งาน
                                </div>
                            ` : ''}
                        </div>
                    </div>

                    <!-- Footer / Prep Guide Button -->
                    <div class="flex items-center justify-between gap-2 pt-2 border-t border-rose-100/80 flex-wrap">
                        <div class="text-[11px] text-slate-400 font-medium">
                            รหัสตำแหน่ง: <span class="font-bold text-rose-700 font-english">${ApiClient.escapeHTML(targetAnalysis.job_id || "TARGET-JOB")}</span>
                        </div>
                        <div>
                            <button onclick="JobComponents.showPrepGuide('${targetAnalysis.title.replace(/'/g, "\\'")}', ${JSON.stringify(targetAnalysis.missing_skills || []).replace(/"/g, '&quot;')})" class="glow-btn-pink px-4 py-2 rounded-xl text-xs font-extrabold transition-all flex items-center gap-2 cursor-pointer shadow-sm">
                                <i class="fa-solid fa-rocket"></i>
                                <span>ดูแนวทางเตรียมตัว</span>
                            </button>
                        </div>
                    </div>

                </div>
            </div>
            `;
        }

        // SECTION 2: TOP MATCHED RECOMMENDATIONS BY CURRENT SKILLS
        html += `
        <div class="space-y-4 animate__animated animate__fadeInUp">
            <div class="flex items-center justify-between px-1 flex-wrap gap-2">
                <div>
                    <span class="text-xs font-black tracking-wider uppercase text-rose-700 bg-rose-50 border border-rose-200 px-3 py-1 rounded-xl inline-flex items-center gap-1.5 shadow-2xs">
                        <i class="fa-solid fa-award text-rose-500"></i> ส่วนที่ 2: ตำแหน่งงานที่ตรงกับทักษะปัจจุบัน (Matched by Current Skills)
                    </span>
                    <h3 class="text-xl sm:text-2xl font-black text-slate-900 mt-2 flex items-center gap-2">
                        <i class="fa-solid fa-trophy text-amber-500"></i> อันดับตำแหน่งงานที่เหมาะสมที่สุด (Top 5 Matches)
                    </h3>
                    <p class="text-xs text-slate-500 font-medium">ระบบได้คัดเลือกและจัดอันดับงานที่เหมาะสมกับทักษะของคุณมากที่สุด</p>
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
                        </div>

                        <div class="flex flex-wrap items-center gap-1.5 mt-2 ml-9">
                            <span class="inline-flex items-center gap-1.5 text-[11px] font-extrabold bg-slate-50 text-slate-700 border border-slate-200 px-2.5 py-0.5 rounded-lg shadow-2xs">
                                <i class="fa-solid fa-graduation-cap text-slate-400"></i> ${ApiClient.escapeHTML(job.experience_level || "Entry-Level / Fresher")}
                            </span>
                            <span class="inline-flex items-center gap-1.5 text-[11px] font-extrabold bg-slate-50 text-slate-700 border border-slate-200 px-2.5 py-0.5 rounded-lg shadow-2xs">
                                <i class="fa-solid fa-clock text-slate-400"></i> ประสบการณ์: ${JobComponents.formatExperienceYears(job.years_of_experience)}
                            </span>
                            ${JobComponents.renderKeywordBadges(job.keywords_list || job.keywords, job.title, job.experience_level)}
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
                        ${job.missing_skills.length > 0 ? `
                            <div class="pt-1.5 text-[11px] text-rose-700 font-bold flex items-center gap-1.5">
                                <i class="fa-solid fa-circle-info"></i> แนะนำ: ศึกษาทักษะเหล่านี้เพิ่มเติม เพื่อเพิ่มโอกาสในการได้งาน
                            </div>
                        ` : ''}
                    </div>
                </div>

                <!-- Footer -->
                <div class="flex items-center justify-between gap-2 pt-2 border-t border-slate-100 flex-wrap">
                    <div class="text-[11px] text-slate-400 font-medium">
                        รหัสตำแหน่ง: <span class="font-bold text-slate-600 font-english">${ApiClient.escapeHTML(job.job_id || "JOB-" + (index + 1))}</span>
                    </div>
                    <div>
                        <button onclick="JobComponents.showPrepGuide('${job.title.replace(/'/g, "\\'")}', ${JSON.stringify(job.missing_skills || []).replace(/"/g, '&quot;')})" class="glow-btn-pink px-4 py-2 rounded-xl text-xs font-extrabold transition-all flex items-center gap-2 cursor-pointer shadow-sm">
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
