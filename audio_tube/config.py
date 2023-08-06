from dataclasses import dataclass
import dotenv


@dataclass
class Config:
    bot_token: str


def get_bot_config() -> Config:
    env: dict = dotenv.dotenv_values()
    return Config(
        bot_token=env.get("TOKEN", "No Token")
    )


OUTPUT_DIR = "data"

# prefer preview image sizes
PREVIEW_HEIGHT = 138
PREVIEW_WIDTH = 246

# max podcast duration: 2 hours and 30 minutes (value in a seconds)
MAX_PODCAST_DURATION = 9000
