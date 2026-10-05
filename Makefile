PYTHON ?= python3
BOOK ?= jupyter-book
PORT ?= 3000
CONTENT_PORT ?= 3100
BIND ?= 127.0.0.1

.PHONY: preview build serve

# Development server: HTML application + MyST content server.
preview:
	env -u BASE_URL $(BOOK) start --port $(PORT) --server-port $(CONTENT_PORT)

# Root URL for the local static export (no GitHub Pages prefix).
build:
	env -u BASE_URL $(BOOK) build --html --strict
	$(PYTHON) scripts/check_site.py

# Serve the exported site without starting the MyST application.
serve:
	$(PYTHON) scripts/check_site.py
	$(PYTHON) -m http.server $(PORT) --bind $(BIND) --directory _build/html
