# Contributing to Awesome MICCAI 2026

Thank you for your interest in contributing to this curated list of MICCAI 2026 papers with public code!

## 🤖 How This Repository Works

This repository is **bot-maintained**. A GitHub Actions workflow runs daily to:

1. Search arXiv for papers mentioning "MICCAI 2026"
2. Extract papers that have public code repositories (GitHub, GitLab, Hugging Face)
3. Normalize and validate repository links
4. Apply weighted multi-label categorization
5. Regenerate README category blocks and validate generated markdown

If any quality gate fails, the workflow fails and no update is committed.

**Important:** Manual edits to auto-generated sections in `README.md` will be overwritten by the bot.

## 👥 Human Contributions

Human contributions are welcome for **quality control and oversight**. Your help ensures accuracy and completeness of the list.

### Ways to Contribute

| Contribution Type | How to Help |
|------------------|-------------|
| 🐛 **Report incorrect paper** | Not MICCAI 2026, stale entry, wrong metadata, malformed/broken link |
| ➕ **Add missing paper** | Bot missed a valid MICCAI 2026 paper with code |
| 🔗 **Fix broken link** | Code repository link no longer works |
| 🏷️ **Suggest category change** | Paper is in the wrong category |
| 📁 **Propose new category** | Suggest a new category for better organization |

### Contribution Guidelines

#### ✅ Requirements for All Contributions

1. **Paper must be associated with MICCAI 2026** — Include evidence (arXiv comment/proceedings/workshop page)
2. **Code repository must be public** — Private repos cannot be verified
3. **No duplicate entries** — Check the list before submitting
4. **One paper per PR** — Keep changes focused and reviewable

#### ❌ What NOT to Edit Manually

- Auto-generated paper lists between `<!-- BEGIN ... -->` and `<!-- END ... -->` markers
- The "Last Updated" timestamp
- Any content that the bot regularly updates

Manual edits to these sections **will be overwritten** on the next bot run.

## 📝 How to Contribute

### Reporting Issues

Use our issue templates for:

- [Report an Error](../../issues/new?template=report_error.yml) — Wrong info, broken links, duplicates
- [Add Missing Paper](../../issues/new?template=add_missing_paper.yml) — Paper the bot missed
- [Suggest Category Change](../../issues/new?template=suggest_category.yml) — Improve classification

When reporting issues, include direct evidence (URL + short explanation). Reports without evidence are harder to action.

### Submitting Pull Requests

1. Fork the repository
2. Make your changes (one paper per PR)
3. Fill out the PR template completely
4. Submit for review

**Note:** PRs that bulk-edit auto-generated content will be closed.

## 📂 Repository Structure

```
.
├── README.md              # Main awesome list (auto-updated)
├── scripts/
│   ├── update_papers.py   # Discovery, normalization, categorization, rendering
│   └── validate_readme.py # README integrity and quality checks
├── .github/
│   ├── workflows/         # GitHub Actions automation
│   ├── ISSUE_TEMPLATE/    # Issue templates
│   └── CONTRIBUTING.md    # This file
└── requirements.txt       # Python dependencies for bot
```

## 🏷️ Categories

Papers are categorized into:

- **Segmentation** — Medical image segmentation methods
- **Reconstruction** — Image reconstruction and restoration
- **Classification** — Disease classification and diagnosis
- **Image Registration** — Alignment and transformation methods
- **Domain Adaptation** — Transfer learning and cross-domain methods
- **Generative Models** — GANs, diffusion models, VAEs
- **General** — Papers that don't fit other categories

Multi-category appearances are expected for truly multi-task papers and are not treated as duplication.

## ❓ Questions?

If you're unsure about anything, feel free to open a [discussion](../../discussions) or issue. We're happy to help!

---

Thank you for helping make this resource better for the medical imaging research community! 🏥
