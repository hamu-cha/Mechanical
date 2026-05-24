import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
from matplotlib.ticker import AutoMinorLocator
from matplotlib import patches

class AnimationController:
   def __init__(self, t_frames):
       self.t_frames = t_frames

       if "frame" not in st.session_state:
           st.session_state.frame = 0
       if "playing" not in st.session_state:
           st.session_state.playing = False

   def playstop(self):
       if st.button("Play/Stop"):
           st.session_state.playing = not st.session_state.playing

   def next(self):
       if st.button("Next"):
           st.session_state.playing = False
           st.session_state.frame = (st.session_state.frame + 1) % self.t_frames

   def back(self):
       if st.button("Back"):
           st.session_state.playing = False
           st.session_state.frame = (st.session_state.frame - 1) % self.t_frames

   def reset(self):
       if st.button("Reset"):
           st.session_state.playing = False
           st.session_state.frame = 0

   def layout(self):
       col1, col2, col3, col4 = st.columns(4)
       with col1:
           self.back()
       with col2:
           self.playstop()
       with col3:
           self.next()
       with col4:
           self.reset()

   def update_frame(self, sleep):
       if st.session_state.playing:
           st.session_state.frame = (st.session_state.frame + 1) % self.t_frames
           time.sleep(sleep)
           st.rerun()

class PhysicalObject:
    def __init__(self, xran, yran):
        self.fig, self.ax = plt.subplots(figsize=(7, 3.75))

        self.xmin, self.xmax = xran
        self.ymin, self.ymax = yran

        self.ax.set_aspect('equal')
        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)

    def create_ball(self, radius, center_pos, color="red"):
        patch = patches.Circle(xy=center_pos, radius=radius, color=color)
        return patch, np.array(center_pos)

    def draw_ball(self, ball_patch):
        self.ax.add_patch(ball_patch)

class Ball:
    def __init__(self, m, r, x, v):
        self.m = m
        self.r = r
        self.x = float(x)
        self.v = float(v)

    def step(self, dt):
        self.x += self.v * dt


    def collide(ball1, ball2):
        dist = abs(ball1.x - ball2.x)
        if dist <= ball1.r + ball2.r:
            ball1.v, ball2.v = ball2.v, ball1.v


    def collide_wall(ball, xmin, xmax):
        if ball.x - ball.r <= xmin or ball.x + ball.r >= xmax:
            ball.v *= -1



class Calculations():
    def __init__(self):
        pass
    @staticmethod
    def diff(object1, object2):
        return np.linalg.norm(np.array(object1) - np.array(object2))

class DrawFigure:
    def __init__(self, figsize = (7, 3.75), xran = None, yran = None, mode = None, w = 0.005, ticknums = (4, 4)):

        self.fig, self.ax = plt.subplots(figsize = figsize)

        if xran is None or yran is None:
            self.xmin, self.xmax = self.ax.get_xlim()
            self.ymin, self.ymax = self.ax.get_ylim()
        else:
            self.xmin, self.xmax = xran
            self.ymin, self.ymax = yran

        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)

        plt.rcParams['mathtext.fontset'] = 'cm'
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams["font.size"] = 16

        if mode == 'xy':
            self.ax.quiver([-0.5, 0], [0, self.ymin], [self.xmax + 0.5, 0], [0, self.ymax - self.ymin],
            angles='xy', scale_units='xy', scale=1.0, width=w,
            headwidth=4.5, headlength=7.5, headaxislength=6, zorder=2)

            self.ax.spines['right'].set_visible(False)
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['left'].set_visible(False)
            self.ax.spines['bottom'].set_visible(False)

            self.ax.spines['bottom'].set_position(('data', 0))
            self.ax.spines['left'].set_position(('data', 0))

            self.ax.tick_params(axis='both',which = 'major', direction = 'inout', 
                                length = 7, width = 0.75)
            for label in self.ax.get_xticklabels() + self.ax.get_yticklabels():
                label.set_bbox(dict(facecolor='white', edgecolor='none', pad=1.5))

        else:
            self.xticknums, self.yticknums = ticknums
            self.ax.tick_params(axis='both',which = 'major', direction = 'in', length = 7, width = 0.75)
            self.ax.tick_params(axis='both',which = 'minor', direction = 'in', length = 4, width = 0.75)

            self.ax.minorticks_on()
            self.ax.xaxis.set_minor_locator(AutoMinorLocator(self.xticknums))
            self.ax.yaxis.set_minor_locator(AutoMinorLocator(self.xticknums))