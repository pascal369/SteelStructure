import numpy as np

# ========= 入力 =========
Ro = 2262  # 外半径 mm
Ri =2250  # 内半径 mm

# 開口（中心角[deg], 開始角[deg]）
# 角度は「X軸右=0°, 反時計回り」
openings = [
    (18.3, 180),   # α1
    (39.0, 270),   # α2
    (38.8,   0),   # α3
    (16.6,  60),   # α4
      # α5
]

# 分割数（精度）
N = 2000


# ========= 角度マスク作成 =========
theta = np.linspace(0, 2*np.pi, N)
mask = np.ones_like(theta, dtype=bool)

for ang, center in openings:
    half = np.deg2rad(ang/2)
    c = np.deg2rad(center)

    d = np.angle(np.exp(1j*(theta - c)))
    mask &= (np.abs(d) > half)

theta_valid = theta[mask]


# ========= 極座標積分 =========
# 微小面積 dA = r dr dθ
Nr = 200
r = np.linspace(Ri, Ro, Nr)

dtheta = (2*np.pi)/N
dr = (Ro - Ri)/Nr

A = 0.0
Cx = 0.0
Cy = 0.0
Ix = 0.0
Iy = 0.0
Ixy = 0.0

for t in theta_valid:
    for rr in r:
        dA = rr * dr * dtheta
        x = rr * np.cos(t)
        y = rr * np.sin(t)

        A += dA
        Cx += x * dA
        Cy += y * dA

        Ix += y**2 * dA
        Iy += x**2 * dA
        Ixy += x*y * dA

# ========= 重心 =========
Cx /= A
Cy /= A

# ========= 重心まわり =========
Ix_c = Ix - A * Cy**2
Iy_c = Iy - A * Cx**2
Ixy_c = Ixy - A * Cx * Cy

# ========= 主軸 =========
I_avg = (Ix_c + Iy_c)/2
R = np.sqrt(((Ix_c - Iy_c)/2)**2 + Ixy_c**2)

I1 = I_avg + R
I2 = I_avg - R

theta_p = 0.5 * np.arctan2(-2*Ixy_c, (Iy_c - Ix_c))
theta_p_deg = np.degrees(theta_p)


# ========= 出力 =========
print("=== 断面性能 ===")
print(f"A = {A:.2f} mm^2 ({A/100:.2f} cm^2)")
print(f"Cx = {Cx:.2f} mm, Cy = {Cy:.2f} mm")

print("\n--- 断面二次モーメント（重心）---")
print(f"Ix = {Ix_c:.3e} mm^4")
print(f"Iy = {Iy_c:.3e} mm^4")
print(f"Ixy = {Ixy_c:.3e} mm^4")

print("\n--- 主軸 ---")
print(f"I1 = {I1:.3e} mm^4")
print(f"I2 = {I2:.3e} mm^4")
print(f"主軸角 = {theta_p_deg:.2f} deg")