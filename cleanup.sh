#!/bin/bash
# 删除冗余文件的脚本

# 已过时的总结和日志文件
rm -f AGENT_A_COMPLETION_SUMMARY.txt
rm -f AGENT_A_SUMMARY.md
rm -f AGENT_A_UPDATES.md
rm -f AGENT_B_FILE_INDEX.md
rm -f AGENT_B_IMPLEMENTATION_SUMMARY.md
rm -f AGENT_B_IMPROVEMENT_GUIDE.md
rm -f AGENT_B_QUICK_START.md
rm -f CORRECTION_LOG.md
rm -f DELIVERY_CHECKLIST.md
rm -f DOCUMENTATION_INDEX.md
rm -f FILES_UPDATED.md
rm -f FINAL_DELIVERY_SUMMARY.txt
rm -f PROJECT_COMPLETION.md
rm -f PROJECT_DELIVERY_REPORT.md
rm -f PROJECT_SUMMARY.md
rm -f RESOURCE_INDEX.md
rm -f SYSTEM_EVOLUTION_SUMMARY.md

# 重复的示例文件
rm -f example_agent_a.py
rm -f example_agent_b_improvement.py

# 重复的指南和README
# (保留QUICKSTART.md、USAGE_GUIDE.md、README_EVOLUTION.md中最详细的)
# 本脚本只删除完全重复的文件

echo "清理完毕！已删除以下冗余文件："
echo "- Agent A/B的重复总结文档"
echo "- 项目完成声明（重复的总结）"
echo "- 日志和检查清单"
echo "- 重复的示例文件"
echo ""
echo "保留的主要文件："
echo "✓ 核心模块 (agent_a.py, agent_b.py等)"
echo "✓ 演化系统 (evolution_system.py, integrated_evolution.py等)"
echo "✓ 主要文档 (README.md, QUICKSTART.md, USAGE_GUIDE.md等)"
echo "✓ 示例代码 (evolution_examples.py)"
echo "✓ 测试 (test_integration.py)"
