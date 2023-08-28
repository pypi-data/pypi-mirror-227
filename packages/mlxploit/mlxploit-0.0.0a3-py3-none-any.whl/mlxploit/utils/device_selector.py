import torch


def select_device(device = None):
    if device is None:
        return 'cuda' if torch.cuda.is_available() else 'cpu'
    return device