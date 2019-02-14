import re
import requests
import sys
import threading

try:
    from bs4 import BeautifulSoup
    from colorama import Fore, init, Style, Back
except ImportError:
    print("Please install Beautiful Soup and colorama: pip3 install bs4\npip3 install colorama-")

init()

mails = []

# TODO: Implement Threading
threads = []

def findMail(pageURL):
    try:
        url = requests.get(pageURL, timeout=5)
        page = url.text
        #print(f"{Fore.GREEN}[+] {pageURL}{Style.RESET_ALL}\n")

        page = page.replace('(at)', '@')
        page = page.replace('(AT)', '@')
        page = page.replace('_at_', '@')
        page = page.replace('_AT_', '@')
        page = page.replace('[AT]', '@')
        page = page.replace('[at]', '@')

        page = page.replace('_dot_', '.')
        page = page.replace('_DOT_', '.')

        page = page.replace('com.', 'com')
        page = page.replace('de.', 'de')
        page = page.replace('at.', 'at')

        pattern = r"[\w\d_.]+@[\w\d_-]+.[\w\d_.]+"
        data = re.findall(pattern, page)

        for mail in data:
            if " " in str(mail) or "user.token" in str(mail) or "user.options" in str(mail) or mail in mails or 'png' in mail or "." not in mail or "jpg" in mail:
                pass 
            else:   
                mails.append(mail)
                print(mail)
    except Exception:
        print(f"{Fore.RED} [-] Error accessing {pageURL}{Style.RESET_ALL}\n")
        pass

def searchGoogle(term):
    try:
        #print(f"{Fore.GREEN}[+] Term: {term}{Style.RESET_ALL}\n")
        url = 'https://www.google.com/search?q=' + term

        res = requests.get(url, timeout=5, verify=True)

        #print("Connection")

        soup = BeautifulSoup(res.content, 'html.parser')
        links = soup.find_all("a")
        for link in soup.find_all("a", href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
            l = re.split(":(?=http)", link["href"].replace("/url?q=",""))
            linkStr = ''.join(l)
            #print (l)
            findMail(linkStr)
    except requests.exceptions.Timeout:
        print("Timeout")
        

try:
    if sys.argv[1] != "" or " ":
        with open(str(sys.argv[1]), 'r') as f:
            for line in f:
                for query in line.split():
                    searchGoogle(query)

        print(f"{Fore.GREEN}[+] Found {len(mails)} Mails{Style.RESET_ALL}")
        for mail in mails:
            print(f"{Back.GREEN}{mail}{Style.RESET_ALL}")
    else:
        sys.exit()

except Exception as e:
    print(f"{Fore.RED}Usage: MailScraper.py <wordlist>")
    print(f"{Fore.RED} [-]", e)
    #sys.exit()
    print(f"{Fore.GREEN}[+] Found {len(mails)} Mails{Style.RESET_ALL}")
    with open("result.txt" 'w') as f:    
        for mail in mails:
            print(f"{Back.GREEN}{mail}{Style.RESET_ALL}")
            f.write(f"{mail}\n")
    f.close()

except KeyboardInterrupt:
    print(f"{Fore.RED}[-] Keyboard Interrupt by user")
    #sys.exit()
    print(f"{Fore.GREEN}[+] Found {len(mails)} Mails{Style.RESET_ALL}")
    with open("result.txt", 'w') as f:    
        for mail in mails:
            print(f"{Back.GREEN}{mail}{Style.RESET_ALL}")
            f.write(f"{mail}\n")
    f.close()
