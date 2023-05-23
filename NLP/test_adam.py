# 3d plot of the test function
from numpy import arange
from numpy import meshgrid
from numpy.random import rand,seed
from math import sqrt
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

# contour plot of the test function
from numpy import asarray

# objective function
def objective(x, y):
    return x ** 2.0 + y ** 2.0

# derivative of objective function
def derivative(x, y):
 return asarray([x * 2.0, y * 2.0])


def surface_plot():
    # define range for input
    r_min, r_max = -1.0, 1.0

    # sample input range uniformly at 0.1 increments
    xaxis = arange(r_min, r_max, 0.1)
    yaxis = arange(r_min, r_max, 0.1)

    # create a mesh from the axis
    x, y = meshgrid(xaxis, yaxis)

    # compute targets
    results = objective(x, y)

    # create a surface plot with the jet color scheme
    figure = pyplot.figure()
    axis = figure.add_subplot(projection = '3d')
    axis.plot_surface(x, y, results, cmap='jet')

    # show the plot
    pyplot.show()


def contour_plot():
    # define range for input
    bounds = asarray([[-1.0, 1.0], [-1.0, 1.0]])
    # sample input range uniformly at 0.1 increments
    xaxis = arange(bounds[0, 0], bounds[0, 1], 0.1)
    yaxis = arange(bounds[1, 0], bounds[1, 1], 0.1)
    # create a mesh from the axis
    x, y = meshgrid(xaxis, yaxis)
    # compute targets
    results = objective(x, y)
    # create a filled contour plot with 50 levels and jet color scheme
    pyplot.contourf(x, y, results, levels=50, cmap='jet')
    # show the plot
    pyplot.show()


# gradient descent algorithm with adam
def adam(objective, derivative, bounds, n_iter, alpha, beta1, beta2, eps=1e-8):
    solutions = list()
    # generate an initial point
    x = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
    score = objective(x[0], x[1])
    # initialize first and second moments
    m = [0.0 for _ in range(bounds.shape[0])]
    v = [0.0 for _ in range(bounds.shape[0])]
    # run the gradient descent updates
    for t in range(n_iter):
        # calculate gradient g(t)
        g = derivative(x[0], x[1])
        # build a solution one variable at a time
        for i in range(x.shape[0]):
            # m(t) = beta1 * m(t-1) + (1 - beta1) * g(t)
            m[i] = beta1 * m[i] + (1.0 - beta1) * g[i]
            # v(t) = beta2 * v(t-1) + (1 - beta2) * g(t)^2
            v[i] = beta2 * v[i] + (1.0 - beta2) * g[i]**2
            # mhat(t) = m(t) / (1 - beta1(t))
            mhat = m[i] / (1.0 - beta1**(t+1))
            # vhat(t) = v(t) / (1 - beta2(t))
            vhat = v[i] / (1.0 - beta2**(t+1))
            # x(t) = x(t-1) - alpha * mhat(t) / (sqrt(vhat(t)) + eps)
            x[i] = x[i] - alpha * mhat / (sqrt(vhat) + eps)

        # evaluate candidate point
        score = objective(x[0], x[1])
        # keep track of solutions
        solutions.append(x.copy())
        # report progress
        print('>%s/%s f(%s) = %.5f' % (str(t).zfill(2), str(n_iter), x, score))

    return solutions


# seed the pseudo random number generator
seed(928374)
# define range for input
bounds = asarray([[-1.0, 1.0], [-1.0, 1.0]])

# n_iter 和 alpha 具有关系：n_iter * alpha > 1
# 若刚好等于1，结果接近0但可能不为0；
# 若小于1，越小结果离0越远，图像上曲线未到达中心零点处；
# 若大于1，结果为0之后迭代不会提前终止，图像上曲线抵达了中心零点处；

# define the total iterations
n_iter = 60
# steps size
alpha = 0.02
# factor for average gradient
beta1 = 0.8
# factor for average squared gradient
beta2 = 0.999
# perform the gradient descent search with adam
solutions = adam(objective, derivative, bounds, n_iter, alpha, beta1, beta2)

# sample input range uniformly at 0.1 increments
xaxis = arange(bounds[0,0], bounds[0,1], 0.1)
yaxis = arange(bounds[1,0], bounds[1,1], 0.1)
# create a mesh from the axis
x, y = meshgrid(xaxis, yaxis)
# compute targets
results = objective(x, y)
# create a filled contour plot with 50 levels and jet color scheme
pyplot.contourf(x, y, results, levels=50, cmap='jet')

# plot the sample as black circles
solutions = asarray(solutions)
pyplot.plot(solutions[:, 0], solutions[:, 1], '.-', color='r')

# show the plot
pyplot.show()

