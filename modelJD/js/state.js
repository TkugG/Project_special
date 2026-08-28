/**
 * Global Reactive State Store for AI Job Matcher
 */
window.AppState = {
    userSkills: [],
    selectedRole: '',
    allSkills: [],
    allRoles: [],
    latestResults: null,
    listeners: {
        skills: [],
        role: [],
        results: []
    },

    subscribe(type, fn) {
        if (this.listeners[type]) {
            this.listeners[type].push(fn);
        }
    },

    notify(type) {
        if (this.listeners[type]) {
            this.listeners[type].forEach(fn => {
                try { fn(this); } catch (e) { console.error(`Listener error for ${type}:`, e); }
            });
        }
        // Always update skill count badge in header
        const badge = document.getElementById('headerSkillBadge');
        if (badge) {
            badge.innerText = `${this.userSkills.length} ทักษะ`;
            badge.style.display = this.userSkills.length > 0 ? 'inline-flex' : 'none';
        }
    },

    addSkill(skillName) {
        if (!skillName) return false;
        const clean = skillName.trim().toLowerCase();
        if (!clean) return false;

        // Check if exists in catalog
        const existsInDB = this.allSkills.some(s => s.toLowerCase().trim() === clean);
        if (this.allSkills.length > 0 && !existsInDB) {
            Swal.fire({
                icon: 'warning',
                title: 'ไม่พบทักษะในระบบ',
                text: `ไม่พบทักษะ "${skillName}" ในฐานข้อมูลมาตรฐาน กรุณาเลือกจากรายการแนะนำครับ`,
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
                customClass: { popup: 'rounded-xl shadow-lg text-sm' }
            });
            return false;
        }

        // Duplicate check
        if (this.userSkills.includes(clean)) {
            Swal.fire({
                icon: 'info',
                title: 'ทักษะซ้ำ',
                text: `คุณได้เลือกทักษะ "${clean}" ไว้แล้วครับ`,
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 2000,
                timerProgressBar: true,
                customClass: { popup: 'rounded-xl shadow-lg text-sm' }
            });
            return false;
        }

        this.userSkills.push(clean);
        this.notify('skills');
        return true;
    },

    removeSkill(index) {
        if (index >= 0 && index < this.userSkills.length) {
            this.userSkills.splice(index, 1);
            this.notify('skills');
        }
    },

    clearSkills() {
        this.userSkills = [];
        this.notify('skills');
    },

    setSkills(skills) {
        this.userSkills = Array.isArray(skills) ? [...skills] : [];
        this.notify('skills');
    },

    setRole(role) {
        this.selectedRole = (role || '').trim();
        this.notify('role');
    },

    setResults(results) {
        this.latestResults = results;
        this.notify('results');
    }
};
