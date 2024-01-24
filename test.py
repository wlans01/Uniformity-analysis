"Sensor position	no collimator	Collimator"
from numpy.polynomial import Polynomial
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 균일도
def uniformity(a, b):
    return ((b - a) / b) * 100

if __name__ == '__main__':

    # file 블러오거
    data = pd.read_excel('data.xlsx')
    data = data.to_numpy()

    sensor_position = data[:, 0]
    no_collimator = data[:, 1]
    collimator = data[:, 2]

    # polynomial fitting

    polynomial_number = 2

    polynomial_no_collimator = Polynomial.fit(sensor_position, no_collimator, polynomial_number)
    polynomial_collimator = Polynomial.fit(sensor_position, collimator, polynomial_number)

    polynomial_no_collimator_fit = polynomial_no_collimator(sensor_position)
    polynomial_collimator_fit = polynomial_collimator(sensor_position)

    # 양끝값과 중앙값 구하기
    no_collimator_left = polynomial_no_collimator_fit[0]
    no_collimator_right = polynomial_no_collimator_fit[-1]
    no_collimator_max = max(polynomial_no_collimator_fit)

    no_collimator_left_uniformity = uniformity(no_collimator_left, no_collimator_max)
    no_collimator_right_uniformity = uniformity(no_collimator_right, no_collimator_max)


    collimator_left = polynomial_collimator_fit[0]
    collimator_right = polynomial_collimator_fit[-1]
    collimator_max = max(polynomial_collimator_fit)

    collimator_left_uniformity = uniformity(collimator_left, collimator_max)
    collimator_right_uniformity = uniformity(collimator_right, collimator_max)


    print('no collimator left: ', no_collimator_left)
    print('no collimator right: ', no_collimator_right)
    print('no collimator max: ', no_collimator_max)
    print('no collimator left uniformity: ', no_collimator_left_uniformity)
    print('no collimator right uniformity: ', no_collimator_right_uniformity)

    print('collimator left: ', collimator_left)
    print('collimator right: ', collimator_right)
    print('collimator max: ', collimator_max)
    print('collimator left uniformity: ', collimator_left_uniformity)
    print('collimator right uniformity: ', collimator_right_uniformity)

    

    no_collimator_fit_mean = np.mean(polynomial_no_collimator_fit)
    no_collimator_fit_std = np.std(polynomial_no_collimator_fit)

    collimator_fit_mean = np.mean(polynomial_collimator_fit)
    collimator_fit_std = np.std(polynomial_collimator_fit)


    # 그래프 그리기
    plt.subplot(1, 3, 1)
    plt.plot(sensor_position, no_collimator, 'r-', label='no collimator')
    plt.plot(sensor_position, polynomial_no_collimator_fit, 'r--', label='no collimator fit')
    plt.plot(sensor_position, collimator, 'b-', label='collimator')
    plt.plot(sensor_position, polynomial_collimator_fit, 'b--', label='collimator fit')
    plt.legend()

    plt.subplot(1, 3, 2)
    plt.plot(sensor_position, no_collimator, 'r-', label='no collimator')
    plt.plot(sensor_position, polynomial_no_collimator_fit, 'r--', label='no collimator fit')
    plt.hlines(no_collimator_fit_mean,sensor_position[0],sensor_position[-1], colors='gray', linestyles='dashed', label='no collimator mean')
    plt.legend()

    plt.subplot(1, 3, 3)
    plt.plot(sensor_position, collimator, 'b-', label='collimator')
    plt.plot(sensor_position, polynomial_collimator_fit, 'b--', label='collimator fit')
    plt.hlines(collimator_fit_mean,sensor_position[0],sensor_position[-1], colors='gray', linestyles='dashed', label='collimator mean')
    plt.legend()

    plt.show()

    data = pd.read_excel('data.xlsx')
    # Calculate the mean and standard deviation for the 'no collimator' column
    no_collimator_mean = data['no collimator'].mean()

    no_collimator_std = data['no collimator'].std()

    # Plotting the 'no collimator' data
    plt.figure(figsize=(12, 6))
    plt.plot(data['Sensor position'], data['no collimator'], label='No Collimator', color='blue')
    plt.axhline(y=no_collimator_mean, color='red', linestyle='--', label=f'Mean: {no_collimator_mean:.2e}')
    plt.fill_between(data['Sensor position'], no_collimator_mean - no_collimator_std, no_collimator_mean + no_collimator_std, color='grey', alpha=0.5, label=f'Std Dev: {no_collimator_std:.2e}')

    plt.xlabel('Sensor position')
    plt.ylabel('Intensity')
    plt.title('No Collimator')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Calculate the mean and standard deviation for the 'collimator' column
    collimator_mean = data['Collimator'].mean()
    collimator_std = data['Collimator'].std()

    # Plotting the 'collimator' data
    plt.figure(figsize=(12, 6))
    plt.plot(data['Sensor position'], data['Collimator'], label='Collimator', color='blue')
    plt.axhline(y=collimator_mean, color='red', linestyle='--', label=f'Mean: {collimator_mean:.2e}')
    plt.fill_between(data['Sensor position'], collimator_mean - collimator_std, collimator_mean + collimator_std, color='grey', alpha=0.5, label=f'Std Dev: {collimator_std:.2e}')

    plt.xlabel('Sensor position')
    plt.ylabel('Intensity')
    plt.title('Collimator')
    plt.legend()
    plt.grid(True)
    plt.show()

    print("")
    # 표준편차 / 평균 = 변동계수
    cv_no_collimator = round(((1- (no_collimator_std / no_collimator_mean)) * 100),2)
    cv_collimator = round(((1-(collimator_std / collimator_mean)) * 100),2)
    
    print('cv_no_collimator: ', cv_no_collimator ,"%")
    print('cv_collimator: ', cv_collimator ,"%")


    print("")
    # 피팅 데이터 균일도
    # no collimator
    cv_no_collimator_fit = round(((1- (no_collimator_fit_std / no_collimator_fit_mean)) * 100),2)
    cv_collimator_fit = round(((1-(collimator_fit_std / collimator_fit_mean)) * 100),2)

    print('cv_no_collimator_fit: ', cv_no_collimator_fit ,"%")
    print('cv_collimator_fit: ', cv_collimator_fit ,"%")











