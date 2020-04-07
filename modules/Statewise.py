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
    else:
        failed = "Wrong input. Eg - /covid Kerala \n\nVisit https://www.covid19india.org/ for more info."
        return failed
    reft = str(k['lastupdatedtime'])
    date = reft.split(" ", 1)[0]
    day = date.split("/", 2)[0]
    month = date.split("/", 2)[1]
    year = date.split("/", 2)[2]
    lref = year + "-" + month + "-" + day + " " + reft.split(" ", 1)[1]
    refresht = timeago.format(lref, curr_time_split)
    status = str("<b>State: <u>{} - {}</u></b> \n<code>😷  Confirmed  |  {} \n🤗  Recovered  |  {} \n💀  Deaths     |  {} \n🤧  Total      |  {}</code> \n\n<b>New Cases</b> \n<code>😷  Confirmed  |  {} \n💀  Deaths     |  {} \n🤗  Recovered  |  {}</code> \n\n<i>Refreshed: {}</i>".format(k['state'], k['statecode'], k['active'], k['recovered'], k['deaths'], k['confirmed'], k['deltaconfirmed'], k['deltadeaths'], k['deltarecovered'], refresht))
    return status
