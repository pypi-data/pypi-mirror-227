import typer
from typing import Optional
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

import toml

from mlxploit.attack.modes import attack_modes
from mlxploit.attack.adversarial.attacker import Adversarial
from mlxploit.options import options
from mlxploit.utils import banner
from mlxploit.scan.scanner import Scanner

# Get meta data from pyproject.toml
# Resource: https://github.com/python-poetry/poetry/issues/273#issuecomment-1628665507
pyproject = toml.load('pyproject.toml')
__version__ = pyproject["tool"]["poetry"]["version"]

console = Console()

app = typer.Typer()


@app.command(name="attack", help="Attack ML Model")
def attack(
    target: options['target'],
    mode: options['attack_mode']    = None,
    device: options['device']       = None,
    quiet: options['quiet']         = False,
    verbose: options['verbose']     = False,
):
    console.quiet = quiet

    banner.display(console, "Attack ML Model")

    # Mode selector
    mode_name = None
    if mode is None:
        while mode is None:
            q_text = ""
            for i, attack_mode in enumerate(attack_modes):
                q_text += f"[bold bright_green]{i+1}[/bold bright_green]. {attack_mode[1]}"
                if i < (len(attack_modes) - 1):
                    q_text += "\n"
            print("\n", Panel.fit(
                q_text,
                title=":question_mark: What attack mode do you use? :question_mark:",
                padding=(1, 2)))

            choice = Prompt.ask("\n:memo: Choose number")

            try:
                if int(choice) < 1:
                    raise
                choiced_mode = attack_modes[int(choice) - 1]
                mode = choiced_mode[0]
                mode_name = choiced_mode[1]

                proceed = Confirm.ask(f"\n:question_mark: {mode_name} was choosed. Proceed?", default=False)
                if not proceed:
                    mode = None
                    mode_name = None
            except:
                print(":exclamation: [red]Please choose correct number.[/red]")

    print("\n", Panel.fit(f"[bold bright_cyan]{mode_name}[/bold bright_cyan]",
                        title=":boom: Attack Mode :boom:",
                        padding=(1, 2)))
    
    console.print(f"\n:rocket: Starting {mode_name}...")

    if mode == 'adversarial':
        attacker = Adversarial(target, device=device, console=console)
        attacker.attack()
    elif mode == 'inversion':
        pass


@app.command(name="scan", help="Scan ML Model")
def scan(
    target:     options['target'],
    mode:       options['scan_mode']    = 'all',
    device:     options['device']       = None,
    quiet:      options['quiet']        = False,
    verbose:    options['verbose']      = False,
):
    console.quiet = quiet

    banner.display(console, "Scan ML Model")

    scanner = Scanner(target, mode=mode, device=device, quiet=quiet, verbose=verbose)
    scanner.scan()


@app.command(name="version", help="Display the version of MLexploit")
def version():
    print(f"MLexploit version {__version__}")

