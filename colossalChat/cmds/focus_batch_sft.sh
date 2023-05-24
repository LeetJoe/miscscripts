#!/bin/bash

# 对前128条中文ins集中训练 100 次 * max_epochs

function start_train
{
    dataset_dir=$1
    dataset_file=$2
    pretrain=$3
    save_path=$4
    if test -f ${dataset_dir}${dataset_file}
    then
        dataset=${dataset_dir}${dataset_file}
        dt=`date -R`
        echo ${dt}: ${dataset}, ${path_next} "=>" ${path_now} >> batch_sft.log
        # echo $pretrain
        # echo $dataset
        torchrun --standalone --nproc_per_node=4 train_sft_batch.py \
            --pretrain ${pretrain} \
            --model 'llama' \
            --strategy colossalai_zero2 \
            --log_interval 10 \
            --save_path  ${save_path} \
            --dataset ${dataset} \
            --batch_size 2 \
            --accumulation_steps 32 \
            --lr 2e-5 \
            --max_datasets_size 128 \
            --max_epochs 4
    fi
}


path_next="/data1/neosong/models/colossalChat/sftTrained/batch/turn_even"
path_now="/data1/neosong/models/colossalChat/sftTrained/batch/turn_odd"

dirch="/data1/neosong/datasets/InstructionWild/qapairs/128_ch/"
dsfile="instinwild_ch_128_000.json"

for i in {0..99}
do
    start_train ${dirch} ${dsfile} ${path_next} ${path_now}
    tmp=${path_next}
    path_next=${path_now}
    path_now=${tmp}
done

echo "Done."
