# AGENTS.md — AI Instructions & Project Context

Welcome AI Agent! Before making any changes or recommendations in this repository, please read **[CONTEXT.md](file:///c:/Users/ASUS/Documents/modelJD_V4/CONTEXT.md)** for full architecture, invariant rules, and recent decisions.

## Quick Summary for AI Agents:
1. **System Type:** SkillMatch IT — Thai IT Job Recommendation & 8 IT Curriculum Career Classifier (FastAPI + Vanilla JS SPA).
2. **Key Invariants:**
   - **Frontend:** Vanilla JavaScript (ES6+), NO build step (no Vite, no React, no Tailwind build). Bump `?v=X.X.X` in `index.html` after editing `js/`.
   - **8 Tracks Naming:** Always use `ชื่อไทย (English Title)` (e.g. `นักพัฒนาและออกแบบสื่อผสม (Multimedia Designer & Developer)`).
   - **Skills:** 444 Thai market canonical skills (normalized from 115 real jobs in `data/thai_jobs_dataset.csv`). Do NOT re-introduce Kaggle's 1,784 skills text into the UI.
   - **Demarcation:**
     - 8.3 is Creative Media, UI/UX, Motion, 3D, Game. NO `html` or `css` in 8.3!
     - 8.7 is Web Developer, Frontend, CMS, Responsive Web, HTML5, CSS3, JS.
3. **Verification Command:**
   - Always run `python src/validate.py` to ensure all 5 test suites pass.
