#!/usr/bin/env python3
"""真实执行源码 — 13_02_三维点云可视化"""
def exp_13_2():
    """实验2: 点云与三维重建基础"""
    eid = '13_02_三维点云可视化'
    d = exp_start(eid, '三维点云可视化')
    files = []

    # 使用matplotlib的3D绘图
    from mpl_toolkits.mplot3d import Axes3D

    # 1. 生成随机点云
    np.random.seed(42)
    n_points = 500
    # 球面上的点
    phi = np.random.uniform(0, 2*np.pi, n_points)
    theta = np.random.uniform(0, np.pi, n_points)
    r = 1.0 + np.random.normal(0, 0.05, n_points)
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    fig = plt.figure(figsize=(14, 6))

    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1.scatter(x, y, z, c=z, cmap='viridis', s=5, alpha=0.7)
    ax1.set_title('球面点云', fontproperties=FONT)
    ax1.set_xlabel('X'); ax1.set_ylabel('Y'); ax1.set_zlabel('Z')

    # 2. 使用bunny或其它形状
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    # 环形
    t = np.linspace(0, 2*np.pi, 200)
    r_torus = 1.0
    R_torus = 0.3
    x_torus = (r_torus + R_torus * np.cos(10*t)) * np.cos(t)
    y_torus = (r_torus + R_torus * np.cos(10*t)) * np.sin(t)
    z_torus = R_torus * np.sin(10*t)
    ax2.scatter(x_torus, y_torus, z_torus, c=t, cmap='plasma', s=10)
    ax2.set_title('环形点云', fontproperties=FONT)
    ax2.set_xlabel('X'); ax2.set_ylabel('Y'); ax2.set_zlabel('Z')

    fig.suptitle('三维点云可视化', fontproperties=FONT, fontsize=14)
    fig.tight_layout()
    p1 = os.path.join(d, '01_三维点云.png')
    save_img(fig, p1); files.append(p1)

    # 图2: 从深度图重建点云
    gray = load_gray(os.path.join(DATA_CV, 'lena.jpg'))
    if gray is not None:
        small_depth = cv2.resize(gray, (64, 64)).astype(np.float32) / 255.0

        fig = plt.figure(figsize=(14, 6))
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.imshow(small_depth, cmap='gray')
        ax1.set_title('模拟深度图', fontproperties=FONT)
        ax1.axis('off')

        ax2 = fig.add_subplot(1, 2, 2, projection='3d')
        ys, xs = np.mgrid[0:64, 0:64]
        ax2.scatter(xs.flatten()[::8], ys.flatten()[::8], small_depth.flatten()[::8]*100,
                    c=small_depth.flatten()[::8], cmap='viridis', s=2, alpha=0.5)
        ax2.set_title('深度图→点云', fontproperties=FONT)
        ax2.view_init(elev=30, azim=-60)

        fig.suptitle('深度图重建三维点云', fontproperties=FONT, fontsize=14)
        fig.tight_layout()
        p2 = os.path.join(d, '02_深度图到点云.png')
        save_img(fig, p2); files.append(p2)

    exp_done(eid, d, files, {})


# ══════════════════════════════════════════════════════════════
#  第14章: 运动对象检测 (5个实验)
# ══════════════════════════════════════════════════════════════
