#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from tools.db_utils import PGConn

from dotenv import load_dotenv
load_dotenv()

from tools.db_utils import PGConn


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nyx.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    PGConn()

    ip   = os.getenv('HOST_ADDRESS')
    port = os.getenv('HOST_PORT')
    execute_from_command_line([sys.argv[0], 'runserver', f'{ip}:{port}'])

    # execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
