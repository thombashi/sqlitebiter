FROM ubuntu:20.04

LABEL maintainer="Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>"
LABEL org.opencontainers.image.source https://github.com/thombashi/sqlitebiter

ENV DEBIAN_FRONTEND noninteractive

ARG version

RUN set -eux \
    && apt-get -qq update \
    && apt-get install -qq --no-install-recommends \
    libsqlite3-0 \
    python3 \
    python3-pip \
    && python3 -m pip install --no-cache-dir --retries 30 "sqlitebiter[all]==${version}" --disable-pip-version-check \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["sqlitebiter"]
CMD ["--help"]
