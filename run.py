from app.init import create_app
from app.config import Config

config = Config()

app = create_app()

if __name__ == "__main__":
    app.run(
        host=config.web_host,
        port=config.web_port,
        debug=config.debug
    )