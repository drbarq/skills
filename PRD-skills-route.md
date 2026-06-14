# PRD — `joetustin.com/skills` route

**Owner:** Joe Tustin
**Implementer:** Claude Code, working in the personal-site repo (`.../joetustin/personal`)
**Status:** Ready to build

---

## 1. Goal

Add a public `/skills` section to joetustin.com that hosts downloadable Claude **Agent Skills**
and makes them installable in one step. The headline interaction: a visitor (often arriving from
a LinkedIn post) tells Claude *"go to joetustin.com/skills, find the United skill, and load it,"*
and Claude reads the catalog, downloads the right skill, and installs it.

Ship the first skill, `cobranded-card-bonus-dispute`, and build the section so adding more skills
later is trivial.

## 2. Why it's shaped this way

A skill is distributed in two layers:

- **Source of truth** lives in a **dedicated public GitHub repo** (canonical, versioned,
  *auditable*). Auditability is a hard requirement here: this skill reads users' credit card
  statements, so "read the source before you run it" is the trust mechanism. Do **not** put the
  skill source only in the (private) site repo.
- **Distribution surface** is `joetustin.com/skills`: it serves the landing page, the machine-
  readable catalog (`index.json`), and the prebuilt download artifacts (`.tar.gz` for Claude
  Code, `.skill` for Claude.ai / Cowork). Install URLs must be clean `joetustin.com/skills/...`
  URLs.

The `.tar.gz` and `.skill` are **build outputs** (produced by `build.sh` from the skill source),
committed into the site's static directory and served verbatim.

## 3. Provided assets

A ready-made bundle accompanies this PRD (the `Skills/` directory / `Skills.zip`). Reuse it
rather than rebuilding from scratch:

```
Skills/
├── src/cobranded-card-bonus-dispute/     # the skill source (SKILL.md + references/ + scripts/)
├── public/
│   ├── index.html                        # styled standalone landing page (port into a route)
│   ├── index.json                        # the catalog  → serve at /skills/index.json
│   ├── cobranded-card-bonus-dispute.tar.gz   # Claude Code install artifact
│   └── cobranded-card-bonus-dispute.skill    # Claude.ai / Cowork upload artifact
├── build.sh                              # regenerates the two artifacts from src/
└── README.md
```

The example data in the skill is already scrubbed (fictional persona, placeholder numbers).
Keep it that way — never commit real account/card/member data.

## 4. Architecture / where things live

| Thing | Lives in | Served at |
|---|---|---|
| Skill source | Public GitHub repo (e.g. `github.com/drbarq/skills`) | — (GitHub) |
| Build script `build.sh` | Both repos (or just the skill repo) | — |
| Landing page | Site repo, as a real route | `joetustin.com/skills` |
| Catalog `index.json` | Site repo, static asset | `joetustin.com/skills/index.json` |
| `*.tar.gz`, `*.skill` | Site repo, static assets (vendored build outputs) | `joetustin.com/skills/<name>.tar.gz` etc. |

Update flow: edit `src/` in the skill repo → run `./build.sh` → copy the refreshed artifacts and
`index.json` into the site's static dir → deploy.

> If Joe prefers a single repo, the section can live entirely in the site repo **only if that
> repo is (or becomes) public** — otherwise auditability is lost. Default to the two-repo split
> above.

## 5. Functional requirements

1. **Landing page** at `/skills` renders the catalog (currently one skill) with, per skill:
   title, one-line summary, what-it-does bullets, and three install methods (Tell Claude /
   Claude Code / Claude.ai-Cowork), plus a "read the source" link.
2. **Catalog endpoint:** `GET https://joetustin.com/skills/index.json` returns the JSON in
   `public/index.json` with `Content-Type: application/json`. This is the contract Claude reads
   to discover and install skills — its URLs and `keywords` must be intact.
3. **Download endpoints:** `GET https://joetustin.com/skills/cobranded-card-bonus-dispute.tar.gz`
   and `…/cobranded-card-bonus-dispute.skill` return the files as **downloads** (binary, correct
   content-type, `Content-Disposition: attachment` preferred). They must **not** be rewritten,
   transformed, or 404'd by the framework router or a trailing-slash rule.
4. **Self-install flow works end to end:** from a Claude Code / Cowork session, the catalog is
   fetchable and the `.tar.gz` downloads and extracts to a folder named
   `cobranded-card-bonus-dispute/` (so it lands cleanly in `~/.claude/skills/`).
5. **Extensible:** adding skill #2 = drop a `src/<name>/`, run `build.sh`, add a catalog entry
   and a page entry. No structural changes.

## 6. Design requirements

- The page must read as a **native section of joetustin.com**, not a separate brand. Reuse the
  site's existing header/nav, footer, fonts, and color tokens.
- `public/index.html` is a **styled reference** (warm `#F2EDE4` paper, Fraunces/Inter/JetBrains
  Mono, a single clay accent in the `--accent` CSS variable, a `home / skills` breadcrumb). Port
  its **structure and copy** into a real route; swap its standalone styles for the site's own
  design system where they exist. If the site already defines type/color tokens, use those and
  drop the page's local `:root` block; map the page's `--accent` to the site accent.
- No "Smokin' Robots" branding on this page (that's the writing sub-brand, not skills).
- Quality floor: responsive to mobile, visible keyboard focus, `prefers-reduced-motion`
  respected, copy-to-clipboard buttons functional.

## 7. Stack-specific guidance

The site appears to be **Next.js (App Router)** — adapt if the repo shows otherwise; inspect
before implementing.

**If Next.js (App Router):**
- Static assets → `public/skills/index.json`, `public/skills/cobranded-card-bonus-dispute.tar.gz`,
  `public/skills/cobranded-card-bonus-dispute.skill`. Files in `public/` are served verbatim at
  the matching path, which gives the required `joetustin.com/skills/...` URLs. Confirm no
  `next.config` rewrite/redirect or middleware intercepts `/skills/*` static files.
- Page → `app/skills/page.tsx` (server component is fine; the copy buttons + tabs need a small
  client component, `"use client"`). Reuse the site's layout so header/footer come for free.
- Verify `.tar.gz`/`.skill` aren't caught by any catch-all route; static `public/` files take
  precedence, but a trailing-slash redirect can interfere — test the exact URLs.
- Set long-cache headers on the artifacts if desired, but **bump the catalog `version` and the
  artifact filename or a query string when a skill changes** so users don't get stale installs.

**If a static host (Astro/Eleventy/plain):** publish the `public/` files at the `/skills` path
and render the page from `index.html`/a template.

## 8. Implementation steps

1. Inspect the repo; identify the framework, the static/public dir, and the site's design tokens
   and layout components.
2. Create the public skill repo (or confirm it exists) and push `src/cobranded-card-bonus-dispute/`
   + `build.sh` + a README. (Joe may do this manually — coordinate.)
3. Copy `index.json`, `cobranded-card-bonus-dispute.tar.gz`, and `cobranded-card-bonus-dispute.skill`
   into the site's static dir under a `skills/` subfolder.
4. Build the `/skills` page route from `public/index.html`'s structure + copy, restyled to the
   site's design system, reusing the site header/footer.
5. Wire the three install methods exactly as in the reference (Tell Claude prompt, Claude Code
   `curl | tar` one-liner, `.skill` download + Settings upload).
6. Confirm routing serves the JSON and the two artifacts correctly (see acceptance criteria).
7. Add a link to `/skills` from the site nav and/or the relevant section of the homepage.

## 9. Acceptance criteria

- [ ] `curl -sI https://joetustin.com/skills/index.json` → `200`, `content-type: application/json`.
- [ ] `curl -sI https://joetustin.com/skills/cobranded-card-bonus-dispute.tar.gz` → `200`,
      downloadable (octet-stream/gzip), not HTML.
- [ ] `curl -sI https://joetustin.com/skills/cobranded-card-bonus-dispute.skill` → `200`,
      downloadable.
- [ ] `curl -s https://joetustin.com/skills/cobranded-card-bonus-dispute.tar.gz | tar -tz | head`
      lists `cobranded-card-bonus-dispute/SKILL.md`.
- [ ] In a Claude Code / Cowork session: *"go to joetustin.com/skills, find the United/Chase
      bonus-dispute skill, and install it"* results in the skill installed under `~/.claude/skills/`.
- [ ] `/skills` renders with the site's header/footer/fonts; responsive on mobile; keyboard focus
      visible; copy buttons work.
- [ ] No real personal data anywhere in the page, catalog, or shipped skill (grep for account/
      card/member identifiers returns nothing).
- [ ] Nav links to `/skills` from the site.

## 10. Out of scope / later

- Additional skills (the section is built to hold many).
- Optional: also publish the skill repo as a **Claude Code plugin marketplace**
  (`.claude-plugin/marketplace.json` + `plugin.json`) for the `/plugin install …` path.
- Optional: lightweight download/usage analytics.
- The LinkedIn launch post (separate deliverable).

## 11. Notes for the implementer

- The catalog's `keywords` are how Claude matches a plain-language request ("the United one") to
  the right skill — preserve them and add relevant terms for each new skill.
- Don't transform or minify the `.tar.gz`/`.skill`; serve the exact bytes from `build.sh`.
- Keep "self-advocacy / productivity tool, not legal or financial advice" disclaimer on the page.
- Re-run `build.sh` and re-copy artifacts whenever the skill source changes; stale artifacts are
  the most likely failure mode.
