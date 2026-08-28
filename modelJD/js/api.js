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
                const res = await fetch(`${window.location.origin}/`, { method: "GET" });
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
                const res = await fetch(`${testUrl}/`, { method: "GET" });
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
            return await fetch(`${this.baseUrl}${endpoint}`, options);
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
            return { skills: AppState.allSkills, roles: AppState.allRoles };
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
