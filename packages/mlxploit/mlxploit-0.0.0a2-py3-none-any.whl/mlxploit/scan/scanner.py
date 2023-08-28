import torch
from torchinfo import summary

from rich.console import Console

from mlxploit.utils.device_selector import select_device
from mlxploit.utils.model_loader import load_model


class Scanner():
    def __init__(
        self,
        target: str,
        mode: str = 'all',
        device: str = None,
        quiet: bool = False,
        verbose: bool = False,
        console: Console = None,
    ):
        self.device = select_device(device)

        # Config
        self.quiet = quiet
        self.verbose = verbose
        self.console = console

        # Scan mode
        self.mode = mode

        # Model
        self.model = load_model(target)
        self.model_params = {}


    def scan(self):
        """
        Scan ML Model
        """
        # TODO: Scan poisoning
        if self.mode == 'all':
            self.console.print(":mag: Scanning ML model entirely...")

        for name, param in self.model.named_parameters():
            self.model_params[name] = param


    def summarize(self):
        """
        Output summary of ML Model
        *This method depends on `torchinfo` developed by TylerYep. Repo: https://github.com/TylerYep/torchinfo.
        """
        verbose_n = 1
        if self.quiet is True:
            verbose_n = 0
        elif self.verbose is True:
            verbose_n = 2

        self.console.print(summary(self.model, device=self.device, verbose=verbose_n))
