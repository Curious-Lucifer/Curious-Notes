import os
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler

from pathlib import Path

import typer
import mkdocs.commands.serve

app = typer.Typer()

mkdocsa_name = 'mkdocs.yml'
docs_root_path = Path('docs')


@app.command()
def build():
    site_path = Path('site').absolute()
    current_dir = os.getcwd()
    os.chdir(docs_root_path)
    typer.echo('Building docs')
    subprocess.run(['mkdocs', 'build', '--site-dir', site_path], check=True)
    os.chdir(current_dir)


@app.command()
def serve():
    typer.echo('This is here only to preview a site with docs already built.')
    typer.echo('Make sure you run the build command first.')
    os.chdir('site')
    server_address = ('', 8000)
    server = HTTPServer(server_address, SimpleHTTPRequestHandler)
    typer.echo('Serving at : http://127.0.0.1:8000')
    server.serve_forever()


@app.command()
def live():
    os.chdir(docs_root_path)
    mkdocs.commands.serve.serve(dev_addr='127.0.0.1:8000')


if __name__ == '__main__':
    app()
