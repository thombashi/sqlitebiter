AUTHOR := thombashi
PACKAGE := sqlitebiter
BUILD_WORK_DIR := _work
DOCS_DIR := docs
DOCS_BUILD_DIR := $(DOCS_DIR)/_build
PKG_BUILD_DIR := $(BUILD_WORK_DIR)/$(PACKAGE)
SCRIPTS := $(shell \find . -not -path '*/\.*' -type f -regextype posix-extended -regex .+\.sh$)

PYTHON := python3
SUDO := sudo


.PHONY: build-remote
build-remote: clean
	@mkdir -p $(BUILD_WORK_DIR)
	@cd $(BUILD_WORK_DIR) && \
		git clone https://github.com/$(AUTHOR)/$(PACKAGE).git --depth 1 && \
		cd $(PACKAGE) && \
		$(PYTHON) -m tox -e build
	ls -lh $(PKG_BUILD_DIR)/dist/*

.PHONY: build
build: clean
	@$(PYTHON) -m tox -e build
	ls -lh dist/*

.PHONY: build-deb
build-deb: setup-ci
	$(MAKE) clean
	$(SUDO) apt -qq update
	$(SUDO) apt install -qq -y --no-install-recommends git fakeroot rename
	./scripts/build_linux_package.sh
	ls -lh dist/*

.PHONY: check
check:
	@$(PYTHON) -m tox -e lint
	$(PYTHON) -m pip check

.PHONY: clean
clean:
	@rm -rf $(BUILD_WORK_DIR)
	@$(PYTHON) -m tox -e clean

.PHONY: docs
docs:
	@$(PYTHON) -m tox -e docs

.PHONY: fmt
fmt:
	shfmt -i 4 -l -w -sr $(shell \find . -not -path '*/\.*' -type f -regextype posix-extended -regex .+\.sh$)
	@$(PYTHON) -m tox -e fmt

.PHONY: readme
readme:
	@$(PYTHON) -m tox -e readme

.PHONY: release
release:
	cd $(PKG_BUILD_DIR) && $(PYTHON) setup.py release --verbose
	$(MAKE) clean

.PHONY: setup-ci
setup-ci:
	$(PYTHON) -m pip install --disable-pip-version-check --upgrade tox

.PHONY: setup-dev
setup-dev: setup-ci
	@$(PYTHON) -m pip install -q --disable-pip-version-check --upgrade -e .[test] releasecmd
	@$(PYTHON) -m pip check

.PHONY: latest-release-assets
latest-release-assets:
	curl -sSL https://api.github.com/repos/thombashi/sqlitebiter/releases/latest | jq -r '.assets[].browser_download_url' > scripts/latest_release_assets.list
