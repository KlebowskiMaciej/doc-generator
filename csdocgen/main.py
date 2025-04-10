import click
import os
from csdocgen.generator import CSDocGenerator

@click.command()
@click.option("--path", required=True, help="Path to the C# file")
def main(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No such file: {path}")

    with open(path, 'r', encoding='utf-8') as file:
        code_content = file.read()

    generator = CSDocGenerator()
    documented_code = generator.insert_docs_to_code(code_content)

    with open(path, 'w', encoding='utf-8') as file:
        file.write(documented_code)

    click.echo(f"Documentation added successfully to {path}")

if __name__ == "__main__":
    main()
