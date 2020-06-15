from win32 import win32gui, win32api
from ctypes import windll
import time

from vk_code import VK_CODE



def pressAndHold(*args):
    '''
    press and hold. Do NOT release.
    accepts as many arguments as you want.
    e.g. pressAndHold('left_arrow', 'a','b').
    '''
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0, 0, 0)
        time.sleep(.05)


def press(*args):
    '''
    one press, one release.
    accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
    '''
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0, 0, 0)
        time.sleep(.05)
        win32api.keybd_event(VK_CODE[i], 0, 0x0002, 0)


def release(*args):
    '''
    release depressed keys
    accepts as many arguments as you want.
    e.g. release('left_arrow', 'a','b').
    '''
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0, 0x0002, 0)


class WindowAction:
    @staticmethod
    def switch_forward():
        pressAndHold("alt")
        press("tab")
        time.sleep(0.6)
        release("alt")
        pass

    @staticmethod
    def switch_backward():
        pressAndHold("alt")
        pressAndHold("shift")
        press("tab")
        time.sleep(0.6)
        release("alt")
        release("shift")
        pass

    @staticmethod
    def minimize_all():
        pressAndHold("win")
        press("m")
        release("win")
        pass

    @staticmethod
    def maximize_all():
        pressAndHold("win")
        pressAndHold("shift")
        press("m")
        release("shift")
        release("win")
        pass

    pass
