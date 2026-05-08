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
- Conference scope: `neurips-2025`
- Discovery mode: `strict`
- Tracks: `all`
- Total code-backed papers: `94`
- Fetched arXiv records: `500`
- Unique arXiv records: `0`
- Filtered (non-target): `0`
- Filtered (track): `0`
- Filtered (no code links): `406`

| Category | Count | Gap to 1000 |
|---|---:|---:|
| Segmentation | 17 | 983 |
| Reconstruction | 5 | 995 |
| Classification | 87 | 913 |
| Image Registration | 8 | 992 |
| Domain Adaptation | 6 | 994 |
| Generative Models | 12 | 988 |
| General | 6 | 994 |
<!-- END COVERAGE_REPORT -->

## 📊 Segmentation

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN SEGMENTATION_PAPERS -->
* **[Rethinking IRSTD: Single-Point Supervision Guided Encoder-only Framework is Enough for Infrared Small Target Detection](https://arxiv.org/abs/2604.05363v1)** - [Code](https://github.com/nirixiang/spire-irstd) (confidence: medium)
* **[Point-to-Mask: From Arbitrary Point Annotations to Mask-Level Infrared Small Target Detection](https://arxiv.org/abs/2603.16257v1)** - [Code](https://github.com/gaoscience/point-to-mask) (confidence: high)
* **[CSPENet: Contour-Aware and Saliency Priors Embedding Network for Infrared Small Target Detection](https://arxiv.org/abs/2505.09943v1)** - [Code](https://github.com/idip2025/cspenet) (confidence: high)
* **[Vision-Language Model for Object Detection and Segmentation: A Review and Evaluation](https://arxiv.org/abs/2504.09480v1)** - [Code](https://github.com/better-chao/perceptual_abilities_evaluation) (confidence: high)
* **[Unleashing the Power of Generic Segmentation Models: A Simple Baseline for Infrared Small Target Detection](https://arxiv.org/abs/2409.04714v1)** - [Code](https://github.com/o937-blip/simir) (confidence: high)
* **[Towards Robust Infrared Small Target Detection: A Feature-Enhanced and Sensitivity-Tunable Framework](https://arxiv.org/abs/2407.20090v3)** - [Code](https://github.com/yuchuang1205/fest-framework) (confidence: medium)
* **[Background Semantics Matter: Cross-Task Feature Exchange Network for Clustered Infrared Small Target Detection](https://arxiv.org/abs/2407.20078v3)** - [Code](https://github.com/grokcv/bafe-net) (confidence: medium)
* **[SMPISD-MTPNet: Scene Semantic Prior-Assisted Infrared Ship Detection Using Multi-Task Perception Networks](https://arxiv.org/abs/2407.18487v1)** - [Code](https://github.com/greekinroma/kmndnet) (confidence: medium)
* **[Mitigate Target-level Insensitivity of Infrared Small Target Detection via Posterior Distribution Modeling](https://arxiv.org/abs/2403.08380v1)** - [Code](https://github.com/li-haoqing/irstd-diff) (confidence: high)
* **[Click on Mask: A Labor-efficient Annotation Framework with Level Set for Infrared Small Target Detection](https://arxiv.org/abs/2310.12562v1)** - [Code](https://github.com/li-haoqing/com) (confidence: high)
* **[Mapping Degeneration Meets Label Evolution: Learning Infrared Small Target Detection with Single Point Supervision](https://arxiv.org/abs/2304.01484v3)** - [Code](https://github.com/xinyiying/lesps) (confidence: medium)
* **[ABC: Attention with Bilinear Correlation for Infrared Small Target Detection](https://arxiv.org/abs/2303.10321v1)** - [Code](https://github.com/panpeiwen/abc) (confidence: medium)
* **[Local Contrast and Global Contextual Information Make Infrared Small Object Salient Again](https://arxiv.org/abs/2301.12093v3)** - [Code](https://github.com/wcyjerry/basicisos) (confidence: medium)
* **[A Multi-task Framework for Infrared Small Target Detection and Segmentation](https://arxiv.org/abs/2206.06923v1)** - [Code](https://github.com/chenastron/mtunet) (confidence: high)
* **[A Survey of Self-Supervised and Few-Shot Object Detection](https://arxiv.org/abs/2110.14711v3)** - [Code](https://github.com/gabrielhuang/awesome-few-shot-object-detection) (confidence: medium)
* **[Agnostic Lane Detection](https://arxiv.org/abs/1905.03704v1)** - [Code](https://github.com/cardwing/codes-for-lane-detection) (confidence: medium)
* **[Towards Pedestrian Detection Using RetinaNet in ECCV 2018 Wider Pedestrian Detection Challenge](https://arxiv.org/abs/1902.01031v1)** - [Code](https://github.com/miltonbd/eccv_2018_pedestrian_detection_challenege) (confidence: medium)
<!-- END SEGMENTATION_PAPERS -->

## 🔧 Reconstruction

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN RECONSTRUCTION_PAPERS -->
* **[Rethinking IRSTD: Single-Point Supervision Guided Encoder-only Framework is Enough for Infrared Small Target Detection](https://arxiv.org/abs/2604.05363v1)** - [Code](https://github.com/nirixiang/spire-irstd) (confidence: medium)
* **[DISTA-Net: Dynamic Closely-Spaced Infrared Small Target Unmixing](https://arxiv.org/abs/2505.19148v2)** - [Code](https://github.com/grokcv/grokcso) (confidence: medium)
* **[ARFC-WAHNet: Adaptive Receptive Field Convolution and Wavelet-Attentive Hierarchical Network for Infrared Small Target Detection](https://arxiv.org/abs/2505.10595v2)** - [Code](https://github.com/leaf2001/arfc-wahnet) (confidence: medium)
* **[DPDETR: Decoupled Position Detection Transformer for Infrared-Visible Object Detection](https://arxiv.org/abs/2408.06123v2)** - [Code](https://github.com/gjj45/dpdetr) (confidence: medium)
* **[Local Motion and Contrast Priors Driven Deep Network for Infrared Small Target Super-Resolution](https://arxiv.org/abs/2201.01014v5)** - [Code](https://github.com/xinyiying/mocopnet) (confidence: high)
<!-- END RECONSTRUCTION_PAPERS -->

## 🏷️ Classification

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN CLASSIFICATION_PAPERS -->
* **[Rethinking IRSTD: Single-Point Supervision Guided Encoder-only Framework is Enough for Infrared Small Target Detection](https://arxiv.org/abs/2604.05363v1)** - [Code](https://github.com/nirixiang/spire-irstd) (confidence: high)
* **[Rethinking Representations for Cross-Domain Infrared Small Target Detection: A Generalizable Perspective from the Frequency Domain](https://arxiv.org/abs/2604.01934v1)** - [Code](https://github.com/fuyimin96/s2cpnet) (confidence: high)
* **[FSGNet: A Frequency-Aware and Semantic Guidance Network for Infrared Small Target Detection](https://arxiv.org/abs/2603.25389v1)** - [Code](https://github.com/wangtao-bao/fsgnet) (confidence: high)
* **[Point-to-Mask: From Arbitrary Point Annotations to Mask-Level Infrared Small Target Detection](https://arxiv.org/abs/2603.16257v1)** - [Code](https://github.com/gaoscience/point-to-mask) (confidence: high)
* **[MI-DETR: A Strong Baseline for Moving Infrared Small Target Detection with Bio-Inspired Motion Integration](https://arxiv.org/abs/2603.05071v1)** - [Code](https://github.com/nliu-25/mi-detr) (confidence: high)
* **[No Memorization, No Detection: Output Distribution-Based Contamination Detection in Small Language Models](https://arxiv.org/abs/2603.03203v3)** - [Code](https://github.com/sela-omer/contamination-detection-small-lm) (confidence: high)
* **[Dynamic High-frequency Convolution for Infrared Small Target Detection](https://arxiv.org/abs/2602.02969v1)** - [Code](https://github.com/tinalrj/dhif) (confidence: high)
* **[DCCS-Det: Directional Context and Cross-Scale-Aware Detector for Infrared Small Target](https://arxiv.org/abs/2601.16428v1)** - [Code](https://huggingface.co/inpeerreview/infraredsmalltargetdetection-irstd.dccs) (confidence: medium)
* **[FeedbackSTS-Det: Sparse Frames-Based Spatio-Temporal Semantic Feedback Network for Moving Infrared Small Target Detection](https://arxiv.org/abs/2601.14690v2)** - [Code](https://github.com/idip-lab/feedbacksts-det) (confidence: high)
* **[Gradient-Guided Learning Network for Infrared Small Target Detection](https://arxiv.org/abs/2512.09497v1)** - [Code](https://github.com/yuchuang1205/msda-net) (confidence: high)
* **[Traffic Scene Small Target Detection Method Based on YOLOv8n-SPTS Model for Autonomous Driving](https://arxiv.org/abs/2512.09296v1)** - [Code](https://github.com/songhanwu/yolov8n-spts) (confidence: high)
* **[Rethinking Infrared Small Target Detection: A Foundation-Driven Efficient Paradigm](https://arxiv.org/abs/2512.05511v1)** - [Code](https://github.com/yuchuang1205/fdep-framework) (confidence: high)
* **[Difference Decomposition Networks for Infrared Small Target Detection](https://arxiv.org/abs/2512.03470v4)** - [Code](https://github.com/greekinroma/irstd_hc_platform) (confidence: high)
* **[Ivan-ISTD: Rethinking Cross-domain Heteroscedastic Noise Perturbations in Infrared Small Target Detection](https://arxiv.org/abs/2510.12241v1)** - [Code](https://github.com/nanjin1/ivan-istd) (confidence: high)
* **[TY-RIST: Tactical YOLO Tricks for Real-time Infrared Small Target Detection](https://arxiv.org/abs/2509.22909v1)** - [Code](https://github.com/moured/ty-rist) (confidence: high)
* **[Rethinking Evaluation of Infrared Small Target Detection](https://arxiv.org/abs/2509.16888v2)** - [Code](https://github.com/lartpang/pyirstdmetrics) (confidence: high)
* **[Lightweight Deep Unfolding Networks with Enhanced Robustness for Infrared Small Target Detection](https://arxiv.org/abs/2509.08205v1)** - [Code](https://github.com/xianchaoxiu/l-rpcanet) (confidence: high)
* **[HyperTea: A Hypergraph-based Temporal Enhancement and Alignment Network for Moving Infrared Small Target Detection](https://arxiv.org/abs/2508.10678v1)** - [Code](https://github.com/lurenjia-lrj/hypertea) (confidence: high)
* **[SeqCSIST: Sequential Closely-Spaced Infrared Small Target Unmixing](https://arxiv.org/abs/2507.09556v1)** - [Code](https://github.com/grokcv/seqcsist) (confidence: medium)
* **[DRPCA-Net: Make Robust PCA Great Again for Infrared Small Target Detection](https://arxiv.org/abs/2507.09541v1)** - [Code](https://github.com/grokcv/drpca-net) (confidence: high)
* **[SDS-Net: Shallow-Deep Synergism-detection Network for infrared small target detection](https://arxiv.org/abs/2506.06042v1)** - [Code](https://github.com/physilearn/sds-net) (confidence: high)
* **[SAMamba: Adaptive State Space Modeling with Hierarchical Vision for Infrared Small Target Detection](https://arxiv.org/abs/2505.23214v1)** - [Code](https://github.com/zhengshuchen/samamba) (confidence: high)
* **[DISTA-Net: Dynamic Closely-Spaced Infrared Small Target Unmixing](https://arxiv.org/abs/2505.19148v2)** - [Code](https://github.com/grokcv/grokcso) (confidence: medium)
* **[AuxDet: Auxiliary Metadata Matters for Omni-Domain Infrared Small Target Detection](https://arxiv.org/abs/2505.15184v2)** - [Code](https://github.com/grokcv/auxdet) (confidence: high)
* **[ARFC-WAHNet: Adaptive Receptive Field Convolution and Wavelet-Attentive Hierarchical Network for Infrared Small Target Detection](https://arxiv.org/abs/2505.10595v2)** - [Code](https://github.com/leaf2001/arfc-wahnet) (confidence: high)
* **[CSPENet: Contour-Aware and Saliency Priors Embedding Network for Infrared Small Target Detection](https://arxiv.org/abs/2505.09943v1)** - [Code](https://github.com/idip2025/cspenet) (confidence: high)
* **[Case Study: Fine-tuning Small Language Models for Accurate and Private CWE Detection in Python Code](https://arxiv.org/abs/2504.16584v1)** - [Code](https://huggingface.co/datasets/floxihunter) (confidence: high) | [Code2](https://huggingface.co/floxihunter/codegen-mono-cwedetect)
* **[Rethinking Generalizable Infrared Small Target Detection: A Real-scene Benchmark and Cross-view Representation Learning](https://arxiv.org/abs/2504.16487v1)** - [Code](https://github.com/luy0222/realscene-istd) (confidence: high)
* **[Vision-Language Model for Object Detection and Segmentation: A Review and Evaluation](https://arxiv.org/abs/2504.09480v1)** - [Code](https://github.com/better-chao/perceptual_abilities_evaluation) (confidence: high)
* **[Detection-Friendly Nonuniformity Correction: A Union Framework for Infrared UAVTarget Detection](https://arxiv.org/abs/2504.04012v1)** - [Code](https://github.com/ivplaboratory/unicd) (confidence: high)
* **[Low-Level Matters: An Efficient Hybrid Architecture for Robust Multi-frame Infrared Small Target Detection](https://arxiv.org/abs/2503.02220v1)** - [Code](https://github.com/zhihuashen/lvnet) (confidence: high)
* **[SoccerSynth-Detection: A Synthetic Dataset for Soccer Player Detection](https://arxiv.org/abs/2501.09281v2)** - [Code](https://github.com/open-starlab/soccersynth-detection) (confidence: high)
* **[EDNet: Edge-Optimized Small Target Detection in UAV Imagery -- Faster Context Attention, Better Feature Fusion, and Hardware Acceleration](https://arxiv.org/abs/2501.05885v1)** - [Code](https://github.com/zsniko/ednet) (confidence: high)
* **[Pinwheel-shaped Convolution and Scale-based Dynamic Loss for Infrared Small Target Detection](https://arxiv.org/abs/2412.16986v1)** - [Code](https://github.com/jn-yang/pconv-sdloss-data) (confidence: high)
* **[From Easy to Hard: Progressive Active Learning Framework for Infrared Small Target Detection with Single Point Supervision](https://arxiv.org/abs/2412.11154v3)** - [Code](https://github.com/yuchuang1205/pal) (confidence: high)
* **[MaDiNet: Mamba Diffusion Network for SAR Target Detection](https://arxiv.org/abs/2411.07500v1)** - [Code](https://github.com/joyezlearning/madinet) (confidence: high)
* **[Correlation of Object Detection Performance with Visual Saliency and Depth Estimation](https://arxiv.org/abs/2411.02844v1)** - [Code](https://github.com/mbar0075/object-detection-correlation-saliency-vs-depth) (confidence: high)
* **[DATransNet: Dynamic Attention Transformer Network for Infrared Small Target Detection](https://arxiv.org/abs/2409.19599v5)** - [Code](https://github.com/greekinroma/datransnet) (confidence: high)
* **[Infrared Small Target Detection in Satellite Videos: A New Dataset and A Novel Recurrent Feature Refinement Framework](https://arxiv.org/abs/2409.12448v3)** - [Code](https://github.com/xinyiying/rfr) (confidence: high)
* **[Unleashing the Power of Generic Segmentation Models: A Simple Baseline for Infrared Small Target Detection](https://arxiv.org/abs/2409.04714v1)** - [Code](https://github.com/o937-blip/simir) (confidence: high)
* **[Beyond Full Labels: Energy-Double-Guided Single-Point Prompt for Infrared Small Target Label Generation](https://arxiv.org/abs/2408.08191v5)** - [Code](https://github.com/xdfai/edgsp) (confidence: medium)
* **[DPDETR: Decoupled Position Detection Transformer for Infrared-Visible Object Detection](https://arxiv.org/abs/2408.06123v2)** - [Code](https://github.com/gjj45/dpdetr) (confidence: high)
* **[Pick of the Bunch: Detecting Infrared Small Targets Beyond Hit-Miss Trade-Offs via Selective Rank-Aware Attention](https://arxiv.org/abs/2408.03717v2)** - [Code](https://github.com/grokcv/serankdet) (confidence: medium)
* **[Towards Robust Infrared Small Target Detection: A Feature-Enhanced and Sensitivity-Tunable Framework](https://arxiv.org/abs/2407.20090v3)** - [Code](https://github.com/yuchuang1205/fest-framework) (confidence: high)
* **[Background Semantics Matter: Cross-Task Feature Exchange Network for Clustered Infrared Small Target Detection](https://arxiv.org/abs/2407.20078v3)** - [Code](https://github.com/grokcv/bafe-net) (confidence: high)
* **[SMPISD-MTPNet: Scene Semantic Prior-Assisted Infrared Ship Detection Using Multi-Task Perception Networks](https://arxiv.org/abs/2407.18487v1)** - [Code](https://github.com/greekinroma/kmndnet) (confidence: high)
* **[Sparse Prior Is Not All You Need: When Differential Directionality Meets Saliency Coherence for Infrared Small Target Detection](https://arxiv.org/abs/2407.15369v1)** - [Code](https://github.com/grokcv/sdd) (confidence: high)
* **[Lost in UNet: Improving Infrared Small Target Detection by Underappreciated Local Features](https://arxiv.org/abs/2406.13445v1)** - [Code](https://github.com/wuzhou-quan/hintu) (confidence: high)
* **[MWIRSTD: A MWIR Small Target Detection Dataset](https://arxiv.org/abs/2406.08063v1)** - [Code](https://github.com/avinres/mwirstd) (confidence: high)
* **[Triple-domain Feature Learning with Frequency-aware Memory Enhancement for Moving Infrared Small Target Detection](https://arxiv.org/abs/2406.06949v2)** - [Code](https://github.com/uestc-nnlab/tridos) (confidence: high)
* **[Multi-Scale Direction-Aware Network for Infrared Small Target Detection](https://arxiv.org/abs/2406.02037v4)** - [Code](https://github.com/yuchuang1205/msda-net) (confidence: high)
* **[Diff-Mosaic: Augmenting Realistic Representations in Infrared Small Target Detection via Diffusion Prior](https://arxiv.org/abs/2406.00632v1)** - [Code](https://github.com/yupeilin2388/diff-mosaic) (confidence: high)
* **[Infrared Small Target Detection with Scale and Location Sensitivity](https://arxiv.org/abs/2403.19366v1)** - [Code](https://github.com/ying-fu/mshnet) (confidence: high)
* **[HCF-Net: Hierarchical Context Fusion Network for Infrared Small Object Detection](https://arxiv.org/abs/2403.10778v1)** - [Code](https://github.com/zhengshuchen/hcfnet) (confidence: high)
* **[Mitigate Target-level Insensitivity of Infrared Small Target Detection via Posterior Distribution Modeling](https://arxiv.org/abs/2403.08380v1)** - [Code](https://github.com/li-haoqing/irstd-diff) (confidence: high)
* **[SIRST-5K: Exploring Massive Negatives Synthesis with Self-supervised Learning for Robust Infrared Small Target Detection](https://arxiv.org/abs/2403.05416v1)** - [Code](https://github.com/luy0222/sirst-5k) (confidence: high)
* **[Exploring Hyperspectral Anomaly Detection with Human Vision: A Small Target Aware Detector](https://arxiv.org/abs/2401.01093v1)** - [Code](https://github.com/majitao-xd/stad-had) (confidence: high)
* **[Improved Dense Nested Attention Network Based on Transformer for Infrared Small Target Detection](https://arxiv.org/abs/2311.08747v3)** - [Code](https://github.com/edwardbao1006/bit\_sirst) (confidence: high)
* **[Click on Mask: A Labor-efficient Annotation Framework with Level Set for Infrared Small Target Detection](https://arxiv.org/abs/2310.12562v1)** - [Code](https://github.com/li-haoqing/com) (confidence: high)
* **[ILNet: Low-level Matters for Salient Infrared Small Target Detection](https://arxiv.org/abs/2309.13646v1)** - [Code](https://github.com/li-haoqing/ilnet) (confidence: high)
* **[Enhancing Infrared Small Target Detection Robustness with Bi-Level Adversarial Framework](https://arxiv.org/abs/2309.01099v1)** - [Code](https://github.com/liuzhu-cv/balistd) (confidence: high)
* **[Unsupervised Adversarial Detection without Extra Model: Training Loss Should Change](https://arxiv.org/abs/2308.03243v1)** - [Code](https://github.com/cyclebooster/unsupervised-adversarial-detection-without-extra-model) (confidence: high)
* **[EFLNet: Enhancing Feature Learning for Infrared Small Target Detection](https://arxiv.org/abs/2307.14723v2)** - [Code](https://github.com/yangbo0411/infrared-small-target) (confidence: high)
* **[Object-aware Gaze Target Detection](https://arxiv.org/abs/2307.09662v2)** - [Code](https://github.com/francescotonini/object-aware-gaze-target-detection) (confidence: high)
* **[Monte Carlo Linear Clustering with Single-Point Supervision is Enough for Infrared Small Target Detection](https://arxiv.org/abs/2304.04442v1)** - [Code](https://github.com/yeren123455/sirst-single-point-supervision) (confidence: high)
* **[Mapping Degeneration Meets Label Evolution: Learning Infrared Small Target Detection with Single Point Supervision](https://arxiv.org/abs/2304.01484v3)** - [Code](https://github.com/xinyiying/lesps) (confidence: high)
* **[ABC: Attention with Bilinear Correlation for Infrared Small Target Detection](https://arxiv.org/abs/2303.10321v1)** - [Code](https://github.com/panpeiwen/abc) (confidence: high)
* **[Underwater target detection based on improved YOLOv7](https://arxiv.org/abs/2302.06939v1)** - [Code](https://github.com/nzwang/yolov7-ac) (confidence: high)
* **[Local Contrast and Global Contextual Information Make Infrared Small Object Salient Again](https://arxiv.org/abs/2301.12093v3)** - [Code](https://github.com/wcyjerry/basicisos) (confidence: medium)
* **[One-Stage Cascade Refinement Networks for Infrared Small Target Detection](https://arxiv.org/abs/2212.08472v2)** - [Code](https://github.com/yimiandai/open-deepinfrared) (confidence: high)
* **[Mul-GAD: a semi-supervised graph anomaly detection framework via aggregating multi-view information](https://arxiv.org/abs/2212.05478v1)** - [Code](https://github.com/liuyishoua/mul-graph-fusion) (confidence: high)
* **[UIU-Net: U-Net in U-Net for Infrared Small Object Detection](https://arxiv.org/abs/2212.00968v1)** - [Code](https://github.com/danfenghong/ieee_tip_uiu-net) (confidence: high)
* **[Table Detection in the Wild: A Novel Diverse Table Detection Dataset and Method](https://arxiv.org/abs/2209.09207v2)** - [Code](https://huggingface.co/datasets/n3011) (confidence: high)
* **[A Multi-task Framework for Infrared Small Target Detection and Segmentation](https://arxiv.org/abs/2206.06923v1)** - [Code](https://github.com/chenastron/mtunet) (confidence: high)
* **[Multitask AET with Orthogonal Tangent Regularity for Dark Object Detection](https://arxiv.org/abs/2205.03346v1)** - [Code](https://github.com/cuiziteng/maet) (confidence: high)
* **[Trustworthy Anomaly Detection: A Survey](https://arxiv.org/abs/2202.07787v1)** - [Code](https://github.com/yuan-shuhan/trustworthy-anomaly-detection-papers) (confidence: high)
* **[Real-Time Seizure Detection using EEG: A Comprehensive Comparison of Recent Approaches under a Realistic Setting](https://arxiv.org/abs/2201.08780v2)** - [Code](https://github.com/aitrics/eeg_real_time_seizure_detection) (confidence: high)
* **[Local Motion and Contrast Priors Driven Deep Network for Infrared Small Target Super-Resolution](https://arxiv.org/abs/2201.01014v5)** - [Code](https://github.com/xinyiying/mocopnet) (confidence: medium)
* **[BEVDet: High-performance Multi-camera 3D Object Detection in Bird-Eye-View](https://arxiv.org/abs/2112.11790v3)** - [Code](https://github.com/huangjunjie2017/bevdet) (confidence: high)
* **[AGPCNet: Attention-Guided Pyramid Context Networks for Infrared Small Target Detection](https://arxiv.org/abs/2111.03580v1)** - [Code](https://github.com/tianfang-zhang/agpcnet) (confidence: high)
* **[A Survey of Self-Supervised and Few-Shot Object Detection](https://arxiv.org/abs/2110.14711v3)** - [Code](https://github.com/gabrielhuang/awesome-few-shot-object-detection) (confidence: high)
* **[Non-Convex Tensor Low-Rank Approximation for Infrared Small Target Detection](https://arxiv.org/abs/2105.14974v2)** - [Code](https://github.com/liuting20a/asttv-ntla) (confidence: high)
* **[TJU-DHD: A Diverse High-Resolution Dataset for Object Detection](https://arxiv.org/abs/2011.09170v1)** - [Code](https://github.com/tjubiit/tju-dhd) (confidence: high)
* **[RGBT Salient Object Detection: A Large-scale Dataset and Benchmark](https://arxiv.org/abs/2007.03262v6)** - [Code](https://github.com/lz118/rgbt-salient-object-detection) (confidence: high)
* **[Large Scale Open-Set Deep Logo Detection](https://arxiv.org/abs/1911.07440v4)** - [Code](https://github.com/mubastan/osld) (confidence: high)
* **[Agnostic Lane Detection](https://arxiv.org/abs/1905.03704v1)** - [Code](https://github.com/cardwing/codes-for-lane-detection) (confidence: high)
* **[Towards Pedestrian Detection Using RetinaNet in ECCV 2018 Wider Pedestrian Detection Challenge](https://arxiv.org/abs/1902.01031v1)** - [Code](https://github.com/miltonbd/eccv_2018_pedestrian_detection_challenege) (confidence: high)
<!-- END CLASSIFICATION_PAPERS -->

## 🔄 Image Registration

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN IMAGE_REGISTRATION_PAPERS -->
* **[MI-DETR: A Strong Baseline for Moving Infrared Small Target Detection with Bio-Inspired Motion Integration](https://arxiv.org/abs/2603.05071v1)** - [Code](https://github.com/nliu-25/mi-detr) (confidence: medium)
* **[Rethinking Infrared Small Target Detection: A Foundation-Driven Efficient Paradigm](https://arxiv.org/abs/2512.05511v1)** - [Code](https://github.com/yuchuang1205/fdep-framework) (confidence: medium)
* **[Ivan-ISTD: Rethinking Cross-domain Heteroscedastic Noise Perturbations in Infrared Small Target Detection](https://arxiv.org/abs/2510.12241v1)** - [Code](https://github.com/nanjin1/ivan-istd) (confidence: medium)
* **[HyperTea: A Hypergraph-based Temporal Enhancement and Alignment Network for Moving Infrared Small Target Detection](https://arxiv.org/abs/2508.10678v1)** - [Code](https://github.com/lurenjia-lrj/hypertea) (confidence: high)
* **[SeqCSIST: Sequential Closely-Spaced Infrared Small Target Unmixing](https://arxiv.org/abs/2507.09556v1)** - [Code](https://github.com/grokcv/seqcsist) (confidence: high)
* **[Rethinking Generalizable Infrared Small Target Detection: A Real-scene Benchmark and Cross-view Representation Learning](https://arxiv.org/abs/2504.16487v1)** - [Code](https://github.com/luy0222/realscene-istd) (confidence: medium)
* **[Infrared Small Target Detection in Satellite Videos: A New Dataset and A Novel Recurrent Feature Refinement Framework](https://arxiv.org/abs/2409.12448v3)** - [Code](https://github.com/xinyiying/rfr) (confidence: high)
* **[Local Motion and Contrast Priors Driven Deep Network for Infrared Small Target Super-Resolution](https://arxiv.org/abs/2201.01014v5)** - [Code](https://github.com/xinyiying/mocopnet) (confidence: medium)
<!-- END IMAGE_REGISTRATION_PAPERS -->

## 🔀 Domain Adaptation

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN DOMAIN_ADAPTATION_PAPERS -->
* **[Rethinking Representations for Cross-Domain Infrared Small Target Detection: A Generalizable Perspective from the Frequency Domain](https://arxiv.org/abs/2604.01934v1)** - [Code](https://github.com/fuyimin96/s2cpnet) (confidence: high)
* **[Ivan-ISTD: Rethinking Cross-domain Heteroscedastic Noise Perturbations in Infrared Small Target Detection](https://arxiv.org/abs/2510.12241v1)** - [Code](https://github.com/nanjin1/ivan-istd) (confidence: high)
* **[SAMamba: Adaptive State Space Modeling with Hierarchical Vision for Infrared Small Target Detection](https://arxiv.org/abs/2505.23214v1)** - [Code](https://github.com/zhengshuchen/samamba) (confidence: medium)
* **[Rethinking Generalizable Infrared Small Target Detection: A Real-scene Benchmark and Cross-view Representation Learning](https://arxiv.org/abs/2504.16487v1)** - [Code](https://github.com/luy0222/realscene-istd) (confidence: high)
* **[Vision-Language Model for Object Detection and Segmentation: A Review and Evaluation](https://arxiv.org/abs/2504.09480v1)** - [Code](https://github.com/better-chao/perceptual_abilities_evaluation) (confidence: medium)
* **[Triple-domain Feature Learning with Frequency-aware Memory Enhancement for Moving Infrared Small Target Detection](https://arxiv.org/abs/2406.06949v2)** - [Code](https://github.com/uestc-nnlab/tridos) (confidence: medium)
<!-- END DOMAIN_ADAPTATION_PAPERS -->

## 🎨 Generative Models

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN GENERATIVE_MODELS_PAPERS -->
* **[Point-to-Mask: From Arbitrary Point Annotations to Mask-Level Infrared Small Target Detection](https://arxiv.org/abs/2603.16257v1)** - [Code](https://github.com/gaoscience/point-to-mask) (confidence: medium)
* **[Dynamic High-frequency Convolution for Infrared Small Target Detection](https://arxiv.org/abs/2602.02969v1)** - [Code](https://github.com/tinalrj/dhif) (confidence: medium)
* **[Ivan-ISTD: Rethinking Cross-domain Heteroscedastic Noise Perturbations in Infrared Small Target Detection](https://arxiv.org/abs/2510.12241v1)** - [Code](https://github.com/nanjin1/ivan-istd) (confidence: medium)
* **[Case Study: Fine-tuning Small Language Models for Accurate and Private CWE Detection in Python Code](https://arxiv.org/abs/2504.16584v1)** - [Code](https://huggingface.co/datasets/floxihunter) (confidence: medium) | [Code2](https://huggingface.co/floxihunter/codegen-mono-cwedetect)
* **[MaDiNet: Mamba Diffusion Network for SAR Target Detection](https://arxiv.org/abs/2411.07500v1)** - [Code](https://github.com/joyezlearning/madinet) (confidence: high)
* **[Neural Real-Time Recalibration for Infrared Multi-Camera Systems](https://arxiv.org/abs/2410.14505v1)** - [Code](https://github.com/theictlab/neural-recalibration) (confidence: medium)
* **[Infrared Small Target Detection in Satellite Videos: A New Dataset and A Novel Recurrent Feature Refinement Framework](https://arxiv.org/abs/2409.12448v3)** - [Code](https://github.com/xinyiying/rfr) (confidence: medium)
* **[Beyond Full Labels: Energy-Double-Guided Single-Point Prompt for Infrared Small Target Label Generation](https://arxiv.org/abs/2408.08191v5)** - [Code](https://github.com/xdfai/edgsp) (confidence: high)
* **[Diff-Mosaic: Augmenting Realistic Representations in Infrared Small Target Detection via Diffusion Prior](https://arxiv.org/abs/2406.00632v1)** - [Code](https://github.com/yupeilin2388/diff-mosaic) (confidence: high)
* **[Mitigate Target-level Insensitivity of Infrared Small Target Detection via Posterior Distribution Modeling](https://arxiv.org/abs/2403.08380v1)** - [Code](https://github.com/li-haoqing/irstd-diff) (confidence: high)
* **[SIRST-5K: Exploring Massive Negatives Synthesis with Self-supervised Learning for Robust Infrared Small Target Detection](https://arxiv.org/abs/2403.05416v1)** - [Code](https://github.com/luy0222/sirst-5k) (confidence: high)
* **[Enhancing Infrared Small Target Detection Robustness with Bi-Level Adversarial Framework](https://arxiv.org/abs/2309.01099v1)** - [Code](https://github.com/liuzhu-cv/balistd) (confidence: medium)
<!-- END GENERATIVE_MODELS_PAPERS -->

## 📚 General

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN GENERAL_PAPERS -->
* **[What is the Role of Small Models in the LLM Era: A Survey](https://arxiv.org/abs/2409.06857v7)** - [Code](https://github.com/tigerchen52/role_of_small_models) (confidence: medium)
* **[SimpleFusion: A Simple Fusion Framework for Infrared and Visible Images](https://arxiv.org/abs/2406.19055v1)** - [Code](https://github.com/hxwxss/simplefusion-a-simple-fusion-framework-for-infrared-and-visible-images) (confidence: medium)
* **[Poisson multi-Bernoulli mixture filter with general target-generated measurements and arbitrary clutter](https://arxiv.org/abs/2210.12983v2)** - [Code](https://github.com/agarciafernandez/mtt) (confidence: medium) | [Code2](https://github.com/yuhsuansia/extented-target-pmbm-filter-independent-clutter-sources)
* **[A Poisson multi-Bernoulli mixture filter for coexisting point and extended targets](https://arxiv.org/abs/2011.04464v2)** - [Code](https://github.com/agarciafernandez/coexisting-point-extended-target-pmbm-filter) (confidence: medium) | [Code2](https://github.com/yuhsuansia/coexisting-point-extended-target-pmbm-filter)
* **[Extended target Poisson multi-Bernoulli mixture trackers based on sets of trajectories](https://arxiv.org/abs/1911.09025v1)** - [Code](https://github.com/yuhsuansia/extended-target-pmbm-tracker) (confidence: medium)
* **[Target-Guided Open-Domain Conversation](https://arxiv.org/abs/1905.11553v2)** - [Code](https://github.com/squareroot3/target-guided-conversation) (confidence: medium)
<!-- END GENERAL_PAPERS -->

---

**Repository Topics**: awesome, awesome-list, miccai, miccai2026, medical-imaging, deep-learning, computer-vision, segmentation, reconstruction, classification, medical-image-analysis, artificial-intelligence

**Conference Scope**: neurips-2025
**Discovery Mode**: strict

**Last Updated**: 2026-05-08 11:20 UTC by GitHub Actions

**License**: Apache License 2.0
