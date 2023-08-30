import torch

x1 = torch.load("data_save/res1.pt");
x2 = torch.load("data_save/res2.pt");

y = torch.eq(x1, x2);

print(torch.any(y));
