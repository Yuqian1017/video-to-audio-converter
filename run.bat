@echo off
chcp 65001 >nul
title 视频转音频工具

echo ================================
echo    视频转音频工具 启动中...
echo ================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未安装 Python，请先安装
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 安装依赖
echo 📦 检查依赖...
pip install -q flask yt-dlp 2>nul

echo.
echo ✅ 启动成功！
echo.
echo 🌐 打开浏览器访问: http://127.0.0.1:8080
echo.
echo 按 Ctrl+C 停止服务
echo ================================
echo.

REM 打开浏览器
start http://127.0.0.1:8080

REM 启动 Flask
python app.py

pause
