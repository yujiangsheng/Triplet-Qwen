#!/usr/bin/env python3
"""
快速启动演化演示的脚本

这个脚本提供了快速选择不同演化演示的菜单
"""

import os
import sys


def print_banner():
    """打印欢迎横幅"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║           🚀 Agent 演化演示启动器                                 ║
║                                                                    ║
║    观察Agent A和B从60%准确率逐步改进到94%准确率的过程          ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)


def show_menu():
    """显示菜单"""
    print("\n选择您想要的演化演示:\n")
    
    demos = [
        {
            'num': 1,
            'name': '可视化演化展示',
            'file': 'evolution_demo.py',
            'desc': '实时展示10轮演化过程，包含性能指标和改进说明',
            'time': '~3-5分钟',
            'level': '初级 ⭐'
        },
        {
            'num': 2,
            'name': '交互式演化分析',
            'file': 'interactive_evolution_demo.py',
            'desc': '深入分析Agent学习过程、规则演化、反馈循环',
            'time': '~15分钟',
            'level': '中级'
        },
        {
            'num': 3,
            'name': '完整示例代码',
            'file': 'evolution_examples.py',
            'desc': '5个完整的Python代码示例，展示API使用',
            'time': '~5-10分钟',
            'level': '中级'
        },
        {
            'num': 4,
            'name': '演化演示指南',
            'file': 'EVOLUTION_DEMO_GUIDE.md',
            'desc': '详细的文字说明文档，包含原理、建议和分析',
            'time': '~20分钟阅读',
            'level': '高级'
        },
    ]
    
    for demo in demos:
        print(f"\n{demo['num']}️⃣  {demo['name']}")
        print(f"   📄 文件: {demo['file']}")
        print(f"   📝 说明: {demo['desc']}")
        print(f"   ⏱️  耗时: {demo['time']}")
        print(f"   📊 难度: {demo['level']}")
    
    print("\n0️⃣  退出")
    print("\n" + "-" * 68)


def run_demo(choice):
    """运行选中的演化演示"""
    
    demos = {
        '1': ('evolution_demo.py', 'python3 evolution_demo.py'),
        '2': ('interactive_evolution_demo.py', 'python3 interactive_evolution_demo.py'),
        '3': ('evolution_examples.py', 'python3 evolution_examples.py'),
        '4': ('EVOLUTION_DEMO_GUIDE.md', None),  # 文档文件，无法直接执行
    }
    
    if choice not in demos:
        print("\n❌ 无效选择！")
        return False
    
    file_name, command = demos[choice]
    
    # 检查文件是否存在
    if not os.path.exists(file_name):
        print(f"\n❌ 文件不存在: {file_name}")
        return False
    
    print(f"\n{'=' * 68}")
    print(f"▶️  启动: {file_name}")
    print(f"{'=' * 68}\n")
    
    if choice == '4':
        # 打开文档
        print("📖 演化演示指南内容:\n")
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                # 只显示前50行
                lines = content.split('\n')[:50]
                for line in lines:
                    print(line)
                print(f"\n... (查看完整内容请打开 {file_name})")
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
    else:
        # 运行Python脚本
        exit_code = os.system(command)
        return exit_code == 0
    
    return True


def show_recommendations():
    """显示推荐"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                          推荐使用流程                              ║
╚════════════════════════════════════════════════════════════════════╝

🎯 如果您是第一次使用:
   1️⃣ 运行可视化演化展示 (选项1)
      → 快速了解演化全过程 (3-5分钟)
   
   2️⃣ 阅读演化演示指南 (选项4)
      → 深入理解演化原理 (20分钟)
   
   3️⃣ 运行交互式演化分析 (选项2)
      → 深度分析具体细节 (15分钟)

🎓 如果您想学习代码:
   1️⃣ 运行完整示例代码 (选项3)
      → 看实际API使用 (5-10分钟)
   
   2️⃣ 查看源代码
      → 阅读evolution_system.py等

💡 推荐首次选择: 选项1 (可视化演化展示) ⭐

""")


def main():
    """主程序"""
    print_banner()
    show_recommendations()
    
    while True:
        show_menu()
        choice = input("请选择 (0-4): ").strip()
        
        if choice == '0':
            print("\n👋 感谢使用Agent演化演示!")
            break
        
        if choice in ['1', '2', '3', '4']:
            success = run_demo(choice)
            if choice in ['1', '2', '3'] and success:
                print("\n✅ 演示完成！")
            elif choice == '4':
                print("\n✅ 文档预览完成！(完整内容在 EVOLUTION_DEMO_GUIDE.md)")
        else:
            print("\n❌ 无效选择，请重试")
        
        if choice != '0':
            input("\n按Enter键返回菜单...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 再见！")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
