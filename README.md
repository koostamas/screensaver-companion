# Screensaver Companion
A Companion app for the [Screensaver Chrome Extension](https://github.com/koostamas/screensaver) (Windows only!)

## How to use
1. Clone the repository
2. Install `pyuac`, `infi.systray` and `win32gui` with `pip`
3. Run the script

## Setting up auto-launch with Task Scheduler
1. Open Task Scheduler
2. Create a new task
3. On the Settings tab, check Run with highest privileges
4. On the Triggers tab, add a trigger for any user at log on
5. On the actions tab, add a new Action to start a program
  1. The program should be the path to the `pythonw` (mind the w, to run the script without console) executable on your system
  2. The arguments should be `server.py`
  3. Start in should be the path to the cloned repository on your system
6. Done, this task will run the server every time you log into your computer

