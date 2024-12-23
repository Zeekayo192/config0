# 1. Клонирование репозитория

Склонируйте репозиторий с исходным кодом и тестами:

```
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Установка зависимостей при запуске

```
pip install subprocess

```

# Создайте виртуальное окружение

```bash
# Активируйте виртуальное окружение
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для MacOS/Linux:
source venv/bin/activate
```


# 3. Структура проекта
Проект содержит следующие файлы и директории:
```bash
unittests.py              # файл для тестирования
hw2.py                  # файл с программой
output.png             # файл с выводом программы 
```

# 4. Запуск проекта
```bash
npm install -g @mermaid-js/mermaid-cli
py hw2.py C:\Users\user\AppData\Roaming\npm\mmdc.cmd C:\Users\user\Desktop\Test111 output.png 2024-01-01     
# py hw2.py <путь к mermaid визуализатору> <путь к репозиторию> <выходной файл> <дата(гггг-мм-дд)>
```


# 5. Unittest
```bash
py -m unittest unittests.py
```

