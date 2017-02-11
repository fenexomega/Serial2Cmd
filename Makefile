PREFIX=$(DESTDIR)/usr
BIN_DIR=$(PREFIX)/bin
SHARE_DIR=(PREFIX)/share/serial2cmd
LIB_DIR=$(PREFIX)/bin/serial2cmd

all: generate run

generate:
	@echo "generating ui files"
	@pyuic5 editor.ui -o serial2cmd/editor.py

run:
	@echo "Running app"
	@python3 serial2cmd/serial2cmd_ui.py

install: 
	@chmod +x run.py
	@cp run.py $(BIN_DIR)
	@cp -r serial2cmd/ $(LIB_DIR)
	@mkdir -p $(SHARE_DIR)
	@cp config.json $(SHARE_DIR)
	@cp -r icons $(SHARE_DIR)
