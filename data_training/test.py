import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import random

# TensorFlow 1.x 호환 모드 활성화
tf.compat.v1.disable_eager_execution()

# 데이터 로드 및 셔플
food = np.load('D:\\project\\OhMea\\Today-Study\\data_training\\result.npy')
np.random.shuffle(food)

# 데이터 셋 나누기
row = food.shape[0]
train_num = int(row * 0.7)

x_train = food[:train_num, :30000]
x_test = food[train_num:, :30000]

y_train = food[:train_num, 30000:]
y_test = food[train_num:, 30000:]

# 하이퍼파라미터 설정
learning_rate = 0.001
batch_size = 500
training_epochs = 500
keep_prob = tf.compat.v1.placeholder(tf.float32)

# 입력 플레이스홀더 설정
X = tf.compat.v1.placeholder(tf.float32, [None, 30000])
x_img = tf.reshape(X, [-1, 100, 100, 3])
Y = tf.compat.v1.placeholder(tf.float32, [None, 3])

# 첫 번째 CNN 층
W1 = tf.Variable(tf.random.truncated_normal(shape=[5, 5, 3, 64], stddev=5e-2))
b1 = tf.Variable(tf.constant(0.1, shape=[64]))
L1 = tf.nn.relu(tf.nn.conv2d(x_img, W1, strides=[1,1,1,1], padding='SAME') + b1)
L1 = tf.nn.max_pool2d(L1, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
L1 = tf.nn.dropout(L1, rate=1-keep_prob)

# 두 번째 CNN 층
W2 = tf.Variable(tf.random.truncated_normal(shape=[3, 3, 64, 64], stddev=5e-2))
b2 = tf.Variable(tf.constant(0.1, shape=[64]))
L2 = tf.nn.relu(tf.nn.conv2d(L1, W2, strides=[1,1,1,1], padding='SAME') + b2)
L2 = tf.nn.max_pool2d(L2, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
L2 = tf.nn.dropout(L2, rate=1-keep_prob)

# 세 번째 CNN 층
W3 = tf.Variable(tf.random.truncated_normal(shape=[3, 3, 64, 128], stddev=5e-2))
b3 = tf.Variable(tf.constant(0.1, shape=[128]))
L3 = tf.nn.relu(tf.nn.conv2d(L2, W3, strides=[1,1,1,1], padding='SAME') + b3)
L3 = tf.nn.dropout(L3, rate=1-keep_prob)

# 네 번째 CNN 층
W4 = tf.Variable(tf.random.truncated_normal(shape=[3, 3, 128, 128], stddev=5e-2))
b4 = tf.Variable(tf.constant(0.1, shape=[128]))
L4 = tf.nn.relu(tf.nn.conv2d(L3, W4, strides=[1,1,1,1], padding='SAME') + b4)
L4 = tf.nn.dropout(L4, rate=1-keep_prob)

# 다섯 번째 CNN 층
W5 = tf.Variable(tf.random.truncated_normal(shape=[3, 3, 128, 128], stddev=5e-2))
b5 = tf.Variable(tf.constant(0.1, shape=[128]))
L5 = tf.nn.relu(tf.nn.conv2d(L4, W5, strides=[1,1,1,1], padding='SAME') + b5)
L5 = tf.nn.dropout(L5, rate=1-keep_prob)
L5 = tf.nn.max_pool2d(L5, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

# fully connected layer 1
L5_flat = tf.reshape(L5, [-1, 128*13*13])

fc_W1 = tf.compat.v1.get_variable("W4", shape=[128*13*13, 384],
                                  initializer=tf.compat.v1.initializers.glorot_uniform())
fc_b1 = tf.Variable(tf.random.normal([384]))
fc_L1 = tf.nn.relu(tf.matmul(L5_flat, fc_W1) + fc_b1)
fc_L1 = tf.nn.dropout(fc_L1, rate=1-keep_prob)

# fully connected layer 2
fc_W2 = tf.compat.v1.get_variable("W5", shape=[384, 3],
                                  initializer=tf.compat.v1.initializers.glorot_uniform())
fc_b2 = tf.Variable(tf.random.normal([3]))
logits = tf.matmul(fc_L1, fc_W2) + fc_b2
y_pred = tf.nn.softmax(logits)

# 손실 함수 및 옵티마이저 설정
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y))
optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

# 정확도 계산
correct_prediction = tf.equal(tf.argmax(y_pred, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Saver 객체 생성
saver = tf.compat.v1.train.Saver()

# 모델 로드 및 예측
with tf.compat.v1.Session() as sess:
    # 모델 복원
    saver.restore(sess, './model.ckpt')
    print("Model restored.")

    # 테스트 정확도 출력
    print("Testing Accuracy:", sess.run(accuracy, feed_dict={X: x_test, Y: y_test, keep_prob: 1.0}))

    # 시각화를 위한 데이터 준비
    random_idxs = random.sample(range(len(x_test)), 20)
    x_show = x_test[random_idxs]
    y_show = y_test[random_idxs]

    # 시각화
    food_list = ['carrot', 'egg plant', 'korean_melon']
    
    fig = plt.figure(figsize=(15, 6))
    for i in range(20):
        subplot = fig.add_subplot(2, 10, i + 1)
        subplot.set_xticks([])
        subplot.set_yticks([])
        subplot.set_title(food_list[np.argmax(sess.run(logits, feed_dict={X: [x_show[i]], keep_prob: 1.0}))])
        subplot.imshow(x_show[i].reshape(100, 100, 3).astype(np.uint8)) 
    
    plt.show()
