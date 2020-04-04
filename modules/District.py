import json, requests

url = "https://api.covid19india.org/state_district_wise.json"

def getDistricts(state="Kerala"):
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    if state in data:
        district = data[state]["districtData"]
        distdata = str("District-wise Reports\n\n")
        for key,value in district.items():
            distdata = distdata + str("{} : {}\n".format(key,value["confirmed"]))
        return distdata
    else:
        failed = "Wrong input. Eg - /idist Kerala \n\nVisit https://www.covid19india.org/ for more info."
        return failed

def getDelta(state="Kerala"):
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    if state in data:
        district = data[state]["districtData"]
        distdata = str("District-wise Reports\n\n")
        for key,value in district.items():
            distdata = distdata + str("{} : {}\n".format(key,value["delta"]["confirmed"]))
        return distdata
    else:
        failed = "Wrong input. Eg - /inew_dist Kerala \n\nVisit https://www.covid19india.org/ for more info."
        return failed
