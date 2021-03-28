AUTHOR := thombashi
PACKAGE := sqlitebiter
BUILD_WORK_DIR := _work
DOCS_DIR := docs
DOCS_BUILD_DIR := $(DOCS_DIR)/_build
PKG_BUILD_DIR := $(BUILD_WORK_DIR)/$(PACKAGE)
SCRIPTS := $(shell \find . -not -path '*/\.*' -type f -regextype posix-extended -regex .+\.sh$)


.PHONY: build-remote
build-remote:
	@rm -rf $(BUILD_WORK_DIR)
	@mkdir -p $(BUILD_WORK_DIR)
	@cd $(BUILD_WORK_DIR) && \
		git clone https://github.com/$(AUTHOR)/$(PACKAGE).git && \
		cd $(PACKAGE) && \
		tox -e build
	ls -lh $(PKG_BUILD_DIR)/dist/*

.PHONY: build
build:
	@make clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	travis lint
	@tox -e lint
	pip check

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
	@cd $(PKG_BUILD_DIR) && python setup.py release --sign
	@make clean

.PHONY: setup
setup:
	@pip install --upgrade -e .[test] releasecmd tox
	pip check
