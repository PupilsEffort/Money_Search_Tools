import requests
import threading
import re


targets = []
names = []

def icp_info(host):
    url = "https://icp.chinaz.com/ajaxsync.aspx?at=beiansl&callback=jQuery111305329118231795913_1554378576520&host=%s&type=host"%host
    html = requests.get(url,timeout=(5,10)).text
    pattern = re.compile('SiteName:"(.*?)",MainPage:"(.*?)"',re.S)
    info = re.findall(pattern,html)
    for i in range(0,32):
        try:
            name = info[i][0]
            target = info[i][1]
            print("%s:%s"%(name,target))
            if target not in targets:
                targets.append(target)
                with open("icp_info.txt","a+") as f:
                    f.write("%s:%s"%(name,target) + "\n")
                    continue
            else:
                continue
        except Exception as e:
            continue
def start():
    with open("url.txt","r+") as a:
        for b in a:
            b = b.strip()
            icp_info(host=b)
    a.close()
def main():
     thread = threading.Thread(target=start,)  
     thread.start()  

if __name__ == '__main__':
    main()