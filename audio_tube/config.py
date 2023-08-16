from dataclasses import dataclass
import dotenv


@dataclass
class Config:
    bot_token: str
    admin_id: int


def get_bot_config() -> Config:
    env: dict = dotenv.dotenv_values()
    return Config(
        bot_token=env.get("TOKEN", "No Token"),
        admin_id=int(env.get("ADMIN_ID", "No admin id"))
    )


OUTPUT_DIR = "data"

# prefer preview image sizes
PREVIEW_HEIGHT = 138
PREVIEW_WIDTH = 246

# maximum podcast duration in seconds
MAX_PODCAST_DURATION = 9000

# minimum difference between two loads (minutes)
MIN_DIFF_DOWNLOAD = 3
