#!/usr/bin/env python3
"""真实执行源码 — 08_05_OpenCV性能优化"""
def exp_8_5():
    """实验5: OpenCV性能测量与优化"""
    eid = '08_05_OpenCV性能优化'
    d = exp_start(eid, 'OpenCV性能优化')
    files = []

    gray = load_gray(os.path.join(DATA_CV, 'lena.jpg'))

    # 测试不同操作性能
    results = {}

    # 多次运行取平均
    for name, func in [
        ('cv2.blur(5x5)', lambda: cv2.blur(gray, (5,5))),
        ('cv2.GaussianBlur(5x5)', lambda: cv2.GaussianBlur(gray, (5,5), 0)),
        ('cv2.medianBlur(5)', lambda: cv2.medianBlur(gray, 5)),
        ('cv2.bilateralFilter', lambda: cv2.bilateralFilter(gray, 9, 75, 75)),
        ('cv2.Canny', lambda: cv2.Canny(gray, 50, 150)),
        ('cv2.Sobel', lambda: cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)),
        ('cv2.equalizeHist', lambda: cv2.equalizeHist(gray)),
    ]:
        times = []
        for _ in range(10):
            t0 = time.time()
            func()
            times.append((time.time() - t0) * 1000)
        results[name] = {'mean_ms': np.mean(times), 'std_ms': np.std(times)}

    # 图: 性能对比柱状图
    fig, ax = plt.subplots(figsize=(12, 5))
    names = list(results.keys())
    means = [results[n]['mean_ms'] for n in names]
    stds = [results[n]['std_ms'] for n in names]

    bars = ax.bar(range(len(names)), means, yerr=stds, color=plt.cm.viridis(np.linspace(0.2, 0.8, len(names))))
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=30, ha='right', fontsize=9)
    ax.set_ylabel('时间 (ms)', fontproperties=FONT)
    ax.set_title('OpenCV操作性能对比 (512×512图像, 10次平均)', fontproperties=FONT, fontsize=14)
    for bar, v in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(stds), f'{v:.1f}ms',
                ha='center', va='bottom', fontsize=8)
    fig.tight_layout()
    p1 = os.path.join(d, '01_性能对比.png')
    save_img(fig, p1); files.append(p1)

    exp_done(eid, d, files, {'benchmarks': {k: round(v['mean_ms'], 2) for k, v in results.items()}})


# ══════════════════════════════════════════════════════════════
#  第9章: 特征提取 (7个实验)
# ══════════════════════════════════════════════════════════════
