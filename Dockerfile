FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/tox-venv/bin:$PATH"

# ── Sistema base + deadsnakes PPA per Python 3.11, 3.12, 3.13, 3.14 ──────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        software-properties-common \
        ca-certificates \
        curl \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y --no-install-recommends \
        python3.11 python3.11-dev python3.11-venv \
        python3.12 python3.12-dev python3.12-venv \
        python3.13 python3.13-dev python3.13-venv \
        python3.14 python3.14-dev python3.14-venv \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# ── tox in un venv isolato (evita il blocco pip di Ubuntu 24.04) ──────────────
RUN python3.12 -m venv /opt/tox-venv \
    && /opt/tox-venv/bin/pip install --quiet --upgrade pip tox

WORKDIR /app

# Copia prima solo i file di dipendenze per sfruttare la cache di Docker
COPY pyproject.toml setup.cfg requirements.txt requirements_test.txt tox.ini runtests.py ./

# Copia il codice sorgente e i test
COPY soft_delete_model_mixin/ soft_delete_model_mixin/
COPY tests/ tests/

CMD ["tox", "--parallel", "auto", "--parallel-live"]
