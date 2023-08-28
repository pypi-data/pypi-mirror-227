import typing
import array
from typing import List
from rclpy.node import Node
from raya.constants import *
from raya_constants.interfaces import *
from raya.exceptions_handler import *
from raya.controllers.base_controller import BaseController
from raya.exceptions import *

SIZE = 20
SIZE_PART_BUFFER = (640 * 1024)


class SoundData():

    def __init__(self,
                 channels=1,
                 sample_rate=8000,
                 sample_format=SAMPLE_S16LE,
                 coding_format='PCM'):
        self.channels = channels
        self.sample_rate = sample_rate
        self.sample_format = sample_format
        self.coding_format = coding_format
        self.data = array.array('B', [])

    def addData(self, data):
        pass

    def getData(self):
        return

    def clearData(self):
        pass

    def getChannels(self):
        return

    def getSampleRate(self):
        return

    def getSampleFormat(self):
        return

    def getCodingFormat(self):
        return

    def setChannels(self, channels: int):
        self.channels = channels

    def setSampleRate(self, sample_rate: int):
        self.sample_rate = sample_rate

    def setSampleFormat(self, sample_format: int):
        self.sample_format = sample_format

    def setCodingFormat(self, coding_format: str):
        self.coding_format = coding_format

    def getSampleWidth(self):
        return


class SoundController(BaseController):

    def __init__(self, name: str, node: Node, interface, extra_info):
        pass

    async def play_sound_from_file(self,
                                   filepath: str,
                                   volume: int = 100,
                                   callback_feedback=None,
                                   callback_finish=None,
                                   wait=True) -> None:
        return

    async def play_sound_from_data(self,
                                   audio_raw: list,
                                   volume: int = 100,
                                   callback_feedback=None,
                                   callback_finish=None,
                                   wait=True) -> None:
        return

    async def play_predefined_sound(self,
                                    sound_name: str,
                                    volume: int = 100,
                                    callback_feedback=None,
                                    callback_finish=None,
                                    wait=True) -> None:
        return

    def get_predefined_sounds(self) -> List[str]:
        return

    async def record_sound(self,
                           duration: float = 60.0,
                           mic_id: str = '',
                           path: str = '',
                           callback_finish: typing.Callable = None,
                           callback_finish_async: typing.Callable = None,
                           wait: bool = True) -> SoundData:
        return

    def is_playing(self):
        return

    def is_recording(self):
        return

    async def play_sound(self,
                         name: str = None,
                         path: str = None,
                         data: SoundData = None,
                         volume: int = 100,
                         callback_finish: typing.Callable = None,
                         callback_finish_async: typing.Callable = None,
                         callback_feedback: typing.Callable = None,
                         callback_feedback_async: typing.Callable = None,
                         wait: bool = True) -> None:
        pass

    async def cancel_sound(self):
        pass
