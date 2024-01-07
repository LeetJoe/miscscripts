## 机器学习与模型识别实践作业

本作业 github 地址：[https://github.com/LeetJoe/miscscripts/tree/main/UCAS/PRML/homework](https://github.com/LeetJoe/miscscripts/tree/main/UCAS/PRML/homework)

选题：手写数字识别

选用方法：SVM、Gradient Boosting 和 CNN


## 系统环境

1. 操作系统：MacOS 14.1.1 (23B81)
2. CPU：2.6 GHz 六核Intel Core i7
3. 内存：16GB 2400 MHz DDR4


## 软件环境

```
# 创建 conda 虚拟环境并激活
conda create -n prml
conda activate prml

# 安装 python 及依赖模块
conda install python 3.6.13
conda install tensorflow=1.13.1
conda install chardet
conda install numpy

```

## 训练数据

由于计算资源有限，我从 [MINIST](http://yann.lecun.com/exdb/mnist/) 中截取了不超过 10000 条训练数据和不超过 2000 条测试数据，并没有使用全部的数据。

为了对比这三种训练方法的性能，我设置了不同的训练规模的数据，来对比它们在训练时间和正确率上的差异。


## 训练结果

原始实验记录见 [record.txt](data/record.txt)。

<table>
	<tr>
		<th rowspan="2">训练集</th><th rowspan="2">测试集</th><th colspan="2">SVM</th><th colspan="2">Boosting</th><th colspan="2">CNN</th>
	</tr>
	<tr>
		<th>time(s)</th><th>acc</th><th>time(s)</th><th>acc</th><th>time(s)</th><th>acc</th>
	</tr>
	<tr>
		<td style="text-align:right">2000</td><td style="text-align:right">400</td>
		<td style="text-align:right">15.26</td><td style="text-align:right">0.8775</td>
		<td style="text-align:right">367.13</td><td style="text-align:right">0.8725</td>
		<td style="text-align:right; color:orange;">369.13</td><td style="text-align:right">0.9525</td>
	</tr>
	<tr>
		<td style="text-align:right">4000</td><td style="text-align:right">800</td>
		<td style="text-align:right">41.27</td><td style="text-align:right">0.9175</td>
		<td style="text-align:right">832.65</td><td style="text-align:right">0.8837</td>
		<td style="text-align:right; color:orange;">797.00</td><td style="text-align:right">0.9450</td>
	</tr>
	<tr>
		<td style="text-align:right">6000</td><td style="text-align:right">1200</td>
		<td style="text-align:right">150.18</td><td style="text-align:right">0.9283</td>
		<td style="text-align:right">1232.20</td><td style="text-align:right">0.8875</td>
		<td style="text-align:right; color:orange;">1188.28</td><td style="text-align:right">0.9433</td>
	</tr>
	<tr>
		<td style="text-align:right">8000</td><td style="text-align:right">1600</td>
		<td style="text-align:right">196.83</td><td style="text-align:right">0.9231</td>
		<td style="text-align:right"></td><td style="text-align:right"></td>
		<td style="text-align:right; color:orange;">1554.01</td><td style="text-align:right">0.9500</td>
	</tr>
	<tr>
		<td style="text-align:right">10000</td><td style="text-align:right">2000</td>
		<td style="text-align:right">290.56</td><td style="text-align:right">0.9335</td>
		<td style="text-align:right"></td><td style="text-align:right"></td>
		<td style="text-align:right; color:orange;">1201.65</td><td style="text-align:right">0.9505</td>
	</tr>
</table>


## 结果分析

由于 CNN 利用了多核运行，其并发数设置为 12，实际运行并发在 10 左右，所以其运行时间应乘以 10 才近似等于其实际运行时间。

由于计算资源有限，为避免训练时间过长，我设置了当在测试集上的正确率超过 95% 或达到指定 epochs 时就停止训练，在此条件下比较不同训练方法、训练规模在训练时间和训练正确率上的差异。

从结果来看：
* CNN 在测试集上正确率最高，而且在不同规模的数据集上结果都比较稳定；
* SVM 在测试集上正确率没有 CNN 高但是仍然优于 Boosting；在训练速度上有很大的优势；
* Boosting 没有使用并行计算，训练速度不如 SVM 但是也比 CNN 快很多；不过测试集上正确率在三者之中是最低的。



