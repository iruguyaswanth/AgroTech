#!/usr/bin/env python
"""
AgroTech - Django management script
Run: python manage.py runserver
"""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrotech_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed:\n"
            "  pip install django pillow"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
