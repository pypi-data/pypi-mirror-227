from rich import print
from rich.console import Console

from mlxploit.utils.device_selector import select_device
from mlxploit.utils.model_loader import load_model


class Adversarial():
    def __init__(
        self,
        target: str,
        device: str = None,
        verbose: bool = False,
        console: Console = None
    ):
        self.device = select_device(device)

        # Config
        self.verbose = verbose

        # Model
        self.target_model = load_model(target)
        self.device = device
        self.console = console

    
    def attack(self):
        self.console.print(":bomb: Generating adversarial examples...")
