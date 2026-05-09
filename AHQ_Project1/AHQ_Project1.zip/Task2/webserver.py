import socket
import os
import urllib.parse

HOST = '127.0.0.1'
PORT = 9927

def get_content_type(file_path):
    if file_path.endswith(".html"):
        return "text/html"
    elif file_path.endswith(".css"):
        return "text/css"
    elif file_path.endswith(".png"):
        return "image/png"
    elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
        return "image/jpeg"
    elif file_path.endswith(".mp4"):
        return "video/mp4"
    else:
        return "application/octet-stream"

def serve_file(filename, client_socket, client_address):
    try:
        with open(filename, 'rb') as file:
            content = file.read()
        content_type = get_content_type(filename)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n"
        client_socket.sendall(response.encode() + content)
        # Log successful response
        client_ip, client_port = client_address
        print(f"\nResponse: 200 OK")
        print(f"Client: {client_ip}:{client_port}")
        print(f"Server Port: {PORT}")
        print(f"File: {filename}")
    except FileNotFoundError:
        send_404(client_socket, client_address, filename)

def handle_file_request(filename, client_socket, client_address):
    extension = filename.split('.')[-1].lower()
    file_path = f"./{filename}"

    if os.path.isfile(file_path):
        serve_file(file_path, client_socket, client_address)
    else:
        if extension in ["jpg", "jpeg", "png"]:
            redirect_url = f"https://www.google.com/search?tbm=isch&q={urllib.parse.quote(filename)}"
            search_type = "Image Search"
        elif extension in ["mp4", "avi", "mov"]:
            redirect_url = f"https://www.google.com/search?tbm=vid&q={urllib.parse.quote(filename)}"
            search_type = "Video Search"
        else:
            redirect_url = f"https://www.google.com/search?q={urllib.parse.quote(filename)}"
            search_type = "Web Search"

        response = (
            "HTTP/1.1 307 Temporary Redirect\r\n"
            f"Location: {redirect_url}\r\n"
            "Content-Type: text/html\r\n\r\n"
        )
        client_socket.sendall(response.encode())
        
        # Log redirect response
        client_ip, client_port = client_address
        print(f"\nResponse: 307 Temporary Redirect")
        print(f"Client: {client_ip}:{client_port}")
        print(f"Server Port: {PORT}")
        print(f"Requested File: {filename}")
        print(f"Redirect Type: {search_type}")
        print(f"Redirect URL: {redirect_url}")

def send_404(client_socket, client_address, requested_path="Unknown"):
    client_ip, client_port = client_address
    html = (
        "<html><head><title>Error 404</title></head>"
        "<body>"
        "<h1 style='color:red;'>The file is not found</h1>"
        f"<p>Client IP: {client_ip}</p>"
        f"<p>Client Port: {client_port}</p>"
        "</body></html>"
    )
    response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n" + html
    client_socket.sendall(response.encode())
    
    # Log 404 response
    print(f"\nResponse: 404 Not Found")
    print(f"Client: {client_ip}:{client_port}")
    print(f"Server Port: {PORT}")
    print(f"Requested Path: {requested_path}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server running on http://{HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                request = client_socket.recv(1024).decode()
                if not request:
                    continue

                print("----- New Request -----")
                print(request)

                request_line = request.splitlines()[0]
                method, path, _ = request_line.split()

                # Default routing for English version
                if path in ["/", "/index.html", "/en", "/main_en.html"]:
                    path = "/main_en.html"
                # Default routing for Arabic version
                elif path in ["/ar", "/main_ar.html"]:
                    path = "/main_ar.html"

                # Handle media file requests
                if path.startswith("/handle_request"):
                    parsed_url = urllib.parse.urlparse(path)
                    params = urllib.parse.parse_qs(parsed_url.query)
                    filename = params.get('filename', [''])[0]
                    handle_file_request(filename, client_socket, client_address)
                    continue

                # Serve requested file or show 404 error
                filepath = path.lstrip("/")
                if os.path.isfile(filepath):
                    serve_file(filepath, client_socket, client_address)
                else:
                    send_404(client_socket, client_address, filepath)

if __name__ == "__main__":
    start_server()
