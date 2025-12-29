"""
配置文件 - 系统参数和常量定义
"""

# ==================== 模型配置 ====================

# Qwen模型名称
QWEN_MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

# 模型生成参数
GENERATION_CONFIG = {
    "extraction": {
        "max_new_tokens": 256,
        "temperature": 0.3,  # 降低以获得更一致的结果
        "top_p": 0.9,
    },
    "revision": {
        "max_new_tokens": 256,
        "temperature": 0.3,
        "top_p": 0.9,
    },
    "validation": {
        "max_new_tokens": 256,
        "temperature": 0.3,
        "top_p": 0.9,
    }
}

# ==================== 双智能体系统配置 ====================

# 最大迭代次数
MAX_ITERATIONS = 3

# 语义角色定义
SEMANTIC_ROLES = {
    "AGENT": "ARG0",  # 施事者
    "PATIENT": "ARG1",  # 受事者
    "THEME": "ARG1",  # 主题
    "EXPERIENCER": "ARG0",  # 经历者
    "INSTRUMENT": "ARG2",  # 工具
    "CAUSE": "ARG2",  # 原因
}

# 修饰语类型
MODIFIER_TYPES = [
    "time",      # 时间
    "location",  # 地点
    "manner",    # 方式
    "cause",     # 原因
    "purpose",   # 目的
    "frequency", # 频度
    "duration",  # 持续时间
]

# 时间关键词（中英文）
TIME_KEYWORDS = {
    "zh": [
        "每天", "每月", "每年", "每周", "每小时",
        "早上", "晚上", "白天", "夜间", "午间", "清晨",
        "昨天", "今天", "明天", "后天", "前天",
        "今年", "去年", "明年",
        "当时", "那时", "此时", "现在"
    ],
    "en": [
        "every", "daily", "monthly", "yearly", "weekly", "hourly",
        "morning", "evening", "day", "night", "noon", "midnight",
        "yesterday", "today", "tomorrow",
        "this year", "last year", "next year",
        "then", "now", "at that time"
    ]
}

# 地点关键词（中英文）
LOCATION_KEYWORDS = {
    "zh": [
        "在", "地", "处", "里", "上", "下", "前", "后", "左", "右",
        "学校", "公园", "家", "办公室", "医院", "商店", "餐厅",
        "北京", "上海", "广州", "深圳"  # 示例城市
    ],
    "en": [
        "at", "in", "on", "by", "near", "beside", "inside", "outside",
        "school", "park", "home", "office", "hospital", "store", "restaurant",
        "London", "New York", "Paris"  # 示例城市
    ]
}

# 方式关键词（中英文）
MANNER_KEYWORDS = {
    "zh": [
        "快速", "缓慢", "仔细", "粗糙", "小心", "谨慎",
        "很", "非常", "特别", "相当", "比较",
        "轻轻", "轻快", "沉重", "急促"
    ],
    "en": [
        "quickly", "slowly", "carefully", "roughly", "cautiously",
        "very", "extremely", "particularly", "quite", "rather",
        "gently", "heavily", "rapidly"
    ]
}

# ==================== 输出配置 ====================

# 输出格式
OUTPUT_FORMAT = {
    "separator": "=" * 70,
    "subseparator": "-" * 70,
    "indentation": "  ",
}

# 结果保存路径
RESULTS_DIR = "results"
RESULTS_FILE = "results.json"

# ==================== 日志配置 ====================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "dual_agent.log"
