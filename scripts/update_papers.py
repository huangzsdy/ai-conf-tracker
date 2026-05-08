#!/usr/bin/env python3
"""Update the Awesome MICCAI README from arXiv data.

Pipeline stages:
1) Discover: fetch candidate MICCAI papers from arXiv
2) Normalize: clean and canonicalize repository links
3) Validate: reject malformed/unsupported records
4) Categorize: multi-label category + confidence assignment
5) Render: deterministically regenerate README category blocks and coverage report

Usage (without VPN/proxy):
    HTTPS_PROXY=http://127.0.0.1:7890 python scripts/update_papers.py

Usage (with proxy environment):
    export HTTPS_PROXY=http://127.0.0.1:7890
    export HTTP_PROXY=http://127.0.0.1:7890
    python scripts/update_papers.py --conference-scope cvpr-2025
"""

from __future__ import annotations

import argparse
import csv
import os
import re
from datetime import datetime, timezone
import time
from typing import Any, Dict, List, Optional, Pattern, Sequence, Tuple
from urllib.parse import urlparse

import arxiv


CATEGORY_ORDER = [
    "Segmentation",
    "Reconstruction",
    "Classification",
    "Image Registration",
    "Domain Adaptation",
    "Generative Models",
    "General",
]

CATEGORY_MARKERS = {
    "Segmentation": "SEGMENTATION",
    "Reconstruction": "RECONSTRUCTION",
    "Classification": "CLASSIFICATION",
    "Image Registration": "IMAGE_REGISTRATION",
    "Domain Adaptation": "DOMAIN_ADAPTATION",
    "Generative Models": "GENERATIVE_MODELS",
    "General": "GENERAL",
}

ALLOWED_CODE_HOSTS = {"github.com", "gitlab.com", "huggingface.co"}
TRACK_OPTIONS = {"main", "workshops", "challenges", "all"}
# Conference scope format: "conference-year" (e.g., "miccai-2026", "cvpr-2025", "nips-2024")
# Or "conference-all-years" for all years (e.g., "miccai-all-years")

# Helper to extract conference name and year from scope
def parse_conference_scope(conference_scope: str) -> Tuple[str, Optional[int]]:
    """Parse conference scope into (conference_name, year). year None means all years."""
    if conference_scope == "miccai-all-years" or conference_scope.endswith("-all-years"):
        # Keep backward compatibility
        conf_name = conference_scope.replace("-all-years", "")
        return conf_name, None

    # Try to extract year: conference-year format
    parts = conference_scope.rsplit("-", 1)
    if len(parts) == 2 and parts[1].isdigit():
        return parts[0].lower(), int(parts[1])
    return conference_scope.lower(), None

# (regex pattern, weight)
CATEGORY_RULES = {
    "Segmentation": [
        (r"\bsegmentation\b", 3),
        (r"\bsegment\b", 2),
        (r"\bdelineation\b", 2),
        (r"\bcontour\b", 2),
        (r"\bmask\b", 1),
        (r"\bmasking\b", 1),
    ],
    "Reconstruction": [
        (r"\breconstruction\b", 3),
        (r"\breconstruct\b", 2),
        (r"\brestoration\b", 2),
        (r"\brestore\b", 1),
        (r"\bsuper[- ]resolution\b", 2),
        (r"\bdenoising\b", 2),
    ],
    "Classification": [
        (r"\bclassification\b", 3),
        (r"\bclassify\b", 2),
        (r"\bclassifier\b", 2),
        (r"\brecognition\b", 2),
        (r"\bdetection\b", 2),
        (r"\bdiagnosis\b", 1),
    ],
    "Image Registration": [
        (r"\bregistration\b", 3),
        (r"\balignment\b", 2),
        (r"\bdeformable\b", 2),
        (r"\bdeformation\b", 2),
    ],
    "Domain Adaptation": [
        (r"\bdomain adaptation\b", 3),
        (r"\btransfer learning\b", 2),
        (r"\bcross[- ]domain\b", 2),
        (r"\bdomain shift\b", 2),
        (r"\bdomain generalization\b", 3),
        (r"\bgeneralization\b", 1),
    ],
    "Generative Models": [
        (r"\bgenerative\b", 3),
        (r"\bgeneration\b", 2),
        (r"\bsynthesis\b", 2),
        (r"\bgan\b", 2),
        (r"\bdiffusion\b", 2),
        (r"\bvae\b", 2),
        (r"\bautoencoder\b", 2),
        (r"\bflow matching\b", 2),
    ],
}
CATEGORY_COMPILED_RULES: Dict[str, List[Tuple[Pattern[str], int]]] = {
    category: [(re.compile(pattern), weight) for pattern, weight in rules]
    for category, rules in CATEGORY_RULES.items()
}

CATEGORY_THRESHOLDS = {
    "Segmentation": 2,
    "Reconstruction": 2,
    "Classification": 2,
    "Image Registration": 2,
    "Domain Adaptation": 2,
    "Generative Models": 2,
}

REPO_URL_PATTERN = re.compile(
    r"https?://(?:www\.)?(?:github\.com|gitlab\.com|huggingface\.co)/[^\s\]\[<>\"')]+",
    flags=re.IGNORECASE,
)

ARXIV_ABS_PATTERN = re.compile(r"^https?://arxiv\.org/abs/\d{4}\.\d{4,5}(?:v\d+)?$")
MICCAI_2026_PATTERN = re.compile(r"\bmiccai\s*[-_ ]?\s*2026\b|\bmiccai(?:'26|26)\b", re.IGNORECASE)
MICCAI_PATTERN = re.compile(r"\bmiccai\b", re.IGNORECASE)
MICCAI_2025_PATTERN = re.compile(r"\bmiccai\s*[-_ ]?\s*2025\b|\bmiccai(?:'25|25)\b", re.IGNORECASE)

# Conference-year pattern: e.g., "cvpr-2025", "nips-2024", "miccai-2026"
CONF_YEAR_PATTERN = re.compile(r"(?P<conf>[a-z]+)[-_]?(?P<year>20\d{2}|\d{2})", re.IGNORECASE)
MICCAI_EXPLICIT_YEAR_PATTERN = re.compile(
    r"\bmiccai\s*[-_ ]?(?P<year>20\d{2}|'?\d{2})\b", re.IGNORECASE
)
MICCAI_SUBMISSION_PATTERN = re.compile(
    r"\b(submitted|under review|accepted|camera[- ]ready)\b.{0,32}\bmiccai\b",
    re.IGNORECASE,
)

TRACK_PATTERNS = {
    "workshops": re.compile(r"\bworkshop\b", re.IGNORECASE),
    "challenges": re.compile(r"\bchallenge\b", re.IGNORECASE),
}

SCOPE_LINE_PATTERN = re.compile(r"\*\*Conference Scope\*\*: [^\n]*")
MODE_LINE_PATTERN = re.compile(r"\*\*Discovery Mode\*\*: [^\n]*")
COVERAGE_BLOCK_PATTERN = re.compile(
    r"<!-- BEGIN COVERAGE_REPORT -->(?P<body>.*?)<!-- END COVERAGE_REPORT -->", re.S
)


def _normalize_host(host: str) -> str:
    host = host.lower().strip()
    return host[4:] if host.startswith("www.") else host


def _clean_url_candidate(url: str) -> str:
    url = url.strip()
    url = url.split("}{", 1)[0]
    url = re.sub(r"[.,;:!?\]\}>\"'\s]+$", "", url)
    return url


def _canonical_repo_key(parsed_path: str, host: str) -> Optional[Tuple[str, str, str]]:
    segments = [segment for segment in parsed_path.split("/") if segment]
    if len(segments) < 2:
        return None

    owner = segments[0].lower()
    repo = segments[1].lower()

    blocked_owner_paths = {"orgs", "topics", "collections", "about", "search", "settings"}
    if owner in blocked_owner_paths:
        return None

    repo = repo[:-4] if repo.endswith(".git") else repo
    if not owner or not repo:
        return None

    return host, owner, repo


def normalize_repository_url(url: str) -> Optional[Tuple[str, Tuple[str, str, str]]]:
    cleaned = _clean_url_candidate(url)
    try:
        parsed = urlparse(cleaned)
    except ValueError:
        return None

    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None

    host = _normalize_host(parsed.netloc)
    if host not in ALLOWED_CODE_HOSTS:
        return None

    repo_key = _canonical_repo_key(parsed.path, host)
    if repo_key is None:
        return None

    canonical_url = f"https://{repo_key[0]}/{repo_key[1]}/{repo_key[2]}"
    return canonical_url, repo_key


def get_repository_links(text: str) -> List[str]:
    candidates = REPO_URL_PATTERN.findall(text or "")
    deduped: List[str] = []
    seen_keys = set()

    for candidate in candidates:
        normalized = normalize_repository_url(candidate)
        if normalized is None:
            continue
        canonical_url, repo_key = normalized
        if repo_key in seen_keys:
            continue
        seen_keys.add(repo_key)
        deduped.append(canonical_url)

    return deduped


def score_categories(title: str, abstract: str) -> Dict[str, int]:
    title_l = title.lower()
    abstract_l = abstract.lower()

    scores: Dict[str, int] = {}
    for category, rules in CATEGORY_COMPILED_RULES.items():
        score = 0
        for pattern, weight in rules:
            title_hit = pattern.search(title_l)
            abstract_hit = pattern.search(abstract_l)
            if title_hit:
                score += weight * 2
            elif abstract_hit:
                score += weight
        scores[category] = score
    return scores


def categorize_paper(title: str, abstract: str, scores: Optional[Dict[str, int]] = None) -> List[str]:
    if scores is None:
        scores = score_categories(title, abstract)
    categories = [
        category
        for category in CATEGORY_ORDER
        if category in scores and scores[category] >= CATEGORY_THRESHOLDS.get(category, 2)
    ]
    if not categories:
        categories = ["General"]
    return categories


def get_category_confidence(category_scores: Dict[str, int], categories: Sequence[str]) -> Dict[str, str]:
    confidence: Dict[str, str] = {}
    for category in categories:
        if category == "General":
            confidence[category] = "medium"
            continue
        score = category_scores.get(category, 0)
        confidence[category] = "high" if score >= 4 else "medium"
    return confidence


def _extract_arxiv_year(arxiv_url: str) -> Optional[int]:
    match = re.search(r"/abs/(\d{2})\d{2}\.\d{4,5}", arxiv_url)
    if match:
        return int(match.group(1))
    # Legacy arXiv IDs such as /abs/cs/0601001
    legacy_match = re.search(r"/abs/[a-z\-]+/(\d{2})\d{4}", arxiv_url, re.IGNORECASE)
    if legacy_match:
        return int(legacy_match.group(1))
    return None


def _extract_explicit_miccai_years(text: str) -> List[int]:
    years: List[int] = []
    for match in MICCAI_EXPLICIT_YEAR_PATTERN.finditer(text):
        value = match.group("year").replace("'", "")
        year = int(value)
        if year < 100:
            year += 2000
        years.append(year)
    return years


def _infer_track(text: str) -> str:
    if TRACK_PATTERNS["challenges"].search(text):
        return "challenges"
    if TRACK_PATTERNS["workshops"].search(text):
        return "workshops"
    return "main"


def track_matches(requested_track: str, inferred_track: str) -> bool:
    if requested_track == "all":
        return True
    return requested_track == inferred_track


def _extract_explicit_conf_years(text: str, conference_name: str) -> List[int]:
    """Extract explicit conference years from text (e.g., 'miccai 2025', 'cvpr2025', 'cvpr'25')."""
    years: List[int] = []
    # Pattern: conference name followed by year
    pattern = re.compile(rf"\b{re.escape(conference_name)}\s*[-_]?\s*(20\d{{2}}|\d{{2}})", re.IGNORECASE)
    for match in pattern.finditer(text):
        value = match.group(1).replace("'", "")
        year = int(value)
        if year < 100:
            year += 2000
        years.append(year)
    return years


def is_target_conference_paper(text: str, arxiv_url: str, mode: str, conference_scope: str) -> bool:
    """Check if a paper matches the target conference based on scope.

    Args:
        text: Combined text from title, abstract, and comments
        arxiv_url: The arXiv URL of the paper
        mode: "strict" or "broad"
        conference_scope: e.g., "miccai-2026", "cvpr-2025", "nips-2024", "miccai-all-years"
    """
    conf_name, conf_year = parse_conference_scope(conference_scope)

    # Normalize conference name for pattern matching
    conf_name_lower = conf_name.lower()
    conf_pattern = re.compile(rf"\b{re.escape(conf_name_lower)}\b", re.IGNORECASE)

    # Year-specific scope (e.g., "miccai-2026", "cvpr-2025")
    if conf_year is not None:
        # Extract years mentioned in the text
        explicit_years = _extract_explicit_conf_years(text, conf_name_lower)
        year_short = conf_year % 100  # 2026 -> 26, 2025 -> 25

        if explicit_years:
            # If explicit years mentioned, must include the target year
            if conf_year in explicit_years:
                return True
            # Has explicit year but not target - reject if strict mode
            if mode == "strict":
                return False

        # Check pattern like "MICCAI 2026" or "MICCAI2026" or "MICCAI'26"
        year_pattern = re.compile(rf"{re.escape(conf_name_lower)}\s*[-_]?\s*{conf_year}|{re.escape(conf_name_lower)}(?:'{year_short}|{year_short})", re.IGNORECASE)
        if year_pattern.search(text):
            return True

        if mode == "strict":
            return False

        # In broad mode, check just the conference name
        if not conf_pattern.search(text):
            return False

        # Exclude previous year's pattern if present
        prev_year = conf_year - 1
        prev_year_short = prev_year % 100
        prev_pattern = re.compile(rf"{re.escape(conf_name_lower)}\s*[-_]?\s*{prev_year}|{re.escape(conf_name_lower)}(?:'{prev_year_short}|{prev_year_short})", re.IGNORECASE)
        if prev_pattern.search(text):
            return False

        # Check arXiv submission year
        year = _extract_arxiv_year(arxiv_url)
        if year == year_short:
            return True

        # Check for submission patterns
        return bool(MICCAI_SUBMISSION_PATTERN.search(text))

    # All years scope (e.g., "miccai-all-years")
    if not conf_pattern.search(text):
        return False
    if mode == "strict":
        # Require explicit year in text for strict mode
        return bool(re.search(rf"\b{re.escape(conf_name_lower)}\s*[-_]?\s*20\d{{2}}\b", text, re.IGNORECASE))
    return True


# Backward compatibility alias
is_target_miccai_paper = is_target_conference_paper


def build_queries(mode: str, conference_scope: str) -> List[str]:
    """Build arXiv search queries based on conference scope."""
    conf_name, conf_year = parse_conference_scope(conference_scope)
    conf_name_upper = conf_name.upper()
    conf_name_cap = conf_name.capitalize()

    queries = []

    # Year-specific scope
    if conf_year is not None:
        queries = [f'ti:"{conf_name_cap} {conf_year}"', f'abs:"{conf_name_cap} {conf_year}"', f'co:"{conf_name_cap} {conf_year}"']
        if mode == "broad":
            queries.extend([f'ti:"{conf_name_cap}"', f'abs:"{conf_name_cap}"', f'co:"{conf_name_cap}"'])
        return queries

    # All years scope
    return [f'ti:"{conf_name_cap}"', f'abs:"{conf_name_cap}"', f'co:"{conf_name_cap}"']


def discover_papers(mode: str, conference_scope: str, tracks: str, require_code: bool = True) -> Tuple[List[Dict[str, Any]], Dict[str, int], List[str]]:
    print(
        "[discover] Searching arXiv "
        f"(mode={mode}, conference_scope={conference_scope}, tracks={tracks}, require_code={require_code})"
    )

    queries = build_queries(mode, conference_scope)

    client = arxiv.Client(page_size=100, delay_seconds=3, num_retries=5)
    seen_arxiv = set()
    papers: List[Dict[str, Any]] = []
    failed_queries: List[str] = []
    stats = {
        "fetched_records": 0,
        "unique_arxiv_records": 0,
        "without_code_links": 0,
        "filtered_non_target": 0,
        "filtered_track": 0,
        "accepted_records": 0,
    }

    for query in queries:
        print(f"[discover] Query: {query}")
        try:
            search = arxiv.Search(
                query=query,
                max_results=5000 if conference_scope == "miccai-all-years" else 300,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending,
            )
            results = list(client.results(search))
            print(f"[discover] Results: {len(results)}")
        except Exception as exc:
            failed_queries.append(f"{query}: {exc}")
            print(f"[discover] ERROR: {query} failed -> {exc}")
            continue

        for result in results:
            stats["fetched_records"] += 1
            if result.entry_id in seen_arxiv:
                continue
            seen_arxiv.add(result.entry_id)
            stats["unique_arxiv_records"] += 1

            text = f"{result.title}\n{result.summary}\n{getattr(result, 'comment', '') or ''}"
            if not is_target_miccai_paper(text, result.entry_id, mode, conference_scope):
                stats["filtered_non_target"] += 1
                continue

            inferred_track = _infer_track(text)
            if not track_matches(tracks, inferred_track):
                stats["filtered_track"] += 1
                continue

            links = get_repository_links(text)
            if require_code and not links:
                stats["without_code_links"] += 1
                continue

            papers.append(
                {
                    "title": result.title.strip(),
                    "arxiv_url": result.entry_id.replace("http://", "https://"),
                    "repo_links": links,
                    "published": result.published,
                    "summary": result.summary,
                    "authors": [a.name for a in result.authors],
                    "track": inferred_track,
                }
            )
            stats["accepted_records"] += 1

    return papers, stats, failed_queries


def discover_papers_by_keyword(keyword: str, max_results: int = 500, require_code: bool = True) -> Tuple[List[Dict[str, Any]], Dict[str, int], List[str]]:
    """Discover papers by custom keyword search."""
    print(f"[discover] Searching arXiv by keyword: {keyword} (require_code={require_code})")

    client = arxiv.Client(page_size=100, delay_seconds=5, num_retries=5)
    seen_arxiv = set()
    papers: List[Dict[str, Any]] = []
    stats = {
        "fetched_records": 0,
        "unique_arxiv_records": 0,
        "without_code_links": 0,
        "filtered_non_target": 0,
        "filtered_track": 0,
        "accepted_records": 0,
    }
    failed_queries = []

    # Search by keyword in title and abstract
    query = f"all:{keyword}"

    try:
        print(f"[discover] Query: {query}")
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending,
        )
        results = list(client.results(search))
        print(f"[discover] Results: {len(results)}")
    except Exception as exc:
        failed_queries.append(f"{query}: {exc}")
        print(f"[discover] ERROR: {query} failed -> {exc}")
        return papers, stats, failed_queries

    for result in results:
        stats["fetched_records"] += 1
        if result.entry_id in seen_arxiv:
            continue
        seen_arxiv.add(result.entry_id)

        # Extract code links from comment and links
        comment = getattr(result, "comment", "") or ""
        text = f"{result.title}\n{result.summary}\n{comment}"
        links = get_repository_links(text)

        if require_code and not links:
            stats["without_code_links"] += 1
            continue

        papers.append({
            "title": result.title.strip(),
            "arxiv_url": result.entry_id.replace("http://", "https://"),
            "repo_links": links,
            "published": result.published,
            "summary": result.summary,
            "authors": [a.name for a in result.authors],
            "track": "keyword",
        })
        stats["accepted_records"] += 1

    return papers, stats, failed_queries


def validate_papers_data(papers: List[Dict[str, Any]]) -> Tuple[int, int, int]:
    print("[validate] Validating normalized paper records")

    deduped_papers: List[Dict[str, Any]] = []
    seen_pairs = set()
    removed_duplicates = 0
    rejected_records = 0
    uncertain_records = 0

    for paper in papers:
        arxiv_url = paper.get("arxiv_url", "")
        title = paper.get("title", "").strip()
        links = paper.get("repo_links", [])

        if not title or not ARXIV_ABS_PATTERN.match(arxiv_url):
            rejected_records += 1
            continue

        cleaned_links = []
        seen_repo_keys = set()
        for link in links:
            normalized = normalize_repository_url(link)
            if normalized is None:
                continue
            canonical_url, repo_key = normalized
            if repo_key in seen_repo_keys:
                continue
            seen_repo_keys.add(repo_key)
            cleaned_links.append(canonical_url)

        if not cleaned_links:
            rejected_records += 1
            continue

        pair_key = arxiv_url.lower()
        if pair_key in seen_pairs:
            removed_duplicates += 1
            continue

        seen_pairs.add(pair_key)
        normalized_paper = dict(paper)
        normalized_paper["repo_links"] = cleaned_links

        scores = score_categories(title, paper.get("summary", ""))
        categories = categorize_paper(title, paper.get("summary", ""), scores=scores)
        normalized_paper["category_scores"] = scores
        normalized_paper["categories"] = categories
        normalized_paper["confidence"] = get_category_confidence(scores, categories)
        normalized_paper["is_uncertain"] = (
            categories == ["General"] and max(scores.values()) < 2 if scores else True
        )
        if normalized_paper["is_uncertain"]:
            uncertain_records += 1

        deduped_papers.append(normalized_paper)

    papers[:] = deduped_papers
    print(
        "[validate] Completed: "
        f"kept={len(deduped_papers)} removed_duplicates={removed_duplicates} "
        f"rejected={rejected_records} uncertain={uncertain_records}"
    )
    return removed_duplicates, rejected_records, uncertain_records


def generate_category_markdown(papers: Sequence[Dict[str, Any]], category: str) -> str:
    category_papers = [paper for paper in papers if category in paper["categories"]]
    category_papers.sort(key=_published_sort_key)

    lines = []
    for paper in category_papers:
        title = paper["title"]
        arxiv_url = paper["arxiv_url"]
        links = paper["repo_links"]

        confidence = paper.get("confidence", {}).get(category, "medium")
        confidence_badge = f"(confidence: {confidence})"

        line = f"* **[{title}]({arxiv_url})** - [Code]({links[0]}) {confidence_badge}"
        if len(links) > 1:
            extras = [f"[Code{i + 2}]({url})" for i, url in enumerate(links[1:])]
            line += " | " + " | ".join(extras)

        lines.append(line)

    return "\n".join(lines)


def _published_sort_key(paper: Dict[str, Any]) -> Tuple[float, str]:
    published = paper["published"]
    if published.tzinfo is None:
        published = published.replace(tzinfo=timezone.utc)
    else:
        published = published.astimezone(timezone.utc)
    return (-published.timestamp(), paper["title"].lower())


def replace_category_block(content: str, marker: str, body: str) -> str:
    pattern = rf"(<!-- BEGIN {marker}_PAPERS -->).*?(<!-- END {marker}_PAPERS -->)"
    replacement = f"\\1\n{body}\n\\2" if body else f"\\1\n\\2"

    if not re.search(pattern, content, flags=re.DOTALL):
        raise ValueError(f"Missing marker block for {marker}")

    return re.sub(pattern, replacement, content, flags=re.DOTALL)


def build_coverage_report(
    papers: Sequence[Dict[str, Any]],
    stats: Dict[str, int],
    conference_scope: str,
    mode: str,
    tracks: str,
) -> str:
    category_counts = {category: len([p for p in papers if category in p["categories"]]) for category in CATEGORY_ORDER}
    total = len(papers)

    lines = [
        f"- Conference scope: `{conference_scope}`",
        f"- Discovery mode: `{mode}`",
        f"- Tracks: `{tracks}`",
        f"- Total code-backed papers: `{total}`",
        f"- Fetched arXiv records: `{stats['fetched_records']}`",
        f"- Unique arXiv records: `{stats['unique_arxiv_records']}`",
        f"- Filtered (non-target): `{stats['filtered_non_target']}`",
        f"- Filtered (track): `{stats['filtered_track']}`",
        f"- Filtered (no code links): `{stats['without_code_links']}`",
        "",
        "| Category | Count | Gap to 1000 |",
        "|---|---:|---:|",
    ]

    for category in CATEGORY_ORDER:
        count = category_counts[category]
        gap = max(0, 1000 - count)
        lines.append(f"| {category} | {count} | {gap} |")

    return "\n".join(lines)


def update_readme(
    papers: Sequence[Dict[str, Any]],
    stats: Dict[str, int],
    conference_scope: str,
    mode: str,
    tracks: str,
    readme_path: str = "README.md",
) -> Dict[str, int]:
    with open(readme_path, "r", encoding="utf-8") as file:
        content = file.read()

    category_counts: Dict[str, int] = {}
    for category in CATEGORY_ORDER:
        marker = CATEGORY_MARKERS[category]
        body = generate_category_markdown(papers, category)
        content = replace_category_block(content, marker, body)
        category_counts[category] = len([p for p in papers if category in p["categories"]])

    coverage_body = build_coverage_report(papers, stats, conference_scope, mode, tracks)
    coverage_match = COVERAGE_BLOCK_PATTERN.search(content)
    if coverage_match:
        content = COVERAGE_BLOCK_PATTERN.sub(
            f"<!-- BEGIN COVERAGE_REPORT -->\n{coverage_body}\n<!-- END COVERAGE_REPORT -->",
            content,
        )

    content = SCOPE_LINE_PATTERN.sub(f"**Conference Scope**: {conference_scope}", content)
    content = MODE_LINE_PATTERN.sub(f"**Discovery Mode**: {mode}", content)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    content = re.sub(
        r"\*\*Last Updated\*\*: [^\n]*",
        f"**Last Updated**: {timestamp} by GitHub Actions",
        content,
    )

    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(content)

    return category_counts


def export_to_csv(papers: Sequence[Dict[str, Any]], output_path: str) -> None:
    """Export papers to CSV format for Zotero import."""
    fieldnames = ["Title", "Url", "Code Link 1", "Code Link 2", "Code Link 3", "Categories", "Confidence", "Published"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for paper in papers:
            links = paper.get("repo_links", [])
            row = {
                "Title": paper.get("title", ""),
                "Url": paper.get("arxiv_url", ""),
                "Code Link 1": links[0] if len(links) > 0 else "",
                "Code Link 2": links[1] if len(links) > 1 else "",
                "Code Link 3": links[2] if len(links) > 2 else "",
                "Categories": "; ".join(paper.get("categories", [])),
                "Confidence": paper.get("confidence", {}).get(paper.get("categories", ["General"])[0], "medium"),
                "Published": paper.get("published", "").isoformat() if paper.get("published") else "",
            }
            writer.writerow(row)
    print(f"[export] CSV saved to {output_path}")


def export_to_bibtex(papers: Sequence[Dict[str, Any]], output_path: str) -> None:
    """Export papers to BibTeX format for Zotero import."""
    with open(output_path, "w", encoding="utf-8") as f:
        for paper in papers:
            title = paper.get("title", "")
            arxiv_url = paper.get("arxiv_url", "")
            published = paper.get("published")
            links = paper.get("repo_links", [])
            categories = paper.get("categories", [])

            # Generate citation key
            first_author = "Unknown"
            if paper.get("authors"):
                first_author = paper["authors"][0].split()[-1]  # Last name
            year = published.year if published else "20xx"
            key = f"{first_author}{year}".replace(",", "").replace(" ", "")

            # Format the entry
            f.write(f"@article{{{key},\n")
            f.write(f"  title={{{title}}},\n")
            if paper.get("authors"):
                f.write(f"  author={{{' and '.join(paper['authors'])}}},\n")
            if published:
                f.write(f"  year={{{published.year}}},\n")
                f.write(f"  journal={{arXiv preprint}}\n")
            f.write(f"  url={{{arxiv_url}}},\n")
            f.write(f"  note={{Code: {', '.join(links)}}}\n")
            f.write(f"  keywords={{{', '.join(categories)}}}\n")
            f.write("}\n\n")
    print(f"[export] BibTeX saved to {output_path}")


def export_to_ris(papers: Sequence[Dict[str, Any]], output_path: str) -> None:
    """Export papers to RIS format for Zotero import."""
    with open(output_path, "w", encoding="utf-8") as f:
        for paper in papers:
            title = paper.get("title", "")
            arxiv_url = paper.get("arxiv_url", "")
            published = paper.get("published")
            links = paper.get("repo_links", [])
            categories = paper.get("categories", [])

            f.write("TY  - EREP\n")
            f.write(f"TI  - {title}\n")
            if paper.get("authors"):
                for author in paper["authors"]:
                    f.write(f"AU  - {author}\n")
            if published:
                f.write(f"PY  - {published.year}\n")
            f.write(f"DO  - {arxiv_url}\n")
            f.write("M3  - preprint\n")
            f.write(f"UR  - {arxiv_url}\n")
            for link in links:
                f.write(f"L1  - {link}\n")
            for cat in categories:
                f.write(f"KW  - {cat}\n")
            f.write("ER  - \n\n")
    print(f"[export] RIS saved to {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update Awesome conference papers list")
    parser.add_argument(
        "--mode",
        choices=["strict", "broad"],
        default="strict",
        help="Discovery strictness",
    )
    parser.add_argument(
        "--conference-scope",
        type=str,
        default="miccai-2026",
        help="Conference scope (e.g., miccai-2026, cvpr-2025, nips-2024, miccai-all-years)",
    )
    parser.add_argument(
        "--tracks",
        choices=sorted(TRACK_OPTIONS),
        default="all",
        help="Track filter",
    )
    parser.add_argument(
        "--keyword",
        type=str,
        help="Custom keyword search (instead of conference-scope). Searches arXiv by keyword.",
    )
    parser.add_argument(
        "--export",
        choices=["csv", "bibtex", "ris", "all"],
        help="Export format for Zotero (csv, bibtex, ris, or all)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="exports",
        help="Output directory for exported files (default: exports)",
    )
    parser.add_argument(
        "--by-category",
        action="store_true",
        help="Export each category to separate subdirectories",
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=5,
        help="Delay seconds between API requests (default: 5)",
    )
    parser.add_argument(
        "--require-code",
        action="store_true",
        default=True,
        help="Only include papers with code links (default: True)",
    )
    parser.add_argument(
        "--no-require-code",
        action="store_false",
        dest="require_code",
        help="Include all papers regardless of code links",
    )
    args = parser.parse_args()

    # Skip conference scope validation if using keyword search
    if args.keyword:
        conf_name = args.keyword
        conf_year = None
    else:
        conf_name, conf_year = parse_conference_scope(args.conference_scope)
        if not conf_name:
            print(f"[ERROR] Invalid conference scope: {args.conference_scope}")
            return 1

    print(
        f"Starting Awesome {conf_name.upper()} update "
        f"(mode={args.mode}, conference_scope={args.conference_scope}, tracks={args.tracks})"
    )

    # Use keyword search or conference search
    if args.keyword:
        papers, stats, failed_queries = discover_papers_by_keyword(args.keyword, require_code=args.require_code)
    else:
        papers, stats, failed_queries = discover_papers(args.mode, args.conference_scope, args.tracks, require_code=args.require_code)

    if failed_queries:
        print("[discover] Failing update because one or more discovery queries failed:")
        for failure in failed_queries:
            print(f"  - {failure}")
        return 1

    removed_duplicates, rejected_records, uncertain_records = validate_papers_data(papers)
    category_counts = update_readme(
        papers,
        stats,
        args.conference_scope,
        args.mode,
        args.tracks,
    )

    # Export to Zotero-compatible formats if requested
    if args.export:
        # Determine base output directory
        # If using keyword without --by-category, treat like conference search (no keyword subdir)
        if args.keyword and args.by_category:
            # Use keyword as subdirectory only when --by-category is specified
            safe_keyword = re.sub(r'[^\w\-]', '_', args.keyword)
            output_dir = os.path.join(args.output_dir, safe_keyword)
        elif args.keyword:
            # Keyword search but no --by-category: use output_dir directly (like conference)
            output_dir = args.output_dir
        else:
            conf_name, _ = parse_conference_scope(args.conference_scope)
            output_dir = os.path.join(args.output_dir, conf_name)

        os.makedirs(output_dir, exist_ok=True)

        if args.by_category:
            # Export each category to separate subdirectory
            for category in CATEGORY_ORDER:
                category_papers = [p for p in papers if category in p.get("categories", [])]
                if not category_papers:
                    continue

                # Create category subdirectory
                safe_name = re.sub(r'[^\w\-]', '_', category)
                category_dir = os.path.join(output_dir, safe_name)
                os.makedirs(category_dir, exist_ok=True)

                if args.export in ("csv", "all"):
                    export_to_csv(category_papers, os.path.join(category_dir, f"{safe_name}.csv"))
                if args.export in ("bibtex", "all"):
                    export_to_bibtex(category_papers, os.path.join(category_dir, f"{safe_name}.bib"))
                if args.export in ("ris", "all"):
                    export_to_ris(category_papers, os.path.join(category_dir, f"{safe_name}.ris"))
        else:
            # Single file export
            if args.export in ("csv", "all"):
                export_to_csv(papers, os.path.join(output_dir, f"{conf_name}_papers.csv"))
            if args.export in ("bibtex", "all"):
                export_to_bibtex(papers, os.path.join(output_dir, f"{conf_name}_papers.bib"))
            if args.export in ("ris", "all"):
                export_to_ris(papers, os.path.join(output_dir, f"{conf_name}_papers.ris"))

    print("[summary] Pipeline completed")
    print(f"[summary] fetched_records={stats['fetched_records']}")
    print(f"[summary] unique_arxiv_records={stats['unique_arxiv_records']}")
    print(f"[summary] without_code_links={stats['without_code_links']}")
    print(f"[summary] filtered_non_target={stats['filtered_non_target']}")
    print(f"[summary] filtered_track={stats['filtered_track']}")
    print(f"[summary] accepted_records={stats['accepted_records']}")
    print(f"[summary] deduplicated_records={removed_duplicates}")
    print(f"[summary] rejected_records={rejected_records}")
    print(f"[summary] uncertain_records={uncertain_records}")
    print("[summary] category_counts=" + ", ".join(f"{k}:{v}" for k, v in category_counts.items()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
