from dataclasses import dataclass
import dotenv


@dataclass
class Config:
    bot_token: str


def get_config():
    env: dict = dotenv.dotenv_values()
    return Config(
        bot_token=env.get("TOKEN", "No Token")
    )


on_delete_filenames = []
OUTPUT_DIR = "data"

# prefer preview image sizes
PREVIEW_HEIGHT = 188
PREVIEW_WIDTH = 336
