#!/usr/bin/python3

from application.imap_gmail_script import *

def test():
    file = open('GPSFILE.TXT')
    for line in file:
        attachment = line.split(',')
        if len(attachment) > 15:
            print(attachment_handler(attachment))
        

if __name__ == '__main__':
    test()