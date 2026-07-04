#!/usr/bin/env python3
"""真实执行源码 — 14_01_帧差法运动检测"""
def exp_14_1():
    """实验1: 帧差法运动检测"""
    eid = '14_01_帧差法运动检测'
    d = exp_start(eid, '帧差法')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 模拟运动: 创建略有位移的连续帧
    frames = []
    shifts = [(0, 0), (2, 1), (5, 3), (8, 5), (11, 8), (14, 11)]
    for dx, dy in shifts:
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        frame = cv2.warpAffine(gray, M, gray.shape[::-1])
        frames.append(frame)

    # 计算帧差
    diffs = []
    for i in range(1, len(frames)):
        diff = cv2.absdiff(frames[i], frames[i-1])
        _, diff_th = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        diffs.append(diff_th)

    # 图1: 帧序列+帧差
    fig = make_montage(
        frames + diffs,
        ['帧1', '帧2', '帧3', '帧4', '帧5', '帧6',
         '差 2-1', '差 3-2', '差 4-3', '差 5-4', '差 6-5'],
        cols=6, figsize=(18, 8),
        main_title='帧差法运动检测 (模拟平移运动)'
    )
    p1 = os.path.join(d, '01_帧差法.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 累计帧差
    cum_diff = np.zeros_like(gray, dtype=np.float64)
    for d in diffs:
        cum_diff += d.astype(np.float64)
    cum_diff = np.clip(cum_diff, 0, 255).astype(np.uint8)

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    axes[0].imshow(frames[0], cmap='gray'); axes[0].set_title('第一帧', fontproperties=FONT); axes[0].axis('off')
    axes[1].imshow(frames[-1], cmap='gray'); axes[1].set_title('最后一帧', fontproperties=FONT); axes[1].axis('off')
    axes[2].imshow(cum_diff, cmap='hot'); axes[2].set_title('累计帧差 (运动轨迹)', fontproperties=FONT); axes[2].axis('off')
    fig.suptitle('帧差法累计分析', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_累计帧差.png')
    save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {'frames': 6, 'method': 'frame_differencing'})
