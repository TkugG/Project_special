/**
 * SkillMatch IT - Main Application Bootstrapper
 */
window.App = {
    async init() {
        console.log("🚀 Initializing SkillMatch IT SPA Router...");

        // 1. Register SPA Routes (ลบ '#/' ซ้ำซ้อนออก — getCleanHash() จัดการ normalize แล้ว)
        AppRouter.register('#/matcher', MatcherView, { title: 'SkillMatch IT - ค้นหาตำแหน่งงานที่ใช่' });
        AppRouter.register('#/careers', CareersView, { title: 'IT Career Explorer - สำรวจสายงานไอที' });
        AppRouter.register('#/skills', SkillsView, { title: 'IT Skills Taxonomy - คลังทักษะไอที' });

        // 2. Detect backend API
        await ApiClient.detectActiveBackend();

        // 3. Load catalog of skills and roles
        const catalog = await ApiClient.loadSkillsAndRoles();
        console.log(`✅ Loaded ${catalog.skills.length} skills and ${catalog.roles.length} roles from backend.`);

        // 4. Start Router
        AppRouter.init();

        // 5. Global dropdown close listener (ลงทะเบียนครั้งเดียว — ป้องกัน listener leak จาก onMount)
        document.addEventListener('click', (e) => {
            const dropdown = document.getElementById('suggestionsDropdown');
            const searchInput = document.getElementById('skillSearchInput');
            if (dropdown && searchInput &&
                !dropdown.contains(e.target) && e.target !== searchInput) {
                dropdown.classList.add('hidden');
            }
        });
    }
};

window.addEventListener('DOMContentLoaded', () => {
    // #9: wrap in try/catch เพื่อแสดง error แทนหน้าว่างเปล่าเมื่อ backend ไม่พร้อม
    App.init().catch(err => {
        console.error('❌ App initialization failed:', err);
        Swal.fire({
            icon: 'error',
            title: 'ไม่สามารถเริ่มต้นระบบได้',
            text: 'ไม่พบ Backend API กรุณาตรวจสอบว่าเซิร์ฟเวอร์ทำงานอยู่ แล้วรีเฟรชหน้าใหม่',
            confirmButtonColor: '#e11d48',
            confirmButtonText: 'รีเฟรช',
            customClass: { popup: 'rounded-3xl p-6', confirmButton: 'rounded-xl' }
        }).then(() => window.location.reload());
    });
});
