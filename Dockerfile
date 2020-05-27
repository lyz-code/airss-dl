FROM python:3.8-slim-buster as base

FROM base as builder

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app
WORKDIR /app
RUN pip install .

FROM base

RUN apt-get update && apt-get install -y \
    wait-for-it \
 && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv

RUN useradd -m airss
WORKDIR /home/airss
COPY --from=builder /root/.local/share/airss /home/airss/.local/share/airss
COPY --from=builder /app/airss_dl /home/airss/airss_dl
COPY ./docker/entrypoint.sh /home/airss/entrypoint.sh
RUN chown -R airss:airss /home/airss/.local

USER airss
ENV PATH="/opt/venv/bin:$PATH"
ENTRYPOINT ["/home/airss/entrypoint.sh"]
