#!/usr/bin/env python
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def main():
    base_dir = Path(__file__).resolve().parent
    env_file = base_dir / ".env.local"

    if env_file.exists():
        load_dotenv(env_file)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()