#!/usr/bin/env python3
import matplotlib.pyplot as plt

fn = []
xs = []
ys = []

if __name__ == '__main__':
    f = open("db.txt", "r")
    pairs = eval(f.read())

    xs = []
    ys = []

    for k, v in pairs.items():
        x, y = k
        if v == 1:
            xs.append(x)
            ys.append(y)

    plt.plot(xs, ys, 'ro')
    plt.show()
