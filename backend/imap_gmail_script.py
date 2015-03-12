#!/usr/bin/env python3
import getpass
import imaplib
import email
import os
import datetime
import socket

def attachment_handler(attachment):
    fields = ['Temp', 'Pres', 'Lat', 'Long', 'Alt']
    diag_dict = {}
    for entry, data in zip(fields, attachment):
        diag_dict[entry] = data.strip()
    print(diag_dict)

def main():
    ########### Open IMAP connection to Gmail ##############
    M = imaplib.IMAP4_SSL("imap.gmail.com")
    M.login("uivast1@gmail.com", getpass.getpass()) #replace pw w/ getpass.getpass()
    M.select()
    ########### Create a query to search for new mail ###########
    form = "%d-%b-%Y"
    today = datetime.datetime.today()
    s = today.strftime(form)
    query = "(FROM \"sbdservice\" SINCE \"" + s + "\")"
    # typ, data = M.search(None, query)  
    
    typ, data = M.search(None, '(FROM "sbdservice" SINCE "12-October-2014")')  
    if typ != 'OK':                                 #typ is for error checking
       print("Error searching mail.")               #data is a tuple of msg num
       
    if not data[0]:
        print("No new mail")
        
    for msgId in data[0].split():
        typ, messageParts = M.fetch(msgId, '(RFC822)')
        if typ != 'OK':
            print("Error fetching mail.")
    
        emailBody = messageParts[0][1]
        mail = email.message_from_bytes(emailBody)
        for part in mail.walk():
            if part.is_multipart():
                continue
            if part.get('Content-Disposition') is None:
                continue
            if part.get('Content-Disposition') == "inline":
                continue
            attachment = part.get_payload(decode=True).decode("utf-8", "ignore")
            attachment_handler(attachment.split(','))
    M.close()
    M.logout()
    
if __name__ == '__main__':
    main()