import matplotlib.pyplot as plt
import numpy as np
import time


# Проверка нахождения целей в секторе
# dots = Координаты целей X, Y, Z
# source_properties = [Положение источника X,
#                      Положение источника Y,
#                      Радиус действия источника,
#                      Размер сектора действия]
# source_direction = [Направление луча Альфа,
#                     Направление луча Бета]
def detection(dots, source_properties, source_direction):
    # Количество целей в секторе
    num = 0
    for d in range(len(dots)):
        # Треугольник ABC
        x = dots[d, 0] - source_properties[0]
        y = dots[d, 1] - source_properties[1]
        a = np.square(x) + np.square(y) + np.square(dots[d, 2])
        b = np.square(source_properties[2])
        if a <= b:
            z = source_properties[2] * np.cos(source_direction[1])
            c = np.square(x - source_properties[2] * np.sin(source_direction[1])) + \
                np.square(y - z * np.sin(source_direction[0])) + \
                np.square(dots[d, 2] - z * np.cos(source_direction[0]))
            if np.arccos((a + b - c) / (2 * source_properties[2] * np.sqrt(a))) < source_properties[3]:
                num += 1
    return num


# Анализ всего пространства
def analysis(dots, source_properties, freq):
    summaries = np.zeros((freq, freq))
    for alfa in range(freq):
        for beta in range(freq):
            summaries[alfa, beta] = detection(dots, source_properties,
                                              [(alfa / freq - 0.5) * np.pi, (beta / freq - 0.5) * np.pi])
    return summaries


# Анализ пространства по областям вокруг целей
def analysis_areas(dots, source_properties, freq):
    summaries = np.zeros((freq, freq))
    iteration = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
    maximum = 0
    alfa_max = 0
    beta_max = 0
    for i_dot in dots:
        angles = spherical(i_dot, source_properties[0:3])
        if angles != None:
            for section in iteration:
                beta = int((angles[1] / np.pi + 0.5) * freq)
                alfa_start = int((angles[0] / np.pi + 0.5) * freq)
                alfa = alfa_start
                alfa_angle = (alfa / freq - 0.5) * np.pi
                beta_angle = (beta / freq - 0.5) * np.pi
                while check(i_dot, source_properties, [alfa_angle, beta_angle]):
                    while check(i_dot, source_properties, [alfa_angle, beta_angle]):
                        if summaries[alfa, beta] == 0:
                            summaries[alfa, beta] = detection(dots, source_properties, [alfa_angle, beta_angle])
                            if summaries[alfa, beta] > maximum:
                                maximum = summaries[alfa, beta]
                                alfa_max = alfa
                                beta_max = beta
                        alfa += section[0]
                        if (alfa < 0) | (alfa >= freq):
                            break
                        alfa_angle = (alfa / freq - 0.5) * np.pi
                    alfa = alfa_start
                    beta += section[1]
                    if (beta < 0) | (beta >= freq):
                        break
                    alfa_angle = (alfa / freq - 0.5) * np.pi
                    beta_angle = (beta / freq - 0.5) * np.pi
    return summaries, [(alfa_max / freq - 0.5) * np.pi, (beta_max / freq - 0.5) * np.pi]


# Функция перехода в сферическую систему координат
# относительно источника излучения
def spherical(xyz, ray_position):
    dx = xyz[0] - ray_position[0]
    dy = xyz[1] - ray_position[1]
    rad = np.sqrt(np.square(dx) + np.square(dy) + np.square(xyz[2]))
    if ray_position[2] < rad:
        return None
    else:
        a = np.arctan(dy / xyz[2])
        b = np.arcsin(dx / rad)
        return [a, b]


# Проверка нахождения точки в секторе
def check(dot, source_properties, source_direction):
    # Треугольник ABC
    x = dot[0] - source_properties[0]
    y = dot[1] - source_properties[1]
    a = np.square(x) + np.square(y) + np.square(dot[2])
    b = np.square(source_properties[2])
    if a <= b:
        z = source_properties[2] * np.cos(source_direction[1])
        c = np.square(x - source_properties[2] * np.sin(source_direction[1])) + \
            np.square(y - z * np.sin(source_direction[0])) + \
            np.square(dot[2] - z * np.cos(source_direction[0]))
        if np.arccos((a + b - c) / (2 * source_properties[2] * np.sqrt(a))) < source_properties[3]:
            return True
    return False


# Функция воздействия целями
def impact(dots, source_properties, source_direction, armor):
    # Количество целей в секторе
    output = []
    for i_dot in range(len(dots)):
        if check(dots[i_dot], source_properties, source_direction):
            dots[i_dot, 3] += 1
        if dots[i_dot, 3] < armor:
            output.append(dots[i_dot])
    return np.array(output)


result = open('big_result.txt', 'w')
for x in range(0, 20):
    for y in range(0, 20):
        print('Позиция расчета:', x, y)
        result_txt = ''
        for set_data in range(20):
            start_time = time.time()
            # data массив включает 6 параметров
            # N - номер ситуации
            # t - момент времени
            # n - номер цели
            # x, y, z - координаты цели n
            # act - время действия излучения
            data = [['N', 't', 'n', 'x', 'y', 'z', 'act']]
            data_spherical = [['x', 'y']]
            bombs = open(f'bombs/set_{set_data}.txt', 'r')

            freq_time = 3
            fall_speed = 15.0 / freq_time  # Скорость падения
            frequency = 180
            life = 3 * freq_time
            ray_prop = [x * 100, y * 100, 2000, 15 * np.pi / 180]  # Характеристики луча

            i = 0
            while 1:
                inpt = list(map(float, bombs.readline().split()))
                if inpt == []:
                    break
                data.append([1, 0, i, float(inpt[0]), float(inpt[1]), float(inpt[2])-500, 0])
                i += 1

            test_date = np.array(data[1:])
            for set_xyz in test_date[:, 3:6]:
                set_ab = spherical(set_xyz, ray_prop[0:3])
                if set_ab != None:
                    data_spherical.append(set_ab)
            test_data_spherical = np.array(data_spherical[1:])

            data_sums, best_angles = analysis_areas(test_date[:, 3:6], ray_prop, frequency)

            #  print(best_angles)
            plt.imshow(data_sums, extent=[-90, 90, 90, -90])
            plt.colorbar()
            plt.scatter(test_data_spherical[:, 1] * 180 / np.pi, test_data_spherical[:, 0] * 180 / np.pi, color='r')
            plt.show()

            flag = 0
            data_calculate = impact(test_date[:, 3:7], ray_prop, best_angles, life)
            for i in range(int(500 / fall_speed)):
                data_calculate[:, 2] -= fall_speed
                # print(data_calculate)
                data_sums, best_angles = analysis_areas(data_calculate[:, 0:3], ray_prop, frequency)

                if (i + 1) % life == 0:
                    plt.imshow(data_sums, extent=[-90, 90, 90, -90])
                    plt.colorbar()
                    data_spherical = [['x', 'y']]
                    for set_xyz in data_calculate[:, 0:3]:
                        set_ab = spherical(set_xyz, ray_prop[0:3])
                        if set_ab != None:
                            data_spherical.append(set_ab)
                    test_data_spherical = np.array(data_spherical[1:])
                    plt.scatter(test_data_spherical[:, 1] * 180 / np.pi,
                                test_data_spherical[:, 0] * 180 / np.pi, color='r')
                    plt.show()

                # print(best_angles)
                data_calculate = impact(data_calculate, ray_prop, best_angles, life)
                if len(data_calculate) == 0:
                    sum_data = np.round((i+2)/freq_time, 1)
                    result_txt += ' ' + str(sum_data)
                    print(sum_data)
                    flag = 1
                    break
            if flag == 0:
                sum_data = 120 - (len(data_calculate))
                result_txt += ' ' + str(sum_data)
                print(sum_data)
            print(time.time() - start_time, 'секунд работы')
        result.write(str(x*100) + ' ' + str(y*100) + result_txt + '\n')
result.close()

#start_time = time.time()
#img2.imshow(analysis(tdate[:, 3:6], ray_prop, 360), extent=[-90, 90, 90, -90])
#print(time.time() - start_time, 'секунд')

# Результатом программы является набор данных
# print(learned_data)
