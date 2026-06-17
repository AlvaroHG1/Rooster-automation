import os
import shutil
import subprocess
import sys
from pathlib import Path
import unittest
from unittest.mock import patch

from app.core.settings import Settings


class TestSettings(unittest.TestCase):
    def test_gmail_app_password_removes_display_grouping_spaces(self):
        env = {
            "ROI_EMAIL": "roi@example.com",
            "ROI_PASSWORD": "roi-password",
            "GMAIL_ADDRESS": "gmail@example.com",
            "GMAIL_APP_PASSWORD": "abcd efgh ijkl mnop",
            "CALDAV_URL": "https://caldav.example.com",
            "CALDAV_USERNAME": "caldav@example.com",
            "CALDAV_PASSWORD": "caldav-password",
        }

        with patch.dict(os.environ, env, clear=True):
            settings = Settings.load()

        self.assertEqual(settings.gmail.app_password, "abcdefghijklmnop")

    def test_app_main_loads_dotenv_before_settings_are_created(self):
        repo_dir = Path(__file__).resolve().parent.parent
        env_content = "\n".join(
            [
                "ROI_EMAIL=roi@example.com",
                "ROI_PASSWORD=roi-password",
                "GMAIL_ADDRESS=from-file@example.com",
                "GMAIL_APP_PASSWORD=abcd efgh ijkl mnop",
                "CALDAV_URL=https://caldav.example.com",
                "CALDAV_USERNAME=caldav@example.com",
                "CALDAV_PASSWORD=caldav-password",
            ]
        )

        tmp_dir = repo_dir / ".tmp-settings-env-test"
        shutil.rmtree(tmp_dir, ignore_errors=True)
        tmp_dir.mkdir()
        try:
            Path(tmp_dir, ".env").write_text(env_content, encoding="utf-8")
            env = os.environ.copy()
            for key in [
                "ROI_EMAIL",
                "ROI_PASSWORD",
                "GMAIL_ADDRESS",
                "GMAIL_APP_PASSWORD",
                "CALDAV_URL",
                "CALDAV_USERNAME",
                "CALDAV_PASSWORD",
            ]:
                env.pop(key, None)
            env["PYTHONPATH"] = str(repo_dir)

            result = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "import app.main; from app.core.settings import settings; print(settings.gmail.address)",
                ],
                cwd=tmp_dir,
                env=env,
                text=True,
                capture_output=True,
                check=True,
            )
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

        self.assertEqual(result.stdout.strip(), "from-file@example.com")


if __name__ == "__main__":
    unittest.main()
