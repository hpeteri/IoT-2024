import socket

def server_run():

    s_address = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(s_address)
    s.listen(1)

    print("[SERVER] Listening on: ", s_address)

    html_response =  """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head><title>Raspberry Pi Pico Web Server</title></head>
<body>
<h1>HELLO, IOT 2024!</h1>
<h2>Finally work!</h2>
</body>
</html>
"""

    while True:
        connection, address = s.accept()
        print("[SERVER] Client connected from", address);

        request = connection.recv(1024)
        print("[SERVER] Request:", request)

        connection.send(html_response.encode('utf-8'))
        connection.close()
