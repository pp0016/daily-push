# Session Backup: Cloud-GitHub Splitter Audit

## Date: 2026-09-27

### User Intent
The user wanted to implement a "Cloud-GitHub Splitter" workflow to efficiently back up a heavy project without exceeding Git size limits or losing media files.

**Workflow Goals:**
1. **2-Step Backup Mechanism:** Copy the original heavy project into a backup directory (C:\Users\renu5\Downloads\backup), then move contents into two separate folders, ignoring auto-generated dependency folders like 
ode_modules and ensuring API keys are removed.
2. **Naming Conventions & Splitting:** Divide into a Git-bound code folder (<ProjectName> copy for git) and a Cloud-bound media folder (<ProjectName> copy for git leftover). Isolate files >= 100MB and media (MP4, MP3, photos, web builds) into the leftover folder.
3. **Specific Git Push Trigger:** Phase 2 is triggered only by any prompt starting with "Init git, commit all files, and push to" to automatically initialize, commit, and push.
4. **Automated Re-merging via MERGE_INSTRUCTIONS_AI.md:** Instruct future AI agents to merge the projects back together using absolute paths provided by the user, then running 
pm install.

---

### Audit Results: 10 Issues Identified

#### ?? Critical Issues
1. **Hardcoded API keys in plaintext:** Real keys were visible in split_project.py (L8-9). *Fix: Replace with regex patterns.*
2. **No .gitignore generated:** Future collaborators could accidentally commit 
ode_modules. *Fix: Auto-generate a .gitignore in the github folder.*
3. **.env files get pushed to GitHub:** Scrubbing replaced only 2 specific keys. *Fix: Route .env* files to cloud leftover OR add to .gitignore.*

#### ?? Functional Gaps
4. **Phase 2 trigger too strict:** SKILL.md said "exact prompt" but user intent was "starts with". *Fix: Reword in SKILL.md.*
5. **SVG files sent to cloud:** SVGs are tiny code files; GitHub repo would look broken without them. *Fix: Remove .svg from media extensions.*
6. **Build folders not handled:** dist/, uild/, .next/, out/ were not ignored and could be huge. *Fix: Add to ignore_dirs.*
7. **No manifest of cloud files:** AI merge agent couldn't verify what was missing. *Fix: Generate CLOUD_FILES_MANIFEST.txt.*
8. **MERGE_INSTRUCTIONS_AI.md doesn't demand absolute paths:** AI might guess relative paths. *Fix: Rewrite template.*

#### ?? Minor / Polish
9. **Phase 2 doesn't know which project folder:** Path not constructed dynamically. *Fix: Update SKILL.md instructions.*
10. **No progress feedback:** Large projects copy silently. *Fix: Add a file counter print in script.*

---

### Artifacts Included in this Backup
- 	ranscript_full.jsonl: The entire un-truncated conversation log, preserving all code, thoughts, and outputs (API keys redacted).
