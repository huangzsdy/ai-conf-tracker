import datetime
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location("update_papers", "scripts/update_papers.py")
update_papers = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = update_papers
SPEC.loader.exec_module(update_papers)


class UpdatePapersTests(unittest.TestCase):
    def test_target_filter_strict_requires_explicit_2026(self):
        text = "Submitted to MICCAI. Code: https://github.com/a/b"
        self.assertFalse(
            update_papers.is_target_miccai_paper(
                text, "https://arxiv.org/abs/2604.12345v1", "strict", "miccai-2026"
            )
        )

    def test_target_filter_broad_accepts_miccai_on_2026_arxiv_id(self):
        text = "Submitted to MICCAI. Code: https://github.com/a/b"
        self.assertTrue(
            update_papers.is_target_miccai_paper(
                text, "https://arxiv.org/abs/2604.12345v1", "broad", "miccai-2026"
            )
        )

    def test_target_filter_broad_rejects_explicit_2025(self):
        text = "Accepted at MICCAI 2025. Code: https://github.com/a/b"
        self.assertFalse(
            update_papers.is_target_miccai_paper(
                text, "https://arxiv.org/abs/2604.12345v1", "broad", "miccai-2026"
            )
        )

    def test_target_filter_broad_rejects_explicit_2024(self):
        text = "Accepted at MICCAI 2024. Code: https://github.com/a/b"
        self.assertFalse(
            update_papers.is_target_miccai_paper(
                text, "https://arxiv.org/abs/2604.12345v1", "broad", "miccai-2026"
            )
        )

    def test_target_filter_all_years_broad_accepts_miccai_without_year(self):
        text = "Submitted to MICCAI with code: https://github.com/a/b"
        self.assertTrue(
            update_papers.is_target_miccai_paper(
                text, "https://arxiv.org/abs/2404.12345v1", "broad", "miccai-all-years"
            )
        )

    def test_extract_arxiv_year_supports_legacy_ids(self):
        self.assertEqual(update_papers._extract_arxiv_year("https://arxiv.org/abs/cs/0601001"), 6)

    def test_track_filter(self):
        self.assertTrue(update_papers.track_matches("all", "workshops"))
        self.assertTrue(update_papers.track_matches("workshops", "workshops"))
        self.assertFalse(update_papers.track_matches("main", "challenges"))

    def test_normalize_repository_url_handles_malformed_concat(self):
        url = "https://github.com/user/repo}{https://github.com/other/repo"
        normalized = update_papers.normalize_repository_url(url)
        self.assertIsNotNone(normalized)
        canonical, key = normalized
        self.assertEqual(canonical, "https://github.com/user/repo")
        self.assertEqual(key, ("github.com", "user", "repo"))

    def test_categorize_paper_reduces_weak_false_positives(self):
        title = "One-Step Video Generation via Latent Flow Matching"
        abstract = (
            "Generative models can help with reconstruction. "
            "Diagnosis is discussed as future work and mask tokens are used in pretraining."
        )
        categories = update_papers.categorize_paper(title, abstract)
        self.assertIn("Generative Models", categories)
        self.assertIn("Reconstruction", categories)
        self.assertNotIn("Segmentation", categories)

    def test_category_confidence(self):
        scores = update_papers.score_categories(
            "Diffusion model for segmentation",
            "This segmentation method uses diffusion and segmentation losses.",
        )
        categories = update_papers.categorize_paper(
            "Diffusion model for segmentation",
            "This segmentation method uses diffusion and segmentation losses.",
        )
        confidence = update_papers.get_category_confidence(scores, categories)
        self.assertIn("Segmentation", confidence)
        self.assertIn(confidence["Segmentation"], {"high", "medium"})

    def test_validate_papers_data_rejects_bad_and_dedupes(self):
        papers = [
            {
                "title": "Good",
                "arxiv_url": "https://arxiv.org/abs/2601.12345v1",
                "repo_links": ["https://github.com/foo/bar", "https://github.com/foo/bar"],
                "summary": "generative diffusion",
                "published": datetime.datetime(2026, 1, 1),
            },
            {
                "title": "Good",
                "arxiv_url": "https://arxiv.org/abs/2601.12345v1",
                "repo_links": ["https://github.com/foo/bar"],
                "summary": "generative diffusion",
                "published": datetime.datetime(2026, 1, 1),
            },
            {
                "title": "Bad",
                "arxiv_url": "https://arxiv.org/abs/not-valid",
                "repo_links": ["https://github.com/foo/bar"],
                "summary": "",
                "published": datetime.datetime(2026, 1, 1),
            },
        ]

        deduped, rejected, uncertain = update_papers.validate_papers_data(papers)
        self.assertEqual(deduped, 1)
        self.assertEqual(rejected, 1)
        self.assertEqual(uncertain, 0)
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["repo_links"], ["https://github.com/foo/bar"])

    def test_update_readme_rewrites_all_blocks(self):
        readme_template = """
**Conference Scope**: miccai-2026
**Discovery Mode**: strict
<!-- BEGIN COVERAGE_REPORT -->
old coverage
<!-- END COVERAGE_REPORT -->
<!-- BEGIN SEGMENTATION_PAPERS -->
* stale
<!-- END SEGMENTATION_PAPERS -->
<!-- BEGIN RECONSTRUCTION_PAPERS -->
* stale
<!-- END RECONSTRUCTION_PAPERS -->
<!-- BEGIN CLASSIFICATION_PAPERS -->
* stale
<!-- END CLASSIFICATION_PAPERS -->
<!-- BEGIN IMAGE_REGISTRATION_PAPERS -->
* stale
<!-- END IMAGE_REGISTRATION_PAPERS -->
<!-- BEGIN DOMAIN_ADAPTATION_PAPERS -->
* stale
<!-- END DOMAIN_ADAPTATION_PAPERS -->
<!-- BEGIN GENERATIVE_MODELS_PAPERS -->
* stale
<!-- END GENERATIVE_MODELS_PAPERS -->
<!-- BEGIN GENERAL_PAPERS -->
* stale
<!-- END GENERAL_PAPERS -->
**Last Updated**: old
""".strip()

        papers = [
            {
                "title": "Paper",
                "arxiv_url": "https://arxiv.org/abs/2601.11111v1",
                "repo_links": ["https://github.com/foo/bar"],
                "categories": ["General"],
                "published": datetime.datetime(2026, 1, 1),
            }
        ]

        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "README.md"
            readme.write_text(readme_template, encoding="utf-8")
            stats = {
                "fetched_records": 1,
                "unique_arxiv_records": 1,
                "without_code_links": 0,
                "filtered_non_target": 0,
                "filtered_track": 0,
                "accepted_records": 1,
            }
            counts = update_papers.update_readme(
                papers,
                stats,
                "miccai-2026",
                "strict",
                "all",
                str(readme),
            )
            content = readme.read_text(encoding="utf-8")

        self.assertEqual(counts["General"], 1)
        self.assertNotIn("* stale", content)
        self.assertIn("[Paper](https://arxiv.org/abs/2601.11111v1)", content)
        self.assertIn("Conference scope: `miccai-2026`", content)


if __name__ == "__main__":
    unittest.main()
