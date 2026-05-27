import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import modules.setting as set


def arrow(ax, start, finish, color, width = 0.005):
    """Draw an arrow from start to finish."""
    x0, y0 = start
    x1, y1 = finish
    ax.quiver(x0, y0, x1 - x0, y1 - y0, color = color,
              angles='xy', scale_units='xy', scale=1.0, width = width, headwidth=4.5,
              headlength=7.5, headaxislength=6, zorder=3)


st.title("等速円運動")

# Simulation parameters
col1, col2 = st.columns(2)
with col1:
    R = st.slider("半径", 3.0, 5.0, 4.0, 0.1)

with col2:
    omega = st.slider("角速度", 1.0, 3.0, 2.0, 0.1)
    
t_frames = 120

# Animation controller
btn = set.AnimationController(t_frames)
btn.layout()

# Display options
col1, col2, col3 = st.columns(3)
with col1:
    show_r = st.checkbox("変位", False)

with col2:
    show_v = st.checkbox("速度", False)

with col3:
    show_a = st.checkbox("加速度", False)


# Current angle
theta = omega * 2 * np.pi * st.session_state.frame / t_frames

# Position vector
x = R * np.cos(theta)
y = R * np.sin(theta)
R_abs = np.sqrt(x**2 + y**2)

# Velocity vector
vx = -R * omega * np.sin(theta)
vy = R * omega * np.cos(theta)
v_abs = np.sqrt(vx**2 + vy**2)

# Acceleration vector
ax = -R * omega**2 * np.cos(theta)
ay = -R * omega**2 * np.sin(theta)
a_abs = np.sqrt(ax**2 + ay**2)

# Create figure
fig, ax_fig = plt.subplots(figsize=(6, 6))

# Circular trajectory
th = np.linspace(0, 2*np.pi, 361)

ax_fig.plot(R*np.cos(th), R*np.sin(th), '--', color="lightgreen")

# Center point
ax_fig.plot(0, 0, "ko")

# Moving object
ax_fig.plot(x, y, "o", color = 'green', markersize=15)

# Displacement vector
if show_r:
    arrow(ax_fig, [0, 0], [x, y], color = 'green')

# Velocity vector
if show_v:
    scale_v = 0.1
    arrow(ax_fig, [x, y], [x + vx*scale_v, y + vy*scale_v], color = 'blue')

# Acceleration vector
if show_a:
    scale_a = 0.1
    arrow(ax_fig, [x, y], [x + ax*scale_a, y + ay*scale_a], color = 'red')

ax_fig.text(-6, 6.5, rf'$(x,\,y)=({x:.2f},\,{y:.2f}), \,|r| = {R_abs:.2f}$')
ax_fig.text(-6, 6.0, rf'$(v_x,\,v_y)=({vx:.2f},\,{vy:.2f}), \,|v| = {v_abs:.2f}$')
ax_fig.text(-6, 5.5, rf'$(a_x,\,a_y)=({ax:.2f},\,{ay:.2f}), \,|a| = {a_abs:.2f}$')

# Figure settings
ax_fig.set_aspect("equal")
ax_fig.grid(False)

ax_fig.set_xlim(-7, 7)
ax_fig.set_ylim(-7, 7)

plt.axis('off')

st.pyplot(fig)
btn.update_frame(0.05)