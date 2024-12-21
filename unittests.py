import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import subprocess

from hw2 import get_commit_tree, generate_mermaid_code

class TestGitGraphGenerator(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_commit_tree(self, mock_run):
        # Настраиваем mock для успешного выполнения команды git log
        mock_run.return_value = MagicMock(returncode=0, stdout='commit_hash|commit_message|2023-12-20 12:00:00 +0000\n', stderr='')

        repo_path = '/path/to/repo'
        date = datetime(2023, 12, 19)

        result = get_commit_tree(repo_path, date)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['hash'], 'commit_hash')
        self.assertEqual(result[0]['message'], 'commit_message')

    @patch('subprocess.run')
    def test_get_commit_tree_no_commits(self, mock_run):
        # Настраиваем mock для случая, когда нет коммитов после заданной даты
        mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')

        repo_path = '/path/to/repo'
        date = datetime(2023, 12, 21)

        result = get_commit_tree(repo_path, date)

        self.assertEqual(result, [])

    def test_generate_mermaid_code(self):
        commit_info = [
            {'hash': 'commit_hash_1', 'message': 'First commit', 'files': ['file1.txt']},
            {'hash': 'commit_hash_2', 'message': 'Second commit', 'files': ['file2.txt']}
        ]

        mermaid_code = generate_mermaid_code(commit_info)

        expected_output = (
            "graph TD;\n"
            '    commit_["Second commit"]\n'
            '    file_file2_txt["file2.txt"]\n'
            '    commit_ --> file_file2_txt\n'
            '    commit_["First commit"]\n'
            '    commit_ --> commit_\n'
            '    file_file1_txt["file1.txt"]\n'
            '    commit_ --> file_file1_txt'
        )
        self.assertEqual(mermaid_code.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()
