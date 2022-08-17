import numpy as np

for j in range(100):
    bombs = open(f'bombs/set_{j}.txt', 'w')

    y = np.random.normal(0, 10, 20)
    x = np.random.uniform(-250, 250, 20)
    z = np.random.normal(0, 15, 20)

    for i in range(20):
        bombs.write(str(x[i]) + ' ' + str(y[i]) + ' ' + str(600 + z[i]) + "\n")
    bombs.close()
