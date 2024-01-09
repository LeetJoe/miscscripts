import os
import pandas as pd
import numpy as np

data_path = '../data'
save_path = '../newdata'

if not os.path.exists(save_path):
    os.makedirs(save_path)

train_data = pd.read_csv(os.path.join(data_path, 'dataTrain.csv'))
test_data = pd.read_csv(os.path.join(data_path, 'dataB.csv'))
submission = pd.read_csv(os.path.join(data_path, 'submit_example_B.csv'))
data_nolabel = pd.read_csv(os.path.join(data_path, 'dataNoLabel.csv'))

train_data['f47'] = train_data['f1'] * 10 + train_data['f2']
test_data['f47'] = test_data['f1'] * 10 + test_data['f2']
train_data['f3'] = train_data['f3'].map({'low': 0, 'mid': 1, 'high': 2})
test_data['f3'] = test_data['f3'].map({'low': 0, 'mid': 1, 'high': 2})

# 暴力Feature 位置
loc_f = ['f1', 'f2', 'f4', 'f5', 'f6']
for df in [train_data, test_data]:
    for i in range(len(loc_f)):
        for j in range(i + 1, len(loc_f)):
            df[f'{loc_f[i]}+{loc_f[j]}'] = df[loc_f[i]] + df[loc_f[j]]
            df[f'{loc_f[i]}-{loc_f[j]}'] = df[loc_f[i]] - df[loc_f[j]]
            df[f'{loc_f[i]}*{loc_f[j]}'] = df[loc_f[i]] * df[loc_f[j]]
            df[f'{loc_f[i]}/{loc_f[j]}'] = df[loc_f[i]] / (df[loc_f[j]]+1)

# 暴力Feature 通话
com_f = ['f43', 'f44', 'f45', 'f46']
for df in [train_data, test_data]:
    for i in range(len(com_f)):
        for j in range(i + 1, len(com_f)):
            df[f'{com_f[i]}+{com_f[j]}'] = df[com_f[i]] + df[com_f[j]]
            df[f'{com_f[i]}-{com_f[j]}'] = df[com_f[i]] - df[com_f[j]]
            df[f'{com_f[i]}*{com_f[j]}'] = df[com_f[i]] * df[com_f[j]]
            df[f'{com_f[i]}/{com_f[j]}'] = df[com_f[i]] / (df[com_f[j]]+1)

# 离散化
all_f = [f'f{idx}' for idx in range(1, 47) if idx != 3]
for df in [train_data, test_data]:
    for col in all_f:
        df[f'{col}_log'] = df[col].apply(lambda x: int(np.log(x)) if x > 0 else 0)
# 特征交叉
log_f = [f'f{idx}_log' for idx in range(1, 47) if idx != 3]
for df in [train_data, test_data]:
    for i in range(len(log_f)):
        for j in range(i + 1, len(log_f)):
            df[f'{log_f[i]}_{log_f[j]}'] = df[log_f[i]]*10000 + df[log_f[j]]

cat_columns = ['f3']
num_columns = [ col for col in train_data.columns if col not in ['id', 'label', 'f3']]
feature_columns = num_columns + cat_columns
target = 'label'

train = train_data[feature_columns]
label = train_data[target]
test = test_data[feature_columns]

#去除干扰数据
train = train[:50000]
label = label[:50000]

pd.DataFrame(data=train).to_csv(os.path.join(save_path, 'dataTrain.csv'), index=False)
pd.DataFrame(data=test).to_csv(os.path.join(save_path, 'dataB.csv'), index=False)
pd.DataFrame(data=label).to_csv(os.path.join(save_path, 'label.csv'), index=False)
