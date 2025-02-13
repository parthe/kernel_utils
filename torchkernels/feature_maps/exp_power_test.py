from .exp_power import ExpPowerORF, ExpPowerRFF
import torch

n,p,d=10,2,7
feature_map = ExpPowerORF(input_dim=d, num_features=p, alpha=1.2)
DEVICE = feature_map.device
X = torch.randn(n,d).to(DEVICE)
Q = torch.randn(d,p).to(DEVICE)
S = torch.randn(p).to(DEVICE)
feature_map.set_Q(Q)
feature_map.test_set_S(S)

Phi = feature_map.c1.to('cpu') * torch.cat([(torch.mm(X, Q)*S).cos(), (torch.mm(X, Q)*S).sin()], dim=-1)
if torch.allclose(feature_map(X), Phi):
    print("ExpPower ORF test complete")
    
feature_map = ExpPowerRFF(input_dim=d, num_features=p, alpha=1.2)
DEVICE = feature_map.device
X = torch.randn(n,d).to(DEVICE)
W1 = torch.randn(d,p).to(DEVICE)
W2 = torch.randn(p).to(DEVICE)
feature_map.set_W1(W1)
feature_map.test_set_W2(W2)
Phi = feature_map.c1.to('cpu') * torch.cat([(torch.mm(X, W1)*W2).cos(), (torch.mm(X, W1)*W2).sin()], dim=-1)
if torch.allclose(feature_map(X), Phi):
    print("ExpPower RFF test complete")