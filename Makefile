AUTHOR := thombashi
PACKAGE := sqlitebiter
BUILD_WORK_DIR := _work
DOCS_DIR := docs
DOCS_BUILD_DIR := $(DOCS_DIR)/_build
DIST_DIR := $(BUILD_WORK_DIR)/$(PACKAGE)/dist


.PHONY: build
build:
	@make clean
	@tox -e build
	ls -lh dist/*

.PHONY: releasebuild
releasebuild:
	@rm -rf $(BUILD_WORK_DIR)/
	@mkdir -p $(BUILD_WORK_DIR)/
	@cd $(BUILD_WORK_DIR); \
		git clone https://github.com/$(AUTHOR)/$(PACKAGE).git; \
		cd $(PACKAGE); \
		python setup.py sdist bdist_wheel
	@twine check $(DIST_DIR)/*
	ls -lh $(DIST_DIR)/*

.PHONY: check
check:
	travis lint
	@tox -e lint

.PHONY: clean
clean:
	@tox -e clean

.PHONY: docs
docs:
	@python setup.py build_sphinx --source-dir=$(DOCS_DIR)/ --build-dir=$(DOCS_BUILD_DIR) --all-files

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: readme
readme:
	@tox -e readme

.PHONY: release
release:
	@cd $(BUILD_WORK_DIR)/$(PACKAGE) && tox -e release
	@make clean

.PHONY: setup
setup:
	@pip install --upgrade -e .[test] tox
