# CryptoAlertBot
Here I use the coinAPI to collect the latest cryptocurrency data. I use this data and compare it the historical data from last week - also taken from coinAPI, and calculate the percentage difference. If any of the cryptocurrencys drop below 5% from last week - then the program emails me these details to inform me and help me react to the changing market. This percentage threshold could eaily be changed to suit your needs. I then use crontabs on mac to schedule the script to be executed every hour.
