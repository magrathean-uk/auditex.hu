import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


class AuditexSiteTests(unittest.TestCase):
    def test_home_is_simple_open_source_landing(self) -> None:
        home = read("index.html")
        self.assertIn("Open-source", home)
        self.assertIn("GitHub", home)
        self.assertNotIn("Read docs", home)
        self.assertNotIn("View sample pack", home)
        self.assertNotIn("trust-pill", home)
        self.assertNotIn("hero-badge", home)
        self.assertNotIn("First screen answer", home)
        self.assertNotIn("Static-site path from first read to first run.", home)
        lowered = home.lower()
        self.assertIn("not certification", lowered)
        self.assertIn("not legal advice", lowered)
        self.assertIn("not guaranteed security", lowered)

    def test_home_has_software_schema_and_social_metadata(self) -> None:
        home = read("index.html")
        self.assertIn('property="og:title"', home)
        self.assertIn('property="og:description"', home)
        self.assertIn('property="og:type"', home)
        self.assertIn('name="twitter:card"', home)
        self.assertIn('"@type":"SoftwareApplication"', home.replace(" ", ""))

    def test_docs_download_and_proof_pages_exist(self) -> None:
        for relpath in [
            "proof/index.html",
            "docs/index.html",
            "docs/quickstart/index.html",
            "docs/provider-coverage/index.html",
            "docs/bundle-anatomy/index.html",
            "docs/mcp-report-packs/index.html",
            "download/index.html",
            "sample-pack/index.html",
        ]:
            self.assertTrue((ROOT / relpath).exists(), relpath)

    def test_docs_hub_links_main_workflows(self) -> None:
        docs = read("docs/index.html")
        self.assertIn("/docs/quickstart/", docs)
        self.assertIn("/docs/provider-coverage/", docs)
        self.assertIn("/docs/bundle-anatomy/", docs)
        self.assertIn("/docs/mcp-report-packs/", docs)
        self.assertIn("/download/", docs)

    def test_quickstart_has_faq_schema(self) -> None:
        quickstart = read("docs/quickstart/index.html")
        self.assertIn('"@type":"FAQPage"', quickstart.replace(" ", ""))
        self.assertIn("First run", quickstart)
        self.assertIn("read-only", quickstart.lower())

    def test_supporting_seo_files_exist(self) -> None:
        self.assertTrue((ROOT / "robots.txt").exists())
        self.assertTrue((ROOT / "sitemap.xml").exists())

    def test_shared_stylesheet_and_accessibility_hooks_exist(self) -> None:
        home = read("index.html")
        self.assertIn("/assets/site.css", home)
        self.assertIn("Skip to content", home)
        self.assertIn("prefers-reduced-motion", read("assets/site.css"))
        self.assertIn(":focus-visible", read("assets/site.css"))

    def test_legal_pages_have_contents_navigation(self) -> None:
        privacy = read("privacy/index.html")
        terms = read("terms/index.html")
        self.assertIn("Contents", privacy)
        self.assertIn("Contents", terms)
        self.assertRegex(privacy, r'href="#[^"]+"')
        self.assertRegex(terms, r'href="#[^"]+"')


if __name__ == "__main__":
    unittest.main()
