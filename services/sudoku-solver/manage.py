from flask.cli import FlaskGroup
from project import server

cli = FlaskGroup(server.app)

if __name__ == "__main__":
    cli()
