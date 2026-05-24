import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pt

class Object():
    def __init__(self, xran = [-15, 15], yran = [-15, 15] , figsize = (6, 6)):
        self.fig, self.ax = plt.subplots(figsize = figsize)
        self.ax.set_aspect('equal')
        self.xmin, self.xmax = xran
        self.ymin, self.ymax = yran
        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)
        self.ax.axis('off')

    def ball(self, center, radius, color):
        ball = pt.Circle(xy = center, radius = radius, fc = color, ec = color)
        self.ax.add_patch(ball)

    def box(self, xy, width, height, color):
        box = pt.Rectangle(xy = xy, width = width, height = height, fc = color, ec = color)
        self.ax.add_patch(box)

    
    def spring(self, xy, length, width=0.5, mode='xp'):
        x0, y0 = xy

        L = abs(length)

        n = max(10, int(360 * L))

        if mode == 'xp':
            x = np.linspace(x0, x0 + L, n + 1)
            y_spring = width * np.sin(2*np.pi*(4*(x-x0)/L - np.pi/8))
            self.ax.plot(x, y_spring + y0, color='black')

        elif mode == 'xm':
            x = np.linspace(x0, x0 - L, n + 1)
            y_spring = width * np.sin(2*np.pi*(4*(x-x0)/L - np.pi/8))
            self.ax.plot(x, y_spring + y0, color='black')

        elif mode == 'yp':
            y = np.linspace(y0, y0 + L, n + 1)
            x_spring = width * np.sin(2*np.pi*(4*(y-y0)/L - np.pi/8))
            self.ax.plot(x_spring + x0, y, color='black')

        elif mode == 'ym':
            y = np.linspace(y0, y0 - L, n + 1)
            x_spring = width * np.sin(2*np.pi*(4*(y-y0)/L - np.pi/8))
            self.ax.plot(x_spring + x0, y, color='black')
       


if __name__ == '__main__':
    obj = Object(xran = [-10, 10], yran = [-10, 10])
    obj.spring(5, 0.5, mode = 'yp')
    obj.ball(center = (0, 5.5), radius = 0.5, color = 'blue')
    obj.box((0, 0), 1, 2, 'red')