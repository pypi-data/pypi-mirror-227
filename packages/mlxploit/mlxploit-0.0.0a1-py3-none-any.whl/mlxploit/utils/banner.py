from rich import print
from rich.console import Console


def display(console: Console, subtitle: str = ""):
    console.print(f"""[bold cyan]
           __            _       _ _   
  /\/\    / /__  ___ __ | | ___ (_) |_ 
 /    \  / / \ \/ / '_ \| |/ _ \| | __|
/ /\/\ \/ /___>  <| |_) | | (_) | | |_ 
\/    \/\____/_/\_\ .__/|_|\___/|_|\__|
                  |_|                   [/bold cyan]
    [bold yellow]{subtitle}[/bold yellow]
""")
