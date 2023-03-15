from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import check_output
import pyuac
from infi.systray import SysTrayIcon
import win32gui

import sys
sys.stdout = open('stdout.txt', 'w')
sys.stderr = open('stderr.txt', 'w')

hostName = "localhost"
serverPort = 32123
webServer = None

def checkWakeLocks(self):
    result = check_output("powercfg requests", shell=True).decode()[10:15]
    if result == "None.":
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write('{"hasWakeLocks": false}'.encode(encoding='utf_8'))
    else:
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write('{"hasWakeLocks": true}'.encode(encoding='utf_8'))
        
def placeWindow(self):
    hwnd = win32gui.FindWindowEx(0,0,0, "Photo Screen Saver Screensaver Page")
    win32gui.SetForegroundWindow(hwnd)
    self.send_response(200)

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/check-wake-locks":
            checkWakeLocks(self)
        elif self.path == "/place-window":
            placeWindow(self)
            
def onQuit(systray):
    webServer.server_close()

def main():
    with SysTrayIcon("screensaver.ico", "Screensaver Companion", on_quit=onQuit) as systray:
        global webServer
        webServer = HTTPServer((hostName, serverPort), MyServer)
        # print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        systray.shutdown()
        # print("Server stopped.")
    
if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        # print("Re-launching as admin!")
        pyuac.runAsAdmin()
    else:        
        main()  # Already an admin here.
