FROM python:3.12-slim

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 安装 uv
RUN pip install --no-cache-dir uv

# 复制依赖文件并安装
COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache-dir -e .

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "src.agent_develop_base.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
