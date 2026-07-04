#!/usr/bin/env python3
"""真实执行源码 — 14_03_光流法"""
def exp_14_3():
    """实验3: 光流法"""
    eid = '14_03_光流法'
    d = exp_start(eid, '光流法')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 模拟运动
    prev = gray.copy()
    M = np.float32([[1, 0, 10], [0, 1, 5]])
    next_frame = cv2.warpAffine(gray, M, gray.shape[::-1])

    # 稠密光流 (Farneback)
    flow = cv2.calcOpticalFlowFarneback(prev, next_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # 可视化光流
    hsv = np.zeros((*gray.shape, 3), dtype=np.uint8)
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 1] = 255
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    flow_rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # 图1: 光流可视化
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(prev, cmap='gray'); axes[0].set_title('前一帧', fontproperties=FONT); axes[0].axis('off')
    axes[1].imshow(next_frame, cmap='gray'); axes[1].set_title('后一帧 (平移)', fontproperties=FONT); axes[1].axis('off')
    axes[2].imshow(flow_rgb); axes[2].set_title('稠密光流 (Farneback)', fontproperties=FONT); axes[2].axis('off')
    fig.suptitle('光流法运动估计', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_光流可视化.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 光流矢量箭头 (稀疏采样)
    step = 16
    y_grid, x_grid = np.mgrid[step//2:gray.shape[0]:step, step//2:gray.shape[1]:step]
    flow_x = flow[y_grid, x_grid, 0]
    flow_y = flow[y_grid, x_grid, 1]

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(prev, cmap='gray')
    ax.quiver(x_grid, y_grid, flow_x, flow_y, color='red', angles='xy', scale_units='xy', scale=0.5, width=0.003)
    ax.set_title('光流矢量场 (16px采样)', fontproperties=FONT, fontsize=14)
    ax.axis('off')
    fig.tight_layout()
    p2 = os.path.join(d, '02_光流矢量场.png')
    save_img(fig, p2); files.append(p2)

    # 图3: 光流幅值分布
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].hist(mag.ravel(), bins=50, color='#2196F3', alpha=0.7)
    axes[0].set_title('光流幅值分布', fontproperties=FONT)
    axes[0].set_xlabel('幅值', fontproperties=FONT)

    axes[1].hist(ang.ravel(), bins=36, color='#FF9800', alpha=0.7)
    axes[1].set_title('光流方向分布', fontproperties=FONT)
    axes[1].set_xlabel('角度(rad)', fontproperties=FONT)

    fig.suptitle('光流统计分析', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p3 = os.path.join(d, '03_光流统计分析.png')
    save_img(fig, p3); files.append(p3)

    exp_done(eid, d, files, {'mean_magnitude': float(np.mean(mag)), 'mean_angle': float(np.mean(ang))})
