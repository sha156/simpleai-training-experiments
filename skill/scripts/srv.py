"""韧性 SSH/SFTP 助手 —— 实训实验服务器（三级链路极不稳定，每次调用都新建连接）。
用法：
    py -3.11 srv.py 'ls /tmp' 'hostname'          # 命令行跑 shell
    import srv; srv.run([...]) / srv.download([...]) / srv.upload_resumable(...)
先按需修改下面的 HOST/PORT（端口经常变，去项目 CLAUDE.md 的"SSH 端口历史"查最新值）。"""
import paramiko, time, os, sys

HOST, PORT, USER, PWD = '10.248.6.104', 21746, 'root', 'sshpassoword'


def connect(retries=4):
    """带重试连接。首连常报 'Error reading SSH protocol banner'，重试即可。"""
    last = None
    for _ in range(retries):
        try:
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(HOST, port=PORT, username=USER, password=PWD,
                      timeout=25, banner_timeout=25, auth_timeout=25)
            return c
        except Exception as e:
            last = e
            time.sleep(3)
    raise last


def run(cmds):
    """一个会话里跑多条 shell 命令，返回合并输出。命令要短要快——链路撑不了长任务。
    注意：带后台 '&' 的命令（如 nohup ... &）会让 channel 挂住/超时，这是正常的，
    进程已经跑起来了，另开连接轮询即可。"""
    c = connect()
    out = []
    try:
        for cmd in cmds:
            i, o, e = c.exec_command(cmd, timeout=60)
            out.append('$ ' + cmd + '\n' +
                       o.read().decode('utf-8', 'replace') +
                       e.read().decode('utf-8', 'replace'))
    finally:
        c.close()
    return '\n'.join(out)


def download(pairs, per_conn=8, tries=4):
    """pairs=[(remote, local), ...]。断点续传：已存在的非空文件跳过；小批量重连；
    单文件失败自动新连重试。返回 [(local, bytes|'ERR:...'), ...]。
    经验：直接 SFTP 拉几十个小文件会掉；更稳的是先在服务器 tar 打包成一个文件再 download。"""
    res = []
    todo = [(r, l) for r, l in pairs if not (os.path.exists(l) and os.path.getsize(l) > 0)]
    for r, l in pairs:
        if (r, l) not in todo:
            res.append((l, os.path.getsize(l)))
    i = 0
    while i < len(todo):
        batch = todo[i:i + per_conn]
        c = None
        try:
            c = connect(); sftp = c.open_sftp()
            for remote, local in batch:
                ok = False
                for _ in range(tries):
                    try:
                        os.makedirs(os.path.dirname(local) or '.', exist_ok=True)
                        sftp.get(remote, local); res.append((local, os.path.getsize(local)))
                        ok = True; break
                    except Exception:
                        break  # 连接多半死了 -> 跳出去重连
                if not ok:
                    last = 'unknown'
                    try: c.close()
                    except Exception: pass
                    for _ in range(tries):
                        try:
                            c = connect(); sftp = c.open_sftp()
                            sftp.get(remote, local); res.append((local, os.path.getsize(local)))
                            ok = True; break
                        except Exception as e:
                            last = e; time.sleep(2)
                    if not ok:
                        res.append((local, 'ERR:' + str(last)))
        finally:
            try: c.close()
            except Exception: pass
        i += per_conn
    return res


def upload_resumable(local, remote, chunk=131072, tries=60):
    """追加模式断点续传上传——唯一能把大文件（如 9.7MB 字体）传上去的办法。
    每次从远端已有大小续传。切勿并发跑多个上传：追加模式并发会把文件搞超长损坏！
    传完务必 md5sum 和本地比对。"""
    total = os.path.getsize(local)
    for _ in range(tries):
        c = None
        try:
            c = connect(); sftp = c.open_sftp()
            try: have = sftp.stat(remote).st_size
            except IOError: have = 0
            if have >= total:
                sftp.close(); c.close(); return have
            with open(local, 'rb') as fh:
                fh.seek(have)
                rf = sftp.open(remote, 'ab'); rf.set_pipelined(True)
                while True:
                    buf = fh.read(chunk)
                    if not buf: break
                    rf.write(buf)
                rf.close()
            sftp.close(); c.close()
            c = connect(); sftp = c.open_sftp()
            sz = sftp.stat(remote).st_size; sftp.close(); c.close()
            if sz >= total: return sz
        except Exception:
            try: c.close()
            except Exception: pass
            time.sleep(2)
    raise RuntimeError('upload incomplete for ' + remote)


def listdir(remote):
    c = connect()
    try:
        return sorted(c.open_sftp().listdir(remote))
    finally:
        c.close()


if __name__ == '__main__':
    print(run(sys.argv[1:] or ['hostname']))
