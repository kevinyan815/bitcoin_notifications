import requests
import time
from datetime import datetime

BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/Jhk8Bgkd9yj-WJk0Oqlga'
BITCOIN_PRICE_THRESHOLD = 8000

def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    # Convert the price to a floating point number
    return float(response_json[0]['price_usd'])

def post_ifttt_webhook(event, value):
    # The payload that will be sent to IFTTT service
    data = {'value1': value}
    # insert out desired event
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # Send a HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        # <b> (bold) tag creates bolded text
        # 24.02.2018 15:09: $<b>10123.4</b>
        row = '{}: $<b>{}<b>'.format(date, price)
        rows.append(row)
    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return '<br>'.join(rows)


def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emergency notification
        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)
        # Send a Telegram notification
        # Once we have 5 items in our bitcoin_history send an update
        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            # Reset the history
            bitcoin_history = []
        # Sleep for 5 minutes
        # (For testing purposes you can set it to a lower number)
        time.sleep(5 * 60)

if __name__ == '__main__':
    main()