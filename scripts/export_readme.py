#!/usr/bin/env python3
"""Parse README.md and export papers to Zotero-compatible formats."""

import csv
import re
import os
from pathlib import Path


def parse_readme_papers(readme_path: str) -> list:
    """Parse papers from README.md."""
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    papers = []
    # Pattern to match paper entries
    pattern = r'\* \*\*\[([^\]]+)\]\(([^\)]+)\)\*\* - \[Code\]\(([^\)]+)\)( \(confidence: (\w+)\))?'

    for match in re.finditer(pattern, content):
        title = match.group(1)
        arxiv_url = match.group(2)
        code_link = match.group(3)
        confidence = match.group(5) if match.group(5) else "medium"

        # Extract arXiv ID for year
        arxiv_id_match = re.search(r'(\d{4}\.\d{4,5})', arxiv_url)
        arxiv_id = arxiv_id_match.group(1) if arxiv_id_match else ""
        year = arxiv_id[:4] if arxiv_id else "20xx"

        papers.append({
            "title": title,
            "arxiv_url": arxiv_url,
            "code_link": code_link,
            "confidence": confidence,
            "year": year,
        })

    return papers


def export_csv(papers: list, output_path: str):
    """Export to CSV for Zotero."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Url", "Code Link", "Confidence", "Year"])
        writer.writeheader()
        for p in papers:
            writer.writerow({
                "Title": p["title"],
                "Url": p["arxiv_url"],
                "Code Link": p["code_link"],
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

            f.write(f"@article{{{key},\n")
            f.write(f"  title={{{p['title']}}},\n")
            f.write(f"  year={{{p['year']}}},\n")
            f.write(f"  journal={{arXiv preprint}},\n")
            f.write(f"  url={{{p['arxiv_url']}}},\n")
            f.write(f"  note={{Code: {p['code_link']}}},\n")
            f.write("}\n\n")
    print(f"[export] BibTeX: {output_path}")


def export_ris(papers: list, output_path: str):
    """Export to RIS for Zotero."""
    with open(output_path, "w", encoding="utf-8") as f:
        for p in papers:
            f.write("TY  - EREP\n")
            f.write(f"TI  - {p['title']}\n")
            f.write(f"PY  - {p['year']}\n")
            f.write(f"DO  - {p['arxiv_url']}\n")
            f.write("M3  - preprint\n")
            f.write(f"UR  - {p['arxiv_url']}\n")
            f.write(f"L1  - {p['code_link']}\n")
            f.write("ER  - \n\n")
    print(f"[export] RIS: {output_path}")


def main():
    readme_path = "README.md"
    output_dir = "exports"
    os.makedirs(output_dir, exist_ok=True)

    papers = parse_readme_papers(readme_path)
    print(f"[parse] Found {len(papers)} papers in README.md")

    base_name = os.path.splitext(os.path.basename(readme_path))[0]
    export_csv(papers, os.path.join(output_dir, f"{base_name}_papers.csv"))
    export_bibtex(papers, os.path.join(output_dir, f"{base_name}_papers.bib"))
    export_ris(papers, os.path.join(output_dir, f"{base_name}_papers.ris"))

    print(f"[done] Exported {len(papers)} papers to {output_dir}/")


if __name__ == "__main__":
    main()