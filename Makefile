AUTHOR := thombashi
PACKAGE := sqlitebiter
BUILD_WORK_DIR := _work
DOCS_DIR := docs
DOCS_BUILD_DIR := $(DOCS_DIR)/_build
PKG_BUILD_DIR := $(BUILD_WORK_DIR)/$(PACKAGE)
SCRIPTS := $(shell \find . -not -path '*/\.*' -type f -regextype posix-extended -regex .+\.sh$)
PYTHON := python3


.PHONY: build-remote
build-remote: clean
	@mkdir -p $(BUILD_WORK_DIR)
	@cd $(BUILD_WORK_DIR) && \
		git clone https://github.com/$(AUTHOR)/$(PACKAGE).git --depth 1 && \
		cd $(PACKAGE) && \
		tox -e build
	ls -lh $(PKG_BUILD_DIR)/dist/*

.PHONY: build
build: clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	@tox -e lint
	$(PYTHON) -m pip check

.PHONY: clean
clean:
	@rm -rf $(BUILD_WORK_DIR)
	@tox -e clean

.PHONY: docs
docs:
	@tox -e docs

.PHONY: fmt
fmt:
	shfmt -i 4 -l -w -sr $(shell \find . -not -path '*/\.*' -type f -regextype posix-extended -regex .+\.sh$)
	@tox -e fmt

.PHONY: readme
readme:
	cd $(DOCS_DIR) && ./update_command_help.py
	@tox -e readme

.PHONY: release
release:
	@cd $(PKG_BUILD_DIR) && $(PYTHON) setup.py release --sign
	@make clean

.PHONY: setup
setup:
	@$(PYTHON) -m pip install  --disable-pip-version-check --upgrade releasecmd tox

.PHONY: setup-dev
setup-dev: setup
	@$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade -e .[test]
	@$(PYTHON) -m pip check
