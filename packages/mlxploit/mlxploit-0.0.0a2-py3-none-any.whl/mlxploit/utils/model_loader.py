import torch
from rich import print


def load_model(model_name):
    model = None

    try:
        model = torch.load(model_name)
    except:
        print(":eyes: [yellow]target is not file path for ML model.[/yellow]")
    
    return model