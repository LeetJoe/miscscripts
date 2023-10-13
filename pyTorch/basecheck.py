
import torch

print("torch version: ", torch.__version__)
print("cuda version: ", torch.version.cuda)
print("cuda is available: ", torch.cuda.is_available())
device_count = torch.cuda.device_count()
print("gpu count: ", device_count)
for i in range(device_count):
    print("--->", torch.cuda.get_device_name(i))


