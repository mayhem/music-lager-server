#!/usr/bin/env python

import sys
import os
import json
import socket

MUSIC_LAGER_SERVER = "localhost"
MUSIC_LAGER_PORT   = 4420

def import_from_file(filename):

    try:
        if filename == '-':
            f = sys.stdin
        else:
            f = open(filename, "r")
    except IOError:
        print "Cannot open file %s" % filename
        return False


    while True:
        line = f.readline()
        if not line: 
            break

        columns = line.split("\t")
        data = {}
        data['user'] = 'mayhemchaos'
        data['timestamp'] = int(columns[0])
        data['track'] = columns[1]
        data['artist'] = columns[2]
        data['album'] = columns[3]
        data['trackMbid'] = columns[4]
        data['artistMbid'] = columns[5]
        data['albumMbid'] = columns[6]
        json_data = json.dumps(data)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((MUSIC_LAGER_SERVER, MUSIC_LAGER_PORT))
        except socket.error, e:
            print "Cannot connect to music lager server: ", e
            return False

        s.send(json_data + "\n")
        s.close()

    f.close();

import_from_file(sys.argv[1])
