#!/bin/bash

dataset=$1 # "agg"
gpu=$2 # "0"
model=$3 # "0"
dropout=$4 # "0.5"
nhidden=$5 # "200"
lr=$6 # "1e-3"
epochs=$7 # "2"
batch=$8 # "500"
gamma=$9 # "1"
retrain=${10} # "0"


dirmodel="models"
dir=$(ls $dirmodel)
for file in ${dir}
do
  if [[ ${file:0:5} == "multi" && $dataset != "mtg" ]]; then
    continue
  fi

  if [[ $dataset == "mtg" && ${file:0:5} != "multi" ]]; then
    continue
  fi

  cd $dirmodel/$file
  echo "------------------$file------------------"

  # train
  stime=`date +%s`
  echo "python train.py -d ../../data_local/$dataset --dataset $dataset --gpu $gpu --model $model --dropout $dropout --n-hidden $nhidden --lr $lr --max-epochs $epochs --batch-size $batch --gamma $gamma --retrain $retrain"
  # run here
  etime=`date +%s`
  let ctime=etime-stime
  echo "time cost: ${ctime}s"

  # validate
  stime=`date +%s`
  echo "python validate.py -d ../../data_local/$dataset --dataset $dataset --gpu $gpu --model $model --dropout $dropout --n-hidden $nhidden --batch-size $batch --gamma $gamma"
  # run here
  etime=`date +%s`
  let ctime=etime-stime
  echo "time cost: ${ctime}s"

  # validate
  stime=`date +%s`
  echo "python test.py -d ../../data_local/$dataset --dataset $dataset --gpu $gpu --model $model --dropout $dropout --n-hidden $nhidden --batch-size $batch --gamma $gamma --epoch=1"
  # run here
  etime=`date +%s`
  let ctime=etime-stime
  echo "time cost: ${ctime}s"

  printf "\n\n"
  cd ../..
done
