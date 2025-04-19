#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import zipfile

zip_path = "db.sqlite3.zip"
db_path = "db.sqlite3"

if not os.path.exists(db_path) and os.path.exists(zip_path):
    print("Unzipping database...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pestopanini.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
