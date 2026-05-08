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

### Common Issues and Solutions

**Q: No papers found?**
- Check if the conference name is correct
- Try using `broad` mode instead of `strict`
- Verify the year format (e.g., use 2025, not '25)

**Q: Too few/large number of papers?**
- Adjust `--mode` from `strict` to `broad` or vice versa
- Modify conference scope to specific year

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
- Conference scope: `cvpr-2025`
- Discovery mode: `strict`
- Tracks: `all`
- Total code-backed papers: `98`
- Fetched arXiv records: `338`
- Unique arXiv records: `328`
- Filtered (non-target): `12`
- Filtered (track): `0`
- Filtered (no code links): `218`

| Category | Count | Gap to 1000 |
|---|---:|---:|
| Segmentation | 24 | 976 |
| Reconstruction | 12 | 988 |
| Classification | 26 | 974 |
| Image Registration | 15 | 985 |
| Domain Adaptation | 6 | 994 |
| Generative Models | 20 | 980 |
| General | 29 | 971 |
<!-- END COVERAGE_REPORT -->

## 📊 Segmentation

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN SEGMENTATION_PAPERS -->
* **[Blind Bitstream-corrupted Video Recovery via Metadata-guided Diffusion Model](https://arxiv.org/abs/2604.13906v1)** - [Code](https://github.com/shuyun-wang/m-gdm) (confidence: medium)
* **[Medal S: Spatio-Textual Prompt Model for Medical Segmentation](https://arxiv.org/abs/2511.13001v1)** - [Code](https://github.com/yinghemedical/medal-s) (confidence: high)
* **[MR6D: Benchmarking 6D Pose Estimation for Mobile Robots](https://arxiv.org/abs/2508.13775v1)** - [Code](https://huggingface.co/datasets/anas-gouda) (confidence: medium)
* **[SIS-Challenge: Event-based Spatio-temporal Instance Segmentation Challenge at the CVPR 2025 Event-based Vision Workshop](https://arxiv.org/abs/2508.12813v1)** - [Code](https://github.com/tub-rip/mousesis) (confidence: high)
* **[Rethinking Query-based Transformer for Continual Image Segmentation](https://arxiv.org/abs/2507.07831v1)** - [Code](https://github.com/soolab/simcis) (confidence: high)
* **[Revisiting Audio-Visual Segmentation with Vision-Centric Transformer](https://arxiv.org/abs/2506.23623v1)** - [Code](https://github.com/spyflying/vct_avs) (confidence: high) | [Code2](https://huggingface.co/nowherespyfly/vct_avs)
* **[Relation3D: Enhancing Relation Modeling for Point Cloud Instance Segmentation](https://arxiv.org/abs/2506.17891v1)** - [Code](https://github.com/howard-coder191/relation3d) (confidence: high)
* **[ScaleLSD: Scalable Deep Line Segment Detection Streamlined](https://arxiv.org/abs/2506.09369v1)** - [Code](https://github.com/ant-research/scalelsd) (confidence: high)
* **[FreeGave: 3D Physics Learning from Dynamic Videos by Gaussian Velocity](https://arxiv.org/abs/2506.07865v1)** - [Code](https://github.com/vlar-group/freegave) (confidence: medium)
* **[LogoSP: Local-global Grouping of Superpoints for Unsupervised Semantic Segmentation of 3D Point Clouds](https://arxiv.org/abs/2506.07857v1)** - [Code](https://github.com/vlar-group/logosp) (confidence: high)
* **[DeformCL: Learning Deformable Centerline Representation for Vessel Extraction in 3D Medical Image](https://arxiv.org/abs/2506.05820v1)** - [Code](https://github.com/barry664/deformcl) (confidence: high)
* **[OV-COAST: Cost Aggregation with Optimal Transport for Open-Vocabulary Semantic Segmentation](https://arxiv.org/abs/2506.03706v1)** - [Code](https://github.com/adityagandhamal/ov-coast) (confidence: high)
* **[Attacking Attention of Foundation Models Disrupts Downstream Tasks](https://arxiv.org/abs/2506.05394v3)** - [Code](https://github.com/hondamunigeprasannasilva/attack-attention) (confidence: medium)
* **[SAM-I2V: Upgrading SAM to Support Promptable Video Segmentation with Less than 0.2% Training Cost](https://arxiv.org/abs/2506.01304v1)** - [Code](https://github.com/showlab/sam-i2v) (confidence: high)
* **[Perceptual Inductive Bias Is What You Need Before Contrastive Learning](https://arxiv.org/abs/2506.01201v2)** - [Code](https://github.com/juz031/midvcl) (confidence: medium)
* **[Synthetic Generation and Latent Projection Denoising of Rim Lesions in Multiple Sclerosis](https://arxiv.org/abs/2505.23353v1)** - [Code](https://github.com/agr78/prlx-gan) (confidence: medium)
* **[Universal Domain Adaptation for Semantic Segmentation](https://arxiv.org/abs/2505.22458v2)** - [Code](https://github.com/ku-vgi/unimap) (confidence: high)
* **[Sketchy Bounding-box Supervision for 3D Instance Segmentation](https://arxiv.org/abs/2505.16399v1)** - [Code](https://github.com/dengq7/sketchy-3dis) (confidence: high)
* **[DiGIT: Multi-Dilated Gated Encoder and Central-Adjacent Region Integrated Decoder for Temporal Action Detection Transformer](https://arxiv.org/abs/2505.05711v1)** - [Code](https://github.com/dotori-hj/digit) (confidence: medium)
* **[Are Synthetic Corruptions A Reliable Proxy For Real-World Corruptions?](https://arxiv.org/abs/2505.04835v1)** - [Code](https://github.com/shashankskagnihotri/benchmarking_robustness) (confidence: medium)
* **[Bounding Box-Guided Diffusion for Synthesizing Industrial Images and Segmentation Map](https://arxiv.org/abs/2505.03623v2)** - [Code](https://github.com/covisionlab/diffusion_labeling) (confidence: high)
* **[Advancing Generalizable Tumor Segmentation with Anomaly-Aware Open-Vocabulary Attention Maps and Frozen Foundation Diffusion Models](https://arxiv.org/abs/2505.02753v1)** - [Code](https://github.com/yankai96/diffugts) (confidence: high)
* **[CAV-MAE Sync: Improving Contrastive Audio-Visual Mask Autoencoders via Fine-Grained Alignment](https://arxiv.org/abs/2505.01237v2)** - [Code](https://github.com/edsonroteia/cav-mae-sync) (confidence: medium)
* **[ReferDINO-Plus: 2nd Solution for 4th PVUW MeViS Challenge at CVPR 2025](https://arxiv.org/abs/2503.23509v2)** - [Code](https://github.com/isee-laboratory/referdino-plus) (confidence: high)
<!-- END SEGMENTATION_PAPERS -->

## 🔧 Reconstruction

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN RECONSTRUCTION_PAPERS -->
* **[Realizing Immersive Volumetric Video: A Multimodal Framework for 6-DoF VR Engagement](https://arxiv.org/abs/2604.09473v1)** - [Code](https://github.com/metaverse-ai-lab-thu/imvid) (confidence: medium)
* **[FIMA-Q: Post-Training Quantization for Vision Transformers by Fisher Information Matrix Approximation](https://arxiv.org/abs/2506.11543v1)** - [Code](https://github.com/shihewang/fima-q) (confidence: medium)
* **[Gradient Inversion Attacks on Parameter-Efficient Fine-Tuning](https://arxiv.org/abs/2506.04453v1)** - [Code](https://github.com/info-ucr/peftleak) (confidence: medium)
* **[Towards In-the-wild 3D Plane Reconstruction from a Single Image](https://arxiv.org/abs/2506.02493v1)** - [Code](https://github.com/jcliu0428/zeroplane) (confidence: high)
* **[Synthetic Generation and Latent Projection Denoising of Rim Lesions in Multiple Sclerosis](https://arxiv.org/abs/2505.23353v1)** - [Code](https://github.com/agr78/prlx-gan) (confidence: high)
* **[Proximal Algorithm Unrolling: Flexible and Efficient Reconstruction Networks for Single-Pixel Imaging](https://arxiv.org/abs/2505.23180v1)** - [Code](https://github.com/pwangcs/proxunroll) (confidence: high)
* **[GoLF-NRT: Integrating Global Context and Local Geometry for Few-Shot View Synthesis](https://arxiv.org/abs/2505.19813v1)** - [Code](https://github.com/klmav-cuc/golf-nrt) (confidence: medium)
* **[Depth-Guided Bundle Sampling for Efficient Generalizable Neural Radiance Field Reconstruction](https://arxiv.org/abs/2505.19793v1)** - [Code](https://github.com/klmav-cuc/gdb-nerf) (confidence: high)
* **[Degradation-Aware Feature Perturbation for All-in-One Image Restoration](https://arxiv.org/abs/2505.12630v1)** - [Code](https://github.com/txphome/dfpir) (confidence: high)
* **[EvEnhancer: Empowering Effectiveness, Efficiency and Generalizability for Continuous Space-Time Video Super-Resolution with Events](https://arxiv.org/abs/2505.04657v1)** - [Code](https://github.com/w-shuoyan/evenhancer) (confidence: high)
* **[CAV-MAE Sync: Improving Contrastive Audio-Visual Mask Autoencoders via Fine-Grained Alignment](https://arxiv.org/abs/2505.01237v2)** - [Code](https://github.com/edsonroteia/cav-mae-sync) (confidence: medium)
* **[NTIRE 2025 Challenge on Image Super-Resolution ($	imes$4): Methods and Results](https://arxiv.org/abs/2504.14582v2)** - [Code](https://github.com/zhengchen1999/ntire2025_imagesr_x4) (confidence: high)
<!-- END RECONSTRUCTION_PAPERS -->

## 🏷️ Classification

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN CLASSIFICATION_PAPERS -->
* **[Let Samples Speak: Mitigating Spurious Correlation by Exploiting the Clusterness of Samples](https://arxiv.org/abs/2512.22874v1)** - [Code](https://github.com/davelee-uestc/nsf_debiasing) (confidence: medium)
* **[OmniTrack++: Omnidirectional Multi-Object Tracking by Learning Large-FoV Trajectory Feedback](https://arxiv.org/abs/2511.00510v2)** - [Code](https://github.com/xifen523/omnitrack) (confidence: medium)
* **[Domain-Adaptive Pretraining Improves Primate Behavior Recognition](https://arxiv.org/abs/2509.12193v1)** - [Code](https://github.com/ecker-lab/dap-behavior) (confidence: high)
* **[CryptoFace: End-to-End Encrypted Face Recognition](https://arxiv.org/abs/2509.00332v1)** - [Code](https://github.com/human-analysis/cryptoface) (confidence: high)
* **[MedErr-CT: A Visual Question Answering Benchmark for Identifying and Correcting Errors in CT Reports](https://arxiv.org/abs/2506.19217v1)** - [Code](https://github.com/babbu3682/mederr-ct) (confidence: high)
* **[SmartHome-Bench: A Comprehensive Benchmark for Video Anomaly Detection in Smart Homes Using Multi-Modal Large Language Models](https://arxiv.org/abs/2506.12992v1)** - [Code](https://github.com/xinyi-0724/smarthome-bench-llm) (confidence: high)
* **[DejaVid: Encoder-Agnostic Learned Temporal Matching for Video Classification](https://arxiv.org/abs/2506.12585v1)** - [Code](https://github.com/darrylho/dejavid) (confidence: high)
* **[HalLoc: Token-level Localization of Hallucinations for Vision Language Models](https://arxiv.org/abs/2506.10286v1)** - [Code](https://github.com/dbsltm/cvpr25_halloc) (confidence: medium)
* **[ScaleLSD: Scalable Deep Line Segment Detection Streamlined](https://arxiv.org/abs/2506.09369v1)** - [Code](https://github.com/ant-research/scalelsd) (confidence: high)
* **[DeformCL: Learning Deformable Centerline Representation for Vessel Extraction in 3D Medical Image](https://arxiv.org/abs/2506.05820v1)** - [Code](https://github.com/barry664/deformcl) (confidence: high)
* **[Video, How Do Your Tokens Merge?](https://arxiv.org/abs/2506.03885v1)** - [Code](https://github.com/sjpollard/video-how-do-your-tokens-merge) (confidence: medium)
* **[Attacking Attention of Foundation Models Disrupts Downstream Tasks](https://arxiv.org/abs/2506.05394v3)** - [Code](https://github.com/hondamunigeprasannasilva/attack-attention) (confidence: medium)
* **[Technical Report for Ego4D Long-Term Action Anticipation Challenge 2025](https://arxiv.org/abs/2506.02550v2)** - [Code](https://github.com/corrineqiu/ego4d-lta-challenge-2025) (confidence: medium)
* **[Towards In-the-wild 3D Plane Reconstruction from a Single Image](https://arxiv.org/abs/2506.02493v1)** - [Code](https://github.com/jcliu0428/zeroplane) (confidence: high)
* **[Perceptual Inductive Bias Is What You Need Before Contrastive Learning](https://arxiv.org/abs/2506.01201v2)** - [Code](https://github.com/juz031/midvcl) (confidence: medium)
* **[PCIE_Interaction Solution for Ego4D Social Interaction Challenge](https://arxiv.org/abs/2505.24404v1)** - [Code](https://github.com/kanokphanl/pcie_ego4d_social_interaction) (confidence: medium)
* **[Boosting Domain Incremental Learning: Selecting the Optimal Parameters is All You Need](https://arxiv.org/abs/2505.23744v1)** - [Code](https://github.com/qwangcv/soyo) (confidence: high)
* **[Synthetic Generation and Latent Projection Denoising of Rim Lesions in Multiple Sclerosis](https://arxiv.org/abs/2505.23353v1)** - [Code](https://github.com/agr78/prlx-gan) (confidence: high)
* **[Point-to-Region Loss for Semi-Supervised Point-Based Crowd Counting](https://arxiv.org/abs/2505.21943v1)** - [Code](https://github.com/elin24/p2rloss) (confidence: medium)
* **[Roboflow100-VL: A Multi-Domain Object Detection Benchmark for Vision-Language Models](https://arxiv.org/abs/2505.20612v4)** - [Code](https://github.com/roboflow/rf100-vl) (confidence: high)
* **[PoseBH: Prototypical Multi-Dataset Training Beyond Human Pose Estimation](https://arxiv.org/abs/2505.17475v1)** - [Code](https://github.com/uyoung-jeong/posebh) (confidence: medium)
* **[Open Set Label Shift with Test Time Out-of-Distribution Reference](https://arxiv.org/abs/2505.05868v1)** - [Code](https://github.com/changkunye/opensetlabelshift) (confidence: medium)
* **[DiGIT: Multi-Dilated Gated Encoder and Central-Adjacent Region Integrated Decoder for Temporal Action Detection Transformer](https://arxiv.org/abs/2505.05711v1)** - [Code](https://github.com/dotori-hj/digit) (confidence: high)
* **[CAV-MAE Sync: Improving Contrastive Audio-Visual Mask Autoencoders via Fine-Grained Alignment](https://arxiv.org/abs/2505.01237v2)** - [Code](https://github.com/edsonroteia/cav-mae-sync) (confidence: medium)
* **[Classifier-to-Bias: Toward Unsupervised Automatic Bias Detection for Visual Classifiers](https://arxiv.org/abs/2504.20902v1)** - [Code](https://github.com/mardgui/c2b) (confidence: high)
* **[SSL4Eco: A Global Seasonal Dataset for Geospatial Foundation Models in Ecology](https://arxiv.org/abs/2504.18256v3)** - [Code](https://github.com/plekhanovaelena/ssl4eco) (confidence: medium)
<!-- END CLASSIFICATION_PAPERS -->

## 🔄 Image Registration

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN IMAGE_REGISTRATION_PAPERS -->
* **[Medal S: Spatio-Textual Prompt Model for Medical Segmentation](https://arxiv.org/abs/2511.13001v1)** - [Code](https://github.com/yinghemedical/medal-s) (confidence: medium)
* **[Rethinking Query-based Transformer for Continual Image Segmentation](https://arxiv.org/abs/2507.07831v1)** - [Code](https://github.com/soolab/simcis) (confidence: medium)
* **[Object-aware Sound Source Localization via Audio-Visual Scene Understanding](https://arxiv.org/abs/2506.18557v2)** - [Code](https://github.com/visualaikhu/oa-ssl) (confidence: medium)
* **[DejaVid: Encoder-Agnostic Learned Temporal Matching for Video Classification](https://arxiv.org/abs/2506.12585v1)** - [Code](https://github.com/darrylho/dejavid) (confidence: medium)
* **[DiscoVLA: Discrepancy Reduction in Vision, Language, and Alignment for Parameter-Efficient Video-Text Retrieval](https://arxiv.org/abs/2506.08887v1)** - [Code](https://github.com/lunarshen/dsicovla) (confidence: high)
* **[DeformCL: Learning Deformable Centerline Representation for Vessel Extraction in 3D Medical Image](https://arxiv.org/abs/2506.05820v1)** - [Code](https://github.com/barry664/deformcl) (confidence: high)
* **[OV-COAST: Cost Aggregation with Optimal Transport for Open-Vocabulary Semantic Segmentation](https://arxiv.org/abs/2506.03706v1)** - [Code](https://github.com/adityagandhamal/ov-coast) (confidence: medium)
* **[Self-Supervised Spatial Correspondence Across Modalities](https://arxiv.org/abs/2506.03148v1)** - [Code](https://github.com/ayshrv/cmrw) (confidence: medium)
* **[Diff2Flow: Training Flow Matching Models via Diffusion Model Alignment](https://arxiv.org/abs/2506.02221v1)** - [Code](https://github.com/compvis/diff2flow) (confidence: high)
* **[Period-LLM: Extending the Periodic Capability of Multimodal Large Language Model](https://arxiv.org/abs/2505.24476v1)** - [Code](https://github.com/keke-nice/period-llm) (confidence: medium)
* **[Roboflow100-VL: A Multi-Domain Object Detection Benchmark for Vision-Language Models](https://arxiv.org/abs/2505.20612v4)** - [Code](https://github.com/roboflow/rf100-vl) (confidence: medium)
* **[Towards Video to Piano Music Generation with Chain-of-Perform Support Benchmarks](https://arxiv.org/abs/2505.20038v1)** - [Code](https://github.com/acappemin/video-to-audio-and-piano) (confidence: medium)
* **[DiGIT: Multi-Dilated Gated Encoder and Central-Adjacent Region Integrated Decoder for Temporal Action Detection Transformer](https://arxiv.org/abs/2505.05711v1)** - [Code](https://github.com/dotori-hj/digit) (confidence: medium)
* **[Object-Shot Enhanced Grounding Network for Egocentric Video](https://arxiv.org/abs/2505.04270v1)** - [Code](https://github.com/yisen-feng/osgnet) (confidence: medium)
* **[CAV-MAE Sync: Improving Contrastive Audio-Visual Mask Autoencoders via Fine-Grained Alignment](https://arxiv.org/abs/2505.01237v2)** - [Code](https://github.com/edsonroteia/cav-mae-sync) (confidence: high)
<!-- END IMAGE_REGISTRATION_PAPERS -->

## 🔀 Domain Adaptation

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN DOMAIN_ADAPTATION_PAPERS -->
* **[Generalized Trajectory Scoring for End-to-end Multimodal Planning](https://arxiv.org/abs/2506.06664v1)** - [Code](https://github.com/nvlabs/gtrs) (confidence: high)
* **[OV-COAST: Cost Aggregation with Optimal Transport for Open-Vocabulary Semantic Segmentation](https://arxiv.org/abs/2506.03706v1)** - [Code](https://github.com/adityagandhamal/ov-coast) (confidence: high)
* **[Conformal Prediction for Zero-Shot Models](https://arxiv.org/abs/2505.24693v1)** - [Code](https://github.com/jusiro/clip-conformal) (confidence: medium)
* **[Universal Domain Adaptation for Semantic Segmentation](https://arxiv.org/abs/2505.22458v2)** - [Code](https://github.com/ku-vgi/unimap) (confidence: high)
* **[Point-to-Region Loss for Semi-Supervised Point-Based Crowd Counting](https://arxiv.org/abs/2505.21943v1)** - [Code](https://github.com/elin24/p2rloss) (confidence: medium)
* **[CoDEx: Combining Domain Expertise for Spatial Generalization in Satellite Image Analysis](https://arxiv.org/abs/2504.19737v1)** - [Code](https://github.com/abhishek19009/codex) (confidence: high)
<!-- END DOMAIN_ADAPTATION_PAPERS -->

## 🎨 Generative Models

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN GENERATIVE_MODELS_PAPERS -->
* **[Blind Bitstream-corrupted Video Recovery via Metadata-guided Diffusion Model](https://arxiv.org/abs/2604.13906v1)** - [Code](https://github.com/shuyun-wang/m-gdm) (confidence: high)
* **[InterAct: Advancing Large-Scale Versatile 3D Human-Object Interaction Generation](https://arxiv.org/abs/2509.09555v1)** - [Code](https://github.com/wzyabcas/interact) (confidence: high)
* **[A Training-Free, Task-Agnostic Framework for Enhancing MLLM Performance on High-Resolution Images](https://arxiv.org/abs/2507.10202v1)** - [Code](https://github.com/yenncye/ecp) (confidence: medium)
* **[Rethinking Query-based Transformer for Continual Image Segmentation](https://arxiv.org/abs/2507.07831v1)** - [Code](https://github.com/soolab/simcis) (confidence: medium)
* **[Revisiting Audio-Visual Segmentation with Vision-Centric Transformer](https://arxiv.org/abs/2506.23623v1)** - [Code](https://github.com/spyflying/vct_avs) (confidence: medium) | [Code2](https://huggingface.co/nowherespyfly/vct_avs)
* **[HalLoc: Token-level Localization of Hallucinations for Vision Language Models](https://arxiv.org/abs/2506.10286v1)** - [Code](https://github.com/dbsltm/cvpr25_halloc) (confidence: medium)
* **[Generalized Trajectory Scoring for End-to-end Multimodal Planning](https://arxiv.org/abs/2506.06664v1)** - [Code](https://github.com/nvlabs/gtrs) (confidence: medium)
* **[Diff2Flow: Training Flow Matching Models via Diffusion Model Alignment](https://arxiv.org/abs/2506.02221v1)** - [Code](https://github.com/compvis/diff2flow) (confidence: high)
* **[Silence is Golden: Leveraging Adversarial Examples to Nullify Audio Control in LDM-based Talking-Head Generation](https://arxiv.org/abs/2506.01591v1)** - [Code](https://github.com/yuangan/silencer) (confidence: high)
* **[Synthetic Generation and Latent Projection Denoising of Rim Lesions in Multiple Sclerosis](https://arxiv.org/abs/2505.23353v1)** - [Code](https://github.com/agr78/prlx-gan) (confidence: high)
* **[Wav2Sem: Plug-and-Play Audio Semantic Decoupling for 3D Speech-Driven Facial Animation](https://arxiv.org/abs/2505.23290v1)** - [Code](https://github.com/wslh852/wav2sem) (confidence: medium)
* **[ConText-CIR: Learning from Concepts in Text for Composed Image Retrieval](https://arxiv.org/abs/2505.20764v1)** - [Code](https://github.com/mvrl/context-cir) (confidence: medium)
* **[Towards Video to Piano Music Generation with Chain-of-Perform Support Benchmarks](https://arxiv.org/abs/2505.20038v1)** - [Code](https://github.com/acappemin/video-to-audio-and-piano) (confidence: high)
* **[GoLF-NRT: Integrating Global Context and Local Geometry for Few-Shot View Synthesis](https://arxiv.org/abs/2505.19813v1)** - [Code](https://github.com/klmav-cuc/golf-nrt) (confidence: high)
* **[Depth-Guided Bundle Sampling for Efficient Generalizable Neural Radiance Field Reconstruction](https://arxiv.org/abs/2505.19793v1)** - [Code](https://github.com/klmav-cuc/gdb-nerf) (confidence: medium)
* **[EvEnhancer: Empowering Effectiveness, Efficiency and Generalizability for Continuous Space-Time Video Super-Resolution with Events](https://arxiv.org/abs/2505.04657v1)** - [Code](https://github.com/w-shuoyan/evenhancer) (confidence: medium)
* **[MeshGen: Generating PBR Textured Mesh with Render-Enhanced Auto-Encoder and Generative Data Augmentation](https://arxiv.org/abs/2505.04656v1)** - [Code](https://github.com/heheyas/meshgen) (confidence: high)
* **[Bounding Box-Guided Diffusion for Synthesizing Industrial Images and Segmentation Map](https://arxiv.org/abs/2505.03623v2)** - [Code](https://github.com/covisionlab/diffusion_labeling) (confidence: high)
* **[Advancing Generalizable Tumor Segmentation with Anomaly-Aware Open-Vocabulary Attention Maps and Frozen Foundation Diffusion Models](https://arxiv.org/abs/2505.02753v1)** - [Code](https://github.com/yankai96/diffugts) (confidence: high)
* **[FreePCA: Integrating Consistency Information across Long-short Frames in Training-free Long Video Generation via Principal Component Analysis](https://arxiv.org/abs/2505.01172v1)** - [Code](https://github.com/josephtitan/freepca) (confidence: high)
<!-- END GENERATIVE_MODELS_PAPERS -->

## 📚 General

*This list is automatically generated. See any issues? Please open a pull request!*

<!-- BEGIN GENERAL_PAPERS -->
* **[Meta-Learning Hyperparameters for Parameter Efficient Fine-Tuning](https://arxiv.org/abs/2603.01759v1)** - [Code](https://github.com/doem97/metalora) (confidence: medium)
* **[Optimizing Multimodal LLMs for Egocentric Video Understanding: A Solution for the HD-EPIC VQA Challenge](https://arxiv.org/abs/2601.10228v1)** - [Code](https://github.com/youngseng/egocentric-co-pilot) (confidence: medium)
* **[NN-Former: Rethinking Graph Structure in Neural Architecture Representation](https://arxiv.org/abs/2507.00880v1)** - [Code](https://github.com/xuruihan/nnformer) (confidence: medium)
* **[Instant Particle Size Distribution Measurement Using CNNs Trained on Synthetic Data](https://arxiv.org/abs/2507.00822v1)** - [Code](https://github.com/yasserelj/synthetic-granular-gen) (confidence: medium)
* **[DIVE: Deep-search Iterative Video Exploration A Technical Report for the CVRR Challenge at CVPR 2025](https://arxiv.org/abs/2506.21891v1)** - [Code](https://github.com/panasonicconnect/dive) (confidence: medium)
* **[Improving Personalized Search with Regularized Low-Rank Parameter Updates](https://arxiv.org/abs/2506.10182v1)** - [Code](https://github.com/adobe-research/polar-vl) (confidence: medium)
* **[Hearing Hands: Generating Sounds from Physical Interactions in 3D Scenes](https://arxiv.org/abs/2506.09989v1)** - [Code](https://github.com/dou-yiming/hearing_hands) (confidence: medium)
* **[UniPre3D: Unified Pre-training of 3D Point Cloud Models with Cross-Modal Gaussian Splatting](https://arxiv.org/abs/2506.09952v1)** - [Code](https://github.com/wangzy22/unipre3d) (confidence: medium)
* **[Unleashing the Potential of Consistency Learning for Detecting and Grounding Multi-Modal Media Manipulation](https://arxiv.org/abs/2506.05890v1)** - [Code](https://github.com/liyih/cscl) (confidence: medium)
* **[GazeNLQ @ Ego4D Natural Language Queries Challenge 2025](https://arxiv.org/abs/2506.05782v1)** - [Code](https://github.com/stevenlin510/gazenlq) (confidence: medium)
* **[LotusFilter: Fast Diverse Nearest Neighbor Search via a Learned Cutoff Table](https://arxiv.org/abs/2506.04790v1)** - [Code](https://github.com/matsui528/lotf) (confidence: medium)
* **[OSGNet @ Ego4D Episodic Memory Challenge 2025](https://arxiv.org/abs/2506.03710v1)** - [Code](https://github.com/yisen-feng/osgnet) (confidence: medium)
* **[PARC: A Quantitative Framework Uncovering the Symmetries within Vision Language Models](https://arxiv.org/abs/2506.14808v1)** - [Code](https://github.com/nvlabs/parc) (confidence: medium)
* **[RC-AutoCalib: An End-to-End Radar-Camera Automatic Calibration Network](https://arxiv.org/abs/2505.22427v1)** - [Code](https://github.com/nycu-acm/rc-autocalib) (confidence: medium)
* **[FRAMES-VQA: Benchmarking Fine-Tuning Robustness across Multi-Modal Shifts in Visual Question Answering](https://arxiv.org/abs/2505.21755v2)** - [Code](https://github.com/chengyuehuang511/frames-vqa) (confidence: medium)
* **[PMA: Towards Parameter-Efficient Point Cloud Understanding via Point Mamba Adapter](https://arxiv.org/abs/2505.20941v1)** - [Code](https://github.com/zyh16143998882/pma) (confidence: medium)
* **[HCQA-1.5 @ Ego4D EgoSchema Challenge 2025](https://arxiv.org/abs/2505.20644v1)** - [Code](https://github.com/hyu-zhang/hcqa) (confidence: medium)
* **[Four Eyes Are Better Than Two: Harnessing the Collaborative Potential of Large Models via Differentiated Thinking and Complementary Ensembles](https://arxiv.org/abs/2505.16784v2)** - [Code](https://github.com/xiongjunguan/egoschema-cvpr25) (confidence: medium)
* **[DeCafNet: Delegate and Conquer for Efficient Temporal Grounding in Long Videos](https://arxiv.org/abs/2505.16376v1)** - [Code](https://github.com/zijialewislu/cvpr2025-decafnet) (confidence: medium)
* **[Neural Video Compression with Context Modulation](https://arxiv.org/abs/2505.14541v1)** - [Code](https://github.com/austin4ustc/dcmvc) (confidence: medium)
* **[Camera-Only 3D Panoptic Scene Completion for Autonomous Driving through Differentiable Object Shapes](https://arxiv.org/abs/2505.09562v1)** - [Code](https://github.com/nicolamarinello/offsetocc) (confidence: medium)
* **[Sparse Point Cloud Patches Rendering via Splitting 2D Gaussians](https://arxiv.org/abs/2505.09413v1)** - [Code](https://github.com/murcherful/gaupcrender) (confidence: medium)
* **[Behind Maya: Building a Multilingual Vision Language Model](https://arxiv.org/abs/2505.08910v2)** - [Code](https://github.com/nahidalam/maya) (confidence: medium)
* **[EmoVLM-KD: Fusing Distilled Expertise with Vision-Language Models for Visual Emotion Analysis](https://arxiv.org/abs/2505.07164v1)** - [Code](https://github.com/sange1104/emovlm-kd) (confidence: medium)
* **[DispBench: Benchmarking Disparity Estimation to Synthetic Corruptions](https://arxiv.org/abs/2505.05091v1)** - [Code](https://github.com/shashankskagnihotri/benchmarking_robustness) (confidence: medium)
* **[Convex Relaxation for Robust Vanishing Point Estimation in Manhattan World](https://arxiv.org/abs/2505.04788v3)** - [Code](https://github.com/wu-cvgl/globustvp) (confidence: medium)
* **[Towards Efficient Benchmarking of Foundation Models in Remote Sensing: A Capabilities Encoding Approach](https://arxiv.org/abs/2505.03299v1)** - [Code](https://github.com/pierreadorni/capabilities-encoding) (confidence: medium)
* **[SeriesBench: A Benchmark for Narrative-Driven Drama Series Understanding](https://arxiv.org/abs/2504.21435v3)** - [Code](https://github.com/zackhxn/seriesbench-cvpr2025) (confidence: medium)
* **[MP-SfM: Monocular Surface Priors for Robust Structure-from-Motion](https://arxiv.org/abs/2504.20040v1)** - [Code](https://github.com/cvg/mpsfm) (confidence: medium)
<!-- END GENERAL_PAPERS -->

---

**Repository Topics**: awesome, awesome-list, miccai, miccai2026, medical-imaging, deep-learning, computer-vision, segmentation, reconstruction, classification, medical-image-analysis, artificial-intelligence

**Conference Scope**: cvpr-2025
**Discovery Mode**: strict

**Last Updated**: 2026-05-08 10:14 UTC by GitHub Actions

**License**: Apache License 2.0
