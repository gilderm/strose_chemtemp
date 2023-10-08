import matplotlib.pylab as plt
import matplotlib.animation as animation
import numpy as np

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

fig, ax = plt.subplots()
x = np.linspace(0, 15, 100)
y = np.sin(x)

ax.plot(x, y, lw=7)

def animate(frame):
   ax.set_xlim(left=0, right=frame)
   pass

ani = animation.FuncAnimation(fig, animate, frames=100)

plt.show()