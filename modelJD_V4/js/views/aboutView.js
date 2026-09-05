/**
 * About View: System Specs, Model Details, and Dataset Statistics
 * Design: Modern White Theme with Accent Pink (SkillMatch IT)
 */
window.AboutView = {
    render() {
        return `
        <div class="space-y-8 view-transition-in">
            <!-- Header Banner -->
            <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm border-t-4 border-t-rose-500 space-y-4">
                <span class="text-xs font-black tracking-wider uppercase text-rose-700 bg-rose-50 border border-rose-200 px-3 py-1 rounded-xl inline-flex items-center gap-1.5 shadow-2xs">
                    <span>ℹ️</span> ข้อมูลระบบและสถิติ
                </span>
                <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2 flex items-center gap-2">
                    <span>⚡</span> System Architecture & ML Specifications
                </h2>
                <p class="text-xs sm:text-sm text-slate-500 font-medium mt-1">
                    ระบบวิเคราะห์ทักษะและจับคู่ตำแหน่งงานไอทีด้วยโมเดลปัญญาประดิษฐ์ผสานข้อมูลตลาดแรงงานจริงในประเทศไทย
                </p>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                <div class="glass-card hover-lift p-6 rounded-3xl border border-slate-200/90 text-center space-y-1.5">
                    <div class="text-3xl font-black text-rose-600 font-english">8</div>
                    <div class="text-xs font-bold text-slate-800">สายงานไอทีหลัก</div>
                    <div class="text-[10px] text-slate-400 font-medium">Standard IT Career Tracks</div>
                </div>
                <div class="glass-card hover-lift p-6 rounded-3xl border border-slate-200/90 text-center space-y-1.5">
                    <div class="text-3xl font-black text-pink-600 font-english">1,600+</div>
                    <div class="text-xs font-bold text-slate-800">คลังทักษะไอทีมาตรฐาน</div>
                    <div class="text-[10px] text-slate-400 font-medium">Master Skills Taxonomy</div>
                </div>
                <div class="glass-card hover-lift p-6 rounded-3xl border border-slate-200/90 text-center space-y-1.5">
                    <div class="text-3xl font-black text-rose-700 font-english">100%</div>
                    <div class="text-xs font-bold text-slate-800">ตลาดงานจริงในไทย</div>
                    <div class="text-[10px] text-slate-400 font-medium">Thai IT Job Market Context</div>
                </div>
                <div class="glass-card hover-lift p-6 rounded-3xl border border-slate-200/90 text-center space-y-1.5">
                    <div class="text-3xl font-black text-slate-800 font-english">3-D</div>
                    <div class="text-xs font-bold text-slate-800">Orthogonal Features</div>
                    <div class="text-[10px] text-slate-400 font-medium">Explainable ML Vector</div>
                </div>
            </div>

            <!-- Career Tracks Table -->
            <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm space-y-4">
                <h3 class="font-black text-base text-slate-900 flex items-center gap-2">
                    <i class="fa-solid fa-briefcase text-rose-600"></i>
                    <span>สายงานด้านเทคโนโลยีสารสนเทศมาตรฐานในระบบ</span>
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-xs text-left text-slate-600">
                        <thead>
                            <tr class="border-b border-slate-200 text-slate-900 font-black">
                                <th class="py-2.5 w-1/3">ชื่อสายงาน</th>
                                <th class="py-2.5">ชื่อมาตรฐานสากล (Industry Standard)</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 font-medium">
                            <tr>
                                <td class="py-2.5 font-bold text-slate-900">เจ้าหน้าที่คอมพิวเตอร์</td>
                                <td class="py-2.5">Computer Officer / IT Support Specialist</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 font-bold text-slate-900">ผู้ดูแลระบบเครือข่ายคอมพิวเตอร์</td>
                                <td class="py-2.5">Network Administrator / System Engineer</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 font-bold text-slate-900">นักพัฒนาและออกแบบสื่อผสม</td>
                                <td class="py-2.5">Multimedia Designer & Developer (UI/UX / Game)</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 font-bold text-slate-900">นักจัดการโครงการสารสนเทศ</td>
                                <td class="py-2.5">IT Project Manager / Coordinator / Scrum Master</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 font-bold text-slate-900">นักวิเคราะห์และออกแบบระบบงาน</td>
                                <td class="py-2.5">System Analyst (SA) / Business Analyst (BA)</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 font-bold text-slate-900">นักพัฒนาซอฟต์แวร์</td>
                                <td class="py-2.5">Software Developer / Engineer / Programmer</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 font-bold text-slate-900">นักออกแบบและพัฒนาเว็บไซต์</td>
                                <td class="py-2.5">Web Designer & Developer / Frontend Web</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 font-bold text-slate-900">ผู้เชี่ยวชาญด้านเทคโนโลยีสารสนเทศ</td>
                                <td class="py-2.5">Specialized IT Professional (AI / Cloud / Data)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Specifications Table -->
            <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm space-y-4">
                <h3 class="font-black text-base text-slate-900 flex items-center gap-2">
                    <i class="fa-solid fa-gears text-rose-600"></i>
                    <span>รายละเอียดโมเดลและการประมวลผล (Machine Learning Specs)</span>
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-xs text-left text-slate-600">
                        <tbody class="divide-y divide-slate-100">
                            <tr>
                                <td class="py-3.5 font-bold text-slate-900 w-1/3">Algorithm</td>
                                <td class="py-3.5">Calibrated Logistic Regression with StandardScaler Pipeline</td>
                            </tr>
                            <tr>
                                <td class="py-3.5 font-bold text-slate-900">Vector Space Model</td>
                                <td class="py-3.5">TF-IDF Vectorizer (sublinear_tf=True, technical token extraction)</td>
                            </tr>
                            <tr>
                                <td class="py-3.5 font-bold text-slate-900">Feature Dimensions</td>
                                <td class="py-3.5">1) Cosine TF-IDF Similarity, 2) Set Overlap Ratio, 3) Exact Match Count</td>
                            </tr>
                            <tr>
                                <td class="py-3.5 font-bold text-slate-900">Skill Gap Engine</td>
                                <td class="py-3.5">Pure Set Theory Mathematical Difference (Job_Skills \\ User_Skills)</td>
                            </tr>
                            <tr>
                                <td class="py-3.5 font-bold text-slate-900">Backend API Framework</td>
                                <td class="py-3.5">FastAPI (latest stable) with Uvicorn ASGI Server and Static Mounting</td>
                            </tr>
                            <tr>
                                <td class="py-3.5 font-bold text-slate-900">Frontend Architecture</td>
                                <td class="py-3.5">Modular SPA (Vanilla JS + TailwindCSS + FontAwesome + SweetAlert2)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- API Reference -->
            <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm space-y-4">
                <h3 class="font-black text-base text-slate-900 flex items-center gap-2">
                    <i class="fa-solid fa-plug text-rose-600"></i>
                    <span>RESTful API Endpoints</span>
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                    <div class="p-4 bg-slate-50 rounded-2xl border border-slate-200">
                        <div class="font-mono font-bold text-rose-600">POST /recommend</div>
                        <p class="text-slate-600 mt-1">ประมวลผลคำนวณและจัดอันดับงานที่ตรงกับทักษะ</p>
                    </div>
                    <div class="p-4 bg-slate-50 rounded-2xl border border-slate-200">
                        <div class="font-mono font-bold text-rose-600">GET /api/roles</div>
                        <p class="text-slate-600 mt-1">ดึงรายชื่อสายงานไอทีหลักพร้อมทักษะแกนหลัก</p>
                    </div>
                    <div class="p-4 bg-slate-50 rounded-2xl border border-slate-200">
                        <div class="font-mono font-bold text-rose-600">GET /api/skills</div>
                        <p class="text-slate-600 mt-1">ดึงรายการคำศัพท์ทักษะมาตรฐาน 1,600+ คำ</p>
                    </div>
                </div>
            </div>
        </div>
        `;
    }
};
