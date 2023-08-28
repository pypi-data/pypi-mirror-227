import typer
from typing_extensions import Annotated

options = {
    # ML model
    'device': Annotated[str, typer.Option("--device", "-d", help="Device to be used for operations. Choose 'cuda' or 'cpu'.")],
    'target': Annotated[str, typer.Option("--target", "-t", help="Target ML model. Specify the the file path or common ML model.")],

    # Output
    'quiet': Annotated[bool, typer.Option("--quiet", "-q", help="Queit mode displays few outputs.")],
    'verbose': Annotated[bool, typer.Option("--verbose", "-v", help="Verbose mode displays louder.")],

    # Attack
    'attack_mode': Annotated[str, typer.Option("--mode", "-m", help="Attack mode.")],

    # Scan
    'scan_mode': Annotated[str, typer.Option("--mode", "-m", help="Scan mode.")],
}