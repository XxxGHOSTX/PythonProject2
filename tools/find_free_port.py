import socket
import sys

for p in range(8080, 8091):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("", p))
            print(p)
            sys.exit(0)
        except OSError:
            continue
# If none found, print 0
print(0)
