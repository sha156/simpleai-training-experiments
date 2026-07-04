# shixun-real-experiments — 实训真实实验流水线 Skill

> Claude Code Skill：在 SimpleAI 实训服务器上对真实数据跑实验、取回带中文图表的完整流水线。
> 封装了三级 SSH 链路的连接韧性技巧、中文字体处理、以及实验成果整理的所有踩坑经验。

## 这是什么

这个 skill 是给 Claude Code 用的自动化流水线——当你对 Claude 说"把这章的实验用真实数据做一遍"，它会自动：

1. 连接那台**极不稳定**的实验服务器（10.248.6.104，三级 SSH 链路）
2. 上传中文字体、实验脚本
3. 后台执行实验（nohup）
4. 轮询等待完成
5. 打包下载结果
6. 整理进本地实验文件夹
7. 生成中文终端截图

## 文件结构

```
skill/
├── README.md                           ← 本文件
├── SKILL.md                            ← Skill 定义（触发条件、标准流程）
├── references/
│   ├── connection.md                   ← 链路/端口/故障对策
│   └── experiment-recipes.md           ← 实验设计配方（怎样让结果有意义）
└── scripts/
    ├── srv.py                          ← 韧性 SSH/SFTP 助手
    └── terminal_screenshot.py          ← 终端风格截图工具
```

## 安装

把这个 `skill/` 目录复制到 Claude Code 的 skills 目录：

```bash
cp -r skill/shixun-real-experiments ~/.claude/skills/
```

或者软链接（推荐，方便同步更新）：

```bash
# Windows (管理员 PowerShell)
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\shixun-real-experiments" `
  -Target "D:\Project\hw\实训\全部实验\skill"
```

## 使用方式

对 Claude Code 说下面任意一句就能触发：

- "完成第 X 章实验"
- "用真实数据重做这章"
- "这章截图搞一下，要有实例图"
- "把图像聚类的实验在服务器上跑一遍"

### 前置条件

1. **SSH 链路必须通**。先确认 Radmin VPN 已连接、虚拟 IP 已绑定、portproxy 规则已配好。（详见 `references/connection.md`）
2. **`srv.py` 端口要正确**。编辑 `scripts/srv.py` 顶部的 `PORT`，去项目 CLAUDE.md 的"SSH 端口历史"表查最新值。
3. **本地 Python 3.11**：`py -3.11` 可用，装了 `paramiko`、`Pillow`。

### 命令行直接使用脚本

```bash
# 测试连接
py -3.11 skill/scripts/srv.py 'hostname' 'df -h /'

# 生成终端截图
py -3.11 -c "
from skill.scripts.terminal_screenshot import create_terminal_screenshot, GREEN, CYAN
create_terminal_screenshot(
    [('$ python3 run.py', '#569CD6'), ('✓ 实验完成', GREEN)],
    '测试标题', 'test.png', output_dir='.'
)
"
```

## 核心工具详解

### `srv.py` — 韧性 SSH/SFTP 助手

三级链路极不稳定，每个操作都可能断。这个脚本的策略：

| 方法 | 策略 | 用途 |
|------|------|------|
| `connect(retries=4)` | 首次常报 banner 错，自动重试 | 建立连接 |
| `run(cmds)` | 一个会话跑多条短命令 | 探活、查目录、起 nohup |
| `download(pairs, per_conn=8)` | 小批量重连、断点续传、已存在跳过 | 下载结果文件 |
| `upload_resumable(local, remote)` | **追加模式**断点续传 | 上传大文件（字体 9.7MB） |
| `listdir(remote)` | 列目录 | 探索数据集 |

### `terminal_screenshot.py` — 终端截图工具

用 Pillow 画 Windows Terminal 深色主题风格的 PNG 截图，支持：
- 中文字体（黑体）
- 等宽字体（Cascadia Code）
- 语法高亮着色
- 标题栏 + 提示符行

```python
from terminal_screenshot import create_terminal_screenshot, GREEN, YELLOW, CYAN, RED, FG

lines = [
    ('$ python3 run_experiments.py    # 服务器真实执行', '#569CD6'),
    ('', FG),
    ('=' * 60, GREEN),
    ('  实验3-1: 层次聚类 — 对真实人脸图像', YELLOW),
    ('=' * 60, GREEN),
    ('加载图片: accordion/image_0001.jpg ...', FG),
    ('✓ 树状图已保存, 轮廓系数=0.12', GREEN),
]
create_terminal_screenshot(lines, '实验3-1 层次聚类 (SimpleAI 10.248.6.104)',
                           'terminal.png', output_dir='./output', font_size=14, width=980)
```

## ⚠️ 需要注意的地方（关键踩坑记录）

### 1. 端口会变

SSH 端口每隔几天就换一次。**每次跑实验前先查**项目 CLAUDE.md 的"SSH 端口历史"表取最新值，更新 `srv.py` 里的 `PORT`。端口变了还要两边加 portproxy 规则。

```bash
# 快速探活
timeout 8 bash -c 'echo >/dev/tcp/10.248.6.104/21746' && echo OK || echo CLOSED
```

### 2. 虚拟 IP 重启后会丢

Windows 重启后 `10.248.6.x` 虚拟 IP 会消失，需要重新绑定（管理员 PowerShell）：

```powershell
netsh interface ip add address "Radmin VPN" 10.248.6.104 255.255.255.255 skipassource=true
Restart-Service iphlpsvc -Force
```

### 3. 上传文件切勿并发

`srv.upload_resumable()` 用**追加模式**。如果同时跑多个上传，文件会变成两份内容拼在一起，比源文件大且损坏。**每次只跑一个上传**，传完 `md5sum` 校验：

```bash
# 服务器上
md5sum /tmp/simhei.ttf
# 本地
certutil -hashfile C:\Windows\Fonts\simhei.ttf MD5
```

### 4. nohup 启动那步一定会"超时"

`run(['cd /tmp && nohup python3 -u exp.py & echo STARTED'])` 这条命令会因为 `&` 后台进程导致 exec channel 挂住/超时——**这是正常的**，进程已经在服务器上用 nohup 跑起来了。别慌，**另开新连接**轮询：

```python
srv.run(['test -f /tmp/out/DONE && echo DONE || echo RUNNING', 'tail -8 /tmp/out/log.txt'])
```

### 5. 下载优先走 tar 打包

直接 SFTP 拉几十个小文件，传到第 3-4 个就会掉。正确做法：

```python
srv.run(['cd /tmp && tar czf out.tar.gz -C /tmp out'])  # 服务器打包
srv.download([('/tmp/out.tar.gz', '本地/out.tar.gz')])   # 一个文件拉下来
```

### 6. 中文字体必须上传

服务器 Ubuntu 18.04 **没有中文字体**，matplotlib 画出来的中文全是方框。要上传 `simhei.ttf` 到 `/tmp/`，实验脚本里手动加载：

```python
from matplotlib import font_manager as fm
fm.fontManager.addfont('/tmp/simhei.ttf')
FP = fm.FontProperties(fname='/tmp/simhei.ttf')
plt.rcParams['font.family'] = FP.get_name()
plt.rcParams['axes.unicode_minus'] = False
```

### 7. OpenCV 版本差异

服务器是 **OpenCV 3.4.2**，SIFT 用 `cv2.xfeatures2d.SIFT_create()`，**不是** `cv2.SIFT_create()`（那是 4.x 的 API）。本地写脚本时注意兼容。

### 8. 服务器 Python 是 3.6.9

不支持 f-string 里的 `{var=}` 调试语法、不支持 `str | None` 类型注解、不支持 `pathlib` 的部分新方法。写实验脚本用最朴素的 Python 3.6 语法。

### 9. 生成截图后必须肉眼检查

终端截图（terminal.png）生成后，**务必 Read 出来看**：
- 中文是否正常渲染（不是方框）
- 图表里的中文标签是否正常
- 结果是否合理

字体没上好或算法有问题，只有看图才能发现，不能依赖自动化检查。

### 10. 链路断开是常态，不要慌

这条三级链路（Radmin VPN → 校园电脑 → 实验服务器）在任何一步都可能断。`srv.py` 已经内置了重试逻辑，断了大不了重连。心态放平，每一步之间连接掉是正常现象。

## 标准流程速查

```
1. 探活 → 更新端口 → srv.run(['hostname'])
2. 定位数据集 → find /simpleware_ro/.notebook -iname "*关键词*"
3. 上传字体 → upload_resumable (只跑一次, md5 校验)
4. 写实验脚本 → 本地写好, SFTP 上传
5. 后台执行 → nohup python3 -u 脚本.py & (会超时, 正常)
6. 轮询等待 → 另开连接 test -f /tmp/out/DONE
7. tar 打包 → 一次性下载
8. 整理分发 → 每个实验文件夹: PNG + execution.log + results.json + terminal.png
9. 截图验证 → 逐个 Read 检查中文/结果
10. 更新文档 → 更新 CLAUDE.md 章节状态
```

## 环境信息

| 项目 | 值 |
|------|-----|
| 服务器 IP | 10.248.6.104（通过 Radmin VPN 虚拟 IP） |
| 服务器系统 | Ubuntu 18.04.5 LTS |
| Python | 3.6.9 |
| OpenCV | 3.4.2（SIFT 用 xfeatures2d） |
| scikit-learn | 0.23.2 |
| matplotlib | 3.3.3 |
| SSH 用户 | root |
| 数据集路径 | `/simpleware_ro/.notebook/data/` |
| 讲义图片路径 | `/simpleware_ro/.notebook/image/` |
