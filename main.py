import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -------------------- GLOBAL STYLE --------------------
plt.rcParams.update({
    "font.size": 9,
    "mathtext.fontset": "cm",
    "font.family": "serif"
})

fig = plt.figure(figsize=(12, 4), dpi=300)

# -------------------- BLOCH SPHERE MESH --------------------
u = np.linspace(0, 2*np.pi, 60)
v = np.linspace(0, np.pi, 60)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones_like(u), np.cos(v))

def draw_bloch(ax, y_offset=0.0):
    ax.plot_wireframe(x, y, z, color='gray', alpha=0.25, linewidth=0.4)

    # Axes
    ax.quiver(0,0,0, 1.2,0,0, color='r', linewidth=1)
    ax.quiver(0,0,0, 0,1.2,0, color='g', linewidth=1)
    ax.quiver(0,0,0, 0,0,1.2, color='b', linewidth=1)

    # Axis labels
    ax.text(1.35, y_offset, 0, r'$X$', color='r', fontsize=10)
    ax.text(0,1.35,0, r'$Y$', color='g', fontsize=10)
    ax.text(0,0,1.35, r'$Z$', color='b', fontsize=10)

    ax.set_box_aspect([1,1,1])
    ax.view_init(elev=20, azim=40)
    ax.set_axis_off()

# ===================== (a) ALICE =====================
ax1 = fig.add_subplot(131, projection='3d')
draw_bloch(ax1, y_offset=+0.06)

# Alice basis states EXCEPT |+⟩
alice_states = {
    r'$|0\rangle$': (0, 0, 1),
    r'$|1\rangle$': (0, 0, -1),
    r'$|-\rangle$': (-1, 0, 0)
}

for label, (xs, ys, zs) in alice_states.items():
    ax1.scatter(xs, ys, zs, s=45, color='black', zorder=5)
    ax1.text(xs*1.15, ys*1.15, zs*1.15,
             label, fontsize=10, fontweight='bold')

# -------- Alice |+⟩ handled SEPARATELY --------
ax1.scatter(1, 0, 0, s=45, color='black', zorder=5)

# 🔧 Move ONLY |+⟩ upward
ax1.text(1.15, -0.3, 0,
         r'$|+\rangle$', fontsize=10, fontweight='bold')

ax1.set_title("(a) Alice: State Preparation\nZ or X Basis",
              fontsize=10, fontweight='bold')

# ===================== (b) EVE =====================
ax2 = fig.add_subplot(132, projection='3d')
draw_bloch(ax2, y_offset=0.0)

theta = np.pi / 4
psi = (np.sin(theta), 0, np.cos(theta))

ax2.scatter(*psi, s=70, color='purple', zorder=6)
ax2.text(psi[0]*1.2, psi[1], psi[2]*1.2,
         r'$|\psi\rangle$', fontsize=11, fontweight='bold')

collapsed = (0, 0, 1)

ax2.quiver(
    psi[0], psi[1], psi[2],
    collapsed[0]-psi[0],
    collapsed[1]-psi[1],
    collapsed[2]-psi[2],
    color='black',
    linestyle=':',
    linewidth=1.2,
    arrow_length_ratio=0.001
)

ax2.text(0,0,1.25, r'$|0\rangle$', fontsize=11, fontweight='bold')

ax2.set_title("(b) Eve: Measurement Disturbance\nState Collapse",
              fontsize=10, fontweight='bold')

# ===================== (c) BOB =====================
ax3 = fig.add_subplot(133, projection='3d')
draw_bloch(ax3, y_offset=-0.06)

# Collapsed state
ax3.scatter(0,0,1, s=70, color='green', zorder=6)
ax3.text(0,0,1.25, r'$|0\rangle$', fontsize=11, fontweight='bold')

# Measurement axis (X basis)
ax3.quiver(-1.2,0,0, 2.4,0,0,
           color='orange', linewidth=3, alpha=0.8)

# -------- ONLY |+⟩ MOVED UP --------
ax3.text(1.15, 0.15, 0, r'$|+\rangle$',
         fontsize=11, fontweight='bold')

ax3.text(-1.35, -0.3, 0, r'$|-\rangle$',
         fontsize=11, fontweight='bold')

ax3.text(0,0,-1.35,
         r'$P(|+\rangle)=P(|-\rangle)=0.5$',
         fontsize=10, ha='center', fontweight='bold')

ax3.set_title("(c) Bob: Measurement Outcome\nRandom Result (p = 0.5)",
              fontsize=10, fontweight='bold')

# ===================== FINAL =====================
plt.suptitle(
    "Bloch Sphere Representation of Quantum State Evolution in BB84",
    fontsize=12, fontweight='bold', y=1.05
)

plt.tight_layout()
plt.savefig("Figure4_Bloch_Sphere_BB84.png", dpi=300, bbox_inches='tight')
plt.savefig("Figure4_Bloch_Sphere_BB84.pdf", bbox_inches='tight')
plt.show()
