#!/usr/bin/env python3
"""真实执行源码 — 06_02_频率域滤波"""
def exp_6_2():
    """实验2: 频率域滤波 - 傅里叶变换与频域操作"""
    eid = '06_02_频率域滤波'
    d = exp_start(eid, '频率域滤波')
    files = []

    gray = load_gray(os.path.join(DATA_CV, 'lena.jpg'))
    gray_f = np.float32(gray) / 255.0

    # FFT
    f = np.fft.fft2(gray_f)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.log(np.abs(fshift) + 1)

    rows, cols = gray.shape
    crow, ccol = rows//2, cols//2

    # 低通滤波器
    def create_lpf(r):
        mask = np.zeros((rows, cols), np.uint8)
        cv2.circle(mask, (ccol, crow), r, 1, -1)
        return mask

    # 高通滤波器
    def create_hpf(r):
        mask = np.ones((rows, cols), np.uint8)
        cv2.circle(mask, (ccol, crow), r, 0, -1)
        return mask

    # 应用不同滤波器
    filter_results = []
    for r in [10, 30, 60, 100]:
        # 低通
        mask_lp = create_lpf(r)
        f_lp = fshift * mask_lp
        img_lp = np.fft.ifft2(np.fft.ifftshift(f_lp))
        img_lp = np.abs(img_lp)
        filter_results.append((img_lp, f'低通 r={r}'))

    # 图1: 频谱可视化
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].imshow(gray, cmap='gray'); axes[0].set_title('原图', fontproperties=FONT); axes[0].axis('off')
    axes[1].imshow(magnitude_spectrum, cmap='hot'); axes[1].set_title('频谱 (对数尺度)', fontproperties=FONT); axes[1].axis('off')
    fig.suptitle('傅里叶变换 — 频谱分析', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_频谱分析.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 低通滤波
    fig = make_montage(
        [gray] + [r[0] for r in filter_results],
        ['原图'] + [r[1] for r in filter_results],
        cols=3, figsize=(14, 8),
        main_title='频率域低通滤波 — 不同截止半径'
    )
    p2 = os.path.join(d, '02_低通滤波.png')
    save_img(fig, p2); files.append(p2)

    # 图3: 高通滤波
    hp_results = []
    for r in [10, 30, 60]:
        mask_hp = create_hpf(r)
        f_hp = fshift * mask_hp
        img_hp = np.fft.ifft2(np.fft.ifftshift(f_hp))
        img_hp = np.abs(img_hp)
        hp_results.append((img_hp, f'高通 r={r}'))

    fig = make_montage(
        [gray] + [r[0] for r in hp_results],
        ['原图'] + [r[1] for r in hp_results],
        cols=2, figsize=(12, 10),
        main_title='频率域高通滤波 — 提取边缘'
    )
    p3 = os.path.join(d, '03_高通滤波.png')
    save_img(fig, p3); files.append(p3)

    # 图4: 滤波器可视化
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    for i, r in enumerate([10, 30, 60, 100]):
        mask = create_lpf(r)
        axes[i].imshow(mask, cmap='gray')
        axes[i].set_title(f'低通 r={r}', fontproperties=FONT)
        axes[i].axis('off')
    fig.suptitle('频域低通滤波器 (白色=通过)', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p4 = os.path.join(d, '04_滤波器可视化.png')
    save_img(fig, p4); files.append(p4)

    exp_done(eid, d, files, {'domain': 'frequency', 'methods': ['FFT','LPF','HPF']})


# ══════════════════════════════════════════════════════════════
#  第7章: 图像分割 (2个实验)
# ══════════════════════════════════════════════════════════════
