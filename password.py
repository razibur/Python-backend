import typer
import random
import string
from typing_extensions import Annotated

app = typer.Typer()

def generate_password(
    length: int = 12,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_numbers: bool = True,
    use_special: bool = True
) -> str:
    characters = []
    
    if use_uppercase:
        characters.extend(string.ascii_uppercase)
    if use_lowercase:
        characters.extend(string.ascii_lowercase)
    if use_numbers:
        characters.extend(string.digits)
    if use_special:
        characters.extend(string.punctuation)
    
    if not characters:
        print("At least one character type must be selected")
        raise ValueError("At least one character type must be selected")
    
    password = []
    if use_uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if use_lowercase:
        password.append(random.choice(string.ascii_lowercase))
    if use_numbers:
        password.append(random.choice(string.digits))
    if use_special:
        password.append(random.choice(string.punctuation))
    
    while len(password) < length:
        password.append(random.choice(characters))
    
    random.shuffle(password)
    return ''.join(password)
    
@app.command()
def generate(
    length: Annotated[int, typer.Option("--length", help="Length of the password")] = 12,
    no_uppercase: Annotated[bool, typer.Option("--no-uppercase", help="Exclude uppercase letters")] = False,
    no_lowercase: Annotated[bool, typer.Option("--no-lowercase", help="Exclude lowercase letters")] = False,
    no_numbers: Annotated[bool, typer.Option("--no-numbers", help="Exclude numbers")] = False,
    no_special: Annotated[bool, typer.Option("--no-special", help="Exclude special characters")] = False,
):
    try:
        password = generate_password(
            length=length,
            use_uppercase=not no_uppercase,
            use_lowercase=not no_lowercase,
            use_numbers=not no_numbers,
            use_special=not no_special,
        )
        print(password)
    except ValueError as e:
        print(f"Error: {e}")
        raise typer.Exit(code=1)
    
@app.command()
def other():
    print("Other command")

if __name__ == "__main__":
    app()