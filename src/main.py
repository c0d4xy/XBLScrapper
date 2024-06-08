import os
import time
import requests
import keyboard
from typing import List
from logger import Logging
from config import Settings

class XBLScrapper():

    def __init__(self) -> None:
        self.logger = Logging()
        self.xbl_api_key = Settings.XBL_API_KEY
        self.api_base_url = "https://xbl.io/api/v2"

    @staticmethod
    def save_gamertags_to_file(gamertags: List[str], file_path: str = "output/gamertags.txt") -> None:
        with open(file_path, "a") as f:
            f.write("\n".join(gamertags) + "\n")

    def get_user_friends(self, gamertag: str) -> (List[str] | None):
        xuid = self.__convert_gamertag_to_xuid(gamertag)

        if not xuid:
            return

        url = self.api_base_url + f"/friends/{xuid}"
        headers = {
            "X-Authorization": self.xbl_api_key,
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status() 
            data = response.json()
            return self.__get_friends_gamertag(data)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error retrieving friends for {gamertag}: {e}")
            return

    def __get_friends_gamertag(self, data: dict) -> List[str]:
        return [friend.get("gamertag") for friend in data.get("people", [])]

    def __convert_gamertag_to_xuid(self, gamertag: str) -> str:
        url = self.api_base_url + f"/search/{gamertag}"
        headers = {
            "X-Authorization": self.xbl_api_key,
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return str(data["people"][0]["xuid"])
        
        except (requests.exceptions.RequestException, IndexError, KeyError) as e:
            self.logger.error(f"Error retrieving XUID for {gamertag}: {e}")
            return
    
    def run_program(self) -> None:

        if os.name == "nt":
            os.system("cls")

        else:
            os.system("clear")

        self.logger.magenta(Settings.ASCII_BANNER)

        initial_gamertag = input(" Enter initial gamertag: ")
        queue = [initial_gamertag]
        processed_gamertags = set()

        while True:

            if keyboard.is_pressed("x"):
                break

            current_gamertag = queue.pop(0)
            if current_gamertag in processed_gamertags:
                continue

            friends = self.get_user_friends(current_gamertag)

            if friends is None:
                self.logger.warning(f"Failed to retrieve friends for {current_gamertag}. Retrying...")
                continue

            processed_gamertags.add(current_gamertag)
            self.logger.success(f"{current_gamertag} -> {len(friends)} friends found")

            if not os.path.exists("output/"):
                os.makedirs("output/")

            XBLScrapper.save_gamertags_to_file(friends)
            queue.extend(friends)
            time.sleep(10)

if __name__ == "__main__":
    XBLScrapper().run_program()
