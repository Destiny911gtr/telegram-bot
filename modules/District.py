import json, requests

url = "https://api.covid19india.org/state_district_wise.json"

def getDistricts(state="Kerala"):
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    if state in data:
        district = data[state]["districtData"]
        distdata = str("<b><u>District-wise Reports</u></b>\n\n")
        for key,value in district.items():
            distdata = distdata + str("<code>> {} : {}</code>\n".format(key,value["confirmed"]))
        return distdata
    else:
        failed = "Wrong input. Eg - <code>/dist Kerala</code> \n\nVisit https://www.covid19india.org/ for more info."
        return failed
