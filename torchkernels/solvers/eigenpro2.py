from torchkernels.linalg.eigh import top_eigensystem, nystrom_extension
from torchkernels.linalg.fmm import KmV
from __init__ import timer
from math import ceil


def eigenpro2(K, X, y, s, q, m=None, epochs=1):
    """
        Storage: (n x q) + s2
        FLOPS at setup: (s x q2) + 
        FLOPS per batch: (n x m) + {(m x q) + (n x q)}
    """
    timer.tic()
    n = X.shape[0]
    nids = torch.randperm(n)[:s]
    E, L, lqp1, beta = top_eigensystem(K, X[nids], q)
    E.mul_(((1-lqp1/L)/L/len(nids)).sqrt())
    a = torch.zeros_like(y, dtype=E.dtype)
    bs_crit = int(beta/lqp1) + 1
    if m is None: m = bs_crit 
    lr = lambda bs: 1/beta if bs < bs_crit else 2/(beta+(bs-1)*lqp1)
    print(f"bs_crit={bs_crit}, m={m}, lr={lr(m)}")
    timer.toc("EigenPro_2 Setup :", restart=True)
    for t in range(epochs):
        batches = torch.randperm(n).split(m)
        for i, bids in enumerate(batches):
            gm = KmV(K, X[bids], X, a) - y[bids].type(a.type())
            a[bids] = a[bids] - lr(len(bids)) * gm
            a[nids] += lr(len(bids)) *  E @ (E.T  @ KmV(K, X[nids], X[bids], gm))
    timer.toc("EigenPro_2 Iterations :")
    return a

if __name__ == "__main__":

    from torchkernels.kernels.radial import LaplacianKernel
    from __init__ import lstsq
    import torch
    torch.set_default_dtype(torch.float64)
    K = LaplacianKernel(bandwidth=1.)
    n, d, c, s, q = 100, 3, 2, 30, 5
    X = torch.randn(n, d)
    y = torch.randn(n, c)
    ahat = eigenpro2(K, X, y, s, q, epochs=100)
    astar = lstsq(K, X, X, y)
    print((KmV(K,X,X,ahat)-y).var())
    print((KmV(K,X,X,astar)-y).var())
