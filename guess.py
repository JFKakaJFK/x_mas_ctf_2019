#!/usr/bin/env python3
import matplotlib.pyplot as plt

import socket
import re

HOST = 'challs.xmas.htsp.ro'  # The server's hostname or IP address
PORT = 13005        # The port used by the server

fn = []
xs = []
ys = []

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    f = open("db.txt", "r")

    pairs = eval(f.read())
    f.close()
    a1, a2 = (None, None)
    was_in_db = False

    while(True):
        data = s.recv(1024)
        data = data.decode('utf-8')
        print(data)

        done = re.search(r'Great! You did it! Now what?', data,
                         re.IGNORECASE | re.MULTILINE)
        if done:
            print('DONE')
            break

        good = re.search(r'Good!', data,
                         re.IGNORECASE | re.MULTILINE)
        if good and not was_in_db:
            pairs[(a1, a2)] = 0
        bad = re.search(r'wrong!', data,
                        re.IGNORECASE | re.MULTILINE)
        if bad:
            if was_in_db:
                print('RIP ...')
                print((a1, a2, pairs[(a1, a2)]))
                break
            pairs[(a1, a2)] = 1

        equation = re.search(r'f\((\d+), (\d+)\)=', data,
                             re.IGNORECASE | re.MULTILINE)

        if equation:
            a1 = int(equation.group(1))
            a2 = int(equation.group(2))

            if (a1, a2) in pairs:
                print(pairs[(a1, a2)])
                s.send(f'{pairs[(a1, a2)]}\n'.encode('ascii'))
                fn.append(pairs[(a1, a2)])
                if(pairs[(a1, a2)] == 1):
                    xs.append(a1)
                    ys.append(a2)
                was_in_db = True
            else:
                s.send('0\n'.encode('ascii'))

        else:
            print('DID WE DO IT?')
            break

    print(fn)
    plt.plot(xs, ys, 'ro')
    plt.show()

    # cmd = ''
    # while cmd != 'q':
    #     data = s.recv(1024)
    #     data = data.decode('utf-8')
    #     print(data)

    #     cmd = input()

    #     s.send('{cmd}\n'.encode('ascii'))

    f = open("db.txt", "w+")
    f.write(str(pairs))
    f.write('\n')
    f.close()
