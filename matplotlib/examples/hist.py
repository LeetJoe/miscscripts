"""
直方图示例
官方文档地址：https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html
在线拾色器：https://www.w3cschool.cn/tools/index?name=cpicker

"""
import numpy as np
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize


def main():
    figsize(12.5, 3)

    # 标准正态分布采样，均值 0 方差 1，注意得到的每个采样并非在 [-1, 1] 而是均值附近的任何值，绝对值可以大于1
    np.random.seed(42)
    data1 = np.random.randn(200)
    np.random.seed(24)
    data2 = np.random.randn(200)
    np.random.seed(66)
    data3 = np.random.randn(200)

    # x 可以输入单个一维数组，也可以是多个一维数组，借助 color/alpha 参数进行颜色区分；使用 label 进行标签；
    # density 为 True 时，纵坐标是分个方块中数量在总数量中的占比；为 False 时，纵坐标就是数量；
    # histtype 方块的形态。bar 是经典形态，多组数据并列显示，横坐标间有间隔（见 rwidth 参数）；barstacked 在数据多维时，不同数据在同一根柱子上垒加；step 只显示梯线，没有填充也没有间隔；stepfilled 在多组数据时柱子相互重叠，如果设置了透明颜色会叠加；
    # bins 是一个数字时，表示横坐标的均分数量，可与下面的 xlim() 搭配使用；如果给定的是一维数组，则相当于指定划分点，除最后一个点是左闭右闭外，其它点都是左闭右开；注意分片数量是数组中数字个数 - 1；
    # range 参数可以使用一个二元 tuple 来限制展示的数值范围，仅在 bins 是数字的时候起作用；如 bins=10, range=(-1, 1) 时，数据中小于 -1 或大于 1 的数据将不会显示；
    # weights 与 x shape 相同，用于指定 x 中每个数字的权重；如果 density=True，每个柱子的纵坐标会进行 normalize(归一化)；
    # cumulative 为 True 的时候，所有柱子从左往右展开时会不断累加；
    # bottom 用于指定 y 轴的起始值；也可以用一个与 bins 数量相同的数组指定每一个柱子的起始值；
    # log 用于指定 y 轴以对数方式伸缩；
    # align 指定柱子在 bin 中的对齐方式，取值有 left/mid/right；orientation 用于指定柱子的方向，取值 horizontal/vertical，注意使用 horizontal 的时候，xy 坐标的地位也会相应转换；
    # rwidth 表示“相对宽度”，是指显示 bar 的区域相对于 bin 的宽度占比，取值 [0, 1]，可以控制不同 bin 中 bar 的间隔。histtype 是 step/stepfilled 时无效；
    # stacked 仅对 histtype=bar/step 有效，histtype=bar 的时候，两个参数一同作用的效果与 histtype=barstacked 效果相同；对 step 类型效果类似。
    plt.hist([data1, data2, data3], histtype="bar", alpha=0.45, bins=20,
             label=["data1", "data2", "data3"], color=["#348ABD", "#ff00ff", "#ffff00"], rwidth=0.8)
    plt.xlim(-3, 3)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()