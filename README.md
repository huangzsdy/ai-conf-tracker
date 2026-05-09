# Awesome AI Conference Papers

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A generic conference paper crawler and organizer that automatically discovers papers with public code implementations from arXiv.

**This repository automatically discovers and organizes conference papers from arXiv that include public code links.** A daily bot run searches arXiv metadata, validates links and formatting, assigns categories with confidence tiers, and regenerates the list deterministically.

## Conference Scope Configuration

This project is **generic** and can be configured to track any conference supported by arXiv (e.g., MICCAI, CVPR, NeurIPS, ICCV, ICLR, MIDL, etc.).

### 🎯 What is Conference Scope?

The conference scope defines which conference papers you want to track. You can configure:
- **Which conference** (MICCAI, CVPR, NeurIPS, etc.)
- **Which year(s)** (specific year or all years)
- **Matching strictness** (strict mode vs broad mode)
- **Which tracks** (main, workshops, challenges)

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run with default settings (MICCAI 2026, strict mode)
python scripts/update_papers.py

# Run with different conference scope
python scripts/update_papers.py --conference-scope cvpr-2025 --mode broad

# Run with all years of a conference
python scripts/update_papers.py --conference-scope miccai-all-years --mode broad
```

### Using in China / Without VPN

The arXiv API may be slow or inaccessible in some regions. Use one of these methods:

#### Method 1: Set Proxy Environment Variables

```bash
# Windows (PowerShell)
$env:HTTPS_PROXY="http://127.0.0.1:7890"
$env:HTTP_PROXY="http://127.0.0.1:7890"
python scripts/update_papers.py

# Windows (CMD)
set HTTPS_PROXY=http://127.0.0.1:7890
set HTTP_PROXY=http://127.0.0.1:7890
python scripts/update_papers.py

# Linux/Mac
export HTTPS_PROXY=http://127.0.0.1:7890
export HTTP_PROXY=http://127.0.0.1:7890
python scripts/update_papers.py
```

#### Method 2: Run with Proxy Prefix

```bash
HTTPS_PROXY=http://127.0.0.1:7890 python scripts/update_papers.py --conference-scope cvpr-2025
```

#### Method 3: Edit Configuration File

Create a `.env` file in the project root:

```
HTTPS_PROXY=http://127.0.0.1:7890
HTTP_PROXY=http://127.0.0.1:7890
```

Then run:
```bash
pip install python-dotenv
python scripts/update_papers.py
```

**Common Proxy Ports:**
- V2Ray: 7890, 1080
- Shadowsocks: 1080, 10808
- Clash: 7890, 8080
- SSH Tunnel: 1081

**Note:** If you don't need a proxy, simply run without setting the environment variables.

### Configuration Options

| Parameter | Description | Example Values |
|---|---|---|
| `--conference-scope` | Conference and year to track | `miccai-2026`, `cvpr-2025`, `nips-2024`, `miccai-all-years` |
| `--mode` | Match strictness | `strict` (exact year match), `broad` (also name match) |
| `--tracks` | Paper tracks to include | `main`, `workshops`, `challenges`, `all` |

### Conference Scope Format

There are two ways to specify conference scope:

- **Specific year**: `{conference}-{year}` (e.g., `miccai-2026`, `cvpr-2025`, `iclr-2026`)
- **All years**: `{conference}-all-years` (e.g., `miccai-all-years`, `cvpr-all-years`)

### Supported Conferences

The crawler works with any conference that has papers submitted to arXiv. Common conferences include:

| Conference | Full Name | Year Format |
|---|---|---|
| `miccai` | Medical Image Computing and Computer Assisted Intervention | MICCAI 2026 |
| `cvpr` | Computer Vision and Pattern Recognition | CVPR 2025 |
| `nips` / `neurips` | Neural Information Processing Systems | NeurIPS 2024 |
| `iccv` | International Conference on Computer Vision | ICCV 2025 |
| `iclr` | International Conference on Learning Representations | ICLR 2026 |
| `midl` | Medical Imaging with Deep Learning | MIDL 2024 |
| `aaai` | AAAI Conference on Artificial Intelligence | AAAI 2025 |
| `ijcai` | International Joint Conference on AI | IJCAI 2024 |

### Detailed Examples

#### Example 1: Track a Specific Conference and Year

```bash
# Track CVPR 2025 papers (strict mode - requires "CVPR 2025" in arXiv metadata)
python scripts/update_papers.py --conference-scope cvpr-2025 --mode strict
```

**What it does:**
- Searches arXiv for papers containing "CVPR 2025" in title, abstract, or comments
- Only includes papers that explicitly mention 2025
- Validates code links (GitHub, GitLab, Hugging Face)

#### Example 2: Track All Years of a Conference

```bash
# Track all CVPR papers across all years (broad mode)
python scripts/update_papers.py --conference-scope cvpr-all-years --mode broad
```

**What it does:**
- Searches arXiv for any paper mentioning "CVPR" (any year)
- Includes papers from all years
- Broader matching (includes papers that just mention "CVPR" without specific year)

#### Example 3: Include Workshops and Challenges

```bash
# Track NeurIPS 2024 including workshops and challenges
python scripts/update_papers.py --conference-scope nips-2024 --tracks all
```

**What it does:**
- Searches for NeurIPS 2024 main track papers
- Also includes workshop papers (if title/abstract mentions "workshop")
- Also includes challenge papers (if title/abstract mentions "challenge")

#### Example 4: Track a Medical Imaging Conference

```bash
# Track MICCAI 2026 (default settings)
python scripts/update_papers.py --conference-scope miccai-2026

# Track all years of MICCAI
python scripts/update_papers.py --conference-scope miccai-all-years
```

#### Example 5: Track ICLR for Paper Collection

```bash
# Track ICLR 2026 with all tracks (main + workshop + rebuttal)
python scripts/update_papers.py --conference-scope iclr-2026 --mode strict --tracks all
```

### Mode Comparison

| Mode | Description | Use Case |
|---|---|---|
| `strict` | Requires exact year in arXiv metadata | When you want papers from a specific year only |
| `broad` | Also matches conference name without year | When you want all papers from a conference (any year) |

**Example with CVPR:**
- `strict` mode: Only papers with "CVPR 2025" explicitly in metadata
- `broad` mode: Also includes papers that just say "CVPR" without year

### Track Options

| Option | Description |
|---|---|
| `main` | Main conference papers only |
| `workshops` | Workshop papers only |
| `challenges` | Challenge/competition papers only |
| `all` | All of the above |

### How the Crawler Works

1. **Discover**: Fetch candidate papers from arXiv using search queries
2. **Filter**: Filter by conference scope and year
3. **Validate**: Check for valid code links (GitHub/GitLab/Hugging Face)
4. **Categorize**: Assign to categories (Segmentation, Reconstruction, etc.)
5. **Render**: Generate README.md with paper list

### Code Structure

This project contains three main Python scripts in the `scripts/` directory:

| Script | Purpose | Key Functions |
|--------|---------|--------------|
| `update_papers.py` | Main crawler - discovers, filters, validates, categorizes papers | `discover_papers()`, `discover_papers_by_keyword()`, `validate_papers_data()`, `categorize_papers()`, `update_readme()` |
| `export_readme.py` | Export existing README data to Zotero formats | `parse_readme_by_category()`, `export_csv()`, `export_bibtex()`, `export_ris()` |
| `validate_readme.py` | Validate README format and check for errors | Validates markers, URLs, duplicates |

#### `update_papers.py` - Main Crawler

The core script with two modes:

**Mode 1: Conference Search**
```
1. discover_papers()          → Fetch papers from arXiv by conference
2. validate_papers_data()    → Clean links, remove duplicates
3. categorize_papers()       → Assign categories by keyword matching
4. update_readme()           → Write to README.md category blocks
5. export_to_csv/bibtex/ris() → Export to Zotero formats
```

**Mode 2: Keyword Search**
```
1. discover_papers_by_keyword() → Fetch papers from arXiv by keyword
2. validate_papers_data()      → Clean links, remove duplicates
3. categorize_papers()       → Assign categories
4. export_to_csv/bibtex/ris() → Export to Zotero formats
```

Key configuration variables (at top of file):
- `CATEGORY_ORDER` - List of category names in display order
- `CATEGORY_RULES` - Keywords and weights for each category
- `CATEGORY_MARKERS` - HTML markers for README blocks
- `ALLOWED_CODE_HOSTS` - Supported code platforms (GitHub, GitLab, HuggingFace)

#### `export_readme.py` - Zotero Export Utility

Parses existing README.md and exports to Zotero-compatible formats with optional keyword filtering.

#### Running the Scripts

```bash
# Install dependencies
pip install -r requirements.txt

# === Conference Search ===
# CVPR 2025 with category subdirectories
python scripts/update_papers.py --conference-scope cvpr-2025 --mode strict --export all --by-category

# MICCAI all years with custom delay (avoid 429 errors)
python scripts/update_papers.py --conference-scope miccai-all-years --mode broad --delay 10 --export all --by-category

# === Keyword Search (from arXiv) ===
# Search by keyword, avoid rate limit with --delay
python scripts/update_papers.py --keyword "infrared small target detection" --delay 10 --export all --by-category

# === Export from existing README ===
# Export all papers to Zotero formats
python scripts/export_readme.py --by-category --format ris

# Filter by keyword (creates separate directory per keyword)
python scripts/export_readme.py --keyword "segmentation" --by-category --format ris

# === Handle 429 Rate Limit ===
# Use proxy to avoid rate limiting
HTTPS_PROXY=http://127.0.0.1:7890 python scripts/update_papers.py --keyword "your keyword" --export all

# Increase delay between requests (default: 5 seconds)
python scripts/update_papers.py --keyword "your keyword" --delay 10 --export all
```

#### Output Directory Structure

**Conference Search:**
```
exports/
└── cvpr-2025/
    ├── Segmentation/Segmentation.ris
    ├── Classification/Classification.ris
    └── ...
```

**Keyword Search:**
```
exports/
└── infrared_small_target_detection/
    ├── Segmentation/Segmentation.ris
    ├── Classification/Classification.ris
    └── ...
```

**Filter from existing README:**
```
exports/
└── segmentation/
    ├── Segmentation/Segmentation.ris
    └── ...
```

#### Common Conference Commands

| Conference | Command |
|-----------|---------|
| CVPR 2025 | `--conference-scope cvpr-2025 --mode strict` |
| NeurIPS 2025 | `--conference-scope neurips-2025 --mode strict` |
| MICCAI 2026 | `--conference-scope miccai-2026 --mode strict` |
| All MICCAI | `--conference-scope miccai-all-years --mode broad` |
| ICCV 2025 | `--conference-scope iccv-2025 --mode strict` |
| ICLR 2026 | `--conference-scope iclr-2026 --mode strict` |

#### Code Requirement Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--require-code` | Only include papers with code links | Enabled (default) |
| `--no-require-code` | Include all papers regardless of code | Disabled |

```bash
# Only papers with code links (default)
python scripts/update_papers.py --keyword "infrared" --require-code

# All papers (with or without code)
python scripts/update_papers.py --keyword "infrared" --no-require-code
```

#### Combined Conference + Keyword Search

Search within a specific conference AND keyword, without creating subdirectories:

```bash
# NeurIPS 2025 + keyword search, no subdirectories
python scripts/update_papers.py --conference-scope neurips-2025 --keyword "infrared small target detection" --export all

# Output: exports/neurips-2025/neurips-2025.ris
```

#### Output Directory Behavior

| Scenario | Command | Output Directory |
|----------|---------|-------------------|
| Conference + category | `--conference-scope cvpr-2025 --by-category` | `exports/cvpr-2025/Segmentation/` |
| Keyword only | `--keyword "infrared"` | `exports/` |
| Keyword + category | `--keyword "infrared" --by-category` | `exports/infrared/Segmentation/` |
| Conference + keyword | `--conference-scope neurips-2025 --keyword "xxx"` | `exports/neurips-2025/` |

### Common Issues and Solutions

**Q: No papers found?**
- Check if the conference name is correct
- Try using `broad` mode instead of `strict`
- Verify the year format (e.g., use 2025, not '25)

**Q: Too few/large number of papers?**
- Adjust `--mode` from `strict` to `broad` or vice versa
- Modify conference scope to specific year

**Q: HTTP 429/503 errors?**
- arXiv API rate limiting (429) or service unavailable (503)
- Solutions:
  - Use proxy: `HTTPS_PROXY=http://127.0.0.1:7890 python scripts/update_papers.py ...`
  - Increase delay: `--delay 10` or `--delay 20`
  - Shorten keyword: use "infrared" instead of "infrared small target detection"
  - Wait a few minutes and retry

## Category Configuration

The crawler automatically categorizes papers into different categories based on keyword matching in title and abstract. These categories are **predefined in the code** and can be modified.

### Default Categories

| Category | English | Chinese | Keywords |
|---|---|---|---|
| Segmentation | 分割 | 图像分割 | segmentation, segment, delineation, contour, mask |
| Reconstruction | 重建 | 图像重建 | reconstruction, reconstruct, restoration, super-resolution, denoising |
| Classification | 分类 | 分类/检测 | classification, classify, classifier, recognition, detection, diagnosis |
| Image Registration | 图像配准 | 图像配准 | registration, alignment, deformable, deformation |
| Domain Adaptation | 域适应 | 域适应 | domain adaptation, transfer learning, cross-domain, domain generalization |
| Generative Models | 生成模型 | 生成模型 | generative, generation, synthesis, GAN, diffusion, VAE, autoencoder |
| General | 通用 | 通用 | (fallback category) |

### How Categorization Works

1. **Keyword Matching**: Each category has predefined regex patterns with weights
2. **Score Calculation**: Papers get scores based on keyword matches in title (2x weight) and abstract
3. **Threshold**: Papers must exceed threshold to be assigned to a category
4. **Multi-label**: Papers can belong to multiple categories
5. **Fallback**: Papers with no strong match go to "General"

### How to Modify Categories

To customize categories, edit `scripts/update_papers.py`:

#### Step 1: Modify CATEGORY_ORDER

```python
# Add, remove, or reorder categories
CATEGORY_ORDER = [
    "Segmentation",
    "Reconstruction",
    "Classification",
    "Image Registration",
    "Domain Adaptation",
    "Generative Models",
    "General",
    # Add new category here
]
```

#### Step 2: Modify CATEGORY_RULES

```python
# Add or modify keyword rules for each category
CATEGORY_RULES = {
    "Segmentation": [
        (r"\bsegmentation\b", 3),  # (pattern, weight)
        (r"\bsegment\b", 2),
        # Add more patterns...
    ],
    # Add new category rules...
}
```

#### Step 3: Modify CATEGORY_MARKERS

```python
# Add markers for template rendering
CATEGORY_MARKERS = {
    "Segmentation": "SEGMENTATION",
    # Add new markers...
}
```

#### Step 4: Modify CATEGORY_THRESHOLDS

```python
# Adjust threshold for each category
CATEGORY_THRESHOLDS = {
    "Segmentation": 2,
    # Adjust thresholds...
}
```

#### Step 5: Update README.md Template

Add category sections in README.md:

```markdown
## Category Name

*This list is automatically generated.*

<!-- BEGIN CATEGORY_MARKER_PAPERS -->
*(papers will be inserted here by crawler)*
<!-- END CATEGORY_MARKER_PAPERS -->
```

### Category Customization Example

**Example: Add "Object Detection" as a new category**

1. Add to CATEGORY_ORDER:
```python
CATEGORY_ORDER = [
    "Segmentation",
    "Object Detection",  # NEW
    "Reconstruction",
    ...
]
```

2. Add to CATEGORY_RULES:
```python
CATEGORY_RULES = {
    "Object Detection": [
        (r"\bobject detection\b", 3),
        (r"\bdetection\b", 2),
        (r"\bdetector\b", 2),
    ],
    ...
}
```

3. Add to CATEGORY_MARKERS:
```python
CATEGORY_MARKERS = {
    "Object Detection": "OBJECT_DETECTION",
    ...
}
```

4. Add section to README.md:
```markdown
## Object Detection

<!-- BEGIN OBJECT_DETECTION_PAPERS -->
*Papers will be inserted here*
<!-- END OBJECT_DETECTION_PAPERS -->
```

### Language-Specific Customization

For different conferences, you may want to add language-specific keywords:

```python
CATEGORY_RULES = {
    "Classification": [
        (r"\bclassification\b", 3),
        (r"\bdetection\b", 2),
        # Add non-English keywords for medical conferences
        (r"\b诊断\b", 3),  # Chinese: diagnosis
        (r"\b分類\b", 3),  # Traditional Chinese: classification
    ],
}
```

## 📋 Table of Contents

- [How to Contribute](#how-to-contribute)
- [Inclusion Policy](#-inclusion-policy)
- [Trust and Validation](#-trust-and-validation)
- [Coverage Report](#-coverage-report)
- [Segmentation](#segmentation)
- [Reconstruction](#reconstruction)
- [Classification](#classification)
- [Image Registration](#image-registration)
- [Domain Adaptation](#domain-adaptation)
- [Generative Models](#generative-models)
- [General](#general)

## 🤝 How to Contribute

Contributions are welcome! While this list is automatically maintained by a bot that searches arXiv for MICCAI papers (scope configurable), we appreciate human oversight to ensure quality and completeness.

**Ways to contribute:**
- 🐛 **Report errors**: broken links, malformed entries, stale papers, wrong category placement
- 📝 **Add missing papers**: papers that match the active conference scope and provide public code
- 🏷️ **Suggest better categorization**: improve multi-label quality without removing valid overlap
- 💡 **Propose taxonomy improvements**: suggest category changes with examples

**Before contributing:**
1. Provide evidence that the paper is associated with the active conference scope
2. Ensure the code repository is public and reachable
3. Verify links and category suggestions are specific and reproducible

## ✅ Inclusion Policy

- The source of truth is arXiv metadata (`title`, `abstract`, and `comment`) plus public repository links.
- Papers must include MICCAI wording in searchable arXiv metadata; when scope is `miccai-2026`, entries must indicate 2026.
- Code links must resolve to supported public hosts: GitHub, GitLab, or Hugging Face.
- A paper may appear in multiple categories intentionally when it strongly matches multiple tasks.

## 🔍 Trust and Validation

- Content between `<!-- BEGIN ... -->` and `<!-- END ... -->` markers is bot-generated and overwritten on each successful run.
- Daily automation fails fast if discovery is incomplete, generated markdown is malformed, or quality checks fail.
- README validation checks marker integrity, malformed URLs, duplicate entries per category, and unsupported code hosts.
- Default automation runs with `--conference-scope miccai-all-years --mode broad --tracks all`.
- Maintainers can narrow scope with `--conference-scope miccai-2026` and stricter matching via `--mode strict`.

## 📈 Coverage Report

<!-- BEGIN COVERAGE_REPORT -->
- Conference scope: `ICCV-2025`
- Discovery mode: `strict`
- Tracks: `all`
- Total code-backed papers: `84`
- Fetched arXiv records: `324`
- Unique arXiv records: `319`
- Filtered (non-target): `10`
- Filtered (track): `0`
- Filtered (no code links): `225`

| Category | Count | Gap to 1000 |
|---|---:|---:|
| Segmentation | 11 | 989 |
| Reconstruction | 9 | 991 |
| Classification | 17 | 983 |
| Image Registration | 19 | 981 |
| Domain Adaptation | 5 | 995 |
| Generative Models | 25 | 975 |
| General | 31 | 969 |
<!-- END COVERAGE_REPORT -->

## 📊 Segmentation

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN SEGMENTATION_PAPERS -->
* **[GDKVM: Echocardiography Video Segmentation via Spatiotemporal Key-Value Memory with Gated Delta Rule](https://arxiv.org/abs/2512.10252v1)** - [Code](https://github.com/wangrui2025/gdkvm) (confidence: high)
* **[Exploiting Domain Properties in Language-Driven Domain Generalization for Semantic Segmentation](https://arxiv.org/abs/2512.03508v2)** - [Code](https://github.com/jone1222/dpmformer) (confidence: high)
* **[MINDiff: Mask-Integrated Negative Attention for Controlling Overfitting in Text-to-Image Personalization](https://arxiv.org/abs/2511.17888v1)** - [Code](https://github.com/seuleepy/mindiff) (confidence: medium)
* **[Controllable-LPMoE: Adapting to Challenging Object Segmentation via Dynamic Local Priors from Mixture-of-Experts](https://arxiv.org/abs/2510.21114v1)** - [Code](https://github.com/csysi/controllable-lpmoe) (confidence: high)
* **[MK-UNet: Multi-kernel Lightweight CNN for Medical Image Segmentation](https://arxiv.org/abs/2509.18493v1)** - [Code](https://github.com/sldgroup/mk-unet) (confidence: high)
* **[The 1st Solution for 7th LSVOS RVOS Track: SaSaSa2VA](https://arxiv.org/abs/2509.16972v2)** - [Code](https://github.com/bytedance/sa2va) (confidence: medium)
* **[Plug-in Feedback Self-adaptive Attention in CLIP for Training-free Open-Vocabulary Segmentation](https://arxiv.org/abs/2508.20265v1)** - [Code](https://github.com/chi-chi-zx/fsa) (confidence: high)
* **[AutoQ-VIS: Improving Unsupervised Video Instance Segmentation via Automatic Quality Assessment](https://arxiv.org/abs/2508.19808v1)** - [Code](https://github.com/wcbup/autoq-vis) (confidence: high)
* **[DictAS: A Framework for Class-Generalizable Few-Shot Anomaly Segmentation via Dictionary Lookup](https://arxiv.org/abs/2508.13560v2)** - [Code](https://github.com/xiaozhen228/dictas) (confidence: high)
* **[OVG-HQ: Online Video Grounding with Hybrid-modal Queries](https://arxiv.org/abs/2508.11903v1)** - [Code](https://github.com/maojiaqi2324/ovg-hq) (confidence: medium)
* **[Revisiting Efficient Semantic Segmentation: Learning Offsets for Better Spatial and Class Feature Alignment](https://arxiv.org/abs/2508.08811v1)** - [Code](https://github.com/hvision-nku/offseg) (confidence: high)
<!-- END SEGMENTATION_PAPERS -->

## 🔧 Reconstruction

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN RECONSTRUCTION_PAPERS -->
* **[MedVSR: Medical Video Super-Resolution with Cross State-Space Propagation](https://arxiv.org/abs/2509.21265v2)** - [Code](https://github.com/cuhk-aim-group/medvsr) (confidence: high)
* **[From Prompt to Progression: Taming Video Diffusion Models for Seamless Attribute Transition](https://arxiv.org/abs/2509.19690v1)** - [Code](https://github.com/lynn-ling-lo/prompt2progression) (confidence: medium)
* **[Objectness Similarity: Capturing Object-Level Fidelity in 3D Scene Evaluation](https://arxiv.org/abs/2509.09143v1)** - [Code](https://github.com/objectness-similarity/osim) (confidence: medium)
* **[VQualA 2025 Challenge on Image Super-Resolution Generated Content Quality Assessment: Methods and Results](https://arxiv.org/abs/2509.06413v1)** - [Code](https://github.com/lighting-yxli/isrgen-qa) (confidence: high)
* **[Towards More Diverse and Challenging Pre-training for Point Cloud Learning: Self-Supervised Cross Reconstruction with Decoupled Views](https://arxiv.org/abs/2509.01250v1)** - [Code](https://github.com/ahapbean/point-pqae) (confidence: high)
* **[Automated Feature Tracking for Real-Time Kinematic Analysis and Shape Estimation of Carbon Nanotube Growth](https://arxiv.org/abs/2508.19232v1)** - [Code](https://github.com/kavehsfv/vftrack) (confidence: medium)
* **[MUSE: Multi-Subject Unified Synthesis via Explicit Layout Semantic Expansion](https://arxiv.org/abs/2508.14440v1)** - [Code](https://github.com/pf0607/muse) (confidence: medium)
* **[RayletDF: Raylet Distance Fields for Generalizable 3D Surface Reconstruction from Point Clouds or Gaussians](https://arxiv.org/abs/2508.09830v1)** - [Code](https://github.com/vlar-group/rayletdf) (confidence: high)
* **[Reverse Convolution and Its Applications to Image Restoration](https://arxiv.org/abs/2508.09824v2)** - [Code](https://github.com/cszn/conversenet) (confidence: high)
<!-- END RECONSTRUCTION_PAPERS -->

## 🏷️ Classification

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN CLASSIFICATION_PAPERS -->
* **[Attention to Neural Plagiarism: Diffusion Models Can Plagiarize Your Copyrighted Images!](https://arxiv.org/abs/2603.00150v1)** - [Code](https://github.com/zzzucf/neural-plagiarism) (confidence: medium)
* **[DeepShield: Fortifying Deepfake Video Detection with Local and Global Forgery Analysis](https://arxiv.org/abs/2510.25237v2)** - [Code](https://github.com/lijichang/deepshield) (confidence: high)
* **[Beyond Single Images: Retrieval Self-Augmented Unsupervised Camouflaged Object Detection](https://arxiv.org/abs/2510.18437v1)** - [Code](https://github.com/xiaohainku/rise) (confidence: high)
* **[CARDIUM: Congenital Anomaly Recognition with Diagnostic Images and Unified Medical records](https://arxiv.org/abs/2510.15208v2)** - [Code](https://github.com/bcv-uniandes/cardium) (confidence: high)
* **[Hierarchical Reasoning with Vision-Language Models for Incident Reports from Dashcam Videos](https://arxiv.org/abs/2510.12190v1)** - [Code](https://github.com/riron1206/kaggle-2coool-2nd-place-solution) (confidence: medium)
* **[Cooperative Pseudo Labeling for Unsupervised Federated Classification](https://arxiv.org/abs/2510.10100v1)** - [Code](https://github.com/krumpguo/fedcopl) (confidence: high)
* **[StyleKeeper: Prevent Content Leakage using Negative Visual Query Guidance](https://arxiv.org/abs/2510.06827v1)** - [Code](https://github.com/naver-ai/stylekeeper) (confidence: medium)
* **[TY-RIST: Tactical YOLO Tricks for Real-time Infrared Small Target Detection](https://arxiv.org/abs/2509.22909v1)** - [Code](https://github.com/moured/ty-rist) (confidence: high)
* **[DinoAtten3D: Slice-Level Attention Aggregation of DinoV2 for 3D Brain MRI Anomaly Classification](https://arxiv.org/abs/2509.12512v1)** - [Code](https://github.com/rafsani/dinoatten3d) (confidence: high)
* **[Objectness Similarity: Capturing Object-Level Fidelity in 3D Scene Evaluation](https://arxiv.org/abs/2509.09143v1)** - [Code](https://github.com/objectness-similarity/osim) (confidence: high)
* **[SALAD -- Semantics-Aware Logical Anomaly Detection](https://arxiv.org/abs/2509.02101v1)** - [Code](https://github.com/maticfuc/salad) (confidence: high)
* **[Toward Socially Aware Vision-Language Models: Evaluating Cultural Competence Through Multimodal Story Generation](https://arxiv.org/abs/2508.16762v1)** - [Code](https://github.com/arkamukherjee0/mmcultural) (confidence: medium)
* **[Normal and Abnormal Pathology Knowledge-Augmented Vision-Language Model for Anomaly Detection in Pathology Images](https://arxiv.org/abs/2508.15256v2)** - [Code](https://github.com/quiil/iccv2025_ano-navila) (confidence: high)
* **[Automated Model Evaluation for Object Detection via Prediction Consistency and Reliability](https://arxiv.org/abs/2508.12082v2)** - [Code](https://github.com/yonseiml/autoeval-det) (confidence: high)
* **[Hybrid Generative Fusion for Efficient and Privacy-Preserving Face Recognition Dataset Generation](https://arxiv.org/abs/2508.10672v2)** - [Code](https://github.com/ferry-li/datacv_fr) (confidence: high)
* **[UniConvNet: Expanding Effective Receptive Field while Maintaining Asymptotically Gaussian Distribution for ConvNets of Any Scale](https://arxiv.org/abs/2508.09000v1)** - [Code](https://github.com/ai-paperwithcode/uniconvnet) (confidence: medium)
* **[Revisiting Efficient Semantic Segmentation: Learning Offsets for Better Spatial and Class Feature Alignment](https://arxiv.org/abs/2508.08811v1)** - [Code](https://github.com/hvision-nku/offseg) (confidence: medium)
<!-- END CLASSIFICATION_PAPERS -->

## 🔄 Image Registration

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN IMAGE_REGISTRATION_PAPERS -->
* **[Towards Zero-Shot Point Cloud Registration Across Diverse Scales, Scenes, and Sensor Setups](https://arxiv.org/abs/2601.02759v1)** - [Code](https://github.com/mit-spark/buffer-x) (confidence: high)
* **[GDKVM: Echocardiography Video Segmentation via Spatiotemporal Key-Value Memory with Gated Delta Rule](https://arxiv.org/abs/2512.10252v1)** - [Code](https://github.com/wangrui2025/gdkvm) (confidence: medium)
* **[Exploiting Domain Properties in Language-Driven Domain Generalization for Semantic Segmentation](https://arxiv.org/abs/2512.03508v2)** - [Code](https://github.com/jone1222/dpmformer) (confidence: medium)
* **[MINDiff: Mask-Integrated Negative Attention for Controlling Overfitting in Text-to-Image Personalization](https://arxiv.org/abs/2511.17888v1)** - [Code](https://github.com/seuleepy/mindiff) (confidence: medium)
* **[Controllable-LPMoE: Adapting to Challenging Object Segmentation via Dynamic Local Priors from Mixture-of-Experts](https://arxiv.org/abs/2510.21114v1)** - [Code](https://github.com/csysi/controllable-lpmoe) (confidence: medium)
* **[Stroke2Sketch: Harnessing Stroke Attributes for Training-Free Sketch Generation](https://arxiv.org/abs/2510.16319v1)** - [Code](https://github.com/rane7/stroke2sketch) (confidence: medium)
* **[Spatial Preference Rewarding for MLLMs Spatial Understanding](https://arxiv.org/abs/2510.14374v1)** - [Code](https://github.com/hanqiu-hq/spr) (confidence: medium)
* **[Hybrid-grained Feature Aggregation with Coarse-to-fine Language Guidance for Self-supervised Monocular Depth Estimation](https://arxiv.org/abs/2510.09320v1)** - [Code](https://github.com/zhangwenyao1/hybrid-depth) (confidence: medium)
* **[IMG: Calibrating Diffusion Models via Implicit Multimodal Guidance](https://arxiv.org/abs/2509.26231v1)** - [Code](https://github.com/shi-labs/img-multimodal-diffusion-alignment) (confidence: medium)
* **[MedVSR: Medical Video Super-Resolution with Cross State-Space Propagation](https://arxiv.org/abs/2509.21265v2)** - [Code](https://github.com/cuhk-aim-group/medvsr) (confidence: medium)
* **[From Prompt to Progression: Taming Video Diffusion Models for Seamless Attribute Transition](https://arxiv.org/abs/2509.19690v1)** - [Code](https://github.com/lynn-ling-lo/prompt2progression) (confidence: medium)
* **[Multi-View Slot Attention Using Paraphrased Texts for Face Anti-Spoofing](https://arxiv.org/abs/2509.06336v2)** - [Code](https://github.com/elune001/mvp-fas) (confidence: medium)
* **[Plug-in Feedback Self-adaptive Attention in CLIP for Training-free Open-Vocabulary Segmentation](https://arxiv.org/abs/2508.20265v1)** - [Code](https://github.com/chi-chi-zx/fsa) (confidence: medium)
* **[Toward Socially Aware Vision-Language Models: Evaluating Cultural Competence Through Multimodal Story Generation](https://arxiv.org/abs/2508.16762v1)** - [Code](https://github.com/arkamukherjee0/mmcultural) (confidence: medium)
* **[MUSE: Multi-Subject Unified Synthesis via Explicit Layout Semantic Expansion](https://arxiv.org/abs/2508.14440v1)** - [Code](https://github.com/pf0607/muse) (confidence: medium)
* **[Beyond Simple Edits: Composed Video Retrieval with Dense Modifications](https://arxiv.org/abs/2508.14039v1)** - [Code](https://github.com/omkarthawakar/bse-covr) (confidence: medium)
* **[Backdooring Self-Supervised Contrastive Learning by Noisy Alignment](https://arxiv.org/abs/2508.14015v1)** - [Code](https://github.com/jsrdcht/noisy-alignment) (confidence: high)
* **[DictAS: A Framework for Class-Generalizable Few-Shot Anomaly Segmentation via Dictionary Lookup](https://arxiv.org/abs/2508.13560v2)** - [Code](https://github.com/xiaozhen228/dictas) (confidence: medium)
* **[Revisiting Efficient Semantic Segmentation: Learning Offsets for Better Spatial and Class Feature Alignment](https://arxiv.org/abs/2508.08811v1)** - [Code](https://github.com/hvision-nku/offseg) (confidence: high)
<!-- END IMAGE_REGISTRATION_PAPERS -->

## 🔀 Domain Adaptation

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN DOMAIN_ADAPTATION_PAPERS -->
* **[Towards Zero-Shot Point Cloud Registration Across Diverse Scales, Scenes, and Sensor Setups](https://arxiv.org/abs/2601.02759v1)** - [Code](https://github.com/mit-spark/buffer-x) (confidence: medium)
* **[Exploiting Domain Properties in Language-Driven Domain Generalization for Semantic Segmentation](https://arxiv.org/abs/2512.03508v2)** - [Code](https://github.com/jone1222/dpmformer) (confidence: high)
* **[DeepShield: Fortifying Deepfake Video Detection with Local and Global Forgery Analysis](https://arxiv.org/abs/2510.25237v2)** - [Code](https://github.com/lijichang/deepshield) (confidence: medium)
* **[Multi-View Slot Attention Using Paraphrased Texts for Face Anti-Spoofing](https://arxiv.org/abs/2509.06336v2)** - [Code](https://github.com/elune001/mvp-fas) (confidence: medium)
* **[Generalizable Object Re-Identification via Visual In-Context Prompting](https://arxiv.org/abs/2508.21222v1)** - [Code](https://github.com/hzzone/vicp) (confidence: medium)
<!-- END DOMAIN_ADAPTATION_PAPERS -->

## 🎨 Generative Models

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN GENERATIVE_MODELS_PAPERS -->
* **[Attention to Neural Plagiarism: Diffusion Models Can Plagiarize Your Copyrighted Images!](https://arxiv.org/abs/2603.00150v1)** - [Code](https://github.com/zzzucf/neural-plagiarism) (confidence: high)
* **[MINDiff: Mask-Integrated Negative Attention for Controlling Overfitting in Text-to-Image Personalization](https://arxiv.org/abs/2511.17888v1)** - [Code](https://github.com/seuleepy/mindiff) (confidence: medium)
* **[Sketch-to-Layout: Sketch-Guided Multimodal Layout Generation](https://arxiv.org/abs/2510.27632v1)** - [Code](https://github.com/google-deepmind/sketch_to_layout) (confidence: high)
* **[DeepShield: Fortifying Deepfake Video Detection with Local and Global Forgery Analysis](https://arxiv.org/abs/2510.25237v2)** - [Code](https://github.com/lijichang/deepshield) (confidence: high)
* **[Stroke2Sketch: Harnessing Stroke Attributes for Training-Free Sketch Generation](https://arxiv.org/abs/2510.16319v1)** - [Code](https://github.com/rane7/stroke2sketch) (confidence: high)
* **[Hierarchical Reasoning with Vision-Language Models for Incident Reports from Dashcam Videos](https://arxiv.org/abs/2510.12190v1)** - [Code](https://github.com/riron1206/kaggle-2coool-2nd-place-solution) (confidence: medium)
* **[StyleKeeper: Prevent Content Leakage using Negative Visual Query Guidance](https://arxiv.org/abs/2510.06827v1)** - [Code](https://github.com/naver-ai/stylekeeper) (confidence: high)
* **[ConceptSplit: Decoupled Multi-Concept Personalization of Diffusion Models via Token-wise Adaptation and Attention Disentanglement](https://arxiv.org/abs/2510.04668v1)** - [Code](https://github.com/ku-vgi/conceptsplit) (confidence: high)
* **[IMG: Calibrating Diffusion Models via Implicit Multimodal Guidance](https://arxiv.org/abs/2509.26231v1)** - [Code](https://github.com/shi-labs/img-multimodal-diffusion-alignment) (confidence: high)
* **[From Prompt to Progression: Taming Video Diffusion Models for Seamless Attribute Transition](https://arxiv.org/abs/2509.19690v1)** - [Code](https://github.com/lynn-ling-lo/prompt2progression) (confidence: high)
* **[DACoN: DINO for Anime Paint Bucket Colorization with Any Number of Reference Images](https://arxiv.org/abs/2509.14685v2)** - [Code](https://github.com/kzmngt/dacon) (confidence: medium)
* **[Objectness Similarity: Capturing Object-Level Fidelity in 3D Scene Evaluation](https://arxiv.org/abs/2509.09143v1)** - [Code](https://github.com/objectness-similarity/osim) (confidence: medium)
* **[Discovering Divergent Representations between Text-to-Image Models](https://arxiv.org/abs/2509.08940v1)** - [Code](https://github.com/adobe-research/compcon) (confidence: high)
* **[VQualA 2025 Challenge on Image Super-Resolution Generated Content Quality Assessment: Methods and Results](https://arxiv.org/abs/2509.06413v1)** - [Code](https://github.com/lighting-yxli/isrgen-qa) (confidence: high)
* **[Towards More Diverse and Challenging Pre-training for Point Cloud Learning: Self-Supervised Cross Reconstruction with Decoupled Views](https://arxiv.org/abs/2509.01250v1)** - [Code](https://github.com/ahapbean/point-pqae) (confidence: high)
* **[AutoQ-VIS: Improving Unsupervised Video Instance Segmentation via Automatic Quality Assessment](https://arxiv.org/abs/2508.19808v1)** - [Code](https://github.com/wcbup/autoq-vis) (confidence: medium)
* **[Automated Feature Tracking for Real-Time Kinematic Analysis and Shape Estimation of Carbon Nanotube Growth](https://arxiv.org/abs/2508.19232v1)** - [Code](https://github.com/kavehsfv/vftrack) (confidence: medium)
* **[Toward Socially Aware Vision-Language Models: Evaluating Cultural Competence Through Multimodal Story Generation](https://arxiv.org/abs/2508.16762v1)** - [Code](https://github.com/arkamukherjee0/mmcultural) (confidence: high)
* **[CineScale: Free Lunch in High-Resolution Cinematic Visual Generation](https://arxiv.org/abs/2508.15774v1)** - [Code](https://github.com/eyeline-labs/cinescale) (confidence: high)
* **[Controllable Latent Space Augmentation for Digital Pathology](https://arxiv.org/abs/2508.14588v1)** - [Code](https://github.com/mics-lab/histaug) (confidence: medium)
* **[MUSE: Multi-Subject Unified Synthesis via Explicit Layout Semantic Expansion](https://arxiv.org/abs/2508.14440v1)** - [Code](https://github.com/pf0607/muse) (confidence: high)
* **[WP-CLIP: Leveraging CLIP to Predict Wölfflin's Principles in Visual Art](https://arxiv.org/abs/2508.12668v1)** - [Code](https://github.com/abhijay9/wpclip) (confidence: medium)
* **[Hybrid Generative Fusion for Efficient and Privacy-Preserving Face Recognition Dataset Generation](https://arxiv.org/abs/2508.10672v2)** - [Code](https://github.com/ferry-li/datacv_fr) (confidence: high)
* **[Preacher: Paper-to-Video Agentic System](https://arxiv.org/abs/2508.09632v6)** - [Code](https://github.com/gen-verse/paper2video) (confidence: medium)
* **[Preview WB-DH: Towards Whole Body Digital Human Bench for the Generation of Whole-body Talking Avatar Videos](https://arxiv.org/abs/2508.08891v1)** - [Code](https://github.com/deepreasonings/wholebodybenchmark) (confidence: high)
<!-- END GENERATIVE_MODELS_PAPERS -->

## 📚 General

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN GENERAL_PAPERS -->
* **[FG-OrIU: Towards Better Forgetting via Feature-Gradient Orthogonality for Incremental Unlearning](https://arxiv.org/abs/2601.13578v1)** - [Code](https://github.com/raian08/fg-oriu) (confidence: medium)
* **[Factorized Learning for Temporally Grounded Video-Language Models](https://arxiv.org/abs/2512.24097v1)** - [Code](https://github.com/nusnlp/d2vlm) (confidence: medium)
* **[TRACE: Textual Reasoning for Affordance Coordinate Extraction](https://arxiv.org/abs/2511.01999v1)** - [Code](https://github.com/jink-ucla/trace) (confidence: medium)
* **[Enhancing Adversarial Transferability by Balancing Exploration and Exploitation with Gradient-Guided Sampling](https://arxiv.org/abs/2511.00411v1)** - [Code](https://github.com/anuin-cat/ggs) (confidence: medium)
* **[Understanding Multi-View Transformers](https://arxiv.org/abs/2510.24907v1)** - [Code](https://github.com/juliengaubil/und3rstand) (confidence: medium)
* **[Enpowering Your Pansharpening Models with Generalizability: Unified Distribution is All You Need](https://arxiv.org/abs/2510.22217v1)** - [Code](https://github.com/yc-cui/unipan) (confidence: medium)
* **[Group Inertial Poser: Multi-Person Pose and Global Translation from Sparse Inertial Sensors and Ultra-Wideband Ranging](https://arxiv.org/abs/2510.21654v1)** - [Code](https://github.com/eth-siplab/groupinertialposer) (confidence: medium)
* **[HccePose(BF): Predicting Front & Back Surfaces to Construct Ultra-Dense 2D-3D Correspondences for Pose Estimation](https://arxiv.org/abs/2510.10177v2)** - [Code](https://github.com/wangyulin-seu/hccepose) (confidence: medium)
* **[SpecGuard: Spectral Projection-based Advanced Invisible Watermarking](https://arxiv.org/abs/2510.07302v1)** - [Code](https://github.com/inzamamuldu/specguard_iccv_2025) (confidence: medium)
* **[VideoMiner: Iteratively Grounding Key Frames of Hour-Long Videos via Tree-based Group Relative Policy Optimization](https://arxiv.org/abs/2510.06040v1)** - [Code](https://github.com/caoxinye/videominer) (confidence: medium)
* **[Guiding Multimodal Large Language Models with Blind and Low Vision People Visual Questions for Proactive Visual Interpretations](https://arxiv.org/abs/2510.01576v1)** - [Code](https://github.com/rgonzalezp/guiding-multimodal-large-language-models-with-blind-and-low-vision-people-visual-questions) (confidence: medium)
* **[A Multi-purpose Tracking Framework for Salmon Welfare Monitoring in Challenging Environments](https://arxiv.org/abs/2509.25969v1)** - [Code](https://github.com/espenbh/boostcomptrack) (confidence: medium)
* **[LayerD: Decomposing Raster Graphic Designs into Layers](https://arxiv.org/abs/2509.25134v1)** - [Code](https://github.com/cyberagentailab/layerd) (confidence: medium)
* **[PU-Gaussian: Point Cloud Upsampling using 3D Gaussian Representation](https://arxiv.org/abs/2509.20207v1)** - [Code](https://github.com/mvg-inatech/pu-gaussian) (confidence: medium)
* **[PS3: A Multimodal Transformer Integrating Pathology Reports with Histology Images and Biological Pathways for Cancer Survival Prediction](https://arxiv.org/abs/2509.20022v1)** - [Code](https://github.com/manahilr/ps3) (confidence: medium)
* **[Global Regulation and Excitation via Attention Tuning for Stereo Matching](https://arxiv.org/abs/2509.15891v1)** - [Code](https://github.com/jarvislee0423/great-stereo) (confidence: medium)
* **[Depth AnyEvent: A Cross-Modal Distillation Paradigm for Event-Based Monocular Depth Estimation](https://arxiv.org/abs/2509.15224v1)** - [Code](https://github.com/bartn8/depthanyevent) (confidence: medium)
* **[Building a General SimCLR Self-Supervised Foundation Model Across Neurological Diseases to Advance 3D Brain MRI Diagnoses](https://arxiv.org/abs/2509.10620v1)** - [Code](https://github.com/emilykaczmarek/3d-neuro-simclr) (confidence: medium)
* **[FlowSeek: Optical Flow Made Easier with Depth Foundation Models and Motion Bases](https://arxiv.org/abs/2509.05297v1)** - [Code](https://github.com/mattpoggi/flowseek) (confidence: medium)
* **[Robust Experts: the Effect of Adversarial Training on CNNs with Sparse Mixture-of-Experts Layers](https://arxiv.org/abs/2509.05086v1)** - [Code](https://github.com/kastel-mobilitylab/robust-sparse-moes) (confidence: medium)
* **[LUT-Fuse: Towards Extremely Fast Infrared and Visible Image Fusion via Distillation to Learnable Look-Up Tables](https://arxiv.org/abs/2509.00346v1)** - [Code](https://github.com/zyb5/lut-fuse) (confidence: medium)
* **[GCAV: A Global Concept Activation Vector Framework for Cross-Layer Consistency in Interpretability](https://arxiv.org/abs/2508.21197v2)** - [Code](https://github.com/zhenghao-he/gcav) (confidence: medium)
* **[TemCoCo: Temporally Consistent Multi-modal Video Fusion with Visual-Semantic Collaboration](https://arxiv.org/abs/2508.17817v1)** - [Code](https://github.com/meiqi-gong/temcoco) (confidence: medium)
* **[PersPose: 3D Human Pose Estimation with Perspective Encoding and Perspective Rotation](https://arxiv.org/abs/2508.17239v2)** - [Code](https://github.com/kenadamsjoseph/perspose) (confidence: medium)
* **[Learning Point Cloud Representations with Pose Continuity for Depth-Based Category-Level 6D Object Pose Estimation](https://arxiv.org/abs/2508.14358v1)** - [Code](https://github.com/zhujunli1993/hrc-pose) (confidence: medium)
* **[CHARM3R: Towards Unseen Camera Height Robust Monocular 3D Detector](https://arxiv.org/abs/2508.11185v1)** - [Code](https://github.com/abhi1kumar/charm3r) (confidence: medium)
* **[Processing and acquisition traces in visual encoders: What does CLIP know about your camera?](https://arxiv.org/abs/2508.10637v2)** - [Code](https://github.com/ryan-caesar-ramos/visual-encoder-traces) (confidence: medium)
* **[TRACE: Learning 3D Gaussian Physical Dynamics from Multi-view Videos](https://arxiv.org/abs/2508.09811v1)** - [Code](https://github.com/vlar-group/trace) (confidence: medium)
* **[Harnessing Input-Adaptive Inference for Efficient VLN](https://arxiv.org/abs/2508.09262v1)** - [Code](https://github.com/secure-ai-systems-group/adaptive-vision-and-language-navigation) (confidence: medium)
* **[Efficient Face Image Quality Assessment via Self-training and Knowledge Distillation](https://arxiv.org/abs/2507.15709v2)** - [Code](https://github.com/sunwei925/efficient-fiqa) (confidence: medium)
* **[LENS: Multi-level Evaluation of Multimodal Reasoning with Large Language Models](https://arxiv.org/abs/2505.15616v1)** - [Code](https://github.com/lens4mllms/lens) (confidence: medium)
<!-- END GENERAL_PAPERS -->

---

**Repository Topics**: awesome, awesome-list, miccai, miccai2026, medical-imaging, deep-learning, computer-vision, segmentation, reconstruction, classification, medical-image-analysis, artificial-intelligence

**Conference Scope**: ICCV-2025
**Discovery Mode**: strict

**Last Updated**: 2026-05-09 02:42 UTC by GitHub Actions

**License**: Apache License 2.0
