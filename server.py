import socket
import threading
import os
from datetime import datetime
from email.utils import formatdate, parsedate_to_datetime
import mimetypes

HOST = "127.0.0.1"
PORT = 8080
WEB_ROOT = "www"
LOG_FILE = "server_log.txt"


def write_log(client_ip, path, status):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{client_ip} | {now} | {path} | {status}\n")


def get_content_type(file_path):
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or "application/octet-stream"


def send_response(conn, status, body=b"", content_type="text/html",
                  last_modified=None, method="GET", connection_type="close"):

    header = f"HTTP/1.1 {status}\r\n"
    header += f"Date: {formatdate(usegmt=True)}\r\n"
    header += "Server: SimplePythonServer\r\n"
    header += f"Content-Length: {len(body)}\r\n"
    header += f"Content-Type: {content_type}\r\n"

    if last_modified:
        header += f"Last-Modified: {last_modified}\r\n"

    header += f"Connection: {connection_type}\r\n"
    header += "\r\n"

    conn.sendall(header.encode())

    if method == "GET" and status != "304 Not Modified":
        conn.sendall(body)


def handle_one_request(conn, client_ip, request):
    print("Request received:")
    print(request)

    lines = request.splitlines()

    if len(lines) == 0:
        return False

    request_line = lines[0].split()

    headers = {}
    for line in lines[1:]:
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()

    connection_type = headers.get("connection", "close").lower()

    if connection_type == "keep-alive":
        response_connection = "keep-alive"
        keep_alive = True
    else:
        response_connection = "close"
        keep_alive = False

    if len(request_line) != 3:
        status = "400 Bad Request"
        body = b"<h1>400 Bad Request</h1>"
        send_response(conn, status, body, method="GET", connection_type=response_connection)
        write_log(client_ip, "-", status)
        return keep_alive

    method, path, version = request_line

    if method not in ["GET", "HEAD"]:
        status = "400 Bad Request"
        body = b"<h1>400 Bad Request</h1>"
        send_response(conn, status, body, method="GET", connection_type=response_connection)
        write_log(client_ip, path, status)
        return keep_alive

    if path == "/":
        path = "/index.html"

    file_path = os.path.normpath(os.path.join(WEB_ROOT, path.lstrip("/")))

    if not file_path.startswith(WEB_ROOT):
        status = "403 Forbidden"
        body = b"<h1>403 Forbidden</h1>"
        send_response(conn, status, body, method=method, connection_type=response_connection)
        write_log(client_ip, path, status)
        return keep_alive

    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        status = "404 File Not Found"
        body = b"<h1>404 File Not Found</h1>"
        send_response(conn, status, body, method=method, connection_type=response_connection)
        write_log(client_ip, path, status)
        return keep_alive

    modified_time = os.path.getmtime(file_path)
    last_modified = formatdate(modified_time, usegmt=True)

    if "if-modified-since" in headers:
        try:
            client_time = parsedate_to_datetime(headers["if-modified-since"]).timestamp()

            if int(modified_time) <= int(client_time):
                status = "304 Not Modified"
                send_response(
                    conn,
                    status,
                    b"",
                    last_modified=last_modified,
                    method=method,
                    connection_type=response_connection
                )
                write_log(client_ip, path, status)
                return keep_alive
        except Exception:
            pass

    with open(file_path, "rb") as f:
        body = f.read()

    status = "200 OK"
    content_type = get_content_type(file_path)

    send_response(
        conn,
        status,
        body,
        content_type=content_type,
        last_modified=last_modified,
        method=method,
        connection_type=response_connection
    )

    write_log(client_ip, path, status)
    return keep_alive


def handle_client(conn, addr):
    client_ip = addr[0]

    try:
        conn.settimeout(10)

        while True:
            request = conn.recv(4096).decode(errors="ignore")

            if not request:
                break

            keep_alive = handle_one_request(conn, client_ip, request)

            if not keep_alive:
                break

    except socket.timeout:
        pass
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server running at http://{HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()