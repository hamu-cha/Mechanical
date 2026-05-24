import streamlit as st
import numpy as np
import sympy as sp
import modules.setting as set

t_frames = 71
btn = set.AnimationController(t_frames)
draw = set.DrawFigure(figsize = (7, 7), xran = (-0.5, 14), yran = (-0.5, 13), mode = 'xy')
draw.ax.set_aspect('equal')
frames = st.session_state.frame

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        ang = st.slider("投射角度", 0, 89, 75, step = 1)
    with col2:
        v0 = st.slider("初速度", 0.0, 20.0, 15.0, step = 0.5)

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        trajectory = st.checkbox("軌跡")
    with col2:
        vertical = st.checkbox("垂直方向")
    with col3:
        holizontal = st.checkbox("水平方向")
    with col4:
        force = st.checkbox("力")
    with col5:
        velocity = st.checkbox("速度")

btn.layout()

# draw parabola line
v0x = v0*np.cos(np.radians(ang))
v0y = v0*np.sin(np.radians(ang))

xx = sp.Symbol("xx")
func = -9.8/2*(xx/v0x)**2 + v0y*xx/v0x
solve = sp.solve(func)
for ans in solve:
    if ans != 0.0:
        solve = float(ans)

x = np.linspace(0, solve, t_frames)[frames]
y = -9.8/2*(x/v0x)**2 + v0y*x/v0x
draw.ax.plot(x, y, 'o', markersize = 10, color = 'green', zorder = 3)
draw.ax.text(13.25, -0.51, r"$x\ \mathrm{[m]}$")
draw.ax.text(-0.5, 13.25, r"$y\ \mathrm{[m]}$")
draw.ax.text(-0.5, -0.5, r"$\mathrm{O}$")

draw.ax.set_xticks(np.arange(2, 13, 2))
draw.ax.set_yticks(np.arange(2, 13, 2))

x_tra = np.linspace(0, solve, t_frames)[0 : frames]
y_tra = -9.8/2*(x_tra/v0x)**2 + v0y*x_tra/v0x

# if tajectory = true
if trajectory:
    draw.ax.plot(x_tra, y_tra, 'o', markersize = 10, color = 'green', alpha = 0.5)
    if vertical:
        draw.ax.plot(x_tra*0, y_tra, 'o', markersize = 10, color = 'red', alpha = 0.5)
    if holizontal: 
        draw.ax.plot(x_tra, x_tra*0, 'o', markersize = 10, color = 'blue')

# if vertical = true
if vertical:
    draw.ax.plot(x*0, y, 'o', markersize = 10, color = 'red')

# if horizon = true
if holizontal:
    draw.ax.plot(x, x*0, 'o', markersize = 10, color = 'blue')

# if force = true
if force:
    draw.ax.quiver(x, y, 0, -1, angles='xy', scale_units='xy', scale=1.0, width=0.005,
            headwidth=4.5, headlength=7.5, headaxislength=6, zorder=2, color = "black")
    
# if velocity = true
if velocity:
    draw.ax.quiver([x, x, x], [y, y, y], [v0x, 0, v0x], [0, v0y - 9.8*x/v0x, v0y - 9.8*x/v0x], 
                    angles = 'xy', scale_units = 'xy', scale=4.0, width=0.005,
                    headwidth = 4.5, headlength = 7.5, headaxislength = 6, zorder = 2, color = ["blue", "red", "green"])
    vy_vec = v0y - 9.8*x/v0x
    vy_vec = np.where(np.abs(vy_vec) < 1e-10, 0.00, vy_vec.round(2))

    draw.ax.text(0.25, 12.5, rf'$v_x$ : {v0x.round(2)} m/s')
    draw.ax.text(0.25, 12.0, rf'$v_y$ : {vy_vec} m/s')

st.selectbox(r'フレーム番号', np.arange(0, t_frames + 1, 1))

st.pyplot(draw.fig)
fps = 60
btn.update_frame(1/fps)