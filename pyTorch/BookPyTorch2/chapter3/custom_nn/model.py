"""Model class manage the network, loss function and optimizer."""

import pickle

# todo 这里的 model 封装到了更高一级的层次，Layer 比较直观，Net 充当了经典意义上的 model，
#  而这里的 Model 则侧重完成 loss 计算、优化器管理、save&load 等事务性的操作。
class Model:

    def __init__(self, net, loss, optimizer):
        self.net = net
        self.loss = loss
        self.optimizer = optimizer

    def forward(self, inputs):
        return self.net.forward(inputs)

    def backward(self, predictions, targets):
        loss = self.loss.loss(predictions, targets)
        grad_from_loss = self.loss.grad(predictions, targets)
        struct_grad = self.net.backward(grad_from_loss)
        return loss, struct_grad

    def apply_grads(self, grads):
        params = self.net.params
        self.optimizer.step(grads, params)

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump(self.net.params, f)

    def load(self, path):
        with open(path, "rb") as f:
            params = pickle.load(f)

        self.net.params = params
        for layer in self.net.layers:
            layer.is_init = True

    @property
    def is_training(self):
        return self.net.is_training

    @is_training.setter
    def is_training(self, is_training):
        self.net.is_training = is_training
