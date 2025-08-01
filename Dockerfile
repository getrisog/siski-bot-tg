FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY pencil_bot/ ./pencil_bot/
COPY gif_urls.txt .

RUN pip install uv
RUN uv venv 
RUN uv sync

ENV PATH="/app/.venv/bin:$PATH"

RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

CMD ["python", "-m", "pencil_bot.main"] 