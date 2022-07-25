import os
from http.server import BaseHTTPRequestHandler, HTTPServer


SERVER_HOST, HTTP_SERVER_PORT = "127.0.0.1", 8080


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Web Server</title></head>", "utf-8"))
        self.wfile.write(bytes(f"<p>Looking at directory: {self.path}</p>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        for path in os.listdir(self.path):
            path_link = os.path.join(self.path, path)
            self.wfile.write(
                bytes(
                    f"<p><a href='http://{SERVER_HOST}:{HTTP_SERVER_PORT}{path_link}'>{path}</a></p>",
                    "utf-8",
                )
            )
        self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    web_server = HTTPServer((SERVER_HOST, HTTP_SERVER_PORT), Server)
    print(f"Server started http://{SERVER_HOST}:{HTTP_SERVER_PORT}")

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
    print("Server stopped.")
