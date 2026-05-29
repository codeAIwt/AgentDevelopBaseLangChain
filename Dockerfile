FROM python:3.12-slim

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src ./src

RUN pip install --no-cache-dir .

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.langchain_agent.main:app", "--host", "0.0.0.0", "--port", "8000"]
