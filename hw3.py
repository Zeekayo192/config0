import argparse
import json
import re

def parse_value(value):
    """Парсит значение и возвращает соответствующий тип."""
    if value.isdigit():
        return int(value)
    elif re.match(r'^".*"$', value):
        return value.strip('"')
    elif re.match(r'^\{.*\}$', value):
        return parse_dict(value.strip('{}'))
    raise ValueError(f"Неизвестное значение: {value}")

def parse_dict(text):
    """Парсит словарь из входного текста."""
    items = {}
    pairs = re.split(r',\s*(?![^{}]*\})', text)  # Разделяем по запятой, игнорируя вложенные словари
    for pair in pairs:
        name_value = pair.split('=')
        if len(name_value) != 2:
            raise ValueError(f"Неверный формат пары: {pair}")
        name = name_value[0].strip()
        value = name_value[1].strip()
        items[name] = parse_value(value)
    return items

def evaluate_expression(expr, context):
    """Вычисляет константное выражение."""
    expr = expr.replace('#(', '').replace(')', ')')

    # Проверка на наличие пустого выражения
    if not expr:
        raise ValueError("Пустое выражение для вычисления.")
    
    # Заменяем имена переменных на их значения
    for name in context:
        expr = expr.replace(name, str(context[name]))

    # Обработка доступа к элементам словаря (например, namem[key])
    expr = re.sub(r'(\w+)\.(\w+)', r'\1[\2]', expr)

    try:
        return eval(expr)
    except SyntaxError as e:
        raise ValueError(f"Ошибка синтаксиса в выражении: {expr}") from e
    except Exception as e:
        raise ValueError(f"Ошибка при вычислении выражения: {expr}") from e

def main():
    parser = argparse.ArgumentParser(description='Конвертер конфигурационного языка в JSON.')
    parser.add_argument('input_file', help='Путь к входному файлу с конфигурацией')
    
    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        lines = file.readlines()

    config = {}
    
    for line in lines:
        line = line.strip()
        if '=' in line:
            name, value = line.split('=', 1)  # Ограничиваем разделение до двух частей
            name = name.strip()
            value = value.strip()
            if value.startswith('#'):
                # Обработка выражения
                result = evaluate_expression(value[1:], config)
                config[name] = result
            else:
                config[name] = parse_value(value)

    print(json.dumps(config, ensure_ascii=False, indent=4))

if __name__ == '__main__':
    main()
