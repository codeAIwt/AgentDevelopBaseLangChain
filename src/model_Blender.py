import os
import subprocess
import platform
from langchain_community.llms import CTransformers
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ===================== 跨平台配置 =====================
def get_blender_path():
    """自动检测操作系统并返回正确的 Blender 路径"""
    system = platform.system()

    if system == "Windows":
        # Windows 路径
        return r"D:\MyAPP\Blender\blender-launcher.exe"
    elif system == "Linux":
        # WSL 中访问 Windows Blender
        # 检查 /mnt/d/ 是否存在（WSL 访问 Windows 磁盘）
        if os.path.exists("/mnt/d/MyAPP/Blender"):
            return "/mnt/d/MyAPP/Blender/blender-launcher.exe"
        # 检查其他常见位置
        elif os.path.exists("/usr/bin/blender"):
            return "/usr/bin/blender"
        else:
            raise FileNotFoundError("未找到 Blender，请检查配置")
    else:
        raise OSError(f"不支持的操作系统: {system}")


# 获取 Blender 路径
BLENDER_PATH = get_blender_path()
print(f"✅ 检测到 Blender: {BLENDER_PATH}")


# WSL 共享目录（用于 Windows 和 WSL 之间交换文件）
WSL_SHARE_DIR = "/mnt/d/WSL_Blender_Temp/"

# 模型文件路径
if platform.system() == "Linux":
    # Linux/WSL 路径
    MODEL_FILE = "/mnt/d/WSL_Blender_Temp/models/qwen2.5-coder-3b-instruct-q5_k_m.gguf"
else:
    # Windows 路径
    MODEL_FILE = r"D:\WSL_Blender_Temp\models\qwen2.5-coder-3b-instruct-q5_k_m.gguf"


# 创建共享目录（如果不存在）
os.makedirs(WSL_SHARE_DIR, exist_ok=True)
os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
# =======================================================


# 全局极简约束
SYSTEM_RULE = """
角色：Blender代码生成器｜只输出纯Python代码
约束：
- 底模纯四边面，无三角/N-gon
- 只用挤出/环切/倒角/缩放
- 禁止三角化/细分
- 不解释、无注释、无空行
"""

# Blender固定模板
BLENDER_TEMPLATE = """
import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 建模逻辑
{{CODE}}

# 相机灯光
bpy.ops.object.camera_add(location=(5,-5,5))
bpy.ops.object.light_add(type='SUN', location=(5,5,5))
"""


# --------------------------
# 纯CPU模型初始化（全局只加载一次）
# --------------------------
def init_llm(max_tokens: int):
    """初始化纯CPU大模型，全局只加载一次，节省时间"""
    print(f"🔄 加载模型... (max_tokens={max_tokens})")

    return CTransformers(
        model=MODEL_FILE,
        model_type="qwen2",  # 根据模型类型修改：qwen2/llama/deepseek
        config={
            "max_new_tokens": max_tokens,
            "temperature": 0.1,
            "context_length": 1024,
            # CPU优化参数
            "threads": os.cpu_count(),  # 使用所有CPU核心
            "batch_size": 8,
            "top_k": 40,
            "top_p": 0.95,
            "stream": False
        }
    )


# 全局预加载模型（只加载一次，避免每次调用都重新加载）
print("🚀 初始化 LLM 模型...")
planner_llm = init_llm(100)
modeling_llm = init_llm(350)
print("✅ 模型加载完成")


# --------------------------
# 极简双Agent（纯CPU版）
# --------------------------
def planner_agent(user_prompt: str) -> str:
    """规划Agent：仅解析需求，输出纯任务描述"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_RULE),
        ("human", "任务：{input}")
    ])
    chain = prompt | planner_llm | StrOutputParser()
    return chain.invoke({"input": user_prompt})


def modeling_agent(task_desc: str) -> str:
    """建模Agent：基于模板补全代码"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_RULE),
        ("human", f"补全{{{{CODE}}}}实现：{task_desc}\n模板：{BLENDER_TEMPLATE}")
    ])
    chain = prompt | modeling_llm | StrOutputParser()
    return chain.invoke({})


# --------------------------
# Blender执行+四边面校验
# --------------------------
def run_and_validate(blender_code: str):
    # 追加拓扑校验代码
    full_code = blender_code + """
import bpy
tris=0
for o in bpy.data.objects:
    if o.type=='MESH':
        for f in o.data.polygons:
            if len(f.vertices)==3:tris+=1
print(f"【拓扑】{'通过' if tris==0 else f'警告：{tris}个三角面'}")
"""

    # 在共享目录保存脚本
    script_path = os.path.join(WSL_SHARE_DIR, "temp_model.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(full_code)

    print(f"📝 脚本已保存: {script_path}")
    print(f"🚀 启动 Blender...")

    # 根据操作系统选择执行方式
    system = platform.system()
    if system == "Windows":
        # Windows 直接执行
        cmd = [BLENDER_PATH, "--background", "--python", script_path]
    else:
        # WSL 执行 Windows 程序
        cmd = ["cmd.exe", "/c", f'"{BLENDER_PATH}"', "--background", "--python", script_path]

    print(f"命令: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=60
        )

        # 只打印关键结果
        for line in result.stdout.split("\n"):
            if "【拓扑】" in line:
                print(line)

        if result.stderr:
            # 过滤掉 Blender 的警告信息
            errors = [line for line in result.stderr.split("\n")
                     if "Warning" not in line and line.strip()]
            if errors:
                print("错误：", "\n".join(errors))

    except subprocess.TimeoutExpired:
        print("❌ Blender 执行超时（60秒）")
    except Exception as e:
        print(f"❌ 执行失败: {str(e)}")

    # 清理临时文件
    if os.path.exists(script_path):
        os.remove(script_path)


# --------------------------
# 主流程
# --------------------------
if __name__ == "__main__":
    # 修改这里的需求即可
    user_requirement = "制作一个带抽屉的简约床头柜底模，两个抽屉，四条腿"

    print(f"\n{'='*60}")
    print(f"需求：{user_requirement}")
    print(f"{'='*60}\n")

    print("⏳ 正在加载模型并生成...")

    task = planner_agent(user_requirement)
    print(f"📋 规划结果：{task}")

    code = modeling_agent(task)
    print(f"\n🔧 生成的代码：\n{code}")

    run_and_validate(code)

    print("\n✅ 建模完成")
