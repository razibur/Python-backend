import typer
import os
import random
import string
from pathlib import Path
import time
from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer()

@app.command()
def find(
    file_type: str,
    directory: str
):
    start_time = time.time()
    if file_type[0] != '.':
        print("File type must start with a dot.")
        raise typer.Exit(code=0)

    base_dir = Path(directory)
    if not base_dir.exists():
        print(f"Directory '{directory}' does not exist.")
        raise typer.Exit(code=0)
    
    matching_files = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task("Searching for files...", start=True)
        for path in base_dir.rglob(f'*{file_type}'):
            if path.is_file():
                matching_files.append(str(path))
                time.sleep(0.3)        

    print(f"Found {len(matching_files)} file(s) with extension '{file_type}':")
    for file_path in matching_files:
        print(file_path)
        
@app.command()
def other(name: str):
    print(f"Other command. {name}")

if __name__ == "__main__":
    app()