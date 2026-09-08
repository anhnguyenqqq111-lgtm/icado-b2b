import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "workspace.py"
SPEC = importlib.util.spec_from_file_location("workspace_cli", SCRIPT)
workspace = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(workspace)


CONFIG = {
    "workflows": {"standard": {"required": ["article.md", "audit-report.md"]}},
}


class TopicValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.old_root = workspace.ROOT
        workspace.ROOT = Path(self.temp.name)
        self.addCleanup(setattr, workspace, "ROOT", self.old_root)
        self.topic = workspace.ROOT / "clients" / "Acme" / "brands" / "Brand" / "keywords" / "topic"
        self.topic.mkdir(parents=True)

    def write_manifest(self, status="backlog", artifacts=""):
        (self.topic / "topic.toml").write_text(
            'schema_version = 1\n'
            'id = "Acme/Brand/topic"\n'
            'client = "Acme"\nbrand = "Brand"\nslug = "topic"\n'
            'workflow = "standard"\n'
            f'status = "{status}"\n\n[artifacts]\n{artifacts}',
            encoding="utf-8",
        )

    def test_missing_manifest_is_error(self):
        errors, warnings = workspace.validate_topic(self.topic, CONFIG)
        self.assertEqual(1, len(errors))
        self.assertEqual([], warnings)

    def test_backlog_missing_artifacts_is_warning(self):
        self.write_manifest()
        errors, warnings = workspace.validate_topic(self.topic, CONFIG)
        self.assertEqual([], errors)
        self.assertEqual(1, len(warnings))

    def test_review_missing_artifacts_is_error(self):
        self.write_manifest(status="review")
        errors, _ = workspace.validate_topic(self.topic, CONFIG)
        self.assertEqual(1, len(errors))

    def test_complete_review_is_valid(self):
        (self.topic / "article.md").write_text("article", encoding="utf-8")
        (self.topic / "audit-report.md").write_text("audit", encoding="utf-8")
        self.write_manifest(
            status="review",
            artifacts='article = "article.md"\naudit_report = "audit-report.md"\n',
        )
        errors, warnings = workspace.validate_topic(self.topic, CONFIG)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)


if __name__ == "__main__":
    unittest.main()
