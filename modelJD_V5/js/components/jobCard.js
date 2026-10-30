/**
 * Job Card & Component Renderers for SkillMatch IT
 * Design: Modern White Theme with Accent Pink (SkillMatch IT)
 */
window.JobComponents = {
    ROLE_QUALIFICATIONS: {
        "ethical_hacker": {
            desc: "ตรวจสอบช่องโหว่ ทำแบบจำลองการเจาะระบบ (Penetration Testing) และจัดทำรายงานความเสี่ยง",
            qual: "มีความรู้เรื่อง Network Security, Cryptography, ใช้เครื่องมือเจาะระบบ (Burp Suite, Nmap) และเข้าใจกฎหมายความมั่นคงไซเบอร์"
        },
        "cybersecurity": {
            desc: "ตรวจจับและวิเคราะห์ภัยคุกคามทางไซเบอร์ ดูแลระบบ Firewall, SIEM และรับมือกับเหตุการณ์ความปลอดภัย",
            qual: "เข้าใจสถาปัตยกรรมความปลอดภัย, การตั้งค่า Firewall, ระบบยืนยันตัวตน และมาตรฐานความปลอดภัยสารสนเทศ"
        },
        "network_engineer": {
            desc: "ออกแบบ ติดตั้ง กำหนดค่า และบำรุงรักษาระบบเครือข่าย ทั้ง LAN, WAN, VPN และอุปกรณ์ Routing/Switching",
            qual: "มีความรู้ด้าน OSI Model, TCP/IP, Routing Protocols, Subnetting และการแก้ไขปัญหาอุปกรณ์เครือข่าย"
        },
        "system_engineer": {
            desc: "ติดตั้ง กำหนดค่า และบริหารจัดการเครื่องแม่ข่าย (Server) ระบบปฏิบัติการ Linux/Windows และระบบ Virtualization",
            qual: "เชี่ยวชาญ Linux/Windows Server, Command Line/Bash, การจัดการสิทธิ์, Backup/Recovery และ Virtualization"
        },
        "data_scientist": {
            desc: "วิเคราะห์ข้อมูลเชิงสถิติขั้นสูง พัฒนาแบบจำลองการทำนาย และค้นหาแนวโน้มเพื่อสนับสนุนการตัดสินใจ",
            qual: "มีพื้นฐานคณิตศาสตร์/สถิติ, ทักษะเขียนโปรแกรมวิเคราะห์ข้อมูล (Python/R), Feature Engineering และ Visualization"
        },
        "data_analyst": {
            desc: "รวบรวม สรุป วิเคราะห์ข้อมูลทางธุรกิจ และจัดทำ Dashboard รายงานผลให้ผู้บริหาร",
            qual: "เชี่ยวชาญการเขียน SQL Query, ใช้เครื่องมือ BI (Power BI/Tableau) และมีทักษะการแปลผลข้อมูลเชิงธุรกิจ"
        },
        "data_engineer": {
            desc: "ออกแบบและสร้างท่อลำเลียงข้อมูล (Data Pipeline / ETL), จัดการ Data Warehouse และระบบ Big Data",
            qual: "ทักษะการออกแบบ Relational Database, Normalization, เครื่องมือ Data Pipeline (Airflow/Spark) และ SQL ขั้นสูง"
        },
        "bi_analyst": {
            desc: "ออกแบบโมเดลข้อมูลเพื่อการวิเคราะห์ทางธุรกิจ สร้างตัวชี้วัด (KPIs) และรายงานเชิงลึกผ่าน Business Intelligence",
            qual: "เชี่ยวชาญ Data Modeling, ภาษาคำนวณสถิติ (DAX/SQL), การออกแบบ Dashboard และเข้าใจกระบวนการทำงานขององค์กร"
        },
        "ai_engineer": {
            desc: "พัฒนาและปรับปรุงโมเดลประมวลผลข้อมูลขั้นสูง (Deep Learning, NLP, LLM) และเชื่อมต่อเข้ากับระบบประยุกต์",
            qual: "มีพื้นฐานอัลกอริทึม, เฟรมเวิร์ก Deep Learning (TensorFlow/PyTorch), เวกเตอร์ และการนำโมเดลไปใช้งาน (Serving)"
        },
        "frontend_developer": {
            desc: "พัฒนาส่วนติดต่อผู้ใช้ (UI) บนเว็บเบราว์เซอร์ให้ตอบสนองลื่นไหล (Responsive) และเชื่อมต่อ API",
            qual: "เชี่ยวชาญ HTML5, CSS3, JavaScript/TypeScript, ใช้งาน Modern Web Framework (React/Vue) และ Responsive Design"
        },
        "backend_developer": {
            desc: "พัฒนาระบบประมวลผลฝั่งเซิร์ฟเวอร์ ออกแบบ RESTful API จัดการฐานข้อมูลและตรรกะทางธุรกิจ",
            qual: "เข้าใจหลักการ OOP, การออกแบบ RESTful API, การทำงานกับ Database และความปลอดภัยของ Web Services"
        },
        "fullstack_developer": {
            desc: "พัฒนาทั้งระบบหน้าบ้าน (Frontend), ระบบหลังบ้าน (Backend) และดูแลการเชื่อมต่อฐานข้อมูลแบบครบวงจร",
            qual: "มีทักษะครอบคลุมทั้ง Web UI, Server-side Programming, การออกแบบฐานข้อมูล และการใช้ Version Control (Git)"
        },
        "dotnet_developer": {
            desc: "พัฒนาและบำรุงรักษาเว็บแอปพลิเคชันหรือระบบองค์กรด้วยภาษา C# และเฟรมเวิร์ก .NET",
            qual: "เชี่ยวชาญภาษา C#, .NET Core/ASP.NET, Entity Framework, การเชื่อมต่อฐานข้อมูล SQL Server และหลักการ OOP"
        },
        "python_developer": {
            desc: "พัฒนาระบบเว็บแอปพลิเคชัน API หรือระบบประมวลผลอัตโนมัติ (Automation) ด้วยภาษา Python",
            qual: "เชี่ยวชาญไวยากรณ์ภาษา Python, เว็บเฟรมเวิร์ก (FastAPI/Django/Flask), การเขียนสคริปต์ และการจัดการฐานข้อมูล"
        },
        "java_developer": {
            desc: "พัฒนาระบบแอปพลิเคชันระดับองค์กรและไมโครเซอร์วิส (Microservices) ด้วยภาษา Java",
            qual: "เชี่ยวชาญภาษา Java, Spring Boot, การออกแบบเชิงวัตถุ (OOP Design Patterns), Microservices และฐานข้อมูล"
        },
        "devops_cloud": {
            desc: "ออกแบบโครงสร้างพื้นฐานบนคลาวด์ ดูแลระบบ CI/CD Pipeline และบริหารจัดการ Container",
            qual: "เชี่ยวชาญ Cloud Infrastructure (AWS/Azure), Container (Docker/Kubernetes), เครื่องมือ CI/CD และ IaC"
        },
        "qa_tester": {
            desc: "ออกแบบชุดทดสอบ (Test Cases) ดำเนินการทดสอบระบบทั้ง Manual และ Automation เพื่อควบคุมคุณภาพซอฟต์แวร์",
            qual: "เข้าใจวงจรชีวิตการทดสอบ (STLC), การออกแบบกรณีทดสอบ, เครื่องมือทดสอบอัตโนมัติ (Selenium/Postman) และ Bug Tracking"
        },
        "ui_ux_designer": {
            desc: "ออกแบบโครงร่างหน้าจอ (Wireframe), ตัวต้นแบบ (Prototype) และค้นคว้าพฤติกรรมผู้ใช้งาน (User Research)",
            qual: "เชี่ยวชาญเครื่องมือออกแบบ (Figma/Adobe XD), หลักการ User-Centered Design, Usability Testing และ Design System"
        },
        "mobile_developer": {
            desc: "พัฒนาและปรับปรุงแอปพลิเคชันบนระบบปฏิบัติการ iOS หรือ Android",
            qual: "เชี่ยวชาญภาษาและเฟรมเวิร์กมือถือ (Flutter/React Native/Swift/Kotlin), การเรียกใช้ API และ State Management"
        },
        "blockchain": {
            desc: "พัฒนาสัญญาอัจฉริยะ (Smart Contracts) และแอปพลิเคชันแบบกระจายศูนย์ (DApps)",
            qual: "มีความรู้เรื่อง Cryptography, สถาปัตยกรรม Distributed Ledger, การเขียนภาษาเฉพาะ (Solidity) และความปลอดภัย Web3"
        },
        "software_engineer": {
            desc: "ออกแบบโครงสร้างสถาปัตยกรรมซอฟต์แวร์ เขียนโค้ดตามมาตรฐาน และแก้ปัญหาเชิงอัลกอริทึม",
            qual: "เชี่ยวชาญ Data Structures, Algorithms, การเขียนโค้ด Clean Code, การออกแบบระบบ และการทำ Unit Testing"
        }
    },

    getRoleQualifications(title, original_title) {
        const t = `${title || ""} ${original_title || ""}`.toLowerCase();
        
        if (/(ethical hacker|penetration|pentest|hacker)/i.test(t)) return this.ROLE_QUALIFICATIONS["ethical_hacker"];
        if (/(cybersecurity|information security|\bsoc\b|cyber defense|security analyst)/i.test(t)) return this.ROLE_QUALIFICATIONS["cybersecurity"];
        if (/(network engineer|network analyst|noc engineer|network)/i.test(t)) return this.ROLE_QUALIFICATIONS["network_engineer"];
        if (/(system engineer|sysadmin|system administrator)/i.test(t)) return this.ROLE_QUALIFICATIONS["system_engineer"];
        if (/(data science|data scientist)/i.test(t)) return this.ROLE_QUALIFICATIONS["data_scientist"];
        if (/(data analyst|data analytics)/i.test(t)) return this.ROLE_QUALIFICATIONS["data_analyst"];
        if (/(data engineer|big data)/i.test(t)) return this.ROLE_QUALIFICATIONS["data_engineer"];
        if (/(business intelligence|bi analyst|bi developer)/i.test(t)) return this.ROLE_QUALIFICATIONS["bi_analyst"];
        if (/(machine learning|deep learning|ai engineer|ai prompt|artificial intelligence|nlp|llm)/i.test(t)) return this.ROLE_QUALIFICATIONS["ai_engineer"];
        if (/(frontend|front end)/i.test(t)) return this.ROLE_QUALIFICATIONS["frontend_developer"];
        if (/(backend|back end)/i.test(t)) return this.ROLE_QUALIFICATIONS["backend_developer"];
        if (/(fullstack|full stack)/i.test(t)) return this.ROLE_QUALIFICATIONS["fullstack_developer"];
        if (/(\.net|dotnet)/i.test(t)) return this.ROLE_QUALIFICATIONS["dotnet_developer"];
        if (/(python developer|python engineer)/i.test(t)) return this.ROLE_QUALIFICATIONS["python_developer"];
        if (/(java developer|java engineer)/i.test(t)) return this.ROLE_QUALIFICATIONS["java_developer"];
        if (/(devops|cloud|aws|azure|gcp|sre|site reliability|infrastructure)/i.test(t)) return this.ROLE_QUALIFICATIONS["devops_cloud"];
        if (/(qa|quality assurance|tester|testing|test engineer|sdet)/i.test(t)) return this.ROLE_QUALIFICATIONS["qa_tester"];
        if (/(ux|ui\/ux|ui|designer|interaction designer|product designer)/i.test(t)) return this.ROLE_QUALIFICATIONS["ui_ux_designer"];
        if (/(android|ios|mobile|flutter|react native|swift)/i.test(t)) return this.ROLE_QUALIFICATIONS["mobile_developer"];
        if (/(blockchain|solidity|ethereum|web3)/i.test(t)) return this.ROLE_QUALIFICATIONS["blockchain"];
        if (/(software engineer|software developer|programmer)/i.test(t)) return this.ROLE_QUALIFICATIONS["software_engineer"];

        return {
            desc: "ออกแบบ พัฒนา และดูแลระบบสารสนเทศตามมาตรฐานวิชาชีพไอทีและข้อกำหนดขององค์กร",
            qual: "มีความรู้ความเข้าใจในกระบวนการพัฒนาซอฟต์แวร์ การจัดการข้อมูล และการแก้ปัญหาเชิงตรรกะ"
        };
    },

    formatExperienceYears(years) {
        if (!years) return "0-1 ปี";
        let clean = String(years).replace(/years?|yrs?|yr/gi, "").trim();
        return clean ? `${clean} ปี` : "0-1 ปี";
    },

    renderResponsibilities(resps) {
        let items = [];
        if (Array.isArray(resps)) {
            items = resps;
        } else if (typeof resps === 'string') {
            items = resps.split(/[;\n\r|•]+/).map(s => s.trim()).filter(Boolean);
        }

        const cleanItems = items.filter(item => item.length > 8).slice(0, 2);
        if (cleanItems.length === 0) {
            return `<li class="text-slate-500 italic text-xs">ปฏิบัติหน้าที่ตามที่ได้รับมอบหมาย</li>`;
        }

        return cleanItems.map(item => `
            <li class="flex items-start gap-1.5 text-xs text-slate-600 leading-snug">
                <span class="text-rose-500 font-bold">•</span>
                <span>${ApiClient.escapeHTML(item)}</span>
            </li>
        `).join('');
    },

    getReadinessStatus(readiness) {
        const val = Number(readiness) || 0;
        if (val >= 80) {
            return {
                level: 'high',
                text: 'พร้อมมาก',
                shortText: 'พร้อมมาก',
                badgeBg: 'bg-emerald-50 text-emerald-800 border-emerald-300',
                pillBg: 'bg-emerald-50 text-emerald-800 border-emerald-200',
                textColor: 'text-emerald-700',
                iconClass: 'fa-solid fa-circle-check text-emerald-600'
            };
        } else if (val >= 50) {
            return {
                level: 'medium',
                text: 'พร้อมปานกลาง',
                shortText: 'พร้อมปานกลาง',
                badgeBg: 'bg-rose-50 text-rose-800 border-rose-300',
                pillBg: 'bg-rose-50 text-rose-800 border-rose-200',
                textColor: 'text-rose-600',
                iconClass: 'fa-solid fa-circle-notch text-rose-500'
            };
        } else {
            return {
                level: 'low',
                text: 'ยังไม่พร้อม',
                shortText: 'ยังไม่พร้อม',
                badgeBg: 'bg-slate-100 text-slate-700 border-slate-300',
                pillBg: 'bg-slate-50 text-slate-700 border-slate-200',
                textColor: 'text-slate-600',
                iconClass: 'fa-solid fa-circle-pause text-slate-400'
            };
        }
    },

    ROLE_THEMES: {
        'G1': {
            roleId: 'G1',
            icon: 'fa-solid fa-code',
            gradient: 'from-emerald-500 to-teal-600',
            barGradient: 'bg-gradient-to-r from-emerald-500 to-teal-500',
            badgeBg: 'bg-emerald-50 text-emerald-700 border-emerald-300',
            cardBorder: 'border-emerald-200 hover:border-emerald-300',
            cardBg: 'bg-gradient-to-br from-emerald-50/40 via-white to-teal-50/20',
            accentText: 'text-emerald-700',
            iconBg: 'bg-emerald-600 text-white',
            tagLabel: 'Software Development'
        },
        'G2': {
            roleId: 'G2',
            icon: 'fa-solid fa-database',
            gradient: 'from-amber-500 to-yellow-600',
            barGradient: 'bg-gradient-to-r from-amber-500 to-yellow-500',
            badgeBg: 'bg-amber-50 text-amber-800 border-amber-300',
            cardBorder: 'border-amber-200 hover:border-amber-300',
            cardBg: 'bg-gradient-to-br from-amber-50/40 via-white to-yellow-50/20',
            accentText: 'text-amber-700',
            iconBg: 'bg-amber-600 text-white',
            tagLabel: 'Database Administration'
        },
        'G3': {
            roleId: 'G3',
            icon: 'fa-solid fa-chart-pie',
            gradient: 'from-indigo-500 to-blue-600',
            barGradient: 'bg-gradient-to-r from-indigo-500 to-blue-500',
            badgeBg: 'bg-indigo-50 text-indigo-700 border-indigo-300',
            cardBorder: 'border-indigo-200 hover:border-indigo-300',
            cardBg: 'bg-gradient-to-br from-indigo-50/40 via-white to-blue-50/20',
            accentText: 'text-indigo-700',
            iconBg: 'bg-indigo-600 text-white',
            tagLabel: 'System Analyst / Designer'
        },
        'G4': {
            roleId: 'G4',
            icon: 'fa-solid fa-headset',
            gradient: 'from-slate-600 to-slate-800',
            barGradient: 'bg-gradient-to-r from-slate-600 to-slate-700',
            badgeBg: 'bg-slate-100 text-slate-800 border-slate-300',
            cardBorder: 'border-slate-300 hover:border-slate-400',
            cardBg: 'bg-gradient-to-br from-slate-50/40 via-white to-slate-100/20',
            accentText: 'text-slate-800',
            iconBg: 'bg-slate-700 text-white',
            tagLabel: 'Computer Technical Officer'
        },
        'G5': {
            roleId: 'G5',
            icon: 'fa-solid fa-server',
            gradient: 'from-blue-600 to-cyan-700',
            barGradient: 'bg-gradient-to-r from-blue-600 to-cyan-600',
            badgeBg: 'bg-blue-50 text-blue-700 border-blue-300',
            cardBorder: 'border-blue-200 hover:border-blue-300',
            cardBg: 'bg-gradient-to-br from-blue-50/40 via-white to-cyan-50/20',
            accentText: 'text-blue-700',
            iconBg: 'bg-blue-600 text-white',
            tagLabel: 'System Administrator'
        },
        'G6': {
            roleId: 'G6',
            icon: 'fa-solid fa-laptop-code',
            gradient: 'from-pink-500 to-rose-600',
            barGradient: 'bg-gradient-to-r from-pink-500 to-rose-500',
            badgeBg: 'bg-rose-50 text-rose-700 border-rose-300',
            cardBorder: 'border-rose-200 hover:border-rose-300',
            cardBg: 'bg-gradient-to-br from-rose-50/40 via-white to-pink-50/20',
            accentText: 'text-rose-700',
            iconBg: 'bg-rose-600 text-white',
            tagLabel: 'Web Developer'
        },
        'G7': {
            roleId: 'G7',
            icon: 'fa-solid fa-diagram-project',
            gradient: 'from-orange-500 to-red-600',
            barGradient: 'bg-gradient-to-r from-orange-500 to-red-500',
            badgeBg: 'bg-orange-50 text-orange-700 border-orange-300',
            cardBorder: 'border-orange-200 hover:border-orange-300',
            cardBg: 'bg-gradient-to-br from-orange-50/40 via-white to-red-50/20',
            accentText: 'text-orange-700',
            iconBg: 'bg-orange-600 text-white',
            tagLabel: 'IT Project Assistant'
        },
        'G8': {
            roleId: 'G8',
            icon: 'fa-solid fa-palette',
            gradient: 'from-purple-500 to-violet-600',
            barGradient: 'bg-gradient-to-r from-purple-500 to-violet-500',
            badgeBg: 'bg-purple-50 text-purple-700 border-purple-300',
            cardBorder: 'border-purple-200 hover:border-purple-300',
            cardBg: 'bg-gradient-to-br from-purple-50/40 via-white to-violet-50/20',
            accentText: 'text-purple-700',
            iconBg: 'bg-purple-600 text-white',
            tagLabel: 'Content Creator'
        },
        '8.1': { roleId: 'G4', icon: 'fa-solid fa-headset', gradient: 'from-slate-600 to-slate-800', barGradient: 'bg-gradient-to-r from-slate-600 to-slate-700', badgeBg: 'bg-slate-100 text-slate-800 border-slate-300', cardBorder: 'border-slate-300', cardBg: 'bg-white', accentText: 'text-slate-800', iconBg: 'bg-slate-700 text-white', tagLabel: 'Computer Technical Officer' },
        '8.2': { roleId: 'G5', icon: 'fa-solid fa-server', gradient: 'from-blue-600 to-cyan-700', barGradient: 'bg-gradient-to-r from-blue-600 to-cyan-600', badgeBg: 'bg-blue-50 text-blue-700 border-blue-300', cardBorder: 'border-blue-200', cardBg: 'bg-white', accentText: 'text-blue-700', iconBg: 'bg-blue-600 text-white', tagLabel: 'System Administrator' },
        '8.3': { roleId: 'G8', icon: 'fa-solid fa-palette', gradient: 'from-purple-500 to-violet-600', barGradient: 'bg-gradient-to-r from-purple-500 to-violet-500', badgeBg: 'bg-purple-50 text-purple-700 border-purple-300', cardBorder: 'border-purple-200', cardBg: 'bg-white', accentText: 'text-purple-700', iconBg: 'bg-purple-600 text-white', tagLabel: 'Content Creator' },
        '8.4': { roleId: 'G7', icon: 'fa-solid fa-diagram-project', gradient: 'from-orange-500 to-red-600', barGradient: 'bg-gradient-to-r from-orange-500 to-red-500', badgeBg: 'bg-orange-50 text-orange-700 border-orange-300', cardBorder: 'border-orange-200', cardBg: 'bg-white', accentText: 'text-orange-700', iconBg: 'bg-orange-600 text-white', tagLabel: 'IT Project Assistant' },
        '8.5': { roleId: 'G3', icon: 'fa-solid fa-chart-pie', gradient: 'from-indigo-500 to-blue-600', barGradient: 'bg-gradient-to-r from-indigo-500 to-blue-500', badgeBg: 'bg-indigo-50 text-indigo-700 border-indigo-300', cardBorder: 'border-indigo-200', cardBg: 'bg-white', accentText: 'text-indigo-700', iconBg: 'bg-indigo-600 text-white', tagLabel: 'System Analyst / Designer' },
        '8.6': { roleId: 'G1', icon: 'fa-solid fa-code', gradient: 'from-emerald-500 to-teal-600', barGradient: 'bg-gradient-to-r from-emerald-500 to-teal-500', badgeBg: 'bg-emerald-50 text-emerald-700 border-emerald-300', cardBorder: 'border-emerald-200', cardBg: 'bg-white', accentText: 'text-emerald-700', iconBg: 'bg-emerald-600 text-white', tagLabel: 'Software Development' },
        '8.7': { roleId: 'G6', icon: 'fa-solid fa-laptop-code', gradient: 'from-pink-500 to-rose-600', barGradient: 'bg-gradient-to-r from-pink-500 to-rose-500', badgeBg: 'bg-rose-50 text-rose-700 border-rose-300', cardBorder: 'border-rose-200', cardBg: 'bg-white', accentText: 'text-rose-700', iconBg: 'bg-rose-600 text-white', tagLabel: 'Web Developer' },
        '8.8': { roleId: 'G2', icon: 'fa-solid fa-database', gradient: 'from-amber-500 to-yellow-600', barGradient: 'bg-gradient-to-r from-amber-500 to-yellow-500', badgeBg: 'bg-amber-50 text-amber-800 border-amber-300', cardBorder: 'border-amber-200', cardBg: 'bg-white', accentText: 'text-amber-700', iconBg: 'bg-amber-600 text-white', tagLabel: 'Database Administrator' }
    },

    getRoleTheme(roleId) {
        if (!roleId) return this.ROLE_THEMES['G1'];
        const r = String(roleId).toUpperCase().trim();
        const aliasMap = {
            '8.1': 'G4', '8.2': 'G5', '8.3': 'G8', '8.4': 'G7',
            '8.5': 'G3', '8.6': 'G1', '8.7': 'G6', '8.8': 'G2'
        };
        const mapped = aliasMap[roleId] || r;
        return this.ROLE_THEMES[mapped] || this.ROLE_THEMES[roleId] || this.ROLE_THEMES['G1'];
    }
};
