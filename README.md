# 半路极客 · 反应力挑战

一个纯 Python + Bash 的反应力小游戏演示项目：等按钮变绿立刻点一下，测你的反应速度（毫秒），抢跑重来，自动记录最佳成绩。

## 文件

- `hy2.sh`：启动脚本，内嵌一个 Python http.server，打开即玩
- `app.py`：Pterodactyl / Nodaroo 这类 Python 面板的启动套层（面板只认 `.py` 文件，用它调 `bash hy2.sh`）

## 本地运行

```bash
bash hy2.sh
```

打开 http://127.0.0.1:8080/ 即可。端口在 `hy2.sh` 顶部 `PORT` 改。

## 部署到免费面板（Nodaroo 等）

1. 把 `hy2.sh` 和 `app.py` 传到服务器根目录
2. Startup 页的 PY_FILE 保持 `app.py`
3. `PORT` 改成 Network 里分配给你的端口
4. Console 点 Start

## 注意

本程序仅作演示使用。
