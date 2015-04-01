#!/usr/bin/python3
import getpass
import imaplib
import email
import os
import datetime
import socket

def format_longitude(longitude, card):
    if longitude:
        deg = int(longitude[0:3])
        sec = float(longitude[3:])
        longitude =  deg+sec/60
        if card is 'W':
            return float(longitude)*-1
        else:
            return float(longitude)
        

def format_latitude(latitude, card):
    if latitude:
        deg = int(latitude[0:2])
        sec = float(latitude[2:])
        latitude = deg+sec/60
        if card is 'S':
            return float(latitude)*-1
        else:
            return float(latitude)
        
    
def attachment_handler(attachment):
    # fields = ['Temp', 'Pres', 'Lat', 'Long', 'Alt']
    diag_dict = {}
    for num, entry in enumerate(attachment):
        if entry != '$GPGGA':# This approach works as long as we use this format
            continue
        else:
            diag_dict['Time'] = attachment[num+1]
            diag_dict['Latitude'] = format_latitude(attachment[num+2],
                                                    attachment[num+3])
            diag_dict['Longitude'] = format_longitude(attachment[num+4], 
                                                      attachment[num+5])
            diag_dict['NumSats'] = attachment[num+7]
            diag_dict['Altitude'] = attachment[num+9]
        
    # for entry, data in zip(fields, attachment):
    #     diag_dict[entry] = data.strip()
    # print(type(diag_dict))
    return diag_dict

def main():
    ########### Open IMAP connection to Gmail ##############
    M = imaplib.IMAP4_SSL("imap.gmail.com")
    M.login("uivast1@gmail.com", "vastiscool") #replace pw w/ getpass.getpass()
    M.select()
    ########### Create a query to search for new mail ###########
    form = "%d-%b-%Y"
    today = datetime.datetime.today()
    s = today.strftime(form)
    query = "(FROM \"sbdservice\" SINCE \"" + s + "\")"
    # typ, data = M.search(None, query)  
    
    typ, data = M.search(None, '(FROM "sbdservice" SINCE "25-March-2015")')  
    # typ, data = M.search(None, '(NOT SEEN)') # == to new messages
    
    if typ != 'OK':                                 #typ is for error checking
       print("Error searching mail.")               #data is a tuple of msg num
       
    if not data[0]:
        print("No new mail")
        
    # diagnostics = []
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
            # print(msgId)
            # diagnostics.append(attachment_handler(attachment.split(',')))
            diagnostics = attachment_handler(attachment.split(','))
    M.close()
    M.logout()
    # print(diagnostics)

    return diagnostics
    
if __name__ == '__main__':
    main()