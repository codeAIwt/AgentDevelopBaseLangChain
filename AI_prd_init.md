# AI 项目生成规范文档

## 1. 项目角色定义

你是一位专业的 Python 后端开发工程师，专门负责：

- 使用 FastAPI 构建高性能 Web API
- 使用 LangChain 开发 AI Agent 应用
- 使用 PostgreSQL + pgvector 进行数据存储和向量检索
- 遵循现代 Python 项目最佳实践

---

## 2. 项目基本信息

| 项目属性 | 说明 |
|---------|------|
| **项目描述** | 基于私有数据库的智能助手 Agent |
| **Python 版本** | 3.12+ |
| **包管理器** | uv |
| **数据库** | PostgreSQL + pgvector |
| **核心框架** | FastAPI + LangChain |

---

## 3. 项目功能

### 3.1 核心功能模块

#### 3.1.1 自然语言查询引擎

- **功能描述**：将用户的自然语言问题转换为 SQL 查询语句并执行
- **输入**：用户的自然语言问题
- **输出**：查询结果（表格、图表或文本描述）
- **技术实现**：
  - 使用 DeepSeek 模型理解用户意图
  - 自动生成优化的 SQL 查询语句
  - 支持复杂的 JOIN、聚合、过滤操作

#### 3.1.2 数据库 Schema 感知

- **功能描述**：Agent 自动学习和理解数据库结构
- **功能点**：
  - 自动扫描数据库表结构和字段含义
  - 维护数据库元数据缓存
  - 提供 Schema 查询和展示功能
  - 支持中文列名/表名的语义理解

#### 3.1.3 智能查询优化

- **功能描述**：自动优化查询性能和结果质量
- **功能点**：
  - SQL 语法检查和纠错
  - 查询性能分析和慢查询预警
  - 建议索引优化
  - 结果缓存机制
  - 分页和限制控制

#### 3.1.4 对话式交互

- **功能描述**：支持多轮对话，保持上下文理解
- **功能点**：
  - 记住对话历史
  - 支持追问和澄清
  - 上下文相关的建议
  - 支持对话中断和恢复
  - 对话历史持久化

#### 3.1.5 数据分析与洞察

- **功能描述**：提供数据分析和洞察能力
- **功能点**：
  - 趋势分析（时间序列数据）
  - 异常检测（发现数据中的异常点）
  - 对比分析（多维度数据对比）
  - 数据汇总和统计

### 3.2 API 接口功能

| 接口名称 | 方法 | 功能说明 |
|---------|------|---------|
| `/query` | POST | 自然语言查询接口 |
| `/schema` | GET | 获取数据库结构 |
| `/schema/refresh` | POST | 刷新数据库结构缓存 |
| `/history` | GET | 获取查询历史 |
| `/history/{id}` | GET | 获取特定对话详情 |
| `/health` | GET | 健康检查 |
| `/` | GET | 首页 |

---

## 4. 技术栈规范

### 4.1 核心依赖

```toml
[project]
dependencies = [
    # Web框架
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.29.0",

    # 数据库
    "sqlalchemy>=2.0.0",
    "psycopg[binary]>=3.1.0",
    "pgvector>=0.3.0",

    # AI/ML
    "langchain>=0.1.0",
    "langgraph>=0.2.0",
    "langgraph-checkpoint-postgres>=0.1.0",
    "langchain-community>=0.0.20",

    # 数据处理
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",

    # 可视化（可选）
    "matplotlib>=3.7.0",
]
```

### 4.2 开发依赖

```toml
[project.optional-dependencies]
dev = [
    "ruff>=0.3.0",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.27.0",
]
```

---

## 5. 目录结构规范

### 5.1 标准项目结构

```
${PROJECT_NAME}/
├── .env.example              # 环境变量示例
├── .gitignore               # Git忽略规则
├── .python-version          # Python版本
├── pyproject.toml           # 项目配置
├── Dockerfile               # Docker镜像
├── docker-compose.yml       # Docker编排
├── README.md               # 项目说明
├── init-db/
│   └── 01-init.sql         # 数据库初始化
└── src/
    └── ${PROJECT_PACKAGE}/
        ├── __init__.py
        ├── main.py           # 应用入口
        ├── config.py         # 配置管理
        ├── database.py       # 数据库连接
        ├── models.py         # 数据模型
        ├── schemas.py        # Pydantic模型
        ├── agent.py          # Agent核心逻辑
        ├── tools.py          # 工具定义
        ├── chains.py         # LangChain链
        ├── services/
        │   ├── __init__.py
        │   ├── query_service.py    # 查询服务
        │   └── schema_service.py   # Schema服务
        └── api/
            ├── __init__.py
            └── routes.py           # API路由
```

---

## 6. 常量参数规范

### 6.1 目录结构

```
src/
└── ${PROJECT_PACKAGE}/
    ├── constants.py    # 常量定义
    ├── config.py       # 配置管理
    ├── main.py         # 应用入口
    └── ...
```

### 6.2 constants.py 常量定义

```python
# constants.py

# ============ 数据库常量 ============
DB_QUERY_TIMEOUT = 30
DB_MAX_RETRIES = 3
DB_POOL_SIZE = 5
DB_MAX_OVERFLOW = 10

# ============ Agent 常量 ============
DEFAULT_MODEL = "deepseek-chat"
DEFAULT_TEMPERATURE = 0
DEFAULT_TIMEOUT = 10
DEFAULT_MAX_TOKENS = 500
MAX_QUERY_LENGTH = 2000
MAX_RESULT_ROWS = 1000

# ============ 多模型配置 ============
# 支持的模型列表
AVAILABLE_MODELS = {
    "deepseek-chat": {
        "provider": "deepseek",
        "description": "DeepSeek Chat",
        "default": True,
    },
    "deepseek-v4-pro": {
        "provider": "deepseek",
        "description": "DeepSeek V4 Pro",
        "default": False,
    },
    "gpt-4o": {
        "provider": "openai",
        "description": "GPT-4o",
        "default": False,
    },
    "claude-3-opus": {
        "provider": "anthropic",
        "description": "Claude 3 Opus",
        "default": False,
    },
}

# 模型选择策略
MODEL_SELECTION_STRATEGY = {
    "auto": "自动选择最优模型",
    "cost_optimized": "成本优化优先",
    "quality_first": "质量优先",
}

# ============ Checkpointer 配置 ============
# 记忆存储类型
CHECKPOINTER_TYPE = {
    "memory": "MemorySaver",      # 内存存储（开发/实验）
    "sqlite": "SqliteSaver",      # SQLite 存储（本地）
    "postgres": "PostgresSaver",  # PostgreSQL 存储（生产）
}

# 默认 checkpointer 类型
DEFAULT_CHECKPOINTER = CHECKPOINTER_TYPE["postgres"]

# 对话历史配置
MAX_HISTORY_MESSAGES = 50        # 最大保存消息数
MAX_HISTORY_TURNS = 20          # 最大对话轮次
HISTORY_TRIM_STRATEGY = "trim"  # trim | summarize | delete

# ============ 系统常量 ============
SYSTEM_PROMPT = """你是一个智能数据库助手，可以帮助用户查询和分析数据。
你有权限访问数据库工具来完成查询。
请根据用户的问题，生成相应的SQL查询并执行。"""

# 思考模式配置
THINKING_DISABLED = {"thinking": {"type": "disabled"}}

# ============ 缓存配置 ============
CACHE_ENABLED = True
CACHE_TTL = 300
CACHE_MAX_SIZE = 1000
```

### 6.3 config.py 配置管理

```python
# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from .constants import (
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_TIMEOUT,
    DEFAULT_MAX_TOKENS,
)

class Settings(BaseSettings):
    database_url: str
    deepseek_model: str = DEFAULT_MODEL

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

### 6.4 常量分类

| 类别 | 说明 | 示例 |
|------|------|------|
| **数据库常量** | 数据库连接和查询相关 | `DB_QUERY_TIMEOUT`, `DB_POOL_SIZE` |
| **Agent 常量** | LLM 模型参数配置 | `DEFAULT_MODEL`, `DEFAULT_TEMPERATURE` |
| **多模型配置** | 支持的模型列表和选择策略 | `AVAILABLE_MODELS`, `MODEL_SELECTION_STRATEGY` |
| **Checkpointer 配置** | 记忆存储和对话历史管理 | `CHECKPOINTER_TYPE`, `MAX_HISTORY_MESSAGES` |
| **系统常量** | 系统提示词和配置 | `SYSTEM_PROMPT`, `THINKING_DISABLED` |
| **缓存常量** | 缓存策略配置 | `CACHE_ENABLED`, `CACHE_TTL` |

### 6.5 常量使用规范

```python
# ✅ 推荐：从 constants.py 导入使用
from .constants import (
    DEFAULT_TEMPERATURE,
    DEFAULT_TIMEOUT,
    SYSTEM_PROMPT,
)

model = init_chat_model(
    "deepseek-chat",
    temperature=DEFAULT_TEMPERATURE,
    timeout=DEFAULT_TIMEOUT,
)

# ❌ 不推荐：硬编码数值
model = init_chat_model(
    "deepseek-chat",
    temperature=0,
    timeout=10,
)
```

---

## 7. 代码规范

### 7.1 类型提示规范

```python
from typing import Optional, List, Dict, Any

def query_database(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """执行数据库查询"""
    ...

def process_result(data: Any, format: str = "json") -> str:
    """处理查询结果"""
    ...
```

### 6.2 配置文件规范

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    deepseek_model: str = "deepseek-chat"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

### 6.3 SQLAlchemy 2.0 规范

```python
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text

Base = declarative_base()

class QueryHistory(Base):
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50))
    query_text = Column(Text, nullable=False)
    sql_generated = Column(Text)
    result_preview = Column(Text)
    created_at = Column(DateTime)
```

### 6.4 Pydantic V2 规范

```python
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    use_cache: bool = True

class QueryResponse(BaseModel):
    answer: str
    sql: Optional[str] = None
    data: Optional[List[Dict]] = None
    sources: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)
```

---

## 7. 安全规范

### 7.1 禁止的行为

```markdown
❌ 硬编码敏感信息（密码、API密钥、Token）
❌ 直接拼接 SQL（必须使用参数化查询）
❌ 在代码中包含真实的环境变量值
❌ 使用 eval() 执行动态代码
❌ 未验证的用户输入直接使用
❌ 暴露数据库连接凭据import os


### 7.2 必须遵守的规则

```markdown
✅ 所有敏感配置存储在 .env 文件
✅ API 密钥从环境变量读取（LangChain 会自动读取）
✅ 使用 SQLAlchemy ORM 进行数据库操作
✅ 输入验证使用 Pydantic schemas
✅ 遵循最小权限原则
✅ SQL 执行添加超时限制
✅ 敏感数据查询添加审计日志
✅ 使用 init_chat_model() 自动读取 API Key
```

---

## 8. 测试规范

### 8.1 测试文件结构

```python
# tests/test_query.py
import pytest
from fastapi.testclient import TestClient
from src.my_project.main import app

client = TestClient(app)

def test_query_endpoint():
    response = client.post("/query", json={"question": "查询所有用户"})
    assert response.status_code == 200
    assert "answer" in response.json()

def test_schema_endpoint():
    response = client.get("/schema")
    assert response.status_code == 200
    assert "tables" in response.json()
```

### 8.2 测试覆盖要求

- [ ] API 端点测试覆盖率 100%
- [ ] 核心业务逻辑单元测试
- [ ] 数据库操作集成测试
- [ ] Agent 响应验证测试

---

## 9. 环境变量规范

### 9.1 .env.example 模板

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Application
APP_PORT=8000
DEBUG=true
LOG_LEVEL=info

# AI Configuration
# DEEPSEEK_API_KEY 会自动从环境变量读取
# 只需设置环境变量即可，无需在此配置
DEEPSEEK_MODEL=deepseek-chat
```

---

## 10. Agent 开发规范

### 10.1 Agent 架构

```python
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

SYSTEM_PROMPT = """你是一个智能数据库助手，可以帮助用户查询和分析数据。
你有权限访问数据库工具来完成查询。
请根据用户的问题，生成相应的SQL查询并执行。"""

model = init_chat_model(
    "deepseek-chat",
    temperature=0,
    timeout=10,
    max_tokens=1000,
    extra_body={"thinking": {"type": "disabled"}}# 禁用思考模式, deepseek现在与langchain存在兼容性问题
)

agent = create_agent(
    model=model,
    tools=[execute_sql_tool, get_schema_tool],
    system_prompt=SYSTEM_PROMPT,
)
```

### 10.2 工具定义规范

```python
from langchain.agents import tool

@tool
def execute_sql(query: str) -> str:
    """执行SQL查询并返回结果"""
    result = db.execute(query)
    return format_results(result)

@tool
def get_schema(table_name: str = None) -> dict:
    """获取数据库结构信息"""
    schema = scanner.get_schema(table_name)
    return schema
```

### 10.3 初始化参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `model` | LLM 模型实例 | `init_chat_model("deepseek-chat")` |
| `tools` | Agent 可使用的工具列表 | `[execute_sql, get_schema]` |
| `system_prompt` | 系统提示词 | `SYSTEM_PROMPT` 变量 |

### 10.4 init_chat_model 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `temperature` | 生成随机性 | `0` |
| `timeout` | 请求超时时间(秒) | `10` |
| `max_tokens` | 最大生成令牌数 | `1000` |
| `extra_body` | 额外参数 | `{"thinking": {"type": "disabled"}}` |

### 10.5 多模型调用

```python
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from .constants import AVAILABLE_MODELS

def get_model(model_name: str):
    """根据模型名称获取对应的 LLM 实例"""
    model_config = AVAILABLE_MODELS.get(model_name)
    if not model_config:
        raise ValueError(f"Model {model_name} not supported")

    return init_chat_model(
        model=model_name,
        model_provider=model_config["provider"],
        temperature=0,
        timeout=10,
        extra_body={"thinking": {"type": "disabled"}}
    )

# 使用示例
model = get_model("deepseek-chat")  # DeepSeek
# model = get_model("gpt-4o")      # OpenAI
# model = get_model("claude-3-opus")  # Anthropic

agent = create_agent(
    model=model,
    tools=[execute_sql, get_schema],
    system_prompt=SYSTEM_PROMPT,
)
```

### 10.6 Checkpointer 记忆模块

#### 10.6.1 简介

Checkpointer 是 LangGraph 提供的持久化层，用于：
- **对话记忆**：存储对话历史，支持多轮对话
- **错误恢复**：从失败点恢复执行
- **人机交互**：支持工具审批、等待人工输入

#### 10.6.2 支持的存储类型

| 类型 | 类名 | 使用场景 | 安装依赖 |
|------|------|---------|---------|
| 内存 | `MemorySaver` | 开发/实验 | 内置 |
| SQLite | `SqliteSaver` | 本地/轻量级 | `langgraph-checkpoint-sqlite` |
| PostgreSQL | `PostgresSaver` | 生产环境 | `langgraph-checkpoint-postgres` |

#### 10.6.3 基础使用

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver

# 开发环境：使用内存存储
checkpointer = MemorySaver()

# 生产环境：使用 PostgreSQL 存储
# DB_URI = "postgresql://user:password@localhost:5432/dbname"
# with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
#     checkpointer.setup()
```

#### 10.6.4 带 Checkpointer 的 Agent

```python
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.postgres import PostgresSaver

# 初始化 checkpointer
DB_URI = "postgresql://user:password@localhost:5432/dbname"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()

    model = init_chat_model(
        "deepseek-chat",
        temperature=0,
        timeout=10,
        extra_body={"thinking": {"type": "disabled"}}
    )

    agent = create_agent(
        model=model,
        tools=[execute_sql, get_schema],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )

    # 调用时使用 thread_id 标识对话
    config = {"configurable": {"thread_id": "user_123_session_1"}}

    # 第一轮对话
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "查询所有用户"}]},
        config
    )

    # 第二轮对话（自动携带历史）
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "有多少用户？"}]},
        config
    )
```

#### 10.6.5 可配置模型（动态切换）

```python
from langchain.chat_models import init_chat_model

configurable_model = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    temperature=0,
    timeout=10,
)

# 运行时动态切换模型
result = configurable_model.invoke(
    "查询用户",
    config={"configurable": {
        "model": "gpt-4o",
        "model_provider": "openai"
    }}
)
```

---

## 11. Docker 部署规范

### 11.1 Dockerfile

```dockerfile
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

EXPOSE 8000

CMD ["uvicorn", "src.my_project.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 11.2 docker-compose.yml

```yaml
services:
  web:
    build: .
    container_name: ${PROJECT_NAME}-web
    ports:
      - "${APP_PORT:-8000}:8000"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network

  db:
    image: pgvector/pgvector:16
    container_name: ${PROJECT_NAME}-db
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
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
```

---

## 12. 验收检查清单

### 12.1 功能验证

- [ ] 应用可以正常启动
- [ ] API 端点可访问
- [ ] 数据库连接成功
- [ ] Agent 可以处理自然语言查询
- [ ] 查询结果正确返回
- [ ] Schema 信息正确展示

### 12.2 代码质量

- [ ] 无语法错误
- [ ] 所有函数有类型提示
- [ ] 导入语句正确
- [ ] 配置文件格式正确
- [ ] 无循环导入

### 12.3 安全性

- [ ] 无硬编码密钥
- [ ] 敏感信息在 .env 中
- [ ] SQL 注入防护
- [ ] 输入验证完整

### 12.4 部署验证

- [ ] Docker 构建成功
- [ ] docker-compose 启动成功
- [ ] 数据库初始化成功
- [ ] 环境变量配置正确

---

## 13. 特别注意事项

1. **不生成代码注释**（除非用户明确要求）
2. **使用现代 Python 语法**（3.12+）
3. **遵循项目现有风格**（如果存在）
4. **保持代码简洁**（避免不必要的复杂性）
5. **优先使用标准库**（减少依赖）
6. **使用 LangChain init_chat_model()**（无需显式传递 API Key）
7. **模型初始化采用 init_chat_model() 函数**（支持多种模型提供商）
8. **模型Tool定义采用 LangChain @tool 装饰器, 并且每个工具都需要由文本描述**（支持自定义工具）

---

## 14. 执行顺序

生成项目时的标准执行顺序：

1. 创建目录结构
2. 生成配置文件（pyproject.toml, .env.example, .gitignore）
3. 创建 Docker 配置
4. 实现核心代码文件
5. 添加测试文件
6. 初始化 Git 仓库
7. 验证项目完整性

---

**遵循此规范生成的项目代码将具备：可维护性、可扩展性、安全性和专业性。**
