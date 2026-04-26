Project: Multi-threaded Web Server
Name: KIM JUNHYEONG
Student ID: 24134503D

------------------------------------
1. Description
------------------------------------
This project implements a multi-threaded Web server using Python socket programming.

The server supports:
- GET and HEAD methods (HEAD returns only header information)
- Text and image files
- HTTP status codes: 200, 400, 403, 404, 304
- Last-Modified and If-Modified-Since
- Persistent and non-persistent connections (keep-alive / close)
- Logging of client requests

------------------------------------
2. How to Run
------------------------------------
1. Open terminal
2. Navigate to project folder

   cd web_server_project

3. Run the server

   python server.py

4. Open browser and access:

   http://127.0.0.1:8080/

------------------------------------
3. File Structure
------------------------------------
server.py        : main server program
www/             : web files directory (contains index.html and image.jpg)
server_log.txt   : log file
README.txt       : instructions

------------------------------------
4. Notes
------------------------------------
- Default port: 8080
- Server runs on localhost (127.0.0.1)
- Supports HTTP persistent connection (keep-alive) and non-persistent (close)
