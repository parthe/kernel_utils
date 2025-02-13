from .gaussian import GaussianORF, GaussianRFF
import torch

n,p,d=10,2,7
feature_map = GaussianORF(input_dim=d, num_features=p)
DEVICE = feature_map.device
X = torch.randn(n,d).to(DEVICE)
Q = torch.randn(d,p).to(DEVICE)
S = torch.randn(p).to(DEVICE)
feature_map.set_Q(Q)
feature_map.test_set_S(S)

Phi = feature_map.c1.to('cpu') * torch.cat([(torch.mm(X, Q)*S).cos(), (torch.mm(X, Q)*S).sin()], dim=-1)
if torch.allclose(feature_map(X), Phi):
    print("Gaussian ORF test complete")
    
feature_map = GaussianRFF(input_dim=d, num_features=p)
DEVICE = feature_map.device
X = torch.randn(n,d).to(DEVICE)
W1 = torch.randn(d,p).to(DEVICE)
W2 = torch.randn(p).to(DEVICE)
feature_map.set_W1(W1)
feature_map.test_set_W2(W2)
Phi = feature_map.c1.to('cpu') * torch.cat([(torch.mm(X, W1)).cos(), (torch.mm(X, W1)).sin()], dim=-1)
if torch.allclose(feature_map(X), Phi):
    print("Gaussian RFF test complete")