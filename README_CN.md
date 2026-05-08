# AI 会议论文精选

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> 一个通用的会议论文爬取和整理工具，自动从 arXiv 发现附有开源代码的会议论文。

**本项目自动从 arXiv 发现并整理附有开源代码链接的会议论文。** 每日运行的爬虫程序搜索 arXiv 元数据、验证链接格式、按类别和置信度分组，并确定性地生成论文列表。

## 会议范围配置

本项目是**通用型**工具，可以配置为追踪任何在 arXiv 有论文提交的会议（如 MICCAI、CVPR、NeurIPS、ICCV、ICLR、MIDL 等）。

### 🎯 什么是会议范围？

会议范围定义了你想要追踪的会议论文，你可以配置：
- **哪个会议**（MICCAI、CVPR、NeurIPS 等）
- **哪个年份**（特定年份或全部年份）
- **匹配严格程度**（strict 模式 vs broad 模式）
- **哪个轨道**（主会、工作坊、挑战赛）

### 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 使用默认设置运行（MICCAI 2026，strict 模式）
python scripts/update_papers.py

# 使用不同的会议范围
python scripts/update_papers.py --conference-scope cvpr-2025 --mode broad

# 追踪会议的所有年份
python scripts/update_papers.py --conference-scope miccai-all-years --mode broad
```

### 配置参数

| 参数 | 说明 | 示例值 |
|---|---|---|
| `--conference-scope` | 要追踪的会议和年份 | `miccai-2026`, `cvpr-2025`, `nips-2024`, `miccai-all-years` |
| `--mode` | 匹配严格程度 | `strict`（精确年份匹配）, `broad`（也匹配会议名） |
| `--tracks` | 包含的论文轨道 | `main`, `workshops`, `challenges`, `all` |

### 会议范围格式

有两种方式指定会议范围：

- **特定年份**：`{会议名}-{年份}`（如 `miccai-2026`、`cvpr-2025`、`iclr-2026`）
- **全部年份**：`{会议名}-all-years`（如 `miccai-all-years`、`cvpr-all-years`）

### 支持的会议

爬虫适用于任何在 arXiv 有论文提交的会议。常见会议包括：

| 会议缩写 | 全称 | 年份格式 |
|---|---|---|
| `miccai` | Medical Image Computing and Computer Assisted Intervention | MICCAI 2026 |
| `cvpr` | Computer Vision and Pattern Recognition | CVPR 2025 |
| `nips` / `neurips` | Neural Information Processing Systems | NeurIPS 2024 |
| `iccv` | International Conference on Computer Vision | ICCV 2025 |
| `iclr` | International Conference on Learning Representations | ICLR 2026 |
| `midl` | Medical Imaging with Deep Learning | MIDL 2024 |
| `aaai` | AAAI Conference on Artificial Intelligence | AAAI 2025 |
| `ijcai` | International Joint Conference on AI | IJCAI 2024 |

### 详细示例

#### 示例 1：追踪特定会议和年份

```bash
# 追踪 CVPR 2025 论文（strict 模式 - 需要 arXiv 元数据中有 "CVPR 2025"）
python scripts/update_papers.py --conference-scope cvpr-2025 --mode strict
```

**作用：**
- 在 arXiv 中搜索标题、摘要或评论中包含 "CVPR 2025" 的论文
- 只包含明确提及 2025 的论文
- 验证代码链接（GitHub、GitLab、Hugging Face）

#### 示例 2：追踪会议的所有年份

```bash
# 追踪所有 CVPR 论文（broad 模式）
python scripts/update_papers.py --conference-scope cvpr-all-years --mode broad
```

**作用：**
- 在 arXiv 中搜索任何提及 "CVPR" 的论文（不限年份）
- 包含所有年份的论文
- 更广泛的匹配（也包含只提到 "CVPR" 而没有具体年份的论文）

#### 示例 3：包含工作坊和挑战赛

```bash
# 追踪 NeurIPS 2024，包含工作坊和挑战赛
python scripts/update_papers.py --conference-scope nips-2024 --tracks all
```

**作用：**
- 搜索 NeurIPS 2024 主会论文
- 也包含工作坊论文（如果标题/摘要提到 "workshop"）
- 也包含挑战赛论文（如果标题/摘要提到 "challenge"）

#### 示例 4：追踪医学影像会议

```bash
# 追踪 MICCAI 2026（默认设置）
python scripts/update_papers.py --conference-scope miccai-2026

# 追踪所有年份的 MICCAI
python scripts/update_papers.py --conference-scope miccai-all-years
```

#### 示例 5：追踪 ICLR

```bash
# 追踪 ICLR 2026，包含所有轨道
python scripts/update_papers.py --conference-scope iclr-2026 --mode strict --tracks all
```

### 模式对比

| 模式 | 说明 | 使用场景 |
|---|---|---|
| `strict` | 需要在 arXiv 元数据中有精确年份 | 只要特定年份的论文 |
| `broad` | 也匹配没有年份的会议名 | 要追踪会议的所有论文（不限年份） |

**CVPR 示例：**
- `strict` 模式：只包含元数据中明确有 "CVPR 2025" 的论文
- `broad` 模式：也包含只提到 "CVPR" 而没有年份的论文

### 轨道选项

| 选项 | 说明 |
|---|---|
| `main` | 只有主会论文 |
| `workshops` | 只有工作坊论文 |
| `challenges` | 只有挑战赛/竞赛论文 |
| `all` | 以上全部 |

### 爬虫工作流程

1. **发现**：使用搜索查询从 arXiv 获取候选论文
2. **过滤**：按会议范围和年份过滤
3. **验证**：检查有效的代码链接（GitHub/GitLab/Hugging Face）
4. **分类**：分配到类别（分割、重建、分类等）
5. **生成**：生成带论文列表的 README.md

### 常见问题解决

**Q：找不到论文？**
- 检查会议名称是否正确
- 尝试将 `--mode` 从 `strict` 改为 `broad`
- 验证年份格式（如使用 2025，不是 '25）

**Q：论文太少/太多？**
- 调整 `--mode` 从 `strict` 到 `broad` 或反之
- 修改会议范围为特定年份

## 分类配置

爬虫会根据标题和摘要中的关键词匹配自动将论文分类到不同类别。这些类别是**在代码中预定义的**，可以进行修改。

### 默认分类

| 分类 | 中文名称 | 英文名称 | 关键词 |
|---|---|---|---|
| Segmentation | 图像分割 | Segmentation | segmentation, segment, delineation, contour, mask |
| Reconstruction | 图像重建 | Reconstruction | reconstruction, reconstruct, restoration, super-resolution, denoising |
| Classification | 分类/检测 | Classification | classification, classify, classifier, recognition, detection, diagnosis |
| Image Registration | 图像配准 | Image Registration | registration, alignment, deformable, deformation |
| Domain Adaptation | 域适应 | Domain Adaptation | domain adaptation, transfer learning, cross-domain, domain generalization |
| Generative Models | 生成模型 | Generative Models | generative, generation, synthesis, GAN, diffusion, VAE, autoencoder |
| General | 通用 | General | （后备类别） |

### 分类工作原理

1. **关键词匹配**：每个类别都有预定义的正则表达式模式及权重
2. **分数计算**：根据标题中的关键词（2倍权重）和摘要中的关键词为论文打分
3. **阈值**：论文必须超过阈值才能分配到某个类别
4. **多标签**：论文可以属于多个类别
5. **后备**：没有强匹配的论文归入"通用"类别

### 如何修改分类

要自定义分类，请编辑 `scripts/update_papers.py`：

#### 步骤 1：修改 CATEGORY_ORDER

```python
# 添加、删除或重新排序分类
CATEGORY_ORDER = [
    "Segmentation",
    "Reconstruction",
    "Classification",
    "Image Registration",
    "Domain Adaptation",
    "Generative Models",
    "General",
    # 在这里添加新分类
]
```

#### 步骤 2：修改 CATEGORY_RULES

```python
# 为每个分类添加或修改关键词规则
CATEGORY_RULES = {
    "Segmentation": [
        (r"\bsegmentation\b", 3),  # (模式, 权重)
        (r"\bsegment\b", 2),
        # 添加更多模式...
    ],
    # 添加新分类的规则...
}
```

#### 步骤 3：修改 CATEGORY_MARKERS

```python
# 添加模板渲染的标记
CATEGORY_MARKERS = {
    "Segmentation": "SEGMENTATION",
    # 添加新标记...
}
```

#### 步骤 4：修改 CATEGORY_THRESHOLDS

```python
# 调整每个分类的阈值
CATEGORY_THRESHOLDS = {
    "Segmentation": 2,
    # 调整阈值...
}
```

#### 步骤 5：更新 README.md 模板

在 README.md 中添加分类部分：

```markdown
## 分类名称

*此列表是自动生成的。*

<!-- BEGIN 分类标记_PAPERS -->
*（论文将被插入到这里）*
<!-- END 分类标记_PAPERS -->
```

### 分类自定义示例

**示例：添加"目标检测"作为新分类**

1. 添加到 CATEGORY_ORDER：
```python
CATEGORY_ORDER = [
    "Segmentation",
    "目标检测",  # 新增
    "Reconstruction",
    ...
]
```

2. 添加到 CATEGORY_RULES：
```python
CATEGORY_RULES = {
    "目标检测": [
        (r"\bobject detection\b", 3),
        (r"\bdetection\b", 2),
        (r"\bdetector\b", 2),
    ],
    ...
}
```

3. 添加到 CATEGORY_MARKERS：
```python
CATEGORY_MARKERS = {
    "目标检测": "OBJECT_DETECTION",
    ...
}
```

4. 在 README.md 中添加部分：
```markdown
## 目标检测

<!-- BEGIN OBJECT_DETECTION_PAPERS -->
*论文将被插入到这里*
<!-- END OBJECT_DETECTION_PAPERS -->
```

### 语言特定的自定义

对于不同的会议，你可能需要添加特定语言的关键词：

```python
CATEGORY_RULES = {
    "Classification": [
        (r"\bclassification\b", 3),
        (r"\bdetection\b", 2),
        # 为医学会议添加非英语关键词
        (r"\b诊断\b", 3),  # 中文：诊断
        (r"\b分类\b", 3),  # 简体中文：分类
    ],
}
```

## 目录

- [如何贡献](#如何贡献)
- [收录政策](#收录政策)
- [可信度与验证](#可信度与验证)
- [覆盖率报告](#覆盖率报告)
- [分割](#分割)
- [重建](#重建)
- [分类](#分类)
- [图像配准](#图像配准)
- [域适应](#域适应)
- [生成模型](#生成模型)
- [通用](#通用)

## 如何贡献

欢迎贡献！虽然该列表由自动搜索 arXiv 论文的爬虫维护，但我们重视人工审核以确保质量和完整性。

**贡献方式：**
- 🐛 **报告错误**：链接损坏、格式错误、论文过时、分类错误
- 📝 **添加缺失论文**：符合当前会议范围且有开源代码的论文
- 🏷️ **建议更好的分类**：在不去除有效重叠的前提下改进多标签质量
- 💡 **提出分类法改进建议**：带示例说明

**贡献前：**
1. 提供论文符合当前会议范围的证据
2. 确保代码仓库是公开可访问的
3. 验证链接和分类建议是具体可复现的

## 收录政策

- 真相来源是 arXiv 元数据（`title`、`abstract` 和 `comment`）加上公开仓库链接
- 论文必须在 arXiv 可搜索元数据中包含会议名称；当范围是 `miccai-2026` 时，必须标明 2026
- 代码链接必须指向支持的公开平台：GitHub、GitLab 或 Hugging Face
- 当论文强烈匹配多个任务时，可以故意出现在多个类别中

## 可信度与验证

- `<!-- BEGIN ... -->` 和 `<!-- END ... -->` 标记之间的内容是爬虫生成的，每次成功运行都会覆盖
- 如果发现不完整、生成的 markdown 格式错误或质量检查失败，每日自动化会立即失败
- README 验证检查标记完整性、格式错误的 URL、每个类别的重复条目和不支持的代码平台
- 默认自动化运行参数为 `--conference-scope miccai-all-years --mode broad --tracks all`
- 维护者可以通过 `--conference-scope miccai-2026` 和 `--mode strict` 缩小范围

## 覆盖率报告

<!-- BEGIN COVERAGE_REPORT -->
- Conference scope: `miccai-all-years`
- Discovery mode: `broad`
- Tracks: `all`
- Total code-backed papers: `784`
- Fetched arXiv records: `3063`
- Unique arXiv records: `2950`
- Filtered (non-target): `0`
- Filtered (track): `0`
- Filtered (no code links): `2166`

| Category | Count | Gap to 1000 |
|---|---:|---:|
| Segmentation | 351 | 649 |
| Reconstruction | 114 | 886 |
| Classification | 300 | 700 |
| Image Registration | 95 | 905 |
| Domain Adaptation | 62 | 938 |
| Generative Models | 169 | 831 |
| General | 89 | 911 |
<!-- END COVERAGE_REPORT -->

## 分割

*此列表是自动生成的。有问题？请提交 Pull Request！*

<!-- BEGIN SEGMENTATION_PAPERS -->
* **[Glance and Focus Reinforcement for Pan-cancer Screening](https://arxiv.org/abs/2601.19103v2)** - [Code](https://github.com/luffy03/gf-screen) (confidence: high)
* **[SSL-MedSAM2: A Semi-supervised Medical Image Segmentation Framework Powered by Few-shot Learning of SAM2](https://arxiv.org/abs/2512.11548v1)** - [Code](https://github.com/naisops/ssl-medsam2) (confidence: high)
* **[The MICCAI Federated Tumor Segmentation (FeTS) Challenge 2024: Efficient and Robust Aggregation Methods for Federated Learning](https://arxiv.org/abs/2512.06206v1)** - [Code](https://github.com/fets-ai/challenge) (confidence: high)
<!-- END SEGMENTATION_PAPERS -->

## 重建

*此列表是自动生成的。有问题？请提交 Pull Request！*

<!-- BEGIN RECONSTRUCTION_PAPERS -->
*This category is being populated. Check back soon!*
<!-- END RECONSTRUCTION_PAPERS -->

## 分类

*此列表是自动生成的。有问题？请提交 Pull Request！*

<!-- BEGIN CLASSIFICATION_PAPERS -->
*This category is being populated. Check back soon!*
<!-- END CLASSIFICATION_PAPERS -->

## 图像配准

*此列表是自动生成的。有问题？请提交 Pull Request！*

<!-- BEGIN IMAGE_REGISTRATION_PAPERS -->
*This category is being populated. Check back soon!*
<!-- END IMAGE_REGISTRATION_PAPERS -->

## 域适应

*此列表是自动生成的。有问题？请提交 Pull Request！*

<!-- BEGIN DOMAIN_ADAPTATION_PAPERS -->
*This category is being populated. Check back soon!*
<!-- END DOMAIN_ADAPTATION_PAPERS -->

## 生成模型

*此列表是自动生成的。有问题？请提交 Pull Request！*

<!-- BEGIN GENERATIVE_MODELS_PAPERS -->
*This category is being populated. Check back soon!*
<!-- END GENERATIVE_MODELS_PAPERS -->

## 通用

*此列表是自动生成的。有问题？请提交 Pull Request！*

<!-- BEGIN GENERAL_PAPERS -->
*This category is being populated. Check back soon!*
<!-- END GENERAL_PAPERS -->