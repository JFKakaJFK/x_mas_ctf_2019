#!/usr/bin/env python3
import socket
import re
import string

HOST = 'challs.xmas.htsp.ro'  # The server's hostname or IP address
PORT = 13000        # The port used by the server

LETTERS = string.ascii_uppercase + string.ascii_lowercase
# reverse order of string.ascii_letters since points are rewarded like this
print(LETTERS)


def guess(s, word):
    """guess a word, return wheter we are done and the score"""
    print(word)
    s.send(f'{word}\n'.encode('ascii'))
    data = s.recv(1024)
    data = data.decode('utf-8')
    print(data)

    done = not re.search(r'Tell me your guess:', data,
                         re.IGNORECASE | re.MULTILINE)

    score = re.search(r': (\d*)', data,
                      re.IGNORECASE | re.MULTILINE)
    if score:
        score = int(score.group(1))
    return (done or score == 0, score)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    w_index = 0
    l_index = 0  # len(LETTERS) // 2
    word = LETTERS[l_index]

    # first buffer
    data = s.recv(4096)
    data = data.decode('utf-8')
    print(data)

    done = not re.search(r'Tell me your guess:', data,
                         re.IGNORECASE | re.MULTILINE)

    low_ind = 0
    high_ind = len(LETTERS) - 1
    low_score = None
    high_score = None
    while(not done):
        if low_score is None and high_score is None:
            # get low and high
            word = word[:w_index] + LETTERS[low_ind] + word[(w_index + 1):]
            (done, low_score) = guess(s, word)
            if done:
                break
            word = word[:w_index] + LETTERS[high_ind] + word[(w_index + 1):]
            (done, high_score) = guess(s, word)
            if done:
                break
        # print(w_index)
        # print(f'{low_ind}({LETTERS[low_ind]}):{low_score}')
        # print(f'{high_ind}({LETTERS[high_ind]}):{high_score}')

        # next char of word
        if low_ind == high_ind:
            w_index += 1
            word = word + LETTERS[0]

            low_ind = 0
            low_score = None
            high_ind = len(LETTERS) - 1
            high_score = None
            continue
        elif low_ind + 1 == high_ind:
            if low_score < high_score:
                word = word[:w_index] + LETTERS[low_ind] + word[(w_index + 1):]
            else:
                word = word[:w_index] + \
                    LETTERS[high_ind] + word[(w_index + 1):]
            w_index += 1
            word = word + LETTERS[0]

            low_ind = 0
            low_score = None
            high_ind = len(LETTERS) - 1
            high_score = None
            continue

        mid = (low_ind + high_ind) // 2
        word = word[:w_index] + LETTERS[mid] + word[(w_index + 1):]

        (done, score) = guess(s, word)
        if done:
            break
        # print('guess')
        # print(f'{mid}({LETTERS[mid]}):{score}')

        # print(f'{low_score}|{score}|{high_score}')

        if low_score < high_score:  # first half
            # print('first')
            high_ind = mid
            high_score = score
        else:  # second half
            # print('second')
            low_ind = mid
            low_score = score

        # print()
    print('broke')
    print(word)

    cmd = ''
    while cmd != 'q':
        data = s.recv(1024)
        data = data.decode('utf-8')
        print(data)

        cmd = input()

        s.send(f'{cmd}\n'.encode('ascii'))
