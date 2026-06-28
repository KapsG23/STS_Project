from __future__ import annotations

import unittest

from pipeline import SpeechToASLPipeline


class SpeechToASLPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.pipeline = SpeechToASLPipeline(merge_videos=False)

    def test_hospital_question_orders_question_last(self) -> None:
        result = self.pipeline.run_text("Where is the nearest hospital?")
        self.assertEqual(result.gloss, "HOSPITAL WHERE")
        self.assertTrue(any(asset.token == "hospital" and asset.asset_type == "video" for asset in result.assets))

    def test_known_phrase_handles_space_filename(self) -> None:
        result = self.pipeline.run_text("Thank you")
        self.assertEqual(result.gloss, "THANK YOU")
        self.assertTrue(any(asset.asset_type == "video" for asset in result.assets))

    def test_unknown_word_fingerspells(self) -> None:
        result = self.pipeline.run_text("xyz")
        self.assertEqual(result.gloss, "XYZ")
        self.assertEqual([asset.token for asset in result.assets], ["x", "y", "z"])

    def test_simple_sentence_keeps_content_sequence(self) -> None:
        result = self.pipeline.run_text("I want water")
        self.assertEqual(result.gloss, "I WANT WATER")

    def test_greeting_question_is_not_reduced_to_fine(self) -> None:
        result = self.pipeline.run_text("Hey, how are you?")
        self.assertEqual(result.gloss, "HELLO YOU HOW")

    def test_help_question_moves_how_to_end(self) -> None:
        result = self.pipeline.run_text("How can I help you?")
        self.assertEqual(result.gloss, "I HELP YOU HOW")


if __name__ == "__main__":
    unittest.main()
