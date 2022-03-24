#!/usr/bin/env python
def main():
	global username, choices, proxylist, proxy_q, threads_checker, threads_scraper, proxy_checker
	try:
		from datetime import date, datetime
		import re, requests, time, threading, urllib3, json, os
		os.system('cls')
		from queue import Queue
		import tkinter
		from tkinter.filedialog import askopenfilename
	except:
		print(" It seems you are missing some requirements. Please use:\npip install -r requirements.txt using cd on the current directory.")
		if input("Do you want me to manually install them for you? [Y/N]") == "Y":
			if not os.path.exists('requirements.txt'):
				open('requirements.txt', 'w').write("""requests==2.25.1
	tk==0.1.0
	tkfilebrowser==2.3.2
	urllib3==1.26.3
	""")
				os.system('pip install -r requirements.txt')
				os.system('cls')
		else:
			print("Ok have fun downloading them yourself noob.")
			input()
	root = tkinter.Tk()
	root.withdraw()
	urllib3.disable_warnings()
	if not os.path.exists('Results/ProxiesFound'):
		os.mkdir('Results')
		os.mkdir('Results/ProxiesFound')

	#define working lists
	
	working_socks5	= []
	working_socks4	= []
	working_https	= []
	dupes = []
	proxylist = []
	found_dupes = 0
	found_no_dupes = 0
	#Title
	try:
		configDict = open('config.json', 'r').read()
		configDict = json.loads(configDict)
		timeout_scraper = (configDict['timeout_scraper'] / 1000)
		timeout_checker = (configDict['timeout_checker'] / 1000)
		threads_scraper = configDict['threads_scraper']
		threads_checker = configDict['threads_checker']
	except:
		print("Error loading the config, is it in the same dir or did you remove any lines from it?")
		
		if input("Do you want to create the config ? [Y/N]") == "Y":
			open('config.json', 'w').write("""	
{
"threads_scraper":300,
"threads_checker":1000,
"timeout_scraper":10, 
"timeout_checker":5,


"notes":"All have to be integers, the names are pretty self explaining, the time is in seconds. I suggest keeping the scraper timeout under 30 seconds."


}""")
			os.system('cls')
	
	def slowtype(message, delay):
		for i in message:
			print(i, flush=True, end='')
			time.sleep(delay)
	
	def title():
		print("""
	
	
	███████╗██╗     ██╗████████╗███████╗    ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗███████╗███████╗
	██╔════╝██║     ██║╚══██╔══╝██╔════╝    ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝██║██╔════╝██╔════╝
	█████╗  ██║     ██║   ██║   █████╗      ██████╔╝██████╔╝██║   ██║ ╚███╔╝ ██║█████╗  ███████╗
	██╔══╝  ██║     ██║   ██║   ██╔══╝      ██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗ ██║██╔══╝  ╚════██║
	███████╗███████╗██║   ██║   ███████╗    ██║     ██║  ██║╚██████╔╝██╔╝ ██╗██║███████╗███████║
	╚══════╝╚══════╝╚═╝   ╚═╝   ╚══════╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝
	                                                                                            
	
	
	""")
	
	def choices():
		global choices
		choices = input("""
[1] Proxy Scraper
[2] Proxy Checker
[>]  """)
	
	def check_https(current_proxy):
		try:
			proxies = {
				"http":current_proxy,
				"https":current_proxy
			}
			requests.get("http://azenv.net/", proxies=proxies, timeout=timeout_checker)
			working_https.append(current_proxy)
			print(f"{current_proxy} is working. as https")
			with open("working_https.txt", "a") as currHttps:
				currHttps.write(current_proxy + "\n")
			return True
		except:
			return False
			
	def check_socks5(current_proxy):
		try:
			proxies = {
				"http":f"socks5h://{current_proxy}",
				"https":f"socks5h://{current_proxy}"
			}
			requests.get("http://azenv.net/", proxies=proxies, timeout=timeout_checker)
			working_socks5.append(current_proxy)
			print(f"{current_proxy} is working. as socks5")
			with open("working_socks5.txt", "a") as currSocks5:
				currSocks5.write(current_proxy + "\n")
			return True
		except:
			return False
	
	def check_socks4(current_proxy):
		try:
			proxies = {
				"http":f"socks4h://{current_proxy}",
				"https":f"socks4h://{current_proxy}"
			}
			requests.get("http://azenv.net/", proxies=proxies, timeout=timeout_checker)
			working_socks4.append(current_proxy)
			print(f"{current_proxy} is working. as socks4")
			with open("working_socks4.txt", "a") as currSocks4:
				currSocks4.write(current_proxy + "\n")
			return True
		except:
			return False
	
	proxy_q = Queue()
	
	def proxy_checker():
		global proxy_q, proxyFile
		while not proxy_q.empty():
			current_proxy = proxy_q.get()
			print(f"{proxy_q.qsize()} Proxies left.", end='\r')
			if not check_https(current_proxy):
				check_socks5(current_proxy)
	
			proxy_q.task_done()
	
	
	
	
	
	def proxyScraper():
		global currProxyDir
		try:
			if not os.path.exists(f'Resuts/ProxiesFound/Proxies-{date.today()}'):
				os.mkdir(f'Results/ProxiesFound/Proxies-{date.today()}')
			
		except:
			pass
	
	
		currProxyDir = f'Results/ProxiesFound/Proxies-{date.today()}'
		global q
		with open('url.txt', "r") as reader:
			urls = reader.read().split("\n")
		
		q = Queue()
		for url in urls:
			q.put(url)
		
		
		def scraper():
			global urls, document, q, proxies, document, proxylist, currProxyDir
			while not q.empty():
		
				try:
					now = q.get()
					headers= {
						"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
					}
					document = requests.get(now, timeout=10, headers=headers, verify = False).text
				except:
					pass
				try:	
					proxylist += re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+", document)
				except:
					pass
	
				q.task_done()
		
		for i in range(threads_scraper):
			print(f"Thread #{i + 1} Started.", end="\r")
			threading.Thread(target=scraper, daemon=True).start()
		
		print("")
		print('Threads loaded.')
		q.join()
		scraper()
		time.sleep(timeout_scraper)
		print("Verifying dupes..")
		dupes = list(set(proxylist))
		
		now = datetime.now()
		ez = now.strftime('%X')
		a = ez.split(":")
		new = f"{a[0]}h{a[1]}s{a[2]}"
		print("Writing :D")
		with open(f'{currProxyDir}/proxies{new}.txt', "a") as appender:
			for i in dupes:
				appender.write(i + "\n")
	
		
		if input("[1] Check Proxies\n[>]  ") == "1":
			askAndStartChecker()
	
	def askAndStartChecker():
		global proxy_checker, threads_checker, proxy_q
		proxyFile = askopenfilename(title="Choose your file containing your proxies")
		proxyList = open(proxyFile, "r").read().split("\n")
		for i in proxyList:
			proxy_q.put(i)
	
		for _ in range(threads_checker):
			threading.Thread(target=proxy_checker, daemon=True).start()
	
		proxy_checker()
	
	
	title()
	slowtype(f"Welcome to EliteProxies", delay=0.1)
	choices()
	if choices == "1":
		print("Starting Scraping!")
		proxyScraper()
	
	if choices == "2":
		askAndStartChecker()

main()