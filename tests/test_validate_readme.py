import importlib.util
import sys
import unittest


SPEC = importlib.util.spec_from_file_location("validate_readme", "scripts/validate_readme.py")
validate_readme = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = validate_readme
SPEC.loader.exec_module(validate_readme)


def _build_readme(segmentation_body: str, segmentation_count: int = 1) -> str:
    return f"""
**Conference Scope**: miccai-2026
**Discovery Mode**: strict
<!-- BEGIN COVERAGE_REPORT -->
- Conference scope: `miccai-2026`
- Discovery mode: `strict`
- Tracks: `all`
- Total code-backed papers: `{segmentation_count}`
- Fetched arXiv records: `1`
- Unique arXiv records: `1`
- Filtered (non-target): `0`
- Filtered (track): `0`
- Filtered (no code links): `0`

| Category | Count | Gap to 1000 |
|---|---:|---:|
| Segmentation | {segmentation_count} | {max(0, 1000-segmentation_count)} |
| Reconstruction | 0 | 1000 |
| Classification | 0 | 1000 |
| Image Registration | 0 | 1000 |
| Domain Adaptation | 0 | 1000 |
| Generative Models | 0 | 1000 |
| General | 0 | 1000 |
<!-- END COVERAGE_REPORT -->
<!-- BEGIN SEGMENTATION_PAPERS -->
{segmentation_body}
<!-- END SEGMENTATION_PAPERS -->
<!-- BEGIN RECONSTRUCTION_PAPERS -->
<!-- END RECONSTRUCTION_PAPERS -->
<!-- BEGIN CLASSIFICATION_PAPERS -->
<!-- END CLASSIFICATION_PAPERS -->
<!-- BEGIN IMAGE_REGISTRATION_PAPERS -->
<!-- END IMAGE_REGISTRATION_PAPERS -->
<!-- BEGIN DOMAIN_ADAPTATION_PAPERS -->
<!-- END DOMAIN_ADAPTATION_PAPERS -->
<!-- BEGIN GENERATIVE_MODELS_PAPERS -->
<!-- END GENERATIVE_MODELS_PAPERS -->
<!-- BEGIN GENERAL_PAPERS -->
<!-- END GENERAL_PAPERS -->
""".strip()


class ValidateReadmeTests(unittest.TestCase):
    def test_valid_readme_passes(self):
        readme = _build_readme(
            "* **[Paper](https://arxiv.org/abs/2601.12345v1)** - [Code](https://github.com/foo/bar) (confidence: high)"
        )
        errors = validate_readme.validate_readme_text(readme)
        self.assertEqual(errors, [])

    def test_malformed_code_link_fails(self):
        readme = _build_readme(
            "* **[Paper](https://arxiv.org/abs/2601.12345v1)** - "
            "[Code](https://github.com/foo/bar}{https://github.com/foo/bar) (confidence: high)"
        )
        errors = validate_readme.validate_readme_text(readme)
        self.assertTrue(any("invalid or unsupported code URL" in error for error in errors))

    def test_unsupported_host_fails(self):
        readme = _build_readme(
            "* **[Paper](https://arxiv.org/abs/2601.12345v1)** - [Code](https://example.com/foo/bar) (confidence: high)"
        )
        errors = validate_readme.validate_readme_text(readme)
        self.assertTrue(any("invalid or unsupported code URL" in error for error in errors))

    def test_duplicate_arxiv_in_same_category_fails(self):
        readme = _build_readme(
            "\n".join(
                [
                    "* **[Paper A](https://arxiv.org/abs/2601.12345v1)** - [Code](https://github.com/foo/bar) (confidence: high)",
                    "* **[Paper A](https://arxiv.org/abs/2601.12345v1)** - [Code](https://github.com/foo/baz) (confidence: medium)",
                ]
            ),
            segmentation_count=2,
        )
        errors = validate_readme.validate_readme_text(readme)
        self.assertTrue(any("duplicate arXiv entry" in error for error in errors))

    def test_coverage_mismatch_fails(self):
        readme = _build_readme(
            "* **[Paper](https://arxiv.org/abs/2601.12345v1)** - [Code](https://github.com/foo/bar) (confidence: high)",
            segmentation_count=0,
        )
        errors = validate_readme.validate_readme_text(readme)
        self.assertTrue(any("Coverage count mismatch" in error for error in errors))

    def test_missing_confidence_fails(self):
        readme = _build_readme(
            "* **[Paper](https://arxiv.org/abs/2601.12345v1)** - [Code](https://github.com/foo/bar)",
            segmentation_count=1,
        )
        errors = validate_readme.validate_readme_text(readme)
        self.assertTrue(any("missing confidence tag" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
