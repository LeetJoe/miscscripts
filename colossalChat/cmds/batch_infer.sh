#!/bin/bash

file='batch_inference.log'

echo 'Provide a list of the top 10 most popular mobile games in Asia' >> ${file}
echo '' >> ${file}

for i in {0..9}
do
  python llama_inference.py /data1/neosong/models/colossalChat/sftTrained/batch/turn_even --wbits 4 \
  --groupsize 128 --load /data1/neosong/models/colossalChat/inference/4bit/llama7b-4bit-batch-20230523.pt \
  --min_length 200 --max_length 500 \
  --text "Provide a list of the most popular mobile games in Asia" >> ${file}
  echo '' >> ${file}
done

echo '' >> ${file}
echo '' >> ${file}

echo '请讲解如何缓解上班族病的症状' >> ${file}
echo '' >> ${file}

for i in {0..9}
do
  python llama_inference.py /data1/neosong/models/colossalChat/sftTrained/batch/turn_even --wbits 4 \
  --groupsize 128 --load /data1/neosong/models/colossalChat/inference/4bit/llama7b-4bit-batch-20230523.pt \
  --min_length 200 --max_length 500 \
  --text "请讲解如何缓解上班族病的症状" >> ${file}
  echo '' >> ${file}
done


