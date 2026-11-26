import os
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.app import app, retrieve

client = TestClient(app)


class RunbookTest(unittest.TestCase):
    def test_ranked_fixtures(self):
        for question, source in [
            ("DNS lookup times out", "dns.md / Compare resolvers"),
            ("rising queue depth", "queue.md / Diagnose backlog"),
            ("replay failed records", "queue.md / Replay failed records"),
            ("intermittent packet loss", "wan.md / Packet loss"),
        ]:
            with self.subTest(question=question):
                self.assertEqual(retrieve(question)[0]["source"], source)

    def test_unknown(self):
        self.assertEqual(client.post("/ask", json={"question": "Pancake recipe?"}).json()["mode"], "abstain")

    def test_extract(self):
        with patch.dict(os.environ, ANSWER_MODE="extract"):
            result = client.post("/ask", json={"question": "DNS timeout"}).json()
            self.assertEqual(result["answer"], result["sources"][0]["excerpt"])

    def test_generation(self):
        source = "queue.md / Diagnose backlog"
        with patch.dict(os.environ, ANSWER_MODE="generate"), patch("src.app.generate") as model:
            model.return_value = {"answer": "Compare arrival and completion rates.", "citations": [source]}
            result = client.post("/ask", json={"question": "queue depth"}).json()
            self.assertEqual(result["sources"][0]["source"], source)
            model.return_value["citations"] = ["invented source"]
            self.assertEqual(client.post("/ask", json={"question": "queue depth"}).json()["mode"], "abstain")
            model.side_effect = TimeoutError()
            self.assertEqual(client.post("/ask", json={"question": "queue depth"}).status_code, 502)

    def test_invalid_input(self):
        self.assertEqual(client.post("/ask", json={"question": ""}).status_code, 422)
