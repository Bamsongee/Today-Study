import numpy as np
import matplotlib.pyplot as plt

# 데이터 로드 및 셔플
file_path = 'D:\\project\\OhMea\\Today-Study\\data_training\\result.npy'
food = np.load(file_path)

# 데이터 셋 나누기
row = food.shape[0]
train_num = int(row * 0.7)

x_train = food[:train_num, :30000]
x_test = food[train_num:, :30000]

y_train = food[:train_num, 30000:]
y_test = food[train_num:, 30000:]

# 시각화를 위한 데이터 준비
random_idxs = np.random.choice(len(x_test), 20)
x_show = x_test[random_idxs]

# 시각화
fig = plt.figure(figsize=(15, 6))
for i in range(20):
    subplot = fig.add_subplot(2, 10, i + 1)
    subplot.set_xticks([])
    subplot.set_yticks([])
    subplot.imshow(x_show[i].reshape(100, 100, 3).astype(np.uint8))

plt.show()
