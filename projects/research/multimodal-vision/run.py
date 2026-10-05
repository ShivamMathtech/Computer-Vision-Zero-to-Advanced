"""Launch the configured project; shared algorithms live in cvzero.course."""

from pathlib import Path

from cvzero.course.project import main

if __name__ == "__main__":
    main(default_config=Path(__file__).with_name("config.json"))
