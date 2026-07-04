# 实验服务器连接：链路、端口、故障对策

## 三级链路

```
家里电脑 (10.248.6.104:PORT 虚拟IP)
  → netsh portproxy → Radmin VPN
  → 校园电脑 (26.23.91.19:PORT)
  → netsh portproxy → 校园内网
  → 实验服务器 (10.248.6.104:PORT)
```

正因为要穿三跳 + Radmin VPN，这条链路**带宽小、易抖动、SFTP 连接常在传几个文件后就断**。所有脚本都按
"每次操作新建连接 + 重试 + 断点续传"来设计，不要假设一个连接能撑住一批操作。

## SSH 端口

端口**经常变**（每隔几天就换）。当前值和历史在**项目 CLAUDE.md 的"SSH 端口历史"表**里，用前先查。
探活：

```bash
timeout 8 bash -c 'echo >/dev/tcp/10.248.6.104/PORT' && echo OK || echo CLOSED
```

端口一变，家里电脑和校园电脑两端都要加对应的 portproxy 规则（需管理员权限，见项目 CLAUDE.md
"端口转发配置"），并更新 `srv.py` 顶部的 `PORT` 与 CLAUDE.md 端口历史表。

## 虚拟 IP 丢失（重启后常见）

`10.248.6.x` 虚拟 IP 掉了要重新绑（管理员 PowerShell，见项目 CLAUDE.md "虚拟 IP 绑定"）。
症状：探活直接 CLOSED，且 portproxy 规则在但连不通。

## 故障对照表

| 症状 | 原因 | 对策 |
|------|------|------|
| `Error reading SSH protocol banner` | 链路慢/首连握手超时 | **重试**（`connect()` 已内置 retries + banner_timeout=25），一般第 2 次就成 |
| 探活 OK 但认证/banner 一直失败 | portproxy 应答了但后端没真正转发 | 检查校园电脑那端 portproxy、端口是否又变了 |
| SFTP 传到第 3 个文件就 `Socket is closed` / `Server connection dropped` | 链路撑不住持续 SFTP | 用 `download()` 的小批量重连；**更优：服务器先 `tar` 打包成一个文件再拉** |
| `upload_resumable` 传出来的文件比源**更大**、损坏 | 并发跑了多个追加上传 | 只跑一个上传；先 `rm -f` 远端残留再传；传完 `md5sum` 校验 |
| `nohup ... &` 那条 `run()` 超时/挂住 | 后台进程让 exec channel 不关闭 | **正常现象**，进程已在跑；**另开连接**轮询 `/tmp/out/DONE` |
| 大文件下载中途断 | 链路抖动 | `download()` 会跳过已完成、续传；小文件优先走 tar 打包 |

## 反复用到的命令片段

```python
import srv
# 探数据集
srv.run(['find /simpleware_ro/.notebook -iname "*accordion*"',
         'ls /simpleware_ro/.notebook/data/ComputerVision/'])
# 上传脚本（小文件一发即中，失败就 upload_resumable）
srv.upload_resumable('exp.py', '/tmp/exp.py')
# 后台跑（这条会"超时"，无视）
srv.run(['rm -rf /tmp/out && mkdir -p /tmp/out',
         'cd /tmp && nohup python3 -u exp.py > /tmp/out/log.txt 2>&1 & echo STARTED $!'])
# 另开连接轮询
srv.run(['test -f /tmp/out/DONE && echo DONE || echo RUNNING', 'tail -8 /tmp/out/log.txt'])
# tar 打包一次性下载
srv.run(['cd /tmp && tar czf out.tar.gz -C /tmp out'])
srv.download([('/tmp/out.tar.gz', 'out.tar.gz')])
```

## 服务器目录速览（计算机视觉相关）

- `/simpleware_ro/.notebook/data/ComputerVision/`
  - `101_ObjectCategories/` — Caltech-101，`accordion/ airplanes/ camera/ elephant/ ...` 每类 `image_XXXX.jpg`
  - `HierarCluster/` — 人脸库（abma=奥巴马, bush, jobs, putin, hawei…）+ `hcluster.py`，层次聚类用
  - `SpectralClustering/` — 同一批人脸 + `numbers.jpg`，谱聚类用
  - `sift/` `PCV/` `PCV2/` `harris/` `result_sort/` — PCV 教材配套
- `/simpleware_ro/.notebook/image/<课程>/` — 各章节讲义配图（285MB）
- 完整课程/目录清单见项目 `download_server_images.py` 内置列表。
