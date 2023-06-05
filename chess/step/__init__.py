import sys
import os

# Получаем путь к текущей директории скрипта
script_dir = os.path.dirname(os.path.realpath(__file__))

# Получаем путь к директории скриптов (предполагая, что она находится внутри текущей директории)
scripts_dir = os.path.join(script_dir, 'scripts')

# Добавляем директорию скриптов в PYTHONPATH
sys.path.append(scripts_dir)