#!/usr/bin/env python3
"""真实执行源码 — 15_11_异步爬虫"""
def exp_15_11():
    """实验11: 异步爬虫 - asyncio/aiohttp"""
    eid = '15_11_异步爬虫'
    d = exp_start(eid, '异步爬虫')
    files = []

    # 同步vs异步对比
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis('off')

    comparison = (
        '              同步爬虫                          异步爬虫\n'
        '   ┌────────────────────┐          ┌────────────────────────┐\n'
        '   │ 请求1 ████████ (2s) │          │ 请求1 ████████          │\n'
        '   │ 等待...             │          │ 请求2 ████████  (并发)  │\n'
        '   │ 请求2 ████████ (2s) │          │ 请求3 ████████          │\n'
        '   │ 等待...             │          │ 请求4 ████████          │\n'
        '   │ 请求3 ████████ (2s) │          │ 请求5 ████████          │\n'
        '   │ 总时间: 10s          │          │ 总时间: ~2s             │\n'
        '   └────────────────────┘          └────────────────────────┘\n\n'
        '   import requests                   import aiohttp, asyncio\n'
        '   for url in urls:                  async def fetch(url):\n'
        '       r = requests.get(url)             async with session.get(url) as r:\n'
        '       process(r)                            return await r.text()\n'
        '                                       \n'
        '                                   async def main():\n'
        '                                       tasks = [fetch(url) for url in urls]\n'
        '                                       results = await asyncio.gather(*tasks)'
    )
    ax.text(0.5, 0.5, comparison, ha='center', va='center', fontsize=9,
            fontfamily='monospace', transform=ax.transAxes,
            bbox=dict(boxstyle='round', facecolor='#FFF3E0'))
    ax.set_title('同步 vs 异步爬虫', fontproperties=FONT, fontsize=14)

    p1 = os.path.join(d, '01_同步vs异步.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {})
