"""
Test file for Plotly related experiments.
"""

import matplotlib.pyplot as plt

# Define data.
x = [10, 20, 30, 40]
y = [100, 200, 300, 400]
# Create a scatter plot.
plt.scatter(x, y)
# Annotate each point with its coordinate.
for i in range(len(x)):
    plt.annotate(
        f'({x[i]}, {y[i]})',
        (x[i], y[i]),
        textcoords='offset points',
        xytext=(0, 10),
        ha='center',
    )
plt.show()
