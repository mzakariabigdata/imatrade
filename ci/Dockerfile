FROM  ubuntu:22.10

RUN useradd -ms /bin/bash app && \
    mkdir -p /app && \
    chown -R app:app /app && \
    chmod -R 755 /app

COPY ci/Pipfile /app

ENV PS1="app@imatrade:\\w\\$ "

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install --upgrade  pipenv && \
    pipenv lock && \
    pipenv requirements --hash --dev > requirements-dev.txt && \
    pip3 install -r requirements-dev.txt && \
    echo 'PS1="app@imatrade:\\w\\$ "' >> /home/app/.bashrc && \
    echo 'alias python=python3' >> /home/app/.bashrc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

USER app