#!/bin/bash

# 1.bash 对代码缩进要求并不严格；
# 2.虽然支持数字运算，但是尽量避免做数字运算；
# 3."${var}"的变量引用形式虽然是 IDE 建议的，但是并不总是正确，有些时候在作为其它命令的参数时，使用这种格式反而出错，去掉 "" 就正常了；


# 变量
code_base='.'
dataset=icews14
walk_num='200'
min_rule_conf="0.1"

# 列表
valid_thresh_list=('0.9' '0.92' '0.94' '0.96' '0.98')

# 命令行参数，${0} 是脚本文件自身，${#} 表示后面第 # 个参数
cp "${0}" "${data_base}"/origin/

# 循环列表
for valid_thresh in "${valid_thresh_list[@]}"
do
  echo "${valid_thresh}"
done

# 循环 range
for i in {1..10}
do
  echo "${i}"
done

# 获取其它系统命令的返回
str_mln=`head -n 1 "${mln_base}"/result_mln.txt`
str_em=`cat "${exp_base}"/"${i}"/result_em.txt`

# 字符串拼接
 mln_base="${code_base}"/"${dataset}"/mln

# 在拼接字符串中添加换行符
str_report=$(printf "%s, %s\n mln:\n%s" "${valid_thresh}" "${dataset}" "${str_mln}")

# 判断文件/目录是否存在
if [[ ! -e "${mln_base}" ]]; then
  mkdir -p "${mln_base}"
fi

# 判断字符串相等
if [ "${i}" -eq "0" ]; then
  echo "zero"
else
  echo "not zero"
fi

# 数字加减运算
i=4
i_pre=$(( i - 1 ))