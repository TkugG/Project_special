/**
 * SkillMatch IT - Main Application Bootstrapper
 */
window.App = {
    async init() {
        console.log("🚀 Initializing SkillMatch IT SPA Router...");

        // 1. Register SPA Routes
        AppRouter.register('#/', MatcherView, { title: 'SkillMatch IT - ค้นหาตำแหน่งงานที่ใช่' });
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
    }
};

window.addEventListener('DOMContentLoaded', () => {
    App.init();
});
