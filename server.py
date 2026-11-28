#!/usr/bin/env python3
# 半路极客 · 反应力挑战 —— BotKeep 版
# 由 hy2.sh 改写：只用 Python 标准库，不装任何依赖。
# BotKeep 部署：新建 Python 任务，上传本文件（或推到 GitHub），
# 启动命令填：python3 server.py
# 端口：优先读环境变量 SERVER_PORT（BotKeep 官方文档要求监听这个），
# 再读 PORT，没有就用命令行参数，再没有就默认 8080。

import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


class Demo(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        page = """<!doctype html>
<html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>半路极客 · 反应力挑战</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#101920;color:#eff5ef;font:18px/1.5 system-ui,sans-serif;min-height:100vh;display:grid;place-items:center}
main{width:min(92vw,680px);padding:32px 0}header,footer{display:flex;justify-content:space-between;gap:16px;color:#afc3cb}header{border-bottom:1px solid #42545b;padding-bottom:14px}h1{font-size:clamp(38px,8vw,68px);margin:28px 0 0;letter-spacing:-.04em}p{color:#c5d4d8}
button{width:100%;min-height:210px;border:0;border-radius:18px;background:#d6ebff;color:#142432;font:700 clamp(24px,5vw,40px) system-ui;cursor:pointer;box-shadow:0 6px 0 #435b70;touch-action:manipulation}
button[data-state="wait"]{background:#ffc676}button[data-state="go"]{background:#66edaa}footer{margin-top:22px;font-size:15px}
</style><main><header><b>半路极客</b><span>Python 在线 · 端口 __PORT__</span></header>
<h1>反应力挑战</h1><p>等按钮变绿，立刻点一下！抢跑要重来。</p>
<button id="pad" type="button">开始挑战</button>
<footer aria-live="polite"><span id="last">本轮：待挑战</span><span id="record">最佳：—</span></footer></main>
<script>
const pad = document.querySelector('#pad');
const last = document.querySelector('#last');
const record = document.querySelector('#record');
let timer, started, best = Infinity;
pad.onclick = () => {
  if (pad.dataset.state === 'wait') {
    clearTimeout(timer);
    last.textContent = '本轮：抢跑';
    pad.textContent = '点早啦！再试一次';
  } else if (pad.dataset.state === 'go') {
    const ms = Math.round(performance.now() - started);
    best = Math.min(best, ms);
    last.textContent = '本轮：' + ms + ' ms';
    record.textContent = '最佳：' + best + ' ms';
    pad.textContent = '再挑战一次';
  } else {
    pad.dataset.state = 'wait';
    pad.textContent = '等绿灯…';
    last.textContent = '本轮：准备中';
    timer = setTimeout(() => {
      started = performance.now();
      pad.dataset.state = 'go';
      pad.textContent = '现在点！';
    }, 1200 + Math.random() * 2500);
    return;
  }
  pad.dataset.state = 'idle';
};
</script></html>""".replace("__PORT__", str(self.server.server_port)).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)


def get_port():
    # 1. 环境变量 SERVER_PORT（BotKeep 官方文档要求监听这个端口）
    # 2. 环境变量 PORT（其他平台常用）
    for key in ("SERVER_PORT", "PORT"):
        env_port = os.environ.get(key)
        if env_port:
            try:
                return int(env_port)
            except ValueError:
                pass
    # 2. 命令行参数：python3 server.py 8080
    if len(sys.argv) > 1:
        try:
            return int(sys.argv[1])
        except ValueError:
            pass
    # 3. 默认
    return 8080


port = get_port()
if not 1 <= port <= 65535:
    sys.exit("端口号必须是 1 到 65535 之间的整数。")

try:
    server = HTTPServer(("0.0.0.0", port), Demo)
except OSError as error:
    sys.exit(f"端口 {port} 启动失败：{error}")

with server:
    print(f"服务已启动，监听端口：{port}", flush=True)
    print("按 Ctrl+C 停止服务。", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
