import unittest
from app import split_facts, score, terms, choose_evidence

class CoreTests(unittest.TestCase):
    def test_sentence_split(self):
        self.assertGreaterEqual(len(split_facts("The library opens at nine. Students can borrow books.")), 2)
    def test_relevant_terms_score(self):
        value, matched = score("library opening time", "The library opening time is nine in the morning.")
        self.assertGreater(value, 0)
        self.assertIn("library", matched)
    def test_empty_terms(self):
        self.assertEqual(score("the and", "of the and"), (0.0, []))
    def test_rejects_weak_matches(self):
        rows = [{"filename":"test.txt", "content":"The library is open at nine in the morning."}]
        self.assertEqual(choose_evidence("What is the student cafeteria menu?", rows), [])
    def test_selects_focused_statement(self):
        rows = [
            {"filename":"test.txt", "content":"The library opens at nine in the morning."},
            {"filename":"test.txt", "content":"The student cafeteria serves lunch at noon."},
            {"filename":"test.txt", "content":"The library has a reading room."}
        ]
        found = choose_evidence("When does the library open?", rows)
        self.assertTrue(found)
        self.assertLessEqual(len(found), 2)
        self.assertIn("library", found[0][3].lower())

if __name__ == "__main__":
    unittest.main()
