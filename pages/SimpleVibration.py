import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import modules.setting as set


def arrow(ax, start, finish, color, width=0.005):
    x0, y0 = start
    x1, y1 = finish

    ax.quiver(x0, y0, x1 - x0, y1 - y0, angles='xy', scale_units='xy', scale=1,
        color=color, width=width, headwidth=4.5, headlength=7.5, headaxislength=6)


st.title("単振動")

# Display options
col1, col2, col3 = st.columns(3)
with col1:
    show_disp = st.checkbox("変位", True)
with col2:
    show_vel = st.checkbox("速度", False)
with col3:
    show_acc = st.checkbox("加速度", False)

t_frames = 128

btn = set.AnimationController(t_frames)
btn.layout()

frames = st.session_state.frame

fig, ax = plt.subplots(figsize=(10, 3.5))

# Coordinate axes
arrow(ax, [-1.5, 0], [8.5, 0], 'black', 0.004)
arrow(ax, [0, -1.5], [0, 1.5], 'black', 0.004)
arrow(ax, [1.5, -1.5], [1.5, 1.5], 'black', 0.004)
arrow(ax, [2, -1.5], [2, 1.5], 'black', 0.004)

# Circular motion path
theta = np.linspace(0, 2 * np.pi, 361)
ax.plot(np.cos(theta), np.sin(theta), ':', color='green', linewidth=2)

# Current phase angle
th = 4 * np.pi * frames / t_frames

# Current position on circle
x_circle = np.cos(th)
y_circle = np.sin(th)

ax.plot(x_circle, y_circle, 'o', color='green', markersize=10)

# Wave coordinates
theta_wave = np.linspace(0, 4 * np.pi, 721)
x_wave = 2 + 6 * theta_wave / (4 * np.pi)
mask = theta_wave <= th

# Displacement
value0 = np.sin(th)
wave = np.sin(theta_wave)

ax.plot(1.5, value0, 'o', color='green', markersize=10)

if show_disp:
    ax.plot([x_circle, 2 + th / 2], [value0, value0],
        '--', color='gray', linewidth=1)
    
    ax.plot(x_wave[mask], wave[mask],
            color='green', linewidth=2)

    if np.any(mask):
        ax.plot(x_wave[mask][-1], wave[mask][-1],
                'o', color='green', markersize=10)
    
    ax.set_yticks([-1, 1])
    ax.set_yticklabels([r'$-A$', r'$A$'])

# Velocity
if show_vel:
    scale = 0.8

    wave = scale*np.cos(theta_wave)

    ax.plot(x_wave[mask], wave[mask],
            color='blue', linewidth=2)

    # Velocity vector on circular motion
    arrow(ax, [x_circle, y_circle], [x_circle - scale * np.sin(th), y_circle + scale * np.cos(th)], 
          'blue', 0.003)

    # Velocity vector on SHM
    arrow(ax, [1.5, value0], [1.5, value0 + scale * np.cos(th)], 'blue', 0.003)

    ax.set_yticks([-scale, scale])
    ax.set_yticklabels([r'$-A\omega$', r'$A\omega$'])

# Acceleration
if show_acc:
    scale = 0.6

    wave = -scale*np.sin(theta_wave)

    ax.plot(x_wave[mask], wave[mask],
            color='red', linewidth=2)

    # Acceleration vector on circular motion
    arrow(ax, [x_circle, y_circle], [x_circle - scale * np.cos(th), y_circle - scale * np.sin(th)], 
          'red', 0.003)

    # Acceleration vector on SHM
    arrow(ax, [1.5, value0], [1.5, value0 - scale * np.sin(th)], 'red', 0.003)

    ax.set_yticks([-scale, scale])
    ax.set_yticklabels([r'$-A\omega^2$', r'$A\omega^2$'])

# Axis settings
ax.set_xlim(-1.5, 8.5)
ax.set_ylim(-1.8, 1.8)
ax.set_aspect('equal')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 1.5))

ax.tick_params(axis='both', which='major',
               direction='inout', length=7, width=0.75)

ax.set_xticks([3.5, 5, 6.5, 8])
ax.set_xticklabels([r'$\frac{T}{2}$', r'$T$', r'$\frac{3}{2}T$', r'$2T$'])

st.pyplot(fig)

btn.update_frame(0.03)