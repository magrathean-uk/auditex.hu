import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relpath: str) -> str:
    return (ROOT / relpath).read_text(encoding="utf-8")


class AuditexSiteTests(unittest.TestCase):
    def test_home_is_plain_github_first_product_page(self) -> None:
        home = read("index.html")
        for text in [
            "Auditex",
            "https://github.com/magrathean-uk/auditex",
            "Microsoft 365",
            "Google Workspace",
            "Read-only",
            "No content reads",
            "Local raw evidence",
            "MCP-ready report packs",
        ]:
            self.assertIn(text, home)
        lowered = home.lower()
        self.assertIn("not certification", lowered)
        self.assertIn("not legal advice", lowered)
        self.assertIn("not guaranteed security", lowered)
        self.assertNotIn("GitHub is the source of truth", home)
        self.assertNotIn("Open GitHub", home)
        self.assertNotIn("Plain product page", home)
        self.assertNotRegex(home, r'<nav class="footer-links"[^>]*>\\s*<a href="https://github.com/magrathean-uk/auditex">GitHub</a>')
        self.assertNotIn('aria-label="Primary navigation"', home)

    def test_home_has_no_reference_repo_content_screenshots_or_pills(self) -> None:
        home = read("index.html")
        css = read("assets/auditex-plain-v2.css")
        for forbidden in [
            "AppNest",
            "app-screen.png",
            "desktop.png",
            "Instagram",
            "pricing",
            "testimonial",
            "Download Now",
            "Ready to Transform Your Experience",
            "$9",
            "app-hero",
            "audit-panel",
            "panel-bar",
            "source-box",
        ]:
            self.assertNotIn(forbidden, home)

        self.assertNotRegex(home, r'<img[^>]+(app-screen|desktop|screenshot)')
        self.assertNotIn(">Releases<", home)
        self.assertNotIn("border-radius: 999", css)
        self.assertNotIn("border-radius: 50%", css)
        self.assertNotIn("min-height: 70vh", css)
        self.assertNotIn("radial-gradient", css)

    def test_home_has_software_schema_and_social_metadata(self) -> None:
        home = read("index.html")
        self.assertIn('property="og:title"', home)
        self.assertIn('property="og:description"', home)
        self.assertIn('property="og:type"', home)
        self.assertIn('name="twitter:card"', home)
        self.assertIn('"@type":"SoftwareApplication"', home.replace(" ", ""))

    def test_required_public_pages_exist(self) -> None:
        for relpath in [
            "privacy/index.html",
            "terms/index.html",
        ]:
            self.assertTrue((ROOT / relpath).exists(), relpath)

    def test_supporting_seo_files_exist(self) -> None:
        self.assertTrue((ROOT / "robots.txt").exists())
        self.assertTrue((ROOT / "sitemap.xml").exists())
        sitemap = read("sitemap.xml")
        self.assertIn("https://auditex.hu/", sitemap)
        self.assertIn("https://auditex.hu/privacy/", sitemap)
        self.assertIn("https://auditex.hu/terms/", sitemap)

    def test_shared_stylesheet_and_accessibility_hooks_exist(self) -> None:
        home = read("index.html")
        self.assertIn("/assets/auditex-plain-v2.css", home)
        self.assertIn("Skip to content", home)
        self.assertIn("prefers-reduced-motion", read("assets/auditex-plain-v2.css"))
        self.assertIn(":focus-visible", read("assets/auditex-plain-v2.css"))

    def test_footer_has_magrathean_branding(self) -> None:
        home = read("index.html")
        css = read("assets/auditex-plain-v2.css")
        self.assertIn("/assets/magrathean-mark.svg", home)
        self.assertIn("Copyright 2026 Magrathean UK Ltd.", home)
        self.assertIn("Auditex is a trademark of Magrathean UK Ltd.", home)
        self.assertIn('href="mailto:contact@magrathean.uk"', home)
        self.assertRegex(css, r"\.brand-logo \{[^}]*width: 3\.25rem;[^}]*height: 3\.25rem;", re.DOTALL)
        self.assertRegex(css, r"\.site-footer \.brand-logo \{[^}]*width: 2rem;[^}]*height: 2rem;", re.DOTALL)
        self.assertRegex(css, r"\.copyright img \{[^}]*width: 2rem;[^}]*height: 2rem;", re.DOTALL)

    def test_legal_pages_have_contents_navigation(self) -> None:
        privacy = read("privacy/index.html")
        terms = read("terms/index.html")
        self.assertIn("Contents", privacy)
        self.assertIn("Contents", terms)
        self.assertRegex(privacy, r'href="#[^"]+"')
        self.assertRegex(terms, r'href="#[^"]+"')


if __name__ == "__main__":
    unittest.main()
