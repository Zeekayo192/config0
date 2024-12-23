import unittest
from datetime import datetime, timezone
from unittest.mock import patch, mock_open, MagicMock
import os
import zlib
from hw2 import read_git_object, parse_commit_object, parse_tree_object, generate_mermaid_code

class TestGitGraph(unittest.TestCase):

    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=zlib.compress(b"commit 172\x00tree abcdef1234567890abcdef1234567890abcdef12\nparent fedcba9876543210fedcba9876543210fedcba98\nauthor John Doe <john@example.com> 1695478495 +0000\n\nInitial commit\n"))
    def test_read_git_object(self, mock_file, mock_isfile):
        repo_path = "/fake/repo"
        obj_hash = "abcdef1234567890abcdef1234567890abcdef12"
        obj_type, content = read_git_object(repo_path, obj_hash)
        self.assertEqual(obj_type, "commit")
        self.assertIn(b"Initial commit", content)

    def test_parse_commit_object(self):
        data = b"tree abcdef1234567890abcdef1234567890abcdef12\nparent fedcba9876543210fedcba9876543210fedcba98\nauthor John Doe <john@example.com> 1695478495 +0000\n\nInitial commit\n"
        result = parse_commit_object(data)
        self.assertEqual(result['parent'], "fedcba9876543210fedcba9876543210fedcba98")
        self.assertEqual(result['message'], "Initial commit")
        self.assertEqual(result['date'], datetime.fromtimestamp(1695478495, timezone.utc))

    def test_parse_tree_object(self):
        data = b"100644 file1.txt\x00" + b"1234567890abcdef1234" + b"100644 file2.txt\x00" + b"abcdef1234567890abcd"
        result = parse_tree_object(data)
        self.assertEqual(result, ["file1.txt", "file2.txt"])

    def test_generate_mermaid_code(self):
        graph = {
            "abcdef1": {
                "message": "Initial commit",
                "parent": None,
                "files": ["file1.txt", "file2.txt"]
            },
            "1234567": {
                "message": "Second commit",
                "parent": "abcdef1",
                "files": ["file3.txt"]
            }
        }
        result = generate_mermaid_code(graph)
        self.assertIn("abcdef1[\"abcdef1<br>Initial commit<br>file1.txt<br>file2.txt\"]", result)
        self.assertIn("1234567[\"1234567<br>Second commit<br>file3.txt\"]", result)
        self.assertIn("abcdef1 --> 1234567", result)

if __name__ == "__main__":
    unittest.main()
