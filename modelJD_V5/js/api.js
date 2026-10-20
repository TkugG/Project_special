/**
 * API Client & Network Service for AI Job Matcher
 */
window.ApiClient = {
    baseUrl: "http://127.0.0.1:8000",

    escapeHTML(str) {
        const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
        return String(str ?? '').replace(/[&<>"']/g, tag => map[tag] || tag);
    },

    async detectActiveBackend() {
        const ports = [8000, 8001, 8080, 8888, 5000];

        // 1. Try current window origin if on HTTP/HTTPS
        if (window.location.origin && window.location.origin.startsWith("http")) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 800);
                const res = await fetch(`${window.location.origin}/`, { method: "GET", signal: controller.signal });
                clearTimeout(timeoutId);
                const info = await res.json();
                if (info.status === "online") {
                    this.baseUrl = window.location.origin;
                    return this.baseUrl;
                }
            } catch (e) { }
        }

        // 2. Try common local backend ports
        for (const port of ports) {
            const testUrl = `http://127.0.0.1:${port}`;
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 600);
                const res = await fetch(`${testUrl}/`, { method: "GET", signal: controller.signal });
                clearTimeout(timeoutId);
                const info = await res.json();
                if (info.status === "online") {
                    this.baseUrl = testUrl;
                    console.log("✅ Auto-connected to Backend API at:", this.baseUrl);
                    return this.baseUrl;
                }
            } catch (e) { }
        }
        return this.baseUrl;
    },

    async fetchWithRetry(endpoint, options = {}) {
        try {
            const res = await fetch(`${this.baseUrl}${endpoint}`, options);
            if (res.ok) return res;
            throw new Error(`HTTP ${res.status}`);
        } catch (err) {
            console.warn(`Connection to ${this.baseUrl} failed, retrying backend detection...`);
            await this.detectActiveBackend();
            const retryRes = await fetch(`${this.baseUrl}${endpoint}`, options);
            // #6: ตรวจ res.ok ในรอบ retry ด้วย ป้องกัน silent HTTP error
            if (!retryRes.ok) throw new Error(`HTTP ${retryRes.status} on retry`);
            return retryRes;
        }
    },

    async loadSkillsAndRoles() {
        try {
            const [skillsRes, rolesRes] = await Promise.all([
                this.fetchWithRetry("/api/skills", { method: "GET" }),
                this.fetchWithRetry("/api/roles", { method: "GET" })
            ]);

            const skillsData = await skillsRes.json();
            const rolesData = await rolesRes.json();

            if (skillsData && skillsData.skills) {
                AppState.allSkills = skillsData.skills;
            }
            if (rolesData && rolesData.roles) {
                AppState.allRoles = rolesData.roles;
            }
            if (rolesData && rolesData.curriculum_roles) {
                AppState.curriculumRoles = rolesData.curriculum_roles;
            }
            return { skills: AppState.allSkills, roles: AppState.allRoles, curriculum_roles: AppState.curriculumRoles };
        } catch (err) {
            console.warn("Error preloading skills/roles:", err);
            return { skills: [], roles: [] };
        }
    },

    async getRecommendations(role, skills) {
        const response = await this.fetchWithRetry("/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                preference: role || "",
                skills: skills || []
            })
        });
        return await response.json();
    }
};
