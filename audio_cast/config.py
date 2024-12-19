from dataclasses import dataclass
import dotenv


@dataclass
class Config:
    bot_token: str
    admin_id: int
    allowed_list: list[int]


def get_bot_config() -> Config:
    env: dict = dotenv.dotenv_values()
    admin_id = int(env.get("ADMIN_ID", "No admin id"))
    return Config(
        bot_token=env.get("TOKEN", "No Token"),
        admin_id=admin_id,
        allowed_list=[admin_id]
    )


OUTPUT_DIR = "data"

DATABASE_FILE = "db/database.db"
LOG_FILE = "debug.log"

# prefer preview image sizes
PREVIEW_HEIGHT = 138
PREVIEW_WIDTH = 246

# maximum podcast duration in seconds
MAX_PODCAST_DURATION = 9000

# minimum difference between two loads (minutes)
# MIN_DIFF_DOWNLOAD = 3
