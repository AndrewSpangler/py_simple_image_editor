#!/usr/bin/env python
import os, sys, json, tomllib
try:
    from py_simple_readme import readme_generator
    from src.py_simple_image_editor.version import __version__ as version
    IGNORED_METHODS = []
    with open(os.path.join(os.path.dirname(__file__),"./pyproject.toml"), "rb") as f:
        config = tomllib.load(f)
    with open(os.path.join(os.path.dirname(__file__),"./changelog.json")) as f:
        changelog = json.load(f)
    name = config["project"]["name"]
    description = config["project"]["description"]
    author = config["project"]["authors"][0]["name"]
    dependencies = config["project"]["dependencies"]
    installation_message = f"""Available on pip - `pip install {name}`"""
    gen = readme_generator(
        title=f"{name} {version}", ignored=IGNORED_METHODS
    )
    gen.set_changelog(changelog)
    gen.add_heading_1("About", add_toc=True)
    gen.add_paragraph(description)
    gen.add_heading_1("Requirements", add_toc=True)
    gen.add_paragraph(dependencies)
    with open(os.path.join(os.path.dirname(__file__), "README.md"), "w+") as f:
        f.write(gen.assemble())
except Exception as e:
    sys.exit(1)
sys.exit(os.EX_OK)