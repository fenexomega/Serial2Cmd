all: generate run

generate:
	@echo "generating ui files"
	@pyuic5 editor.ui -o serial2cmd/editor.py

run:
	@echo "Running app"
	@python3 serial2cmd/serial2cmd_ui.py
