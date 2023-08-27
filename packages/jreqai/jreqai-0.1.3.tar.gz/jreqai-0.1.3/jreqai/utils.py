def device():
    import torch

    is_m1 = False
    if hasattr(torch.backends, 'mps'):
        is_m1 = torch.backends.mps.is_built() and torch.backends.mps.is_available()
    if is_m1:
        return torch.device('mps')

    is_cuda = torch.cuda.is_available()
    if is_cuda:
        return torch.device('cuda')

    return torch.device('cpu')
