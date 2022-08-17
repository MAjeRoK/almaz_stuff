import numpy as np
import matplotlib.pyplot as plt


# Функция отображения в красивые декартовы координаты
def quoter(data_pixels):
    pixels_result = np.zeros((length * 2, length * 2))

    # Первая четверть
    for n in range(length):
        for m in range(length):
            pixels_result[length + n, length - 1 - m] = data_pixels[n, m]

    # Вторая четверть
    for n in range(length):
        for m in range(length):
            pixels_result[length - 1 - n, length - 1 - m] = data_pixels[n, m]

    # Третья четверть
    for n in range(length):
        for m in range(length):
            pixels_result[length - 1 - n, length + m] = data_pixels[n, m]

    # Четвёртая четверть
    for n in range(length):
        for m in range(length):
            pixels_result[length + n, length + m] = data_pixels[n, m]

    return pixels_result


# Функция отображения в красивые декартовы координаты
def quoter_circle(data_circle):
    circle = []
    l = len(data_circle)

    # Первая четверть
    for n in range(l):
        circle.append(data_circle[n])

    # Вторая четверть
    for n in range(l):
        circle.append([data_circle[l - n - 1, 0], -data_circle[l - n - 1, 1]])

    # Третья четверть
    for n in range(l):
        circle.append(-1 * data_circle[n])

    # Четвёртая четверть
    for n in range(l):
        circle.append([-data_circle[l - n - 1, 0], data_circle[l - n - 1, 1]])

    return np.array(circle)


data = open('fast_result.txt', 'r')

length = 20
data_results = np.zeros((length, length))
counters = []
k = 0
while 1:
    input_data = list(map(float, data.readline().split()))
    if input_data == []:
        break
    i = int(input_data[0] / 100)
    j = int(input_data[1] / 100)
    # print(i, j)
    counters.append(input_data[2::])
    data_results[i, j] = k
    k += 1

# Область опасного местонахождения
length_zone = 250  # Длина сектора разброса
width = 200  # Ширина опасной зоны
circle_danger = []
for i in range(int((length_zone + width) / 25)):
    x = i * 25
    if x < length_zone:
        y = width
    else:
        y = np.sqrt(np.square(width) - np.square(x - length_zone))
    circle_danger.append([x, y])
circle_danger.append([x + 12.5, np.sqrt(np.square(width) - np.square(x + 12.5 - length_zone))])
circle_danger.append([x + 17.5, np.sqrt(np.square(width) - np.square(x + 17.5 - length_zone))])
circle_danger.append([length_zone + width, 0])

# Область возможного местонахождения
length_zone = 250  # Длина сектора разброса
width = 1000  # Ширина зоны нахождения
circle_warning = []
for i in range(int((length_zone + width) / 25)):
    x = i * 25
    if x < length_zone:
        y = width
    else:
        y = np.sqrt(np.square(width) - np.square(x - length_zone))
    circle_warning.append([x, y])
circle_warning.append([x + 12.5, np.sqrt(np.square(width) - np.square(x + 12.5 - length_zone))])
circle_warning.append([x + 17.5, np.sqrt(np.square(width) - np.square(x + 17.5 - length_zone))])
circle_warning.append([length_zone + width, 0])

line_circle_danger = quoter_circle(np.array(circle_danger))
line_circle_warning = quoter_circle(np.array(circle_warning))

# Определяем среднее количество сбитий
average = np.zeros((length, length))
for i in range(length):
    for j in range(length):
        summary = 0
        for point in counters[int(data_results[i, j])]:
            if point < 100:
                summary += 0
            else:
                summary += 120 - point
        average[i, j] = summary / length

print(np.array(counters))
plt.title('Среднее количество пропущенных')
plt.imshow(quoter(average), extent=[-2000, 2000, -2000, 2000])
plt.colorbar()
plt.clim(0, 20)
plt.plot(line_circle_danger[:, 1], line_circle_danger[:, 0], color='r')
plt.plot(line_circle_warning[:, 1], line_circle_warning[:, 0])
plt.show()

# Определяем среднее время сбития без учёта упавших
time = np.zeros((length, length))
for i in range(length):
    for j in range(length):
        summary_time = 0
        for point in counters[int(data_results[i, j])]:
            if point < 100:
                summary_time += 33.3 - point
            else:
                summary_time += 0
        time[i, j] = summary_time / length

plt.title('Среднее оставшеся время')
plt.imshow(quoter(time), extent=[-2000, 2000, -2000, 2000])
plt.colorbar()
plt.clim(0, 33.3)
plt.plot(line_circle_danger[:, 1], line_circle_danger[:, 0], color='r')
plt.plot(line_circle_warning[:, 1], line_circle_warning[:, 0])
plt.show()

max_misses = np.zeros((length, length))
for i in range(length):
    for j in range(length):
        for point in counters[int(data_results[i, j])]:
            if point >= 100:
                if max_misses[i, j] < 120 - point:
                    max_misses[i, j] = 120 - point

plt.title('Максимум пропущенных')
plt.imshow(quoter(max_misses), extent=[-2000, 2000, -2000, 2000])
plt.colorbar()
plt.clim(0, 20)
plt.plot(line_circle_danger[:, 1], line_circle_danger[:, 0], color='r')
plt.plot(line_circle_warning[:, 1], line_circle_warning[:, 0])
plt.show()

min_last_time = np.zeros((length, length))
for i in range(length):
    for j in range(length):
        min_last_time[i, j] = length
        for point in counters[int(data_results[i, j])]:
            if point < 100:
                if min_last_time[i, j] > 33.3 - point:
                    min_last_time[i, j] = 33.3 - point
            else:
                min_last_time[i, j] = 0
                break

plt.title('Минимум оставшегося времени')
plt.imshow(quoter(min_last_time), extent=[-2000, 2000, -2000, 2000])
plt.colorbar()
plt.clim(0, 33.3)
plt.plot(line_circle_danger[:, 1], line_circle_danger[:, 0], color='r')
plt.plot(line_circle_warning[:, 1], line_circle_warning[:, 0])
plt.show()
