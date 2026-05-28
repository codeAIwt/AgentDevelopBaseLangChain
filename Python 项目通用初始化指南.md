# Python 项目通用初始化指南（WSL \+ Docker \+ uv/conda 双版本）


**企业级标准开发环境，一键初始化，开箱即用**
适用于：Web 开发、API 服务、AI 应用、数据处理、工具脚本等所有 Python 项目

---

## 前置条件

- Windows 10/11 \+ WSL2 \+ Ubuntu 24\.04

- Docker Desktop（已启用 WSL2 后端）

- Trae/VS Code（已安装 WSL 远程扩展）

---

## 包管理器选择指南（先看这个！）

|项目类型|推荐工具|核心优势|
|---|---|---|
|**纯 Python 项目**<br>Web开发/API/脚本/自动化|✅ **uv**|速度快10\-100倍，体积小，简单易用|
|**数据科学/机器学习/深度学习**<br>需要CUDA/GPU/复杂C依赖|✅ **conda \(Miniconda\)**|一站式解决Python\+CUDA\+MKL等系统级依赖|
|**混合语言项目**<br>Python\+R/C\+\+/FFmpeg|✅ **conda**|跨语言包管理，ABI兼容性好|

> **请根据当前的AI项目场景选择合适的包管理器**：如果只做RAG/API服务用uv；如果需要PyTorch/TensorFlow GPU训练用conda

---

## 1\. WSL 环境准备

### 1\.1 启动并进入 WSL

```Bash
# Windows PowerShell/CMD 中执行
wsl

# 或直接进入 Ubuntu
wsl -d Ubuntu
```

### 1\.2 创建并进入项目目录

```Bash
# 统一工作区（推荐）
mkdir -p ~/workspace/your-project-name
cd ~/workspace/your-project-name
```

---

## 2\. 项目骨架生成（一键执行）

复制以下整段命令到 WSL 终端执行，自动创建完整项目结构：

```Bash
# 创建目录结构
mkdir -p src/{your_project}/ tests/ resources/ docs/ scripts/ init-db/

# 创建基础文件
touch .env .env.example .gitignore .python-version pyproject.toml uv.lock
touch docker-compose.yml Dockerfile README.md CHANGELOG.md LICENSE
touch environment.yml  # conda专用
touch src/your_project/__init__.py src/your_project/main.py src/your_project/config.py
touch tests/__init__.py tests/test_main.py
```

---

## 3\. 核心配置文件

### 3\.1 通用配置文件

#### `\.gitignore`（Git 忽略文件）

```Plaintext
# 虚拟环境
.venv/
venv/
env/
conda-env/

# Python 缓存
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 环境变量
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 数据库
*.db
*.db-shm
*.db-wal
postgres_data/

# 日志
*.log
logs/

# Docker
.dockerignore

# Conda
environment.lock.yml
conda-bld/

# 其他
.DS_Store
Thumbs.db
```

#### `\.env\.example`（环境变量模板）

```Plaintext
# 数据库配置(根据实际需求配置)
DATABASE_URL=postgresql://{ai_dev}:ai_dev_123@db:5432/ai_db
POSTGRES_USER=ai_dev
POSTGRES_PASSWORD=ai_dev_123
POSTGRES_DB=ai_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

# 应用配置
DEBUG=true
APP_PORT=8000
LOG_LEVEL=info

# API 密钥（根据项目需要添加）
# OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### `\.python\-version`（Python 版本锁定）

```Plaintext
3.12
```

---

### 3\.2 uv 版本配置

#### `pyproject\.toml`（项目配置与依赖）

```Plaintext
[project]
name = "your-project-name"
version = "0.1.0"
description = "项目描述"
authors = [
  { name = "Your Name", email = "your.email@example.com" }
]
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
  "python-dotenv>=1.0.0",
  "fastapi>=0.110.0",
  "uvicorn>=0.29.0",
  "psycopg[binary]>=3.1.0",
  "pgvector>=0.3.0"
]

[project.scripts]
your-project = "your_project.main:main"

[build-system]
requires = ["uv_build>=0.11.0,<0.12.0"]
build-backend = "uv_build"

[tool.ruff]
line-length = 120
select = ["E", "W", "F", "I"]
ignore = ["E501"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

---

### 3\.3 conda 版本配置（机器学习专用）

#### `environment\.yml`（Conda 环境配置）

```YAML
name: your-project-env
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.12
  - python-dotenv=1.0.0
  - fastapi=0.110.0
  - uvicorn=0.29.0
  - psycopg2=2.9.9
  - pgvector=0.3.0
  # 机器学习依赖（需要时取消注释）
  # - pytorch=2.3.0
  # - torchvision=0.18.0
  # - cudatoolkit=12.1
  # - numpy=1.26.4
  # - pandas=2.2.2
  # - scikit-learn=1.4.2
  - pip
  - pip:
    - python-multipart>=0.0.9
    - openai>=1.0.0
```

---

## 4\. Docker 环境配置

### 4\.1 uv 版本 Dockerfile

```Dockerfile
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
RUN uv pip install --system --no-cache-dir .

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "src.your_project.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

### 4\.2 conda 版本 Dockerfile（机器学习专用）

```Dockerfile
# 多阶段构建：第一阶段构建conda环境
FROM continuumio/miniconda3:24.4.0-0 AS builder

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 配置conda源（加速国内访问）
RUN conda config --remove-key channels && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority strict

# 设置工作目录
WORKDIR /app

# 复制环境文件并创建环境
COPY environment.yml ./
RUN conda env create -f environment.yml && \
    conda clean --all --force-pkgs-dirs -y

# 第二阶段：运行时镜像
FROM continuumio/miniconda3:24.4.0-0

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制conda环境
COPY --from=builder /opt/conda/envs/your-project-env /opt/conda/envs/your-project-env

# 激活环境
ENV PATH=/opt/conda/envs/your-project-env/bin:$PATH
ENV CONDA_DEFAULT_ENV=your-project-env

# 设置工作目录
WORKDIR /app

# 复制项目代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "src.your_project.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

### 4\.3 通用 docker\-compose\.yml

```YAML
version: '3.8'

services:
  web:
    build: .
    container_name: ${PROJECT_NAME:-app}-web
    restart: unless-stopped
    ports:
      - "${APP_PORT:-8000}:8000"
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_HOST=${POSTGRES_HOST}
      - POSTGRES_PORT=${POSTGRES_PORT}
      - DEBUG=${DEBUG}
      - LOG_LEVEL=${LOG_LEVEL}
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network

  db:
    image: pgvector/pgvector:16
    container_name: ${PROJECT_NAME:-app}-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres_data:
    name: ${PROJECT_NAME:-app}-postgres-data
```

### 4\.4 数据库初始化脚本

创建 `init\-db/01\-init\.sql`：

```SQL
-- 启用 pgvector 扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- 在这里添加你的表结构和初始数据
-- 示例：
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     username VARCHAR(50) UNIQUE NOT NULL,
--     email VARCHAR(100) UNIQUE NOT NULL,
--     created_at TIMESTAMP DEFAULT NOW()
-- );
```

---

## 5\. Python 环境初始化

### 5\.1 uv 版本（推荐纯Python项目）

```Bash
# 安装 uv（如果未安装）
pip install uv

# 创建虚拟环境（自动使用 .python-version 指定的版本）
uv venv

# 激活虚拟环境
source .venv/bin/activate

# 安装所有依赖
uv pip install -e .

# 生成锁定文件
uv lock
```

---

### 5\.2 conda 版本（推荐机器学习项目）

```Bash
# 安装 Miniconda（如果未安装）
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3
echo 'export PATH=~/miniconda3/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 配置国内源（加速）
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes

# 创建并激活环境
conda env create -f environment.yml
conda activate your-project-env

# 导出锁定的环境（可选，用于精确复现）
conda env export --no-builds > environment.lock.yml
```

---

## 6\. Git 初始化

```Bash
# 初始化 Git 仓库
git init

# 配置用户信息（首次使用）
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 添加初始文件
git add .

# 提交初始版本
git commit -m "Initial commit: Project setup"

# 重命名分支为 main
git branch -m main
```

---

## 7\. 启动开发环境

### 7\.1 复制环境变量文件

```Bash
cp .env.example .env
```

**重要**：编辑 `\.env` 文件，填入你的实际配置（如 API 密钥）。

### 7\.2 启动 Docker 服务

```Bash
# 构建并启动所有服务
docker compose up -d --build

# 查看服务状态
docker compose ps

# 查看应用日志
docker compose logs -f web
```

### 7\.3 验证服务

- API 文档：http://localhost:8000/docs

- 数据库：localhost:5432（使用 DBeaver/Navicat 连接）

---

## 8\. Trae/VS Code 调试配置

创建 `\.vscode/launch\.json`：

```JSON
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.your_project.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000"
            ],
            "jinja": false,
            "envFile": "${workspaceFolder}/.env"
        }
    ]
}
```

---


## 9\. 标准项目结构

```Plaintext
your-project-name/
├── .env                    # 本地环境变量（不提交到 Git）
├── .env.example            # 环境变量模板（提交到 Git）
├── .gitignore              # Git 忽略文件
├── .python-version         # Python 版本锁定
├── docker-compose.yml      # Docker 服务编排
├── Dockerfile              # 应用镜像构建
├── pyproject.toml          # uv 项目配置与依赖
├── uv.lock                 # uv 依赖锁定文件
├── environment.yml         # conda 环境配置
├── environment.lock.yml    # conda 锁定环境（可选）
├── README.md               # 项目说明
├── CHANGELOG.md            # 版本变更记录
├── LICENSE                 # 开源协议
├── init-db/                # 数据库初始化脚本
│   └── 01-init.sql
├── src/                    # 源代码
│   └── your_project/       # 项目主包
│       ├── __init__.py
│       ├── main.py         # 应用入口
│       ├── config.py       # 配置管理
│       ├── models.py       # 数据模型
│       ├── schemas.py      # Pydantic 模式
│       ├── crud.py         # CRUD 操作
│       └── api/            # API 路由
├── tests/                  # 测试代码
│   ├── __init__.py
│   └── test_main.py
├── resources/              # 静态资源
├── docs/                   # 项目文档
└── scripts/                # 辅助脚本
```

---

## 10\. 最佳实践与注意事项

### 安全

- ⚠️ **绝对不要将 ****`\.env`**** 文件提交到 Git！**

- ⚠️ 生产环境必须修改默认密码和密钥

- ⚠️ 不要在代码中硬编码任何敏感信息

- ⚠️ 定期更新依赖包，修复安全漏洞

### 开发规范

- 使用类型注解提高代码可读性和可维护性

- 遵循 PEP 8 代码风格（使用 Ruff 自动检查）

- 编写单元测试和集成测试

- 提交代码前运行测试，确保代码质量

- 使用语义化版本号（Semantic Versioning）

### 部署

- 生产环境禁用 DEBUG 模式

- 使用反向代理（如 Nginx）处理静态资源和 SSL

- 配置日志收集和监控

- 使用 Docker Swarm 或 Kubernetes 进行容器编排

---

## 11\. 故障排查

### 常见问题

1. **Docker 端口被占用**

```Bash
# 查看占用端口的进程
lsof -i :8000
lsof -i :5432

# 杀死进程
kill -9 <PID>
```

2. **数据库连接失败**

    - 检查数据库容器是否正常运行：`docker compose ps`

    - 查看数据库日志：`docker compose logs db`

    - 确认 `\.env` 文件中的数据库配置正确

3. **依赖安装失败**

    - uv：清除缓存 `uv cache clean`，重新安装 `uv pip install \-e \.`

    - conda：更新conda `conda update \-n base \-c defaults conda`，换用国内源

4. **Trae 无法识别虚拟环境**

    - 按 `Ctrl\+Shift\+P`，输入 `Python: Select Interpreter`

    - uv：选择 `\./\.venv/bin/python`

    - conda：选择 `\~/miniconda3/envs/your\-project\-env/bin/python`

---


