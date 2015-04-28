#!/usr/bin/python3
import getpass
import imaplib
import email
import os
import datetime
import socket
from application.gen_gauge import gauge_maker


def format_time(time):
    if time:
        hours = str((int(time[0:2])-7)%24)
        if len(hours) < 2:
            hours = '0'+hours
        mins = time[2:4]
        if len(mins) < 2:
            hours = '0'+hours
        secs = time[4:6]
        if len(secs) < 2:
            hours = '0'+hours
        time = hours + ':' + mins + ':' + secs
    return time
        
def format_longitude(longitude, card):
    if longitude:
        deg = int(longitude[0:3])
        sec = float(longitude[3:])
        longitude =  deg+sec/60
        if card is 'W':
            longitude = longitude * -1
            return str(longitude)[:10]
        else:
            return str(longitude)[:9]
        

def format_latitude(latitude, card):
    if latitude:
        deg = int(latitude[0:2])
        sec = float(latitude[2:])
        latitude = deg+sec/60
        if card is 'S':
            latitude = latitude*-1
            return str(latitude)[:9]
        else:
            return str(latitude)[:8]
        
    
def attachment_handler(attachment):
    diag_dict = {}
    for num, entry in enumerate(attachment):
        if entry != '$GPGGA':# This approach works as long as we use this format
            continue
        else:
            diag_dict['Time'] = format_time(attachment[num+1])
            diag_dict['Latitude'] = format_latitude(attachment[num+2],
                                                    attachment[num+3])
            diag_dict['Longitude'] = format_longitude(attachment[num+4], 
                                                      attachment[num+5])
            diag_dict['Satellites'] = attachment[num+7]
            diag_dict['Altitude'] = attachment[num+9]
            if len(attachment) > 15:
                diag_dict['Velocity'] = attachment[num+15].strip('\n')
            # else:
               #  diag_dict['Velocity'] = 0
    return diag_dict

def search_mail(mail_handle):
    ########### Create a query to search for new mail ###########
    form = "%d-%b-%Y"
    today = datetime.datetime.today()
    s = today.strftime(form)
    query = "(FROM \"sbdservice\" SINCE \"" + s + "\")"
    #print(query)
    # typ, data = mail_handle.search(None, query)  
    
    typ, data = mail_handle.search(None, '(FROM "sbdservice" SINCE "4-April-2015")')  
    # typ, data = M.search(None, '(NOT SEEN)') # == to new messages
    
    if typ != 'OK':                                 #typ is for error checking
       print("Error searching mail.")               #data is a tuple of msg num
    
    return data

def fetch_mail(mail_handle, msgId):
    typ, messageParts = mail_handle.fetch(msgId, '(RFC822)')
    if typ != 'OK':
        print("Error fetching mail.")
    emailBody = messageParts[0][1]
    mail = email.message_from_bytes(emailBody)
    diagnostics = []
    for part in mail.walk():
        if part.is_multipart():
            continue
        if part.get('Content-Disposition') is None:
            continue
        if part.get('Content-Disposition') == "inline":
            continue
        attachment = part.get_payload(decode=True).decode("utf-8", "ignore")
        diagnostics = attachment_handler(attachment.split(','))
    return diagnostics

    
def main(msg=0):
    ########### Open IMAP connection to Gmail ##############
    M = imaplib.IMAP4_SSL("imap.gmail.com")
    M.login("uivast1@gmail.com", "vastiscool") 
    M.select()
    data = search_mail(M)
    print(len(data[0]))
    if len(data[0]) < msg:
        msgID = data[0].split()[-1]
    else:
        msgID = data[0].split()[msg]
    diag = fetch_mail(M, msgID)
    M.close()
    M.logout()
    return diag
    
if __name__ == '__main__':
    main()