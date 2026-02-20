#!/bin/bash

# 杀掉旧进程
pkill -f "video-to-audio-converter/app.py" 2>/dev/null
pkill cloudflared 2>/dev/null
sleep 2

# 启动 Flask 服务
cd /Users/junshi/video-to-audio-converter
PORT=8888 /usr/local/bin/python3 app.py > /tmp/video-audio-flask.log 2>&1 &
sleep 3

# 启动 Cloudflare Tunnel
/usr/local/bin/cloudflared tunnel --url http://127.0.0.1:8888 > /tmp/video-audio-tunnel.log 2>&1 &
sleep 5

# 获取链接并显示
URL=$(grep -oE "https://[a-z0-9-]+\.trycloudflare\.com" /tmp/video-audio-tunnel.log | head -1)
echo "视频转音频服务已启动！"
echo "分享链接: $URL"

# 保存链接到文件
echo "$URL" > /tmp/video-audio-url.txt
