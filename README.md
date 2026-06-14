# Skills — joetustin.com

Source + hosting for the skills published at **[joetustin.com/skills](https://joetustin.com/skills)**.

The pitch: someone tells Claude *"go to joetustin.com/skills, find the United skill, and load it"* —
Claude reads the catalog, downloads the right skill, and installs it. No GitHub, no `/plugin`
commands, just a URL.

## Layout

```
skills/
├── src/                         # edit skills here (each is a folder with SKILL.md at its root)
│   └── signup-bonus-recovery/
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
├── public/                      # deploy this at joetustin.com/skills/
│   ├── index.html               # the landing page  → joetustin.com/skills
│   ├── index.json               # machine-readable catalog → joetustin.com/skills/index.json
│   ├── <skill>.tar.gz           # Claude Code install artifact
│   └── <skill>.skill            # Claude.ai / Cowork upload artifact
├── build.sh                     # repackages public/ artifacts from src/
└── README.md
```

## Workflow

1. Edit or add a skill under `src/`. A skill is just a folder with `SKILL.md` at its root
   (plus optional `references/` and `scripts/`).
2. Run `./build.sh` to regenerate the `.tar.gz` and `.skill` artifacts in `public/`.
3. Update `public/index.json` — add/adjust the skill's entry (name, summary, **keywords**,
   download URLs). Keywords are how Claude matches a user's plain-language request to the skill.
4. Deploy the contents of `public/` so they're served at `joetustin.com/skills/`.

## Integrating into the joetustin.com app

`public/` is a standalone, framework-agnostic version. To make it a native section of the site:

- Drop the static files under the app's `public/skills/` directory so they're served verbatim at
  `/skills/...` (make sure `.tar.gz` and `.skill` are served as downloads, not rewritten by a router), **or**
- Port `index.html` into a real page/route and reuse the site's own header, footer, and fonts.
  The page's accent color is a single CSS variable (`--accent`) so it's easy to match the live theme.

Verify after deploy:

```bash
curl -sI https://joetustin.com/skills/index.json                            # 200, application/json
curl -sI https://joetustin.com/skills/signup-bonus-recovery.tar.gz   # 200, downloadable
```

## How a user installs (what the page tells them)

- **Tell Claude** (Claude Code / Cowork): paste a one-liner pointing at the catalog; Claude does the rest.
- **Claude Code, manual:**
  `mkdir -p ~/.claude/skills && curl -fsSL https://joetustin.com/skills/<skill>.tar.gz | tar -xz -C ~/.claude/skills/`
- **Claude.ai / Cowork:** download the `.skill` file, upload under Settings → Capabilities → Skills.

## Privacy note for skill authors

Skills published here are meant to run locally and hold **no personal data**. Before shipping a
skill, scrub example data of real names, account numbers, card numbers, and member IDs — the
`signup-bonus-recovery` example uses a fictional persona and placeholder numbers for this
reason. Never commit a real user's case file.

## Adding the next skill

Copy an existing `src/<skill>/` as a template, write its `SKILL.md`, run `./build.sh`, add its
entry to `public/index.json`, and add an entry to `public/index.html`. The page and catalog are
built to hold many skills.
