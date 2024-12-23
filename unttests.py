import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
from emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        # Создание конфигурации для тестов
        with open("config.json", 'r') as config_file:
            config = json.load(config_file)
        
        self.emulator = ShellEmulator(config)

    @patch('zipfile.ZipFile.namelist', return_value=['file1.txt', 'file2.txt'])
    @patch('zipfile.ZipFile.extractall')
    def test_load_virtual_fs(self, mock_extractall, mock_namelist):
        self.emulator.load_virtual_fs()
        self.assertEqual(self.emulator.virtual_fs.namelist(), ['file1.txt', 'file2.txt'])

    @patch('zipfile.ZipFile.namelist', return_value=['file1.txt', 'file2.txt'])
    def test_list_files(self, mock_namelist):
        with patch('builtins.print') as mock_print:
            self.emulator.list_files()


    def test_change_directory(self):
        self.emulator.current_path = "/"
        self.emulator.change_directory("folder")
        self.assertEqual(self.emulator.current_path, "/")

    @patch('zipfile.ZipFile.namelist', return_value=['folder/file1.txt'])
    def test_change_directory_not_found(self, mock_namelist):
        with patch('builtins.print') as mock_print:
            self.emulator.change_directory("nonexistent")
            mock_print.assert_called_with("Директория не найдена.")

    def test_print_working_directory(self):
        with patch('builtins.print') as mock_print:
            self.emulator.print_working_directory()
            mock_print.assert_called_with("/")

    @patch('subprocess.call')
    def test_clear_screen(self, mock_call):
        self.emulator.clear_screen()
        mock_call.assert_called_once()

    @patch('builtins.print')
    def test_uname(self, mock_print):
        self.emulator.uname()
        mock_print.assert_called_with("UNIX-like Shell Emulator")

    @patch('builtins.open', new_callable=mock_open, read_data="ls\ncd folder")
    def test_execute_startup_script(self, mock_file):
        self.emulator.execute_startup_script()
        # Проверяем выполнение команд в скрипте
        # Здесь вы можете проверить вызовы методов или их эффекты

    def test_exit_shell(self):
        with patch('sys.exit') as mock_exit:
            self.emulator.exit_shell()
            mock_exit.assert_called_once()

    def test_show_history(self):
        self.emulator.history = ["ls", "pwd", "cd folder"]
        with patch('builtins.print') as mock_print:
            self.emulator.show_history()
            mock_print.assert_called_with("ls\npwd\ncd folder")

if __name__ == '__main__':
    unittest.main()
