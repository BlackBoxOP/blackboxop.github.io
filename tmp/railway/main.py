from bs4 import BeautifulSoup
import requests
import time
import sys
from process import get_vcode

reurl = sys.argv[1]
url = "https://blackboxtw.herokuapp.com/api/"
domain = 'https://tip.railway.gov.tw'
rcgurl = reurl+'recognize'


while True:
    has_t = True
    sess = requests.Session()
    homepage = sess.get(domain + '/tra-tip-web/tip/tip001/tip121/query')
    soup = BeautifulSoup(homepage.text, "lxml")
    csrf = soup.find('input', attrs={"name": "_csrf"})['value']
    quickTipToken = soup.find('input', attrs={"name": "quickTipToken"})['value']
    cookie = sess.cookies.get_dict()['T4TIPSESSIONID']
    sess.close()
    vcode = get_vcode(sess, rcgurl)
    while has_t:
        if 't' in vcode:
            vcode = get_vcode(sess, rcgurl)
        else:
            has_t = False
    data_dict = {'csrf':csrf, 'quickTipToken':quickTipToken, 'vcode':vcode, 'T4TIPSESSIONID':cookie, "submit": "Submit"}
    # print(data_dict)
    r = requests.post(url, params={"admin_key":"0ad1d33f55c56bcd7e57cee1b3a031397acbab2c"}, data=data_dict)