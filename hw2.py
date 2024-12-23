import os
import zlib
from datetime import datetime, timezone
import argparse
import subprocess

def read_git_object(repo_path, obj_hash):
    obj_dir = os.path.join(repo_path, ".git", "objects", obj_hash[:2])
    obj_file = os.path.join(obj_dir, obj_hash[2:])

    if not os.path.isfile(obj_file):
        raise FileNotFoundError(f"Git object {obj_hash} not found.")

    with open(obj_file, 'rb') as f:
        compressed_data = f.read()
        data = zlib.decompress(compressed_data)

    header_end = data.find(b'\x00')
    header = data[:header_end].decode()
    obj_type, _ = header.split(" ", 1)
    content = data[header_end + 1:]

    return obj_type, content

def parse_commit_object(data):
    header, body = data.split(b'\n\n', 1)
    lines = header.decode().split('\n')

    commit_info = {}
    for line in lines:
        if line.startswith("parent"):
            commit_info['parent'] = line.split()[1]
        elif line.startswith("author"):
            parts = line.split()
            timestamp = int(parts[-2])
            commit_info['date'] = datetime.fromtimestamp(timestamp, timezone.utc)

    commit_info['message'] = body.decode().strip()
    return commit_info

def parse_tree_object(data):
    files = []
    i = 0
    while i < len(data):
        end_of_name = data.find(b'\x00', i)
        entry = data[i:end_of_name].decode()
        _, filename = entry.split(" ", 1)
        files.append(filename)
        i = end_of_name + 21
    return files

def get_commit_graph(repo_path, start_date):
    head_path = os.path.join(repo_path, ".git", "refs", "heads", "main")
    with open(head_path, 'r') as f:
        current_commit = f.read().strip()

    graph = {}
    while current_commit:
        obj_type, commit_data = read_git_object(repo_path, current_commit)
        if obj_type != "commit":
            raise ValueError(f"Unexpected object type: {obj_type}")

        commit_info = parse_commit_object(commit_data)

        if commit_info['date'] <= start_date:
            break

        tree_line = commit_data.split(b'\n')[0]
        _, tree_hash = tree_line.split()
        tree_hash = tree_hash.decode()

        obj_type, tree_data = read_git_object(repo_path, tree_hash)
        if obj_type != "tree":
            raise ValueError(f"Unexpected object type: {obj_type}")

        files = parse_tree_object(tree_data)

        graph[current_commit] = {
            'message': commit_info['message'],
            'parent': commit_info.get('parent'),
            'files': files
        }

        current_commit = commit_info.get('parent')

    return graph

def generate_mermaid_code(graph):
    lines = ["graph TD;"]

    for commit_hash, info in graph.items():
        node_id = commit_hash[:7]
        files_list = "<br>".join(info.get('files', []))
        node_label = f"{node_id}<br>{info['message']}<br>{files_list}"
        lines.append(f'    {node_id}["{node_label}"]')

        if info['parent']:
            parent_id = info['parent'][:7]
            lines.append(f'    {parent_id} --> {node_id}')

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Генератор графа зависимостей коммитов.")

    parser.add_argument("visualizer_path", help="Путь к программе для визуализации графов.")
    parser.add_argument("repo_path", help="Путь к анализируемому репозиторию.")
    parser.add_argument("output_image_path", help="Путь к файлу с изображением графа зависимостей.")
    parser.add_argument("date", help="Дата коммитов в формате YYYY-MM-DD.")

    args = parser.parse_args()

    start_date = datetime.strptime(args.date, '%Y-%m-%d').replace(tzinfo=timezone.utc)

    graph = get_commit_graph(args.repo_path, start_date)

    if not graph:
        print("Нет коммитов позже заданной даты.")
        return

    mermaid_code = generate_mermaid_code(graph)

    mermaid_file = "graph.mmd"
    with open(mermaid_file, 'w') as f:
        f.write(mermaid_code)

    print("Mermaid граф успешно сгенерирован.")
    print(mermaid_code)

    try:
        subprocess.run(
            [args.visualizer_path, '-i', mermaid_file, '-o', args.output_image_path],
            check=True
        )
        print(f"Граф сохранен в {args.output_image_path}")
    except FileNotFoundError:
        print(f"Не удалось найти визуализатор: {args.visualizer_path}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды визуализации: {e}")
    except OSError as e:
        print(f"Ошибка ОС: {e}")

if __name__ == "__main__":
    main()
