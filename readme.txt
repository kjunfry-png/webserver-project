Project: Multi-threaded Web Server
Name: 김준형
Student ID: XXXXXXXX

------------------------------------
1. Description
------------------------------------
This project implements a multi-threaded Web server using Python socket programming.

The server supports:
- GET and HEAD methods
- Text and image files
- HTTP status codes: 200, 400, 403, 404, 304
- Last-Modified and If-Modified-Since
- Logging of client requests

------------------------------------
2. How to Run
------------------------------------
1. Open terminal
2. Navigate to project folder

   cd webserver_project

3. Run the server

   python server.py

4. Open browser and access:

   http://127.0.0.1:8080/

------------------------------------
3. File Structure
------------------------------------
server.py        : main server program
www/             : web files directory
server_log.txt   : log file
README.txt       : instructions

------------------------------------
4. Notes
------------------------------------
- Default port: 8080
- Server runs on localhost (127.0.0.1)