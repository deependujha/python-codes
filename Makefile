.phony: setup

setup:
	uv pip install -r requirements.txt

serve:
	uv run mkdocs serve
