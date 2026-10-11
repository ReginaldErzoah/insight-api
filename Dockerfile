
# 1. Start with Python 3.12 and uv
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# 2. Set the working directory inside the image
WORKDIR /app

# 3. Configure uv and Python
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

# 4. Copy dependency metadata
COPY pyproject.toml uv.lock README.md ./

# 5. Copy the application code and required data
COPY src/ ./src/
COPY streamlit_app.py ./
COPY data/ ./data/

# 6. Install the project and production dependencies
RUN uv sync --locked --no-dev

# 7. Document the API port
EXPOSE 8000

# 8. Start FastAPI when the container runs
CMD ["uv", "run", "--no-sync", "uvicorn", "insight_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
