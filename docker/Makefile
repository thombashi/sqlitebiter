REGISTRY := ghcr.io
OWNER := thombashi
USER := thombashi
NAME := sqlitebiter
REPO := $(REGISTRY)/$(OWNER)/$(NAME)

VERSION := $(shell ./extract_version.sh)

HADOLINT_VERSION := v2.8.0


.PHONY: check-github-token
check-github-token:
ifndef GITHUB_TOKEN
	$(error require GITHUB_TOKEN)
endif

.PHONY: lint-dockerfile
lint-dockerfile:
	docker run --rm -i hadolint/hadolint:$(HADOLINT_VERSION) < Dockerfile

.PHONY: docker-login
docker-login: check-github-token
	@echo $(GITHUB_TOKEN) | docker login $(REGISTRY) -u $(USER) --password-stdin

.PHONY: docker-build
docker-build:
	docker build -t $(REPO):v$(VERSION) --pull . --build-arg version=$(VERSION)

.PHONY: docker-push
docker-push:
	docker push $(REPO):v$(VERSION)
