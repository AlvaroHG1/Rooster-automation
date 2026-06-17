import email.message
import unittest
from contextlib import contextmanager

from app.services.gmail_monitor import GmailMonitor


class FakeMail:
    def __init__(self, message_bytes):
        self.message_bytes = message_bytes

    def select(self, mailbox):
        self.selected_mailbox = mailbox

    def search(self, charset, criteria):
        return "OK", [b"42"]

    def fetch(self, uid, query):
        return "OK", [(None, self.message_bytes)]


class TestGmailMonitor(unittest.TestCase):
    def test_first_check_processes_existing_trigger_email(self):
        msg = email.message.EmailMessage()
        msg["Subject"] = "Nieuw rooster gepubliceerd"
        msg.set_content("Het rooster voor week 26 is gepubliceerd.")

        fake_mail = FakeMail(msg.as_bytes())
        monitor = GmailMonitor()

        @contextmanager
        def fake_connect(timeout=10):
            yield fake_mail

        monitor.connect = fake_connect

        result = monitor.check_for_trigger_email()

        self.assertTrue(result["found"])
        self.assertEqual(result["week"], 26)
        self.assertEqual(result["uid"], b"42")
        self.assertEqual(monitor.last_checked_uid, b"42")


if __name__ == "__main__":
    unittest.main()
