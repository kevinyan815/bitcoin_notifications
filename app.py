import requests
bitcoin_api_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
reponse = requests.get(bitcoin_api_url)
response_json = reponse.json()
print(response_json[0])