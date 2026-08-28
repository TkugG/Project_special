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

    renderKeywordBadges(keywords, title, expLevel) {
        let list = [];
        if (Array.isArray(keywords)) {
            list = keywords;
        } else if (typeof keywords === 'string') {
            list = keywords.split(/[;,|]+/).map(k => k.trim()).filter(Boolean);
        }
        if (!list || list.length === 0) return '';

        const titleNorm = (title || "").toLowerCase().replace(/[^a-z0-9]/g, '');
        const expNorm = (expLevel || "").toLowerCase().replace(/[^a-z0-9]/g, '');

        const filtered = list.filter(k => {
            const kNorm = k.toLowerCase().replace(/[^a-z0-9]/g, '');
            if (!kNorm) return false;
            if (titleNorm.includes(kNorm) || kNorm.includes(titleNorm)) return false;
            if (expNorm.includes(kNorm) || kNorm.includes(expNorm)) return false;
            if (["fresher", "junior", "midsenior", "senior", "entrylevel", "intern", "internship"].includes(kNorm)) return false;
            return true;
        });

        if (filtered.length === 0) return '';
        return filtered.slice(0, 3).map(k => `
            <span class="inline-flex items-center gap-1 text-[11px] font-bold bg-rose-50 text-rose-700 border border-rose-200/90 px-2 py-0.5 rounded-md shadow-2xs">
                <i class="fa-solid fa-tag text-[9px] text-rose-400"></i> ${ApiClient.escapeHTML(k)}
            </span>
        `).join('');
    },

    renderResponsibilities(resps) {
        let items = [];
        if (Array.isArray(resps)) {
            items = resps;
        } else if (typeof resps === 'string') {
            items = resps.split(/[;\n\r|•]+/).map(s => s.trim()).filter(Boolean);
        }
        if (!items || items.length === 0) {
            return `<li class="text-slate-400 italic">เรียนรู้และปฏิบัติงานตามที่ได้รับมอบหมายในทีม</li>`;
        }
        return items.slice(0, 4).map(item => `
            <li class="flex items-start gap-2">
                <i class="fa-solid fa-check text-rose-500 text-xs mt-1 shrink-0"></i>
                <span class="leading-relaxed text-slate-700">${ApiClient.escapeHTML(item)}</span>
            </li>
        `).join('');
    },

    getReadinessStatus(readiness) {
        const val = Number(readiness) || 0;
        if (val >= 80) {
            return {
                level: 'high',
                text: 'พร้อมมาก (ทักษะตรง พร้อมยื่นสมัคร)',
                shortText: 'พร้อมมาก',
                badgeBg: 'bg-emerald-50 text-emerald-800 border-emerald-300',
                pillBg: 'bg-emerald-50/90 text-emerald-800 border-emerald-200/90',
                textColor: 'text-emerald-700',
                iconClass: 'fa-solid fa-circle-check text-emerald-600'
            };
        } else if (val >= 50) {
            return {
                level: 'medium',
                text: 'พร้อมปานกลาง (มีพื้นฐาน ฝึกเพิ่ม 1-2 ทักษะ)',
                shortText: 'พร้อมปานกลาง',
                badgeBg: 'bg-rose-50 text-rose-800 border-rose-300',
                pillBg: 'bg-rose-50/90 text-rose-800 border-rose-200/90',
                textColor: 'text-rose-600',
                iconClass: 'fa-solid fa-circle-notch text-rose-500'
            };
        } else {
            return {
                level: 'low',
                text: 'ยังไม่พร้อม (ต้องเรียนรู้และเก็บทักษะเพิ่ม)',
                shortText: 'ยังไม่พร้อม',
                badgeBg: 'bg-slate-100 text-slate-700 border-slate-300',
                pillBg: 'bg-slate-50 text-slate-700 border-slate-200',
                textColor: 'text-slate-600',
                iconClass: 'fa-solid fa-circle-pause text-slate-400'
            };
        }
    },

    showPrepGuide(jobTitle, missingSkills) {
        let missingList = Array.isArray(missingSkills) ? missingSkills : [];
        let missingHtml = missingList.length > 0 
            ? `<div class="mt-3 text-left bg-rose-50/80 p-4 rounded-2xl border border-rose-200">
                 <div class="text-xs font-bold text-rose-900 mb-2 flex items-center gap-2">
                   <i class="fa-solid fa-bullseye text-rose-600"></i>
                   <span>ทักษะสำคัญที่ควรฝึกทำ Project เพิ่ม:</span>
                 </div>
                 <div class="flex flex-wrap gap-1.5">
                   ${missingList.map(s => `<span class="bg-white text-rose-950 px-2.5 py-1 rounded-lg border border-rose-300 text-xs font-bold shadow-2xs">${ApiClient.escapeHTML(s)}</span>`).join('')}
                 </div>
               </div>`
            : `<div class="mt-3 text-left bg-emerald-50 p-3.5 rounded-2xl border border-emerald-200 text-xs font-bold text-emerald-800 flex items-center gap-2">
                 <i class="fa-solid fa-circle-check text-emerald-600 text-sm"></i>
                 <span>ทักษะของคุณครบถ้วนมาก! มั่นใจในการยื่นเรซูเม่ได้เลย</span>
               </div>`;

        Swal.fire({
            title: `<div class="text-lg font-black text-slate-900 flex items-center justify-center gap-2">
                      <i class="fa-solid fa-rocket text-rose-600"></i>
                      <span>แนวทางเตรียมตัวสำหรับ <span class="text-rose-600">${ApiClient.escapeHTML(jobTitle)}</span></span>
                    </div>`,
            html: `
                <div class="text-xs text-slate-600 text-left space-y-3 mt-2">
                    <div class="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs">
                        <p class="font-bold text-slate-900 mb-2 flex items-center gap-2">
                          <i class="fa-solid fa-list-check text-rose-500"></i>
                          <span>Checklist สำหรับนักศึกษา/ผู้สมัครงาน:</span>
                        </p>
                        <ul class="space-y-2 pl-2 text-slate-700">
                            <li class="flex items-start gap-2">
                              <i class="fa-solid fa-chevron-right text-rose-500 text-[10px] mt-1"></i>
                              <span>สร้าง <strong>Portfolio / Mini Project</strong> บน GitHub ที่ใช้งานทักษะหลัก</span>
                            </li>
                            <li class="flex items-start gap-2">
                              <i class="fa-solid fa-chevron-right text-rose-500 text-[10px] mt-1"></i>
                              <span>ฝึกตอบคำถาม <strong>Behavioral & Technical Questions</strong> จากโครงงานที่ทำ</span>
                            </li>
                            <li class="flex items-start gap-2">
                              <i class="fa-solid fa-chevron-right text-rose-500 text-[10px] mt-1"></i>
                              <span>ไฮไลท์ทักษะที่ตรงกันใน <strong>Resume / Transcript</strong> ให้เห็นเด่นชัด</span>
                            </li>
                        </ul>
                    </div>
                    ${missingHtml}
                </div>
            `,
            confirmButtonText: 'เข้าใจแล้ว พร้อมลุย! ✨',
            confirmButtonColor: '#e11d48',
            customClass: {
                popup: 'rounded-3xl p-6 border border-rose-100 shadow-2xl',
                confirmButton: 'glow-btn-pink rounded-xl px-6 py-2.5 font-bold text-xs shadow-md'
            }
        });
    }
};
