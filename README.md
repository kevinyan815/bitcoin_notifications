#bitcoin_notificatins

### 安装和运行

- virtualenv -p python3 venv
- source vent/bin/activate
- python bitcoin_notifications.py &

### 关于Telegram的设置

Telegram的服务需要科学上网才能访问，在IFTTT上使用Telegram Applets时必须先将IFTTT bot添加到你的Telegram账户里，并将创建的IFTTT频道授权给IFTTT bot来管理， 我在网页上没有走通这一步，后来的解决方法是分别在手机上安装了IFTTT和Telegram App，在IFTTT的手机应用里添加`bitcoin_price_update`这事件，需要Telegram授权时会唤起Telegram应用，其实不难只要一直下一步就可以。

### 应用编写步骤

> 这个项目参照了Segmentfault上的文章 https://segmentfault.com/a/1190000014174291 以下是文章内容里的具体步骤

有很多朋友问我学习了Python后，有没有什么好的项目可以练手。

其实，做项目主要还是根据需求来的。但是对于一个初学者来说，很多复杂的项目没办法独立完成，因此博主挑选了一个非常适合初学者的项目，内容不是很复杂，但是非常有趣，我相信对于初学者小白来说是再好不过的项目了。

这个项目中，我们将要建立一个比特币价格的提醒服务。

- 你将主要会学习到`HTTP`的请求，以及如何使用`requests`包来发送这些请求。
- 同时，你会了解`webhooks`和如何使用它将Python app与外部设备连接，例如移动端手机提醒或者 Telegram 服务。

仅仅不到50行的代码就能完成一个比特币价格提醒服务的功能，并且可以轻松的扩展到其它加密数字货币和服务中。

下面我们马上来看看。

## 用Python实现比特币价格提醒

我们都知道，比特币是一个变动的东西。你无法真正的知道它的去向。因此，为了避免我们反复的刷新查看最新动态，我们可以做一个Python app来为你工作。

为此，我们将会使用一个很流行的自动化网站`IFTTT`。IFTTT**("if this, then that")**是一个可以在不同app设备与web服务之间建立连接桥梁的工具。

我们将会创建两个IFTTT applets：

- 一个是当比特币价格下滑到一定阈值后的紧急提醒
- 另一个是常规的比特币价格的更新

两个程序都将被我们的Python app触发，Python app从`Coinmakercap API` (<https://coinmarketcap.com/api/)> 获取数据。

一个IFTTT程序有两个部分组成：**触发部分**和**动作部分**。

在我们的情况下，触发是一个IFTTT提供的webhook服务。你可以将webhook想象为"**user-defined HTTP callbacks**"，更多请参考：[http://timothyfitz.com/2009/0...](http://timothyfitz.com/2009/02/09/what-webhooks-are-and-why-you-should-care/)

我们的Python app将会发出一个HTTP请求到webhook URL，然后webhook URL触发动作。有意思的部分来了，这个动作可以是你想要的任何东西。IFTTT提供了众多的动作像发送一个email，更新一个Google电子数据表，甚至可以给你打电话。

## 配置项目

如果你安装了python3，那么只要再安装一个`requests`包就可以了。

```
$ pip install requests==2.18.4 # We only need the requests package
```

选一个编辑器，比如Pycharm进行代码编辑。

## 获取比特币价格

代码很简单，可以在console中进行。导入`requests`包，然后定义`bitcoin_api_url`变量，这个变量是Coinmarketcap API的URL。

接着，使用`requests.get()`函数发送一个 HTTP GET请求，然后保存响应response。由于API返回一个JSON响应，我们可以通过`.json()`将它转换为python对象。

```
>>> import requests
>>> bitcoin_api_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
>>> response = requests.get(bitcoin_api_url)
>>> response_json = response.json()
>>> type(response_json) # The API returns a list
<class 'list'>
>>> # Bitcoin data is the first element of the list
>>> response_json[0]
{'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'BTC', 'rank': '1', 
 'price_usd': '10226.7', 'price_btc': '1.0', '24h_volume_usd': '7585280000.0',
 'market_cap_usd': '172661078165', 'available_supply': '16883362.0', 
 'total_supply': '16883362.0', 'max_supply': '21000000.0', 
 'percent_change_1h': '0.67', 'percent_change_24h': '0.78', 
 'percent_change_7d': '-4.79', 'last_updated': '1519465767'}
```

上面我们感兴趣的是`price_usd`。

## 发送一个测试的IFTTT提醒

现在我们可以转到IFTTT上面来了。使用IFTTT之前，我们需要创建一个新账户(<https://ifttt.com/join)>，然后安装移动端app（如果你想在手机上接到通知）
设置成功后就开始创建一个新的IFTTT applet用于测试。

创建一个新的测试applet，可以按一下步骤进行：

1. 点击大的 "this" 按钮；
2. 搜索 "webhooks" 服务，然后选择 "Receive a web request"触发;
3. 重命名event为`test_event`;
4. 然后选择大的 "that" 按钮；
5. 搜索 "notifications" 服务，然后选择 "send a notification from the IFTTT app"
6. 改变短信息为 `I just triggered my first IFTTT action!`，然后点击 "Create action";
7. 点击 "Finish" 按钮，完成；

要看如何使用IFTTT webhooks，请点击 "Documentation" 按钮documentation页有webhooks的URL。

```
https://maker.ifttt.com/trigger/{event}/with/key/{your-IFTTT-key}
```

接着，你需要将`{event}`替换为你在步骤3中自己起的名字。`{your-IFTTT-key}`是已经有了的IFTTT key。

现在你可以复制webhook URL，然后开启另一个console。同样导入`requests`然后发送post请求。

```
>>> import requests
>>> # Make sure that your key is in the URL
>>> ifttt_webhook_url = 'https://maker.ifttt.com/trigger/test_event/with/key/{your-IFTTT-key}'
>>> requests.post(ifttt_webhook_url)
<Response [200]>
```

运行完之后，你可以看到：

![clipboard.png](https://segmentfault.com/img/bV7DuP?w=1080&h=246)

## 创建IFTTT Applets

前面只是测试，现在我们到了最主要的部分了。再开始代码之前，我们需要创建两个新的IFTTT applets：一个是比特币价格的紧急通知，另一个是常规的更新。

**比特币价格紧急通知的applet：**

1. 选择 "webhooks" 服务，并且选择 "Receive a web request" 的触发;
2. 命名一个事件 event 为 `bitcoin_price_emergency`;
3. 对于响应的动作部分，选择 "Notifications"服务，然后继续选择 "send a rich notification from the IFTTT app" 动作；
4. 提供一个标题，像 "Bitcoin price emergency!"
5. 设置短信息 为 `Bitcoin price is at ${{Value1}}. Buy or sell now!`(我们一会儿将返回到`{{Value1}}`部分)
6. 可选的，你可以加入一个URL link 到 Coinmarketcap Bitcoin page：`https://coinmarketcap.com/currencies/bitcoin/`;
7. 创建动作，然后完成applet的设置；

**常规价格更新的applet：**

1. 一样的选择 "webhooks" 服务，并且选择 "Receive a web request" 的触发;
2. 命名一个事件 event 为 `bitcoin_price_update`;
3. 对于响应的动作部分，选择 "Telegram" 服务，然后继续选择 "Send message" 动作；
4. 设置短信信息文本为：`Latest bitcoin prices:<br>{{Value1}}`；
5. 创建动作，然后完成applet的设置；

## 将所有连到一起

现在，我们有了IFTTT，下面就是代码了。你将通过创建像下面一样标准的Python命令行app骨架来开始。 代码码上去，然后保存为 `bitcoin_notifications.py`:

```
import requests
import time
from datetime import datetime

def main():
    pass

if __name__ == '__main__':
    main()
```

接着，我们还要将前面两个Python console部分的代码转换为两个函数，函数将返回最近比特币的价格，然后将它们分别post到IFTTT的webhook上去。将下面的代码加入到main()函数之上。

```
BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{your-IFTTT-key}'

def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    # Convert the price to a floating point number
    return float(response_json[0]['price_usd'])


def post_ifttt_webhook(event, value):
    # The payload that will be sent to IFTTT service
    data = {'value1': value}
    # inserts our desired event
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # Sends a HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)
```

除了将价格从一个字符串变成浮点数之外，`get_latest_bitcoin_price`基本没太变。`psot_ifttt_webhook`需要两个参数：`event`和`value`。

`event`参数与我们之前命名的触发名字对应。同时，IFTTT的webhooks允许我们通过requests发送额外的数据，数据作为JSON格式。

这就是为什么我们需要`value`参数：当设置我们的applet的时候，我们在信息文本中有`{{Value1}}`标签。这个标签会被 JSON payload 中的`values1`文本替换。`requests.post()`函数允许我们通过设置`json`关键字发送额外的JSON数据。

现在我们可以继续到我们app的核心main函数码代码了。它包括一个`while True`的循环，由于我们想要app永远的运行下去。在循环中，我们调用Coinmarkertcap API来得到最近比特币的价格，并且记录当时的日期和时间。

根据目前的价格，我们将决定我们是否想要发送一个紧急通知。对于我们的常规更新我们将把目前的价格和日期放入到一个`bitcoin_history`的列表里。一旦列表达到一定的数量(比如说5个)，我们将包装一下，将更新发送出去，然后重置历史，以为后续的更新。

一个需要注意的地方是避免发送信息太频繁，有两个原因：

- Coinmarketcap API 声明他们只有每隔5分钟更新一次，因此更新太频也没有用
- 如果你的app发送太多的请求道 Coinmarketcap API，你的IP可能会被ban

因此，我们最后加入了 "go to sleep" 睡眠，设置至少5分钟才能得到新数据。下面的代码实现了我们的需要的特征：

```
BITCOIN_PRICE_THRESHOLD = 10000  # Set this to whatever you like

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
            post_ifttt_webhook('bitcoin_price_update', 
                               format_bitcoin_history(bitcoin_history))
            # Reset the history
            bitcoin_history = []

        # Sleep for 5 minutes 
        # (For testing purposes you can set it to a lower number)
        time.sleep(5 * 60)
```

我们几乎快成功了。但是还缺一个`format_bitcoin_history`函数。它将`bitcoin_history`作为参数，然后使用被Telegram允许的基本HTML标签（像`<br>`, `<b>`, `<i>` 等等）变换格式。将这个函数复制到main()之上。

```
def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        # <b> (bold) tag creates bolded text
        # 24.02.2018 15:09: $<b>10123.4</b>
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return '<br>'.join(rows)
```

最后在手机上显示的结果是这样的：

![clipboard.png](https://segmentfault.com/img/bV7Dvi?w=256&h=134)

然后，我们的功能就完成了，只要比特币的价格一更新，手机移动端就有提示。当然，如果你嫌烦也可以在app里面off掉。

> 参考：[https://realpython.com/python...](https://realpython.com/python-bitcoin-ifttt/)

 