"""Launch the adjacent project configuration after installing cvzero."""

from pathlib import Path

from cvzero.course.project import main

if __name__ == "__main__":
    main(default_config=Path(__file__).with_name("config.json"))
