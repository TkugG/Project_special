/**
 * Roadmap View: Machine Learning Pipeline Architecture & ITPE Syllabus
 * Design: Modern White Theme with Accent Pink
 */
window.RoadmapView = {
    render() {
        return `
        <div class="space-y-8 view-transition-in">
            <!-- Header Banner -->
            <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm border-t-4 border-t-rose-500 space-y-4">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <span class="text-xs font-black tracking-wider uppercase text-rose-700 bg-rose-50 border border-rose-200 px-3 py-1 rounded-xl inline-flex items-center gap-1.5 shadow-2xs">
                            <span>🧠</span> สถาปัตยกรรมโมเดลและการเรียนรู้
                        </span>
                        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-2 flex items-center gap-2">
                            <span>📐</span> End-to-End ML Pipeline Architecture
                        </h2>
                        <p class="text-xs sm:text-sm text-slate-500 font-medium mt-1">
                            ผังการทำงาน 5 ขั้นตอนของระบบ AI Job Recommendation และการเชื่อมโยงกับกรอบมาตรฐานสมรรถนะไอที
                        </p>
                    </div>
                </div>
            </div>

            <!-- 5-Step Pipeline Cards -->
            <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
                <!-- Step 1 -->
                <div class="glass-card hover-lift rounded-3xl p-5 shadow-sm border border-slate-200/90 space-y-3 flex flex-col justify-between">
                    <div>
                        <div class="w-10 h-10 rounded-2xl bg-rose-100 text-rose-600 flex items-center justify-center font-black text-base shadow-2xs mb-3">1</div>
                        <h3 class="font-black text-sm text-slate-900">Data Normalization</h3>
                        <p class="text-xs text-slate-600 font-medium mt-1 leading-relaxed">
                            สกัดคำศัพท์ 1,600+ ทักษะมาตรฐาน (Atomic Skills) และทำความสะอาดข้อความขยะ
                        </p>
                    </div>
                    <span class="text-[11px] font-bold text-rose-700 bg-rose-50 px-2.5 py-1 rounded-lg border border-rose-200">Regex & Tokenizer</span>
                </div>

                <!-- Step 2 -->
                <div class="glass-card hover-lift rounded-3xl p-5 shadow-sm border border-slate-200/90 space-y-3 flex flex-col justify-between">
                    <div>
                        <div class="w-10 h-10 rounded-2xl bg-pink-100 text-pink-600 flex items-center justify-center font-black text-base shadow-2xs mb-3">2</div>
                        <h3 class="font-black text-sm text-slate-900">3D Vector Extraction</h3>
                        <p class="text-xs text-slate-600 font-medium mt-1 leading-relaxed">
                            สร้าง 3 ฟีเจอร์อิสระ: TF-IDF Cosine, Coverage Ratio, และ Exact Match Count
                        </p>
                    </div>
                    <span class="text-[11px] font-bold text-pink-700 bg-pink-50 px-2.5 py-1 rounded-lg border border-pink-200">Orthogonal Features</span>
                </div>

                <!-- Step 3 -->
                <div class="glass-card hover-lift rounded-3xl p-5 shadow-sm border border-slate-200/90 space-y-3 flex flex-col justify-between">
                    <div>
                        <div class="w-10 h-10 rounded-2xl bg-rose-500 text-white flex items-center justify-center font-black text-base shadow-md mb-3">3</div>
                        <h3 class="font-black text-sm text-slate-900">Logistic Regression</h3>
                        <p class="text-xs text-slate-600 font-medium mt-1 leading-relaxed">
                            ทำนายความน่าจะเป็นและคำนวณคะแนนความเหมาะสม (Match Score %)
                        </p>
                    </div>
                    <span class="text-[11px] font-bold text-rose-700 bg-rose-50 px-2.5 py-1 rounded-lg border border-rose-200">Scikit-Learn Model</span>
                </div>

                <!-- Step 4 -->
                <div class="glass-card hover-lift rounded-3xl p-5 shadow-sm border border-slate-200/90 space-y-3 flex flex-col justify-between">
                    <div>
                        <div class="w-10 h-10 rounded-2xl bg-slate-100 text-slate-700 flex items-center justify-center font-black text-base shadow-2xs mb-3">4</div>
                        <h3 class="font-black text-sm text-slate-900">Diversity Filter</h3>
                        <p class="text-xs text-slate-600 font-medium mt-1 leading-relaxed">
                            กระจายความหลากหลายของสายงาน 21 กลุ่ม ป้องกันการกระจุกตัวใน Top 5
                        </p>
                    </div>
                    <span class="text-[11px] font-bold text-slate-700 bg-slate-50 px-2.5 py-1 rounded-lg border border-slate-200">Career Family Filter</span>
                </div>

                <!-- Step 5 -->
                <div class="glass-card hover-lift rounded-3xl p-5 shadow-sm border border-slate-200/90 space-y-3 flex flex-col justify-between">
                    <div>
                        <div class="w-10 h-10 rounded-2xl bg-rose-100 text-rose-700 flex items-center justify-center font-black text-base shadow-2xs mb-3">5</div>
                        <h3 class="font-black text-sm text-slate-900">Skill Gap Analysis</h3>
                        <p class="text-xs text-slate-600 font-medium mt-1 leading-relaxed">
                            ประเมินความพร้อมและชี้เป้าทักษะที่ขาดด้วยทฤษฎีเซต (Intersection & Difference)
                        </p>
                    </div>
                    <span class="text-[11px] font-bold text-rose-700 bg-rose-50 px-2.5 py-1 rounded-lg border border-rose-200">Set Theory Gap</span>
                </div>
            </div>

            <!-- Mathematical Formulation & Explainable AI -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Mathematical Formulation -->
                <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm space-y-4">
                    <h3 class="font-black text-lg text-slate-900 flex items-center gap-2">
                        <span>🔢</span> 3-Dimensional Feature Representation
                    </h3>
                    <p class="text-xs text-slate-600 leading-relaxed font-medium">
                        เวกเตอร์คุณลักษณะถูกสร้างขึ้นเพื่อลด Bias และสร้างความโปร่งใส (Explainable AI):
                    </p>
                    <div class="space-y-3 text-xs">
                        <div class="bg-slate-50 p-4 rounded-2xl border border-slate-200/80 font-mono text-[11px] text-slate-800 space-y-1">
                            <strong class="text-rose-600">X₁ (Semantic Fit):</strong> Cosine_Sim(TFIDF_User, TFIDF_Job)<br>
                            <span class="text-slate-500 font-sans">วัดความสอดคล้องของบริบทและคีย์เวิร์ด</span>
                        </div>
                        <div class="bg-slate-50 p-4 rounded-2xl border border-slate-200/80 font-mono text-[11px] text-slate-800 space-y-1">
                            <strong class="text-rose-600">X₂ (Coverage Ratio):</strong> |Skills_User ∩ Skills_Job| / |Skills_Job|<br>
                            <span class="text-slate-500 font-sans">สัดส่วนทักษะที่ครอบคลุมข้อกำหนดของงาน</span>
                        </div>
                        <div class="bg-slate-50 p-4 rounded-2xl border border-slate-200/80 font-mono text-[11px] text-slate-800 space-y-1">
                            <strong class="text-rose-600">X₃ (Exact Count):</strong> |Skills_User ∩ Skills_Job|<br>
                            <span class="text-slate-500 font-sans">จำนวนทักษะที่ตรงตัวโดยตรง</span>
                        </div>
                    </div>
                </div>

                <!-- ITPE Framework Alignment -->
                <div class="glass-card rounded-3xl p-6 sm:p-8 shadow-sm space-y-4 flex flex-col justify-between">
                    <div class="space-y-4">
                        <h3 class="font-black text-lg text-slate-900 flex items-center gap-2">
                            <span>🎓</span> ITPE Body of Knowledge Alignment
                        </h3>
                        <p class="text-xs text-slate-600 leading-relaxed font-medium">
                            การจัดกลุ่มทักษะและสายงานในระบบถูกออกแบบให้อิงตามมาตรฐานวิชาชีพไอที:
                        </p>
                        <div class="space-y-2.5 text-xs text-slate-700">
                            <div class="flex items-start gap-2">
                                <span class="text-rose-600 font-bold mt-0.5">✓</span>
                                <span><strong>Fundamental IT Engineering (FE):</strong> ความรู้พื้นฐานด้านอัลกอริทึม, โครงสร้างข้อมูล, เครือข่าย และฐานข้อมูล</span>
                            </div>
                            <div class="flex items-start gap-2">
                                <span class="text-rose-600 font-bold mt-0.5">✓</span>
                                <span><strong>Applied Information Technology (AP):</strong> การออกแบบสถาปัตยกรรมซอฟต์แวร์, การบริหารความปลอดภัย และระบบคลาวด์</span>
                            </div>
                            <div class="flex items-start gap-2">
                                <span class="text-rose-600 font-bold mt-0.5">✓</span>
                                <span><strong>Student-to-Professional Readiness:</strong> บ่งบอกความพร้อมและแนะนำ Mini-Project บน GitHub เพื่อเตรียมสัมภาษณ์งาน</span>
                            </div>
                        </div>
                    </div>
                    <div class="pt-3">
                        <button onclick="window.location.hash = '#/matcher'" class="glow-btn-pink text-xs font-black px-6 py-3 rounded-2xl cursor-pointer shadow-md">
                            ทดลองแมตช์ทักษะของคุณทันที 🚀
                        </button>
                    </div>
                </div>
            </div>
        </div>
        `;
    },

    onMount() {}
};
