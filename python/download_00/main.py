"""
python main.py
python C:\development\always_bet_on_red\python\download_00\main.py

"""

import urllib.request

def main():
    url = "https://www.google.com/"
    response = urllib.request.urlopen(url)
    webContent = response.read().decode('UTF-8')
    print(webContent[0:300])

if __name__ == "__main__":
    main()