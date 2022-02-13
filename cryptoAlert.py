import requests
import pandas as pd
import json

#mailing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



#These are the coins/ I have currently invested in - you can make these whatever you would like
crypto = ['BTC','ETH','SOL','ADA','SAND']
current_price = list()


for coin in crypto:
    url = 'https://rest.coinapi.io/v1/exchangerate/{0}/GBP'.format(coin) #USD/GBP
    headers = {'X-CoinAPI-Key' : 'YOUR-KEY-HERE'}
    response = requests.get(url, headers = headers)
    
    #the response outputs JSON, so we translate this JSON dictionary and store the current rate of the coin as the current price
    content = response.json()
    current_price.append(content['rate'])


previous_price = list()
for coin in crypto:

    #make limit however many days you would like to see, we want to see 8 as we want the week before, 8 because the output includes today.
    url_2 = 'https://rest.coinapi.io/v1/ohlcv/{0}/GBP/latest?period_id=1DAY&limit=8'.format(coin) 
    response_2 = requests.get(url_2, headers=headers)
    content_2 = response_2.json()

    #We will take the days closing price as the price for that day, we take the 7th entry as we want the 7th day (starts from 0)
    previous_price.append(content_2[7]['price_close'])


#calculating the change between the current price and last week
change_percent = list()
for i in range(len(current_price)):
    change = ((float(current_price[i])-previous_price[i])/previous_price[i])*100
    change_percent.append(round(change,2))

#lets update the message that will be sent to your email
msg = ""
for i in range(len(crypto)):
    if change_percent[i] > 0:
        msg = msg + "{0} is up {1}{2} from last week".format(crypto[i],change_percent[i],"%") + "\n"
    elif change_percent[i] < 0:
        msg = msg + "{0} is down {1}{2} from last week".format(crypto[i],change_percent[i],"%") + "\n"
    else:
        msg = msg + "{0} is the same as last week".format(crypto[i]) + "\n"


def send_mail(message):

    mail_content = message

    #The mail addresses and password
    sender_address = 'YOU-EMAIL-HERE'
    sender_pass = 'YOUR-PASSWORD-HERE'    #if you have two factor authentication on then you need to generate an app-specfifc password
    receiver_address = 'YOU-EMAIL-HERE'

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Crypto Alert From Python'   #The subject line


    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')



#If anything has decresased more than 5% then email me
send = False
for i in change_percent:
    if i < -5:
        send = True

if send == True:
    send_mail(msg)
