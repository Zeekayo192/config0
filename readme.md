# 1. Клонирование репозитория

Склонируйте репозиторий с исходным кодом и тестами:

```
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Установка зависимостей при запуске

```
pip install tkinter
pip install zipfile
pip install argparse
pip install shutil

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
virtual_fs.zip           # zip-архив в качестве образа файловой системы
emulator.py                  # файл с программой
config.json                     #конфиг
script.txt                      #стартовый скрипт
```

# 4. Запуск проекта
```bash
py emulator.py config.json    # py название файла <файл с конфигом>
```

# 5. Команды 
```bash
ls
cd <dir>
history
exit
clear
history
pwd
uname
```

# 6. Unittest
```bash
pip install unittest
py -m unittest unttests.py
```