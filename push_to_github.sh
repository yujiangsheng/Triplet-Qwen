#!/bin/bash
# 🚀 Triplet-Qwen GitHub 上传脚本
# 
# 这个脚本会将代码推送到您的GitHub仓库
# 
# 使用说明：
# 1. 修改下面的GitHub用户名为您自己的用户名
# 2. 确保您有GitHub访问权限（SSH密钥或访问令牌）
# 3. 运行此脚本：bash push_to_github.sh

# ============================================================================
# 配置信息 - 请根据您的实际情况修改
# ============================================================================

GITHUB_USER="yujiangsheng"
GITHUB_REPO="Triplet-Qwen"
GITHUB_URL="https://github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

# ============================================================================
# 执行上传
# ============================================================================

echo "🚀 开始推送代码到 GitHub..."
echo "仓库地址: ${GITHUB_URL}"
echo ""

# 添加远程仓库
echo "➕ 添加远程仓库..."
git remote add origin "${GITHUB_URL}" 2>/dev/null || git remote set-url origin "${GITHUB_URL}"

# 显示当前分支
echo "📍 当前分支:"
git branch

echo ""
echo "📤 推送代码到GitHub..."

# 推送到GitHub (main分支)
git push -u origin main

# 检查推送结果
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 代码已成功上传到GitHub!"
    echo ""
    echo "🔗 仓库地址: ${GITHUB_URL}"
    echo "📊 查看项目: https://github.com/${GITHUB_USER}/${GITHUB_REPO}"
else
    echo ""
    echo "❌ 推送失败，请检查:"
    echo "1. GitHub用户名和仓库名是否正确"
    echo "2. 是否有GitHub访问权限"
    echo "3. SSH密钥或访问令牌是否已配置"
    echo ""
    echo "🔧 常见解决方案:"
    echo "- 使用GitHub Personal Access Token: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens"
    echo "- 配置SSH密钥: https://docs.github.com/en/authentication/connecting-to-github-with-ssh"
fi
