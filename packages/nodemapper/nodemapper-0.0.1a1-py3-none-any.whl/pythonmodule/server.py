import http.server
import threading

class server:
    
    def __init__(self, host, port):
        self.httpd = http.server.HTTPServer((host, int(port)), self.get_response_handler())
        self.thread = threading.Thread(target=self.serve)
        self.data = None

    def serve(self):
        while self.running:
            self.httpd.handle_request()

    def start(self):
        self.running = True
        self.thread.start()
    
    def stop(self):
        self.running = False
        self.httpd.server_close()
    
    def get_response_handler(outer_self):
        class response_handler(http.server.SimpleHTTPRequestHandler):
    
            def do_POST(self) -> None:
                length = int(self.headers.get('content-length'))
                data = self.rfile.read(length).decode('utf8')
                self.send_response(200)
                self.end_headers()
                outer_self.data = data
                outer_self.stop()

            def do_OPTIONS(self):
                self.send_response(200, "ok")
                # self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
                self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()

            def end_headers (self):
                self.send_header('Access-Control-Allow-Origin', '*')
                super().end_headers()
        
        return response_handler