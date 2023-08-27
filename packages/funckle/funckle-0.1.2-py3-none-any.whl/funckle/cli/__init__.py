import os
import typer
from pathlib import Path
from cookiecutter.main import cookiecutter

from .login import login_user
from .deploy import deploy_package


app = typer.Typer()

@app.command()
def login():
    login_user()


@app.command()
def new():
    file_path = Path(os.path.abspath(__file__)).joinpath("../../.cookiecutter/new-function").resolve()
    cookiecutter(file_path.absolute().as_posix())

@app.command()
def deploy(folder_path: Path = typer.Argument(Path.cwd()), version: str = typer.Option("0.0.1", help="Version of the function")):
    typer.echo("Deploying Function...")
    deploy_package(
        folder_path=folder_path,
        version=version
    )

if __name__ == "__main__":
    app()