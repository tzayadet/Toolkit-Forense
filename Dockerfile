FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
RUN useradd --create-home --uid 10001 appuser
COPY --chown=appuser:appuser forensic_inventory.py .
USER appuser

ENTRYPOINT ["python", "forensic_inventory.py"]
