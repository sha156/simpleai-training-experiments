#!/usr/bin/env python3
"""真实执行源码 — 13_01_立体视觉与深度图"""
def exp_13_1():
    """实验1: 立体视觉与深度图"""
    eid = '13_01_立体视觉与深度图'
    d = exp_start(eid, '立体视觉与深度图')
    files = []

    img = load_rgb(os.path.join(DATA_CV, 'lena.jpg'))
    if img is None: img = load_rgb(os.path.join(DATA_CV, 'house.jpg'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 模拟视差: 左右略有位移
    h, w = gray.shape
    left = gray[:, :w-20]
    right = gray[:, 20:]

    # StereoBM
    stereo = cv2.StereoBM_create(numDisparities=64, blockSize=15)
    disparity = stereo.compute(left, right)

    # 图1: 立体视觉模拟
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(left, cmap='gray'); axes[0].set_title('左视图', fontproperties=FONT); axes[0].axis('off')
    axes[1].imshow(right, cmap='gray'); axes[1].set_title('右视图 (偏移20px)', fontproperties=FONT); axes[1].axis('off')
    axes[2].imshow(disparity, cmap='plasma'); axes[2].set_title('视差图 (StereoBM)', fontproperties=FONT); axes[2].axis('off')
    fig.suptitle('双目立体视觉 — 视差计算', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_立体视觉与视差.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 不同block size
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    for i, bs in enumerate([5, 9, 15, 21, 31, 51]):
        ax = axes[i//3, i%3]
        try:
            stereo_bs = cv2.StereoBM_create(numDisparities=64, blockSize=bs)
            disp = stereo_bs.compute(left, right)
            ax.imshow(disp, cmap='plasma')
            ax.set_title(f'blockSize={bs}', fontproperties=FONT, fontsize=9)
        except:
            ax.text(0.5, 0.5, 'N/A', ha='center', transform=ax.transAxes)
        ax.axis('off')
    fig.suptitle('StereoBM blockSize参数对比', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p2 = os.path.join(d, '02_StereoBM参数对比.png')
    save_img(fig, p2); files.append(p2)

    # 图3: 视差切片
    fig, ax = plt.subplots(figsize=(10, 5))
    mid_row = disparity[disparity.shape[0]//2, :]
    ax.plot(mid_row, linewidth=1)
    ax.set_title('中心行视差剖面', fontproperties=FONT)
    ax.set_xlabel('列位置', fontproperties=FONT)
    ax.set_ylabel('视差值', fontproperties=FONT)
    ax.axhline(y=np.mean(mid_row), color='red', linestyle='--', label=f'平均={np.mean(mid_row):.1f}')
    ax.legend(prop=FONT)
    fig.tight_layout()
    p3 = os.path.join(d, '03_视差剖面.png')
    save_img(fig, p3); files.append(p3)

    exp_done(eid, d, files, {})
