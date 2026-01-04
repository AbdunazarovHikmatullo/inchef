#!/bin/bash

# Удаляем файл базы данных
if [ -f "db.sqlite3" ]; then
    rm db.sqlite3
    echo "Removed db.sqlite3"
fi

# Удаляем файлы миграций, оставляя __init__.py
# Ищем во всех подпапках в текущей директории
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

echo "All migrations deleted."

# Создаем новые миграции
echo "Running makemigrations..."
python3 manage.py makemigrations

# Применяем миграции
echo "Running migrate..."
python3 manage.py migrate

echo "Database reset complete!"
