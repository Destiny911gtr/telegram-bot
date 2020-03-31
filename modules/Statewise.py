import pytz, requests, time, timeago, datetime, json

url = "https://api.covid19india.org/data.json"
now = datetime.datetime.now()

def getCovid(state="Kerala"):
    curr_time = datetime.datetime.now(pytz.timezone('Asia/Calcutta'))
    curr_time_split = str(curr_time).split('.', 1)[0]
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    states = data["statewise"]
    for j in states:
        if j["state"] == state:
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
