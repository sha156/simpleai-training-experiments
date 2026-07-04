#!/usr/bin/env python3
"""真实执行源码 — 15_13_爬虫法律法规"""
def exp_15_13():
    """实验13: 爬虫法律与道德规范"""
    eid = '15_13_爬虫法律法规'
    d = exp_start(eid, '爬虫法律规范')
    files = []

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('off')

    rules = [
        ('✓', '遵守robots.txt', '#4CAF50'),
        ('✓', '控制请求频率 (不造成服务器负担)', '#4CAF50'),
        ('✓', '仅抓取公开数据', '#4CAF50'),
        ('✓', '标识User-Agent (表明身份)', '#4CAF50'),
        ('✓', '遵守网站ToS (服务条款)', '#4CAF50'),
        ('✗', '绕过认证/付费墙', '#F44336'),
        ('✗', '抓取个人隐私数据', '#F44336'),
        ('✗', 'DDOS式高并发请求', '#F44336'),
        ('✗', '商业机密/版权内容', '#F44336'),
        ('✗', '破解验证码绕过保护', '#F44336'),
    ]

    for i, (icon, rule, color) in enumerate(rules):
        y = 0.9 - i * 0.09
        ax.text(0.1, y, f'{icon} {rule}', fontsize=12, fontproperties=FONT,
                color=color, transform=ax.transAxes)

    ax.set_title('网络爬虫法律法规与道德规范', fontproperties=FONT, fontsize=14)
    p1 = os.path.join(d, '01_爬虫法律法规.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})


# ══════════════════════════════════════════════════════════════
#  第18章: 语音识别 (5个实验) - 服务器运行
# ══════════════════════════════════════════════════════════════
