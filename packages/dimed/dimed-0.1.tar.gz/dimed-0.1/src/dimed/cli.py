import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', default='Dinar', help='Please write your name')
def hi(name):
    """Hi command"""
    click.echo(f'Hi, {name}!')

@cli.command()
@click.option('--age', default=36, help='Please provide your age')
def retired(age):
    """When will you be retired"""
    click.echo(f'You will be retired in {60-age} years')

if __name__ == '__main__':
    cli()
    