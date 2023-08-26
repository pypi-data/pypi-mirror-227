
import pywhatkit
import pyautogui
import time
import pandas as pd

from pynput.keyboard import Key, Controller

class Texter:
    def __init__(self,) -> None:

        self.keyboard = Controller()

    
    def prep_message(self, df: pd.DataFrame) -> str:

        availabilities = "".join([f"\n{day} | {time} | {location}" for day, time, location in zip(df["Day"], df["Time"], df["Location"])])

        return f"""
Court availability updates:
    
    Day    |   Time    | Location {availabilities}
        """


    def send(self, number: str, df: pd.DataFrame) -> None:

        pywhatkit.sendwhatmsg_instantly(
            phone_no=number, 
            message=self.prep_message(df),
        )

        time.sleep(2)
        pyautogui.click()
        time.sleep(2)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)



