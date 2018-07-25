import requests
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/test_event/with/key/Jhk8Bgkd9yj-WJk0Oqlga'
response = requests.post(ifttt_webhook_url)
print (response.status_code)