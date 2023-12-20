import sys,os
import requests
import threading
from urllib.parse import quote

print('''
      _ _                                     
     | (_)                                    
   __| |_ _ __ ___  __ _  ___ _ __   ___ _ __ 
  / _` | | '__/ __|/ _` |/ __| '_ \ / _ \ '__|
 | (_| | | |  \__ \ (_| | (__| | | |  __/ |   
  \__,_|_|_|  |___/\__,_|\___|_| |_|\___|_|   
                                vesion 1.0              
                                by killeveee             
''')
def dirfunc(url, file):
    with open(file, 'r') as file:
        wordlist = [line.strip() for line in file]

    print('Start scan...')
    threads = []
    success_results = []  # 用于保存状态码为200的结果

    def scan_thread(word):
        try:
            u = quote(url + word, safe='/:?=&(\')')
            response = requests.get(u, timeout=5, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
            status_code = response.status_code
            if status_code == 200:
                success_results.append(u)
            print(f"{Colors.GREEN}[+]{status_code} {u}{Colors.RESET}" if status_code == 200 else f"[-]{status_code} {u}")
        except requests.RequestException as e:
            print(f"发生错误: {e}")

    for w in wordlist:
        thread = threading.Thread(target=scan_thread, args=(w,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("\n----------状态码为200的结果------------")
    for result in success_results:
        print(f"{Colors.GREEN}{result}{Colors.RESET}")

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def err():
    print("[!]Parameter Error!",end='')
    helper()

def helper():
     print("""\n\n[-]Help:
Usage: dirscaner.py -u target [-f listfile]

Options:
  -h            show this help message and exit
  -u URL        Target URL(s)
  -f PATH       URL list file,default simple.txt
""")
     exit()
        
if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == '-u' and sys.argv[3] == '-f':
        dirfunc(sys.argv[2], sys.argv[4])
    if len(sys.argv) == 3 and sys.argv[1] == '-u':
        dirfunc(sys.argv[2], os.getcwd()+"\simple.txt")
    elif len(sys.argv) == 2 and sys.argv[1] == '-h':
        helper()
    else:
        err()