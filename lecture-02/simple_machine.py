# Created by mqgao at 2018/11/11

"""
Feature: #Enter feature name here
# Enter feature description here

Scenario: #Enter scenario name here
# Enter steps here

Test File Location: # Enter

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time


titanic_content = pd.read_csv(open('./train.csv'))
# 去掉nan空值
titanic_content = titanic_content.dropna()
age_with_fare = titanic_content[['Age', 'Fare']]
print(age_with_fare)
# 选取其中具有线性特征的样本点
age_with_fare = age_with_fare[ (age_with_fare['Age'] > 22) & (age_with_fare['Fare'] < 400) &  (age_with_fare['Fare'] > 130)]
age = np.array(age_with_fare['Age'].tolist())
fare = np.array(age_with_fare['Fare'].tolist())
print(age)
print(fare)

#定义损失函数
def loss(y_true, yhats): return np.mean(np.abs(y_true - yhats))

#定义算法模型
def model(x, a, b): return a * x + b

#参数初始值
a = 1
b = 0

yhats = np.array([model(x, a, b) for x in age])

#学习阈值
eps = 20

#参数变化的四个方向
directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)]

#学习率
learning_rate = 1e-2

min_loss = float('inf')

batch = 0

#学习过程
while True:
    if loss(y_true=fare, yhats=yhats) < eps: break

    indices = np.random.choice(range(len(age)), size=10)

    sample_x = age[indices]
    sample_y = fare[indices]
    # sample_x = age
    # sample_y = fare

    new_a, new_b = a, b

    for d in directions:
        da, db = d

        #参数的变化过程
        if min_loss != float('inf'):
            _a = a + da * min_loss * learning_rate
            _b = b + db * min_loss * learning_rate
        else:
            _a, _b = a + db, b + db

        y_hats = [model(x, _a, _b) for x in sample_x]
        l = loss(sample_y, np.array([model(x, a + da, b + db) for x in sample_x]))

        if l < min_loss:
            min_loss = l
            new_a, new_b = _a, _b

    total = 10000

    if batch % 100 == 0:
        print('batch {}/ {} fare with {} * age + {}, with loss: {}'.format(batch, total, a, b, l))

    if batch > total: break

    batch += 1

    a, b = new_a, new_b

    # time.sleep(0.01)

plt.scatter(age, fare)
plt.plot(age, [model(x, a, b) for x in age])
plt.show()

