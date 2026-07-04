---
name: shixun-real-experiments
description: >-
  在 SimpleAI 人工智能实训项目（D:\Project\hw\实训）中，把某一章的实验做成"在实验服务器上对真实数据/真实图像
  真实执行"的成果——而不是用 make_blobs/make_moons/digits 这类合成数据糊弄。当用户说"完成实验""做实验""重做实验"
  "把这章做了"，尤其强调"要有实例图""要真实图片"（例如某个 BoVW 实验要出现真实的手风琴/accordion 图片），或者需要
  在那台不稳定的实验服务器（10.248.6.104，SSH 端口经常变）上跑 OpenCV/sklearn/matplotlib 并取回带中文标签的图表时，
  一律使用本 skill。它封装了这台服务器的连接韧性技巧（断点续传、nohup 后台跑+轮询、tar 一次性下载）、中文字体上传、
  以及把结果整理进各实验文件夹并生成中文终端截图的完整流水线。即使用户只说"这章截图搞一下"或"用真实数据跑一遍"，
  只要上下文是这个实训项目，也应该触发，不要退回去用合成数据。
---

# 实训真实实验流水线

## 这个 skill 解决什么问题

实训课程（`D:\Project\hw\实训`，见其 CLAUDE.md）的实验，早期版本图省事用了合成数据
（`sklearn.make_blobs` / `make_moons` / `digits`），出来的图表里没有一张真实图片。用户要的是
**真实实例图**：图像聚类实验要出现真实的人脸/物体，视觉词汇（BoVW）实验要画出真实手风琴上的 SIFT 特征点，
检索实验要展示"查询图 + 检索回来的真实图"。

正确做法是**在实验服务器上对真实数据集真实执行**，把带真实图片的图表取回来。服务器上有现成的数据集
（PCV 教材同款：`101_ObjectCategories` Caltech-101、人脸库等）和正确的库版本（OpenCV 3.4.2 带 SIFT）。
难点全在那条**极不稳定的三级 SSH 链路**上——这个 skill 把踩过的坑固化成可复用的脚本和步骤。

## 环境速查（细节见项目 CLAUDE.md）

- 服务器：`10.248.6.104`，user `root`，password `sshpassoword`，**SSH 端口经常变**（去项目 CLAUDE.md 的
  "SSH 端口历史"表查最新值；也可先 `echo >/dev/tcp/HOST/PORT` 探活）。
- 服务器 Python 3.6.9 / **OpenCV 3.4.2**（SIFT 用 `cv2.xfeatures2d.SIFT_create()`，**不是** `cv2.SIFT_create`）
  / sklearn 0.23.2 / matplotlib 3.3.3。**服务器没有中文字体**，要自己上传 `simhei.ttf`。
- 数据集根目录：`/simpleware_ro/.notebook/data/<课程>/` 和 `/simpleware_ro/.notebook/image/<课程>/`。
  计算机视觉相关在 `ComputerVision/`，里面有 `101_ObjectCategories/`（accordion、airplanes… 每类几十上百张）、
  人脸库 `HierarCluster/`、`SpectralClustering/`、`sift/`、`PCV/` 等。
- 本地 `py -3.11` 有 numpy/cv2/sklearn/matplotlib/PIL；中文字体 `C:\Windows\Fonts\simhei.ttf`（**文件名全小写**）。

## 核心工具：`scripts/srv.py`

一个韧性 SSH/SFTP 助手，**每次调用都新建连接**（这条链路一个 channel 撑不了几个操作）。用前先设置服务器地址：
编辑 `scripts/srv.py` 顶部的 `HOST/PORT/USER/PWD`，或复制到工作目录后改。提供：

- `connect(retries=4)` — 带重试的连接（首次读 banner 常失败，务必重试）。
- `run([cmd, ...])` — 一个会话里跑多条 shell 命令，返回合并输出。**命令要短、要快**。
- `download(pairs, per_conn=8)` — 断点续传下载，小批量重连、单文件失败自动重连、已存在文件跳过。
- `upload_resumable(local, remote)` — **追加模式断点续传上传**，唯一能把大文件（如 9.7MB 字体）传上去的办法。
- `listdir(remote)` — 列目录。

> 命令行直接用：`py -3.11 scripts/srv.py 'ls /tmp' 'hostname'`

## 标准流程

把这些做成 TodoList 逐项推进。**每一步之间连接会掉是常态**，掉了就重连重试，不要慌。

### 1. 探活 + 连通
从项目 CLAUDE.md 查当前 SSH 端口。`timeout 8 bash -c 'echo >/dev/tcp/10.248.6.104/PORT'` 探活，
再用 `srv.run(['hostname'])` 验证（首连常报 "Error reading SSH protocol banner"，重试即可）。
若端口变了，更新项目 CLAUDE.md 的端口历史表。

### 2. 定位真实数据集
`srv.run(['find /simpleware_ro/.notebook -iname "*关键词*"', 'ls .../101_ObjectCategories/'])`
找出这一章要用的真实图片目录和类别。**先搞清楚数据长什么样**，再设计实验——这决定了图表里能放什么实例图。

### 3. 上传中文字体（只需一次，字体会留在 `/tmp/simhei.ttf`）
```python
import srv
srv.run(['rm -f /tmp/simhei.ttf'])           # 先删干净，避免残留把追加上传搞脏
srv.upload_resumable(r'C:\Windows\Fonts\simhei.ttf', '/tmp/simhei.ttf')
# 校验：md5 必须和本地一致，且 matplotlib 能加载
```
**切勿并发跑多个上传**——追加模式并发会让文件超长损坏（踩过：变成 12.9MB > 源 9.7MB）。传完 `md5sum` 对一遍。

### 4. 写服务器端实验脚本
在本地写好一个自包含脚本，SFTP 上传到 `/tmp/`。脚本要点：
- 开头 `matplotlib.use('Agg')`，用 `FontProperties(fname='/tmp/simhei.ttf')` + `plt.rcParams['font.family']` 上中文。
- 对**真实图片**跑算法；每个实验存 `PNG` 到 `/tmp/out/`，写 `results.json`，`print` 中文日志（后面做终端截图用）。
- 用 `try/except` 包住每个实验，一个挂了不影响其它。
- 最后写一个 `/tmp/out/DONE` 标记文件，供轮询判断完成。
- 让结果**有意义、有实例图**：见 `references/experiment-recipes.md`（语义特征而非只看颜色、哈希用于近重复而非语义检索、
  图里直接画真实缩略图/关键点/查询-结果对）。

### 5. 后台执行 + 轮询
```bash
srv.run(['rm -rf /tmp/out && mkdir -p /tmp/out',
         'cd /tmp && nohup python3 -u 脚本.py > /tmp/out/log.txt 2>&1 & echo STARTED $!'])
```
**这一步的 exec channel 十有八九会挂/超时——这是正常的**（`&` 后台进程让 channel 不关闭）。别管它，进程已经
靠 nohup 跑起来了。**另开新连接**轮询：`test -f /tmp/out/DONE && echo DONE || echo RUNNING`，顺便 `tail log.txt`
看进度。跑完 `grep ERROR log.txt` 检查。

### 6. 打包 + 一次性下载
```bash
srv.run(['cd /tmp && tar czf out.tar.gz -C /tmp out'])
srv.download([('/tmp/out.tar.gz', '本地/out.tar.gz')])   # 一个文件比几十个小文件稳得多
```
本地解包。**逐个把关键图 Read 出来看**——确认中文没变成方框、结果合理（这一步不能省，字体没上好或算法有问题只有看图才知道）。

### 7. 整理进各实验文件夹 + 终端截图
每个实验一个文件夹（`01_xxx/`、`02_xxx/`…），清掉旧的合成结果文件，放入：真实结果图（中文名、编号排序）、
`code.py`（该实验真实运行代码）、`execution.log`（真实 stdout 段）、`results.json`、`terminal.png`（中文终端截图）。
终端截图用 `scripts/terminal_screenshot.py` 的 `create_terminal_screenshot(lines, title, 'terminal.png', output_dir=...)`，
`lines` 是 `(文本, 颜色)` 列表，从真实 log 上色而来。参考本次会话在项目里生成的 `organize.py` 模式。

### 8. 更新文档
更新项目 CLAUDE.md 对应章节：状态改为"真实实例图/服务器执行 + 日期"、列出新图表文件名、记录方法与关键指标。
主脚本、完整日志留一份在该章根目录（如 `run_experiments_real.py`、`execution_full.log`）。

## 收尾清理
删掉服务器上的临时打包（`/tmp/out.tar.gz`、`/tmp/ws*`），**保留** `/tmp/simhei.ttf` 供下次复用。
删本地未用的半截下载。

## 参考
- `references/connection.md` — 三级链路细节、端口/portproxy、以及每一类连接故障的对策（务必在链路抽风时读）。
- `references/experiment-recipes.md` — 怎样把实验设计得"结果有意义 + 有真实实例图"（计算机视觉这一章的具体配方）。
