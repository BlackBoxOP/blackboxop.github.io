import requests
from pydub import AudioSegment
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import io
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en,zh-TW;q=0.9,zh;q=0.8,ko;q=0.7,ja;q=0.6',
    "Host": "irs.thsrc.com.tw"
}


server_name = "https://tip.railway.gov.tw"   

def captcha(sess, jsession):
    res = sess.get('https://irs.thsrc.com.tw/IMINT/;jsessionid={}?wicket:interface=:0:BookingS1Form:homeCaptcha:soundLink::ILinkListener'.format(jsession), headers=headers)
    return res.content

def get_vcode(sess, url, jsession):
    s = io.BytesIO(captcha(sess, jsession))
    sound = AudioSegment.from_file(s)
    datas={'swidth':sound.sample_width, 'channels':sound.channels, 'frate':sound.frame_rate}
    res = requests.post(url, files={'file':sound.raw_data, 'data':json.dumps(datas)})
    return res.text

def send_mail(booking_id, message):
    email = "tomas890812@gmail.com"
    password = 'jtmduhzmdyjfohai'
    send_to_email = 'tomas890812@gmail.com'
    subject = 'Booking Succed ID : ' + booking_id
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))
    server.sendmail(email, [send_to_email], msg.as_string())
    server.quit()