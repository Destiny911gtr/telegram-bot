import os, pytz, requests, telepot, time, timeago, datetime, json
from telepot.loop import MessageLoop

now = datetime.datetime.now()
url = "https://api.covid19india.org/data.json"
url2 = "https://api.covid19india.org/state_district_wise.json"
data = ""
k = ""

def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print ('Received: %s' % command)

    if command == '/hi':
        telegram_bot.sendMessage (chat_id, str("Yo, wassup?"))
    elif command == '/time':
        telegram_bot.sendMessage(chat_id, str(now.hour)+str(":")+str(now.minute))
    elif command == '/covid':
        data = ""
        data = getCovid()
        telegram_bot.sendMessage(chat_id, str(data))
        time.sleep(5)
    elif command == '/district':
        data = ""
        data = getDistricts()
        telegram_bot.sendMessage(chat_id, str(data))
        time.sleep(5)

def getCovid():
    curr_time = datetime.datetime.now(pytz.timezone('Asia/Calcutta'))
    curr_time_split = str(curr_time).split('.', 1)[0]
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    state = data["statewise"]
    for j in state:
       if j["state"] == "Kerala":
          k = j
          break
    reft = str(k['lastupdatedtime'])
    date = reft.split(" ", 1)[0]
    day = date.split("/", 2)[0]
    month = date.split("/", 2)[1]
    year = date.split("/", 2)[2]
    lref = year + "-" + month + "-" + day + " " + reft.split(" ", 1)[1]
    refresht = timeago.format(lref, curr_time_split)
    status = str("State: {} \nActive: {} \nRecovered: {} \nDeaths: {} \nTotal: {} \nRefreshed: {}".format(k['state'], k['active'], k['recovered'], k['deaths'], k['confirmed'], refresht))
    return status

def getDistricts():
    json_url = requests.get(url2)
    data = json.loads(json_url.text)
    district = data["Kerala"]["districtData"]
    distData = str("District-wise Reports\n\n")
    for key,value in district.items():
        distData = distData + str("{} : {}\n".format(key,value["confirmed"]))
    return distData

telegram_bot = telepot.Bot(os.getenv("TOKEN"))
print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print ('Up and Running....')

while 1:
    time.sleep(10)
