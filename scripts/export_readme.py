#!/usr/bin/env python3
"""Parse README.md and export papers to Zotero-compatible formats with categories."""

import csv
import re
import os
import argparse
from pathlib import Path


# Category markers in README.md
CATEGORY_BLOCKS = {
    "SEGMENTATION": "Segmentation",
    "RECONSTRUCTION": "Reconstruction",
    "CLASSIFICATION": "Classification",
    "IMAGE_REGISTRATION": "Image Registration",
    "DOMAIN_ADAPTATION": "Domain Adaptation",
    "GENERATIVE_MODELS": "Generative Models",
    "GENERAL": "General",
}


def parse_readme_by_category(readme_path: str) -> dict:
    """Parse papers from README.md, grouped by category."""
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern to match paper entries
    paper_pattern = r'\* \*\*\[([^\]]+)\]\(([^\)]+)\)\*\* - \[Code\]\(([^\)]+)\)( \(confidence: (\w+)\))?'

    # Find all category blocks
    papers_by_category = {}

    for marker, category_name in CATEGORY_BLOCKS.items():
        block_pattern = rf'<!-- BEGIN {marker}_PAPERS -->(.*?)<!-- END {marker}_PAPERS -->'
        match = re.search(block_pattern, content, re.DOTALL)

        if not match:
            continue

        block_content = match.group(1)
        papers_by_category[category_name] = []

        for pm in re.finditer(paper_pattern, block_content):
            title = pm.group(1)
            arxiv_url = pm.group(2)
            code_link = pm.group(3)
            confidence = pm.group(5) if pm.group(5) else "medium"

            # Extract arXiv ID for year
            arxiv_id_match = re.search(r'(\d{4}\.\d{4,5})', arxiv_url)
            arxiv_id = arxiv_id_match.group(1) if arxiv_id_match else ""
            year = arxiv_id[:4] if arxiv_id else "20xx"

            papers_by_category[category_name].append({
                "title": title,
                "arxiv_url": arxiv_url,
                "code_link": code_link,
                "confidence": confidence,
                "year": year,
                "category": category_name,
            })

    return papers_by_category


def flatten_papers(papers_by_category: dict) -> list:
    """Flatten category dict to single list."""
    all_papers = []
    for category, papers in papers_by_category.items():
        all_papers.extend(papers)
    return all_papers


def export_csv(papers: list, output_path: str):
    """Export to CSV for Zotero."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Url", "Code Link", "Category", "Confidence", "Year"])
        writer.writeheader()
        for p in papers:
            writer.writerow({
                "Title": p["title"],
                "Url": p["arxiv_url"],
                "Code Link": p["code_link"],
                "Category": p.get("category", ""),
                "Confidence": p["confidence"],
                "Year": p["year"],
            })
    print(f"[export] CSV: {output_path}")


def export_bibtex(papers: list, output_path: str):
    """Export to BibTeX for Zotero."""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, p in enumerate(papers):
            # Generate citation key
            first_word = p["title"].split()[0].lower()
            first_word = re.sub(r'[^a-z]', '', first_word)
            key = f"{first_word}{p['year']}{i}"
            category = p.get("category", "")

            f.write(f"@article{{{key},\n")
            f.write(f"  title={{{p['title']}}},\n")
            f.write(f"  year={{{p['year']}}},\n")
            f.write(f"  journal={{arXiv preprint}},\n")
            f.write(f"  url={{{p['arxiv_url']}}},\n")
            f.write(f"  note={{Code: {p['code_link']}}},\n")
            if category:
                f.write(f"  keywords={{{category}}},\n")
            f.write("}\n\n")
    print(f"[export] BibTeX: {output_path}")


def export_ris(papers: list, output_path: str):
    """Export to RIS for Zotero."""
    with open(output_path, "w", encoding="utf-8") as f:
        for p in papers:
            category = p.get("category", "")
            f.write("TY  - EREP\n")
            f.write(f"TI  - {p['title']}\n")
            f.write(f"PY  - {p['year']}\n")
            f.write(f"DO  - {p['arxiv_url']}\n")
            f.write("M3  - preprint\n")
            f.write(f"UR  - {p['arxiv_url']}\n")
            f.write(f"L1  - {p['code_link']}\n")
            if category:
                f.write(f"KW  - {category}\n")
            f.write("ER  - \n\n")
    print(f"[export] RIS: {output_path}")


def export_by_category(papers_by_category: dict, output_dir: str, format: str):
    """Export each category to separate subdirectory for Zotero folder import."""
    for category, papers in papers_by_category.items():
        if not papers:
            continue

        # Create category subdirectory
        safe_name = re.sub(r'[^\w\-]', '_', category)
        category_dir = os.path.join(output_dir, safe_name)
        os.makedirs(category_dir, exist_ok=True)

        file_ext = format
        if format == "bib":
            file_ext = "bib"

        path = os.path.join(category_dir, f"{safe_name}.{file_ext}")

        if format == "csv":
            export_csv(papers, path)
        elif format == "bib":
            export_bibtex(papers, path)
        elif format == "ris":
            export_ris(papers, path)


def main():
    parser = argparse.ArgumentParser(description="Export README papers to Zotero formats")
    parser.add_argument("--by-category", action="store_true", help="Export each category as separate files")
    parser.add_argument("--format", choices=["csv", "bib", "ris"], default="ris", help="Export format")
    parser.add_argument("--keyword", type=str, help="Filter papers by keyword in title/abstract")
    parser.add_argument("--output-dir", type=str, default="exports", help="Output directory")
    args = parser.parse_args()

    readme_path = "README.md"
    output_dir = args.output_dir

    # Apply keyword filter if specified
    if args.keyword:
        papers_by_category = parse_readme_by_category(readme_path)
        keyword = args.keyword.lower()
        filtered = {}
        for category, papers in papers_by_category.items():
            filtered_papers = [
                p for p in papers
                if keyword in p["title"].lower()
            ]
            if filtered_papers:
                filtered[category] = filtered_papers
        papers_by_category = filtered
        # Use keyword as subdirectory when filtering
        safe_keyword = re.sub(r'[^\w\-]', '_', args.keyword)
        output_dir = os.path.join(output_dir, safe_keyword)
        print(f"[filter] Filtered by keyword: '{args.keyword}'")
    else:
        papers_by_category = parse_readme_by_category(readme_path)

    os.makedirs(output_dir, exist_ok=True)

    # Count total papers
    total = sum(len(p) for p in papers_by_category.values())
    print(f"[parse] Found {total} papers in {len(papers_by_category)} categories")

    if args.by_category:
        # Export each category to separate file
        export_by_category(papers_by_category, output_dir, args.format)
        print(f"[done] Exported by category to {output_dir}/")
    else:
        # Export all to single file (flattened)
        papers = flatten_papers(papers_by_category)
        base_name = os.path.splitext(os.path.basename(readme_path))[0]

        if args.format == "csv":
            export_csv(papers, os.path.join(output_dir, f"{base_name}_papers.csv"))
        elif args.format == "bib":
            export_bibtex(papers, os.path.join(output_dir, f"{base_name}_papers.bib"))
        else:
            export_ris(papers, os.path.join(output_dir, f"{base_name}_papers.ris"))

        print(f"[done] Exported {total} papers to {output_dir}/")


if __name__ == "__main__":
    main()