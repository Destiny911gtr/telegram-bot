import json, requests

url = "https://api.covid19india.org/state_district_wise.json"

def getDistricts(state="Kerala"):
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    district = data[state]["districtData"]
    distdata = str("District-wise Reports\n\n")
    for key,value in district.items():
        distdata = distdata + str("{} : {}\n".format(key,value["confirmed"]))
    return distdata
