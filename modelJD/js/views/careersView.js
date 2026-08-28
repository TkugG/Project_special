/**
 * Careers View: Comprehensive IT Career Catalog & Exploration
 * Design: Modern White Theme with Accent Pink (SkillMatch IT)
 */
window.CareersView = {
    currentCategory: 'all',
    searchQuery: '',

    categories: [
        { id: 'all', label: 'ทั้งหมด (All)', iconClass: 'fa-solid fa-star' },
        { id: 'dev', label: 'Software & Web', iconClass: 'fa-solid fa-code' },
        { id: 'data', label: 'Data & Analytics', iconClass: 'fa-solid fa-chart-pie' },
        { id: 'cloud', label: 'Cloud & DevOps', iconClass: 'fa-solid fa-cloud' },
        { id: 'sec', label: 'Cybersecurity', iconClass: 'fa-solid fa-shield-halved' },
        { id: 'qa', label: 'QA & Testing', iconClass: 'fa-solid fa-vial-circle-check' },
        { id: 'design', label: 'UI/UX & Mobile', iconClass: 'fa-solid fa-mobile-screen-button' }
    ],

    roleDetails: [
        { title: '.NET Developer', cat: 'dev', exp: '0-2 ปี', skills: ['c#', 'asp.net core', 'sql server', 'entity framework', 'git'], desc: 'พัฒนาและบำรุงรักษาเว็บแอปพลิเคชันหรือระบบองค์กรด้วยภาษา C# และเฟรมเวิร์ก .NET' },
        { title: 'Frontend Developer', cat: 'dev', exp: '0-2 ปี', skills: ['react', 'javascript', 'typescript', 'tailwind', 'html', 'css'], desc: 'พัฒนาส่วนติดต่อผู้ใช้ (UI) บนเว็บเบราว์เซอร์ให้ตอบสนองลื่นไหลและเชื่อมต่อ API' },
        { title: 'Backend Developer', cat: 'dev', exp: '0-2 ปี', skills: ['node.js', 'python', 'java', 'sql', 'rest api', 'docker'], desc: 'พัฒนาระบบประมวลผลฝั่งเซิร์ฟเวอร์ ออกแบบ RESTful API และจัดการฐานข้อมูล' },
        { title: 'Full Stack Developer', cat: 'dev', exp: '1-3 ปี', skills: ['react', 'node.js', 'typescript', 'postgresql', 'docker', 'git'], desc: 'พัฒนาทั้งระบบหน้าบ้าน (Frontend), ระบบหลังบ้าน (Backend) และเชื่อมต่อฐานข้อมูลแบบครบวงจร' },
        { title: 'Python Developer', cat: 'dev', exp: '0-2 ปี', skills: ['python', 'fastapi', 'django', 'postgresql', 'docker'], desc: 'พัฒนาระบบเว็บแอปพลิเคชัน API หรือระบบประมวลผลอัตโนมัติด้วยภาษา Python' },
        { title: 'Java Developer', cat: 'dev', exp: '1-3 ปี', skills: ['java', 'spring boot', 'microservices', 'oracle', 'git'], desc: 'พัฒนาระบบแอปพลิเคชันระดับองค์กรและไมโครเซอร์วิสด้วยภาษา Java' },
        { title: 'Data Scientist', cat: 'data', exp: '1-3 ปี', skills: ['python', 'scikit-learn', 'pandas', 'machine learning', 'sql'], desc: 'วิเคราะห์ข้อมูลเชิงสถิติขั้นสูง พัฒนาแบบจำลองการทำนาย และค้นหาแนวโน้มข้อมูล' },
        { title: 'Data Analyst', cat: 'data', exp: '0-2 ปี', skills: ['sql', 'power bi', 'tableau', 'excel', 'python'], desc: 'รวบรวม สรุป วิเคราะห์ข้อมูลทางธุรกิจ และจัดทำ Dashboard รายงานผลให้ผู้บริหาร' },
        { title: 'Data Engineer', cat: 'data', exp: '1-3 ปี', skills: ['sql', 'python', 'spark', 'airflow', 'data pipeline', 'kafka'], desc: 'ออกแบบและสร้างท่อลำเลียงข้อมูล (Data Pipeline / ETL) และ Data Warehouse' },
        { title: 'AI Engineer', cat: 'data', exp: '1-3 ปี', skills: ['python', 'pytorch', 'tensorflow', 'nlp', 'deep learning', 'llm'], desc: 'พัฒนาโมเดลประมวลผลข้อมูลขั้นสูงและการเชื่อมต่อแบบจำลองเข้ากับระบบประยุกต์' },
        { title: 'Business Intelligence Analyst', cat: 'data', exp: '0-2 ปี', skills: ['power bi', 'sql', 'data modeling', 'dax', 'tableau'], desc: 'ออกแบบโมเดลข้อมูลเพื่อการวิเคราะห์ทางธุรกิจ และสร้างตัวชี้วัด (KPIs)' },
        { title: 'Cloud Engineer', cat: 'cloud', exp: '1-3 ปี', skills: ['aws', 'azure', 'docker', 'kubernetes', 'terraform', 'linux'], desc: 'ออกแบบ ติดตั้ง และดูแลโครงสร้างพื้นฐานบนระบบคลาวด์' },
        { title: 'DevOps Engineer', cat: 'cloud', exp: '1-3 ปี', skills: ['docker', 'kubernetes', 'ci/cd', 'jenkins', 'git', 'linux'], desc: 'ออกแบบโครงสร้างพื้นฐาน ดูแลระบบ CI/CD Pipeline และบริหารจัดการ Container' },
        { title: 'System Engineer', cat: 'cloud', exp: '0-2 ปี', skills: ['linux', 'windows server', 'bash', 'virtualization', 'backup'], desc: 'ติดตั้ง กำหนดค่า และบริหารจัดการเครื่องแม่ข่าย (Server) ระบบปฏิบัติการ Linux/Windows' },
        { title: 'Network Engineer', cat: 'cloud', exp: '0-2 ปี', skills: ['cisco', 'tcp/ip', 'routing', 'switching', 'firewall', 'vpn'], desc: 'ออกแบบ ติดตั้ง กำหนดค่า และบำรุงรักษาระบบเครือข่าย ทั้ง LAN, WAN, VPN' },
        { title: 'Site Reliability Engineer', cat: 'cloud', exp: '1-3 ปี', skills: ['kubernetes', 'prometheus', 'grafana', 'python', 'linux'], desc: 'ดูแลเสถียรภาพ ประสิทธิภาพ และการทำงานต่อเนื่องของระบบ Production' },
        { title: 'Ethical Hacker', cat: 'sec', exp: '1-3 ปี', skills: ['linux', 'penetration testing', 'burp suite', 'nmap', 'network security', 'bash'], desc: 'ตรวจสอบช่องโหว่ ทำแบบจำลองการเจาะระบบ (Penetration Testing) และจัดทำรายงานความเสี่ยง' },
        { title: 'Cybersecurity Analyst', cat: 'sec', exp: '0-2 ปี', skills: ['siem', 'firewall', 'incident response', 'network security', 'soc'], desc: 'ตรวจจับและวิเคราะห์ภัยคุกคามทางไซเบอร์ ดูแลระบบ Firewall, SIEM' },
        { title: 'Information Security Analyst', cat: 'sec', exp: '1-3 ปี', skills: ['iso 27001', 'security audit', 'risk assessment', 'compliance'], desc: 'กำหนดนโยบายความปลอดภัยสารสนเทศ และประเมินความเสี่ยงตามมาตรฐานสากล' },
        { title: 'QA Tester', cat: 'qa', exp: '0-2 ปี', skills: ['test cases', 'manual testing', 'postman', 'jira', 'bug tracking'], desc: 'ออกแบบชุดทดสอบ ดำเนินการทดสอบระบบ Manual และติดตามแก้ไขข้อผิดพลาด' },
        { title: 'QA Automation Engineer', cat: 'qa', exp: '1-3 ปี', skills: ['selenium', 'cypress', 'playwright', 'python', 'javascript', 'postman'], desc: 'พัฒนาชุดคำสั่งทดสอบระบบอัตโนมัติ (Automation Test Scripts) เพื่อเพิ่มประสิทธิภาพ' },
        { title: 'UI/UX Designer', cat: 'design', exp: '0-2 ปี', skills: ['figma', 'wireframing', 'prototyping', 'user research', 'design system'], desc: 'ออกแบบโครงร่างหน้าจอ (Wireframe), ตัวต้นแบบ (Prototype) และค้นคว้าพฤติกรรมผู้ใช้งาน' },
        { title: 'Mobile App Developer', cat: 'design', exp: '0-2 ปี', skills: ['flutter', 'react native', 'swift', 'kotlin', 'dart', 'rest api'], desc: 'พัฒนาและปรับปรุงแอปพลิเคชันบนระบบปฏิบัติการ iOS หรือ Android' },
        { title: 'Flutter Developer', cat: 'design', exp: '0-2 ปี', skills: ['flutter', 'dart', 'rest api', 'state management', 'git'], desc: 'พัฒนา Cross-platform Mobile Application ด้วย Flutter และ Dart' }
    ],

    render() {
        return `
        <div class="space-y-6 view-transition-in">
            <!-- Header Banner -->
            <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm border-t-4 border-t-rose-500 space-y-4">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <span class="text-xs font-black tracking-wider uppercase text-rose-700 bg-rose-50 border border-rose-200 px-3 py-1 rounded-xl inline-flex items-center gap-1.5 shadow-2xs">
                            <i class="fa-solid fa-briefcase text-rose-500"></i> แคตตาล็อกสายงานไอทีมาตรฐาน
                        </span>
                        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2 flex items-center gap-2.5">
                            <i class="fa-solid fa-compass text-rose-600"></i> IT Career Explorer (สำรวจ 45+ สายงาน)
                        </h2>
                        <p class="text-xs sm:text-sm text-slate-500 font-medium mt-1">
                            เรียนรู้คุณสมบัติ หน้าที่ความรับผิดชอบ และชุดทักษะที่จำเป็นของแต่ละตำแหน่งงาน พร้อมส่งตรงไปยังระบบค้นหางาน
                        </p>
                    </div>
                </div>

                <!-- Search Input with Pink Accent Focus -->
                <div class="relative pt-2">
                    <input type="text" id="careerSearchInput"
                        placeholder="พิมพ์ค้นหาสายงานหรือทักษะ... (เช่น Data Scientist, React, Docker, Security)"
                        value="${ApiClient.escapeHTML(this.searchQuery)}"
                        oninput="CareersView.onSearchChange(this.value)"
                        class="w-full p-3.5 pl-11 text-sm border border-slate-300 rounded-2xl focus:ring-2 focus:ring-rose-500/30 focus:border-rose-500 outline-none bg-white shadow-2xs transition placeholder:text-slate-400">
                    <span class="absolute left-4 top-5.5 text-slate-400">
                        <i class="fa-solid fa-magnifying-glass"></i>
                    </span>
                </div>

                <!-- Category Tabs (Clean White & Pink Active) -->
                <div class="flex items-center gap-2 overflow-x-auto pb-2 pt-1 text-xs">
                    ${this.categories.map(cat => `
                        <button onclick="CareersView.setCategory('${cat.id}')"
                            class="px-4 py-2.5 rounded-2xl font-bold transition-all shrink-0 cursor-pointer flex items-center gap-2 ${this.currentCategory === cat.id ? 'glow-btn-pink shadow-md' : 'bg-white hover:bg-rose-50 hover:text-rose-700 text-slate-700 border border-slate-200'}">
                            <i class="${cat.iconClass}"></i>
                            <span>${cat.label}</span>
                        </button>
                    `).join('')}
                </div>
            </div>

            <!-- Career Cards Grid -->
            <div id="careerGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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
            const matchesCat = this.currentCategory === 'all' || role.cat === this.currentCategory;
            const matchesQuery = !this.searchQuery ||
                role.title.toLowerCase().includes(this.searchQuery) ||
                role.desc.toLowerCase().includes(this.searchQuery) ||
                role.skills.some(s => s.toLowerCase().includes(this.searchQuery));
            return matchesCat && matchesQuery;
        });
    },

    renderCards() {
        const grid = document.getElementById("careerGrid");
        if (!grid) return;

        const roles = this.getFilteredRoles();

        if (roles.length === 0) {
            grid.innerHTML = `
                <div class="col-span-full glass-card p-10 rounded-3xl text-center text-slate-500 space-y-2">
                    <div class="text-3xl text-slate-400">
                        <i class="fa-solid fa-magnifying-glass"></i>
                    </div>
                    <div class="font-bold text-base text-slate-700">ไม่พบสายงานที่ตรงกับคำค้นหา</div>
                    <div class="text-xs text-slate-400">ลองค้นหาด้วยคำอื่น เช่น .NET, Python, Security, Cloud</div>
                </div>`;
            return;
        }

        grid.innerHTML = roles.map(role => `
            <div class="glass-card rounded-3xl p-5 md:p-6 shadow-sm hover-lift border border-slate-200/90 flex flex-col justify-between space-y-4">
                <div class="space-y-3">
                    <div class="flex items-start justify-between gap-2">
                        <div>
                            <h3 class="font-black text-base text-slate-900">${ApiClient.escapeHTML(role.title)}</h3>
                            <span class="inline-flex items-center gap-1.5 text-[10px] font-extrabold bg-rose-50 text-rose-800 border border-rose-200 px-2 py-0.5 rounded-lg mt-1">
                                <i class="fa-solid fa-clock text-slate-400"></i> ประสบการณ์: ${ApiClient.escapeHTML(role.exp)}
                            </span>
                        </div>
                        <span class="w-8 h-8 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center text-xs shrink-0 shadow-2xs">
                            <i class="fa-solid fa-crosshairs"></i>
                        </span>
                    </div>

                    <p class="text-xs text-slate-600 font-medium leading-relaxed">
                        ${ApiClient.escapeHTML(role.desc)}
                    </p>

                    <!-- Core Skills -->
                    <div class="space-y-1.5 pt-1">
                        <div class="text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">ทักษะสำคัญ:</div>
                        <div class="flex flex-wrap gap-1">
                            ${role.skills.map(s => `
                                <span class="text-[11px] font-bold bg-slate-50 text-slate-800 px-2.5 py-0.5 rounded-lg border border-slate-200/80">${ApiClient.escapeHTML(s)}</span>
                            `).join('')}
                        </div>
                    </div>
                </div>

                <!-- Actions -->
                <div class="pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
                    <button onclick="CareersView.selectForMatch('${role.title.replace(/'/g, "\\'")}', ${JSON.stringify(role.skills).replace(/"/g, '&quot;')})"
                        class="w-full text-center glow-btn-pink text-xs font-black py-3 px-3 rounded-2xl transition cursor-pointer flex items-center justify-center gap-2 shadow-sm">
                        <i class="fa-solid fa-crosshairs"></i>
                        <span>นำสายงานนี้ไปค้นหางาน</span>
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
            title: `เลือกสายงาน ${roleTitle} แล้ว`,
            text: 'ระบบได้นำเข้าสายงานและทักษะแนะนำไปยังแบบฟอร์มเรียบร้อยครับ',
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 2500,
            timerProgressBar: true,
            customClass: { popup: 'rounded-2xl shadow-xl text-sm border border-rose-100' }
        });
    }
};
