from http.server import BaseHTTPRequestHandler, HTTPServer
from subprocess import check_output
import pyuac
import pywinauto
from infi.systray import SysTrayIcon

import sys
sys.stdout = open('stdout.txt', 'w')
sys.stderr = open('stderr.txt', 'w')

hostName = "localhost"
serverPort = 32123
webServer = None

paused = False

def checkWakeLocks(self):
    result = check_output("powercfg requests", shell=True).decode()[10:15]
    global paused
    if result == "None." and paused == False:
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write('{"hasWakeLocks": false}'.encode(encoding='utf_8'))
    else:
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write('{"hasWakeLocks": true}'.encode(encoding='utf_8'))
        
def placeWindow(self):
    app = pywinauto.application.Application().connect(best_match='Photo Screen Saver Screensaver Page')
    app.top_window().set_focus()
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.send_header("Access-Control-Allow-Origin", "*")
    self.end_headers()
    self.wfile.write('{"status": "OK"}'.encode(encoding='utf_8'))

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/check-wake-locks":
            checkWakeLocks(self)
        elif self.path == "/place-window":
            placeWindow(self)
            
def pause(sysTrayIcon):
    global paused
    paused = True
    sysTrayIcon.update(icon='screensaver_paused.ico')
    
    
def resume(sysTrayIcon):
    global paused
    paused = False
    sysTrayIcon.update(icon='screensaver.ico')
            
def onQuit(systray):
    webServer.server_close()

def main():
    menu_options = (('Pause', None, pause), ('Resume', None, resume))
    with SysTrayIcon("screensaver.ico", "Screensaver Companion", menu_options, on_quit=onQuit) as systray:
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
