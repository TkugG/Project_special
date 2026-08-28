/**
 * Client-Side Hash Router for AI Job Matcher SPA
 */
window.AppRouter = {
    routes: {},
    currentRoute: null,
    viewContainerId: 'router-view',

    register(path, viewObject, meta = {}) {
        this.routes[path] = {
            view: viewObject,
            title: meta.title || 'AI Job Matcher',
            icon: meta.icon || '🎯'
        };
    },

    init() {
        window.addEventListener('hashchange', () => this.handleRouting());
        this.handleRouting();
    },

    getCleanHash() {
        let hash = window.location.hash || '#/';
        // Normalize hash path
        if (hash === '' || hash === '#' || hash === '#/') {
            return '#/matcher';
        }
        return hash;
    },

    handleRouting() {
        const hash = this.getCleanHash();
        let target = this.routes[hash];

        // Fallback to matcher
        if (!target) {
            if (this.routes['#/matcher']) {
                target = this.routes['#/matcher'];
                window.location.hash = '#/matcher';
            } else {
                console.error(`Route not found for hash: ${hash}`);
                return;
            }
        }

        this.currentRoute = hash;

        // 1. Update active states on nav links
        this.updateNavLinks(hash);

        // 2. Render view content into container
        const container = document.getElementById(this.viewContainerId);
        if (container && target.view && typeof target.view.render === 'function') {
            container.innerHTML = target.view.render();
            
            // 3. Trigger view mount lifecycle hook
            if (typeof target.view.onMount === 'function') {
                try {
                    target.view.onMount();
                } catch (e) {
                    console.error(`Error in onMount for route ${hash}:`, e);
                }
            }
        }

        // 4. Update document title
        if (target.title) {
            document.title = target.title;
        }

        // 5. Scroll to top smoothly
        window.scrollTo({ top: 0, behavior: 'instant' });
    },

    updateNavLinks(activeHash) {
        const links = document.querySelectorAll('[data-route]');
        links.forEach(link => {
            const route = link.getAttribute('data-route');
            if (route === activeHash || (activeHash === '#/matcher' && route === '#/')) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    },

    navigate(path) {
        window.location.hash = path;
    }
};
