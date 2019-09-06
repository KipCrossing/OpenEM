
from numpy.linalg import norm
from numpy import (array, dot, arccos, clip)
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plot

H, phase = -0.5,	0.95
# H, phase = 11, 0.676-0.005


print(H*np.sin(np.pi*2*phase))
print(H*np.cos(np.pi*2*phase))

B = H*np.sin(np.pi*2*phase)
A = H*np.cos(np.pi*2*phase)

# get angle


u = array([0, 0, 1, 0])
v = array([0, 0, A, B])
c = dot(u, v)/norm(u)/norm(v)  # -> cosine of the angle
angle = arccos(clip(c, -1, 1))  # if you really want the angle
print(angle/(2*np.pi))

# Get x values of the sine wave

time = np.arange(0, 10, 0.1)


# sin_amplitude of the sine wave is sine of a variable like time

sin_amplitude = np.sin(time)*B
cos_amplitude = np.cos(time)*A
sum_amplitude = np.cos(time)*A + np.sin(time)*B


# Plot a sine wave using time and sin_amplitude obtained for the sine wave
plot.plot(time, cos_amplitude)
plot.plot(time, sin_amplitude)

plot.plot(time, sum_amplitude)
# Give a title for the sine wave plot

plot.title('Sine + CoSine waves')


# Give x axis label for the sine wave plot

plot.xlabel('Time')


# Give y axis label for the sine wave plot

plot.ylabel('amplitude = sin(time)')


plot.grid(True, which='both')


plot.axhline(y=0, color='k')

# plot.show()


soa = np.array([[0, 0, A, 0], [0, 0, 0, B], [0, 0, A, B]])
X, Y, U, V = zip(*soa)
plt.figure()
ax = plt.gca()
ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', color=['r', 'b', 'g'], scale=1)
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
plt.grid(True, which='both')
plt.title('Phase: 2*pi*'+str(angle/(2*np.pi)))
plt.draw()
plt.show()
