/**
 * About View: System Specs, Model Details, and Dataset Statistics
 * Design: Modern White Theme with Accent Pink
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
                    ข้อมูลทางเทคนิคของโมเดลปัญญาประดิษฐ์และฐานข้อมูลตำแหน่งงานไอที
                </p>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                <div class="glass-card hover-lift p-6 rounded-3xl border border-slate-200/90 text-center space-y-1.5">
                    <div class="text-3xl font-black text-rose-600 font-english">1,068</div>
                    <div class="text-xs font-bold text-slate-800">ตำแหน่งงานใน Dataset</div>
                    <div class="text-[10px] text-slate-400 font-medium">Kaggle IT Jobs Dataset</div>
                </div>
                <div class="glass-card hover-lift p-6 rounded-3xl border border-slate-200/90 text-center space-y-1.5">
                    <div class="text-3xl font-black text-pink-600 font-english">1,600+</div>
                    <div class="text-xs font-bold text-slate-800">คำศัพท์ทักษะมาตรฐาน</div>
                    <div class="text-[10px] text-slate-400 font-medium">Atomic IT Skills</div>
                </div>
                <div class="glass-card hover-lift p-6 rounded-3xl border border-slate-200/90 text-center space-y-1.5">
                    <div class="text-3xl font-black text-rose-700 font-english">45</div>
                    <div class="text-xs font-bold text-slate-800">สายงานไอทียอดนิยม</div>
                    <div class="text-[10px] text-slate-400 font-medium">Standardized IT Roles</div>
                </div>
                <div class="glass-card hover-lift p-6 rounded-3xl border border-slate-200/90 text-center space-y-1.5">
                    <div class="text-3xl font-black text-slate-800 font-english">3-D</div>
                    <div class="text-xs font-bold text-slate-800">Orthogonal Features</div>
                    <div class="text-[10px] text-slate-400 font-medium">Explainable AI Vectors</div>
                </div>
            </div>

            <!-- Specifications Table -->
            <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm space-y-4">
                <h3 class="font-black text-base text-slate-900 flex items-center gap-2">
                    <span>⚙️</span> รายละเอียดโมเดลและการประมวลผล (Machine Learning Specs)
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-xs text-left text-slate-600">
                        <tbody class="divide-y divide-slate-100">
                            <tr>
                                <td class="py-3.5 font-bold text-slate-900 w-1/3">Algorithm</td>
                                <td class="py-3.5">Supervised Logistic Regression with L2 Regularization (C=1.0)</td>
                            </tr>
                            <tr>
                                <td class="py-3.5 font-bold text-slate-900">Vector Space Model</td>
                                <td class="py-3.5">TF-IDF Vectorizer (max_features=5000, sublinear_tf=True, token_pattern=r'(?u)\\b[\\w+#.-]+\\b')</td>
                            </tr>
                            <tr>
                                <td class="py-3.5 font-bold text-slate-900">Feature Dimensions</td>
                                <td class="py-3.5">1) Cosine TF-IDF Similarity, 2) Set Overlap Ratio, 3) Exact Match Count</td>
                            </tr>
                            <tr>
                                <td class="py-3.5 font-bold text-slate-900">Diversity Filter</td>
                                <td class="py-3.5">Career Family Clustering (21 Families) ป้องกันการผูกขาดในผลลัพธ์ Top 5</td>
                            </tr>
                            <tr>
                                <td class="py-3.5 font-bold text-slate-900">Skill Gap Engine</td>
                                <td class="py-3.5">Pure Set Theory Mathematical Difference (Job_Skills \\ User_Skills)</td>
                            </tr>
                            <tr>
                                <td class="py-3.5 font-bold text-slate-900">Backend API Framework</td>
                                <td class="py-3.5">FastAPI 3.0.0 (Uvicorn ASGI Server) with CORS & Static Mounting</td>
                            </tr>
                            <tr>
                                <td class="py-3.5 font-bold text-slate-900">Frontend Architecture</td>
                                <td class="py-3.5">Modular Client-Side Router SPA (Vanilla JS + TailwindCSS + Google Fonts)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- API Reference -->
            <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm space-y-4">
                <h3 class="font-black text-base text-slate-900 flex items-center gap-2">
                    <span>🔌</span> RESTful API Endpoints
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                    <div class="p-4 bg-slate-50 rounded-2xl border border-slate-200">
                        <div class="font-mono font-bold text-rose-600">POST /recommend</div>
                        <p class="text-slate-600 mt-1">ประมวลผลคำนวณและจัดอันดับงาน (Dual-Section Output)</p>
                    </div>
                    <div class="p-4 bg-slate-50 rounded-2xl border border-slate-200">
                        <div class="font-mono font-bold text-rose-600">GET /api/skills</div>
                        <p class="text-slate-600 mt-1">ดึงรายการคำศัพท์ทักษะมาตรฐาน 1,600+ คำ</p>
                    </div>
                    <div class="p-4 bg-slate-50 rounded-2xl border border-slate-200">
                        <div class="font-mono font-bold text-rose-600">GET /api/roles</div>
                        <p class="text-slate-600 mt-1">ดึงรายชื่อตำแหน่งงานมาตรฐาน 45 สายงาน</p>
                    </div>
                    <div class="p-4 bg-slate-50 rounded-2xl border border-slate-200">
                        <div class="font-mono font-bold text-rose-600">GET /ui</div>
                        <p class="text-slate-600 mt-1">เปิดหน้าเว็บแอปพลิเคชัน Single Page Application</p>
                    </div>
                </div>
            </div>
        </div>
        `;
    },

    onMount() {}
};
