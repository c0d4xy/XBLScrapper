from pydantic_settings import BaseSettings

class _Settings(BaseSettings):
    XBL_API_KEY: str
    ASCII_BANNER: str = """
 __  _____ _    ___
 \ \/ / _ ) |  / __| __ _ _ __ _ _ __ _ __  ___ _ _
  >  <| _ \ |__\__ \/ _| '_/ _` | '_ \ '_ \/ -_) '_|
 /_/\_\___/____|___/\__|_| \__,_| .__/ .__/\___|_|
                                |_|  |_|  

 Telegram: @c0daxy | Discord: @codaxy
"""

Settings = _Settings(_env_file=".env")
