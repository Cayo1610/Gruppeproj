import matplotlib.pyplot as plt

# Dataset 1 (5 points)
x1 = [1, 2, 3, 4, 5]
y1 = [10, 20, 30, 40, 50]

# Dataset 2 (3 points)
x2 = [100, 200, 300]
y2 = [15, 25, 35]

# Create the first plot with the first x-axis
fig, ax1 = plt.subplots()

ax1.plot(x1, y1, 'b-', label='Dataset 1')
ax1.set_xlabel('X-axis 1 (Dataset 1)', color='b')
ax1.set_ylabel('Y-axis')

# Create the second x-axis using `twiny()`
ax2 = ax1.twiny()

# Adjust the position of the second x-axis to prevent overlap
ax2.spines['top'].set_position(('outward', 50))  # Move the second x-axis upward

ax2.plot(x2, y2, 'r-', label='Dataset 2')
ax2.set_xlabel('X-axis 2 (Dataset 2)', color='r')

# Show the plot
plt.title('Two Plots with Different X-Axes')
plt.show()