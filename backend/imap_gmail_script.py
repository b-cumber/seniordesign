#!/usr/bin/env python
import getpass, imaplib

M = imaplib.IMAP4_SSL("imap.gmail.com")
M.login("uivast1@gmail.com", getpass.getpass())
M.select()
print M.list()
typ, data = M.search(None, 'FROM', '"sbdservice"')  #typ is for error checking
                                                    #data is a tuple of msg num
for num in data[0].split():
    typ, data = M.fetch(num, 'BODYSTRUCTURE')
    print data
M.close()
M.logout()