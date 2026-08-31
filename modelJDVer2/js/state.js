/**
 * Global Reactive State Store for SkillMatch IT (TQF มคอ.2)
 */
window.AppState = {
    userSkills: [],
    selectedRole: '',
    allSkills: [],
    allRoles: [],
    curriculumRoles: [],
    latestResults: null,
    listeners: {
        skills: [],
        role: [],
        results: []
    },

    // Aliases for backward/forward compatibility
    get skillsVocabulary() {
        return this.allSkills;
    },
    set skillsVocabulary(val) {
        this.allSkills = val;
    },
    get rolesList() {
        return this.allRoles;
    },
    set rolesList(val) {
        this.allRoles = val;
    },
    get recommendations() {
        return this.latestResults;
    },
    set recommendations(val) {
        this.latestResults = val;
    },

    subscribe(type, fn) {
        if (this.listeners[type]) {
            this.listeners[type].push(fn);
            // Return an unsubscribe function to prevent listener accumulation
            return () => {
                this.listeners[type] = this.listeners[type].filter(f => f !== fn);
            };
        }
        return () => {}; // noop if type is unrecognized
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

    setUserSkills(skills) {
        this.setSkills(skills);
    },

    setRole(role) {
        this.selectedRole = (role || '').trim();
        this.notify('role');
    },

    setResults(results) {
        this.latestResults = results;
        this.notify('results');
    },

    setRecommendations(results) {
        this.setResults(results);
    }
};
