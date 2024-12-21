import os
import zipfile
import sys
import argparse
import json
import shutil
import subprocess

class ShellEmulator:
    def __init__(self, config):
        self.current_path = "/"
        self.history = []
        self.username = config['username']
        self.virtual_fs_path = config['virtual_fs']
        self.startup_script = config['startup_script']
        self.virtual_fs = None

        self.load_virtual_fs()
        self.execute_startup_script()

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Запуск эмулятора командной строки vshell.')
        parser.add_argument('config', type=str, help='Путь к конфигурационному файлу в формате JSON.')
        
        args = parser.parse_args()
        
        if not os.path.exists(args.config):
            parser.error(f"Файл конфигурации '{args.config}' не найден.")
        
        return args

    def load_virtual_fs(self):
        if not os.path.exists(self.virtual_fs_path):
            print("Ошибка: Файл виртуальной файловой системы не найден.")
            sys.exit(1)

        # Open the zip archive and create a directory for the virtual file system
        self.virtual_fs = zipfile.ZipFile(self.virtual_fs_path, 'r')
        self.virtual_fs.extractall("virtual_fs")

    def execute_startup_script(self):
        if os.path.exists(self.startup_script):
            with open(self.startup_script, 'r') as script_file:
                for command in script_file:
                    self.execute_command(command.strip())

    def list_files(self):
        path = f"virtual_fs{self.current_path}"
        try:
            files = os.listdir(path)
            if files:
                print("\n".join(files))
            else:
                print("Пустая директория")
        except FileNotFoundError:
            print("Директория не найдена")

    def change_directory(self, path):
        if path == "..":
            if self.current_path != "/":
                self.current_path = os.path.dirname(self.current_path) or "/"
            else:
                print("Вы находитесь в корневой директории.")
        else:
            new_path = os.path.join(f"virtual_fs{self.current_path}", path)
            if os.path.isdir(new_path):
                self.current_path = os.path.join(self.current_path, path)
            else:
                print("Директория не найдена.")

    def print_working_directory(self):
        print(f"{self.username}:{self.current_path}")

    def clear_screen(self):
        subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

    def uname(self):
        print("Windows") 

    def exit_shell(self):
        print("Выход из эмулятора.")
        sys.exit(0)

    def execute_command(self, command):
        self.history.append(command)

        command_dict = {
            "ls": self.list_files,
            "cd": lambda path: self.change_directory(path),
            "pwd": self.print_working_directory,
            "clear": self.clear_screen,
            "uname": self.uname,
            "exit": self.exit_shell,
            "history": self.show_history
        }

        parts = command.split()
        cmd_func = command_dict.get(parts[0])

        if cmd_func:
            if parts[0] == "cd":
                cmd_func(parts[1]) if len(parts) > 1 else print("Нужен аргумент для команды cd.")
            else:
                cmd_func()
        else:
            print(f"{self.username}: команда не найдена")

    def show_history(self):
        if self.history:
            print("\n".join(self.history))
        else:
            print("История пуста.")

if __name__ == "__main__":
    args = ShellEmulator.parse_arguments()
    
    with open(args.config, 'r') as config_file:
        config = json.load(config_file)
    
    emulator = ShellEmulator(config)

    while True:
        try:
            command = input(f"{config['username']}:{emulator.current_path} $ ")
            emulator.execute_command(command.strip())
        except EOFError:
            emulator.exit_shell()
