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


OUTPUT_DIR = "data"
