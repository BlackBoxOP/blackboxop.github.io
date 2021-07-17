import requests
from pydub import AudioSegment, audio_segment
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randrange
import io
import json


server_name = "https://tip.railway.gov.tw"   

def captcha(sess):
    sess.get(server_name + '/tra-tip-web/tip/player/nonPicture?pageRandom%20='+str(randrange(299999999)))
    sess.get(server_name + '/tra-tip-web/tip/player/changeVoiceVerifyCode?pageRandom='+str(randrange(299999999)))
    res = sess.get(server_name + '/tra-tip-web/tip/player/audio?pageRandom='+str(randrange(299999999)))
    return res.content

def get_vcode(sess, url):
    s = io.BytesIO(captcha(sess))
    sound_file = AudioSegment.from_file(s)
    sound = sound_file[16000:28000]
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