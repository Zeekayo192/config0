import subprocess
import os
import sys
from datetime import datetime
import argparse

def get_commit_tree(repo_path, date):
    result = subprocess.run(
        ['git', '-C', repo_path, 'log', '--pretty=format:%H|%s|%ci', '--name-only'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    
    if result.returncode != 0:
        print("Ошибка при получении коммитов:", result.stderr)
        return []

    commits = result.stdout.splitlines()
    commit_info = []

    for line in commits:
        if line.strip():  # если строка не пустая
            parts = line.split('|')
            if len(parts) >= 3:
                commit_hash = parts[0].strip()
                commit_message = parts[1].strip()
                commit_date = parts[2].strip()
                
                # Преобразование даты коммита в наивный datetime
                commit_date_naive = datetime.strptime(commit_date[:-6], '%Y-%m-%d %H:%M:%S')
                
                # Фильтрация по дате
                if commit_date_naive > date:
                    commit_info.append({'hash': commit_hash, 'message': commit_message, 'files': []})

    # Получаем файлы для каждого коммита
    for commit in commit_info:
        files_result = subprocess.run(
            ['git', '-C', repo_path, 'diff-tree', '--no-commit-id', '--name-only', '-r', commit['hash']],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        if files_result.returncode == 0:
            commit['files'] = files_result.stdout.splitlines()

    return commit_info

def generate_mermaid_code(commit_info):
    lines = ["graph TD;"]
    
    previous_commit_id = None  # Переменная для хранения предыдущего коммита
    
    # Перебираем коммиты в обратном порядке, чтобы отобразить их от первого к последнему
    for commit in reversed(commit_info):
        node_id = commit['hash'][:7]
        
        # Добавляем узел коммита с сообщением
        lines.append(f'    {node_id}["{commit["message"]}"]')
        
        # Если есть предыдущий коммит, соединяем его с текущим
        if previous_commit_id is not None:
            lines.append(f'    {previous_commit_id} --> {node_id}')

        previous_commit_id = node_id  # Обновляем предыдущий коммит

        for file in commit['files']:
            file_node_id = f'file_{file.replace(".", "_")}'  # Заменяем точки для уникальности узлов
            lines.append(f'    {file_node_id}["{file}"]')
            lines.append(f'    {node_id} --> {file_node_id}')

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Генератор графа зависимостей коммитов.")
    
    parser.add_argument("visualizer_path", help="Путь к программе для визуализации графов.")
    parser.add_argument("repo_path", help="Путь к анализируемому репозиторию.")
    parser.add_argument("output_image_path", help="Путь к файлу с изображением графа зависимостей.")
    parser.add_argument("date", help="Дата коммитов в формате YYYY-MM-DD.")

    args = parser.parse_args()

    # Парсим дату из аргументов
    date = datetime.strptime(args.date, '%Y-%m-%d')
    
    commit_info = get_commit_tree(args.repo_path, date)
    
    if not commit_info:
        print("Нет коммитов позже заданной даты.")
        return
    
    mermaid_code = generate_mermaid_code(commit_info)
    
    # Сохраняем код Mermaid в файл
    mermaid_file = "graph.mmd"
    with open(mermaid_file, 'w') as f:
        f.write(mermaid_code)

    # Генерируем граф с помощью mermaid-cli
    try:
        result = subprocess.run([args.visualizer_path, '-i', mermaid_file, '-o', args.output_image_path], check=True)
        print(f"Граф сохранен в {args.output_image_path}")
    except FileNotFoundError:
        print(f"Не удалось найти исполняемый файл: {args.visualizer_path}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
    except OSError as e:
        print(f"Ошибка ОС: {e}")

if __name__ == "__main__":
    main()
