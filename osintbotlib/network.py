import speedtest
import json 
import requests



def internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 10**6  # Mbps
    upload_speed = st.upload() / 10**6  # Mbps
    ping = st.results.ping  # ms

    return download_speed, upload_speed, ping





def GetIpQuery(ip_addrs): 
    try:
        MainUrl = f"https://ipinfo.io/{ip_addrs}"
        IpQuery = requests.get(url=MainUrl,timeout=10)
        
        if IpQuery.status_code == 200:
            IpQuery = json.loads(IpQuery.text)
            return ["true", IpQuery]
        else:
            return ["false", f"ipinfo.io istek durum kodu: {IpQuery.status_code}"]
    except Exception as err:
        return [ "false", "ipinfo.io isteği başarısız." ]
    

def IpQueryWithShodan(ip_addrs, shodan_api_key):
    try:
        MainUrl = f"https://api.shodan.io/shodan/host/{ip_addrs}?key={shodan_api_key}"
        IpQuery = requests.get(url=MainUrl,timeout=10)
        if IpQuery.status_code == 200:
            IpQuery = json.loads(IpQuery.text)
            return ["true", IpQuery]
        else:
            return ["false", f"shodan.io istek durum kodu: {IpQuery.status_code}"]
    except Exception:
        return [ "false", "shodan.io isteği başarısız." ]
    
