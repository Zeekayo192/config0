# Установка
1. Установка программы и переход в директорию
   ```bash
   git clone <URL репозитория>
   cd <директория проекта>
   ```
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate     # Для Windows
   ```
3. Установите необходимые зависимости :
   ```bash
   Зависимости не требуются
   ```

# Запуск скрипта

Скрипт принимает текст конфигурационного файла через файл и выводит json в стандартный вывод.

```bash
 py hw3.py input.txt
```

# Вывод 
```
{
    "namei": 42,
    "nametwo": 52,
    "names": "Hello, World",
    "namem": {
        "keyi": 100,
        "keys": "Nested String"
    },
    "resultsum": 43,
    "resultsub": 2,
    "resultord": 65,
    "resultmul": 2184
}
```

# Unittest
```bash
py -m unittest unittests.py
```
