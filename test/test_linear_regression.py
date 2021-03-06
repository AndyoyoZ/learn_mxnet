# coding=UTF-8
'''
@Description: 从头实现线性回归算法
@Version: 
@Author: liguoying
@Date: 2019-04-19 18:04:14
'''
from IPython import display
from matplotlib import pyplot as plt
from mxnet import autograd, nd
import random

# random.seed(1234)

num_inputs = 2
num_examples = 1000
true_w = [2, -3.4]
true_b = 4.2
features = nd.random.normal(scale=1, shape=(num_examples, num_inputs))
labels = true_w[0] * features[:,0] + true_w[1] * features[:,1] + true_b
# 加入随机扰动
labels += nd.random.normal(scale=0.01, shape=labels.shape)

def use_svg_display():
    display.set_matplotlib_formats('svg')

def set_figsize(figsize=(3.5, 2.5)):
    use_svg_display()
    # 设置图片尺寸
    plt.rcParams['figure.figsize'] = figsize


# set_figsize()
# plt.scatter(features[:,1].asnumpy(), labels.asnumpy(), 1)
# plt.show()


# 读取数据
def data_iter(batch_size, features, labels):
    num_examples = len(features)
    indices = list(range(num_examples))
    random.shuffle(indices)
    for i in range(0, num_examples, batch_size):
        j = nd.array(indices[i: min(i+batch_size, num_examples)])
        yield features.take(j), labels.take(j)  # take函数返回根据索引对应位置的元素


# 初始化模型参数
w = nd.random.normal(scale=0.01, shape=(num_inputs, 1))
b = nd.zeros(shape=(1,))
# 模型训练中，需要对这些参数求梯度来迭代参数的值，因此我们需要创建它们的梯度
w.attach_grad()
b.attach_grad()


# 定义模型
def linreg(X, w, b):
    return nd.dot(X, w) + b

# 定义损失函数
def squared_loss(y_hat, y):
    return (y_hat - y.reshape(y_hat.shape)) ** 2 / 2

# 定义优化算法
def sgd(params, lr, batch_size):
    for param in params:
        param[:] = param - lr * param.grad / batch_size

# 训练模型
lr = 0.03
num_epochs = 30
net = linreg
loss = squared_loss
batch_size = 30

for epoch in range(num_epochs):
    # 每个迭代周期，会使用训练数据中所有样本一次
    for X, y in data_iter(batch_size, features, labels):
        with autograd.record():
            l = loss(net(X, w, b), y)   # 小批量损失
        l.backward()    # 批量损失对模型参数求导
        sgd([w, b], lr, batch_size)
    train_l = loss(net(features, w, b), labels)
    print("Epoch %d, Loss %f" % (epoch + 1, train_l.mean().asnumpy()))


print(true_w, w)
print(true_b, b)
