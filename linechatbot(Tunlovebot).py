from flask import Flask, request, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
        MessageEvent, TextMessage, TextSendMessage,
        ImageMessage, ImageSendMessage,
        TemplateSendMessage, MessageAction,
        ButtonsTemplate,ConfirmTemplate, URIAction,
        FlexSendMessage, BubbleContainer,
        StickerMessage, StickerSendMessage)
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta

import random
import os
import tempfile
import numpy as np
import calendar
import time
import atexit   #
import pytz     #

thai_months = ['มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม']
thai_days = ['วันอาทิตย์', 'วันจันทร์', 'วันอังคาร', 'วันพุธ', 'วันพฤหัสบดี', 'วันศุกร์', 'วันเสาร์']

#--------------Tunbot_Love----------------------------
channel_access_token = "---------------------------------"
channel_secret = "------------------------------"
user_id = "------------"
#----------------------------------------------------------------

#------------------------------------------------------------------------
from wit import Wit
wit_access_token = "-----------------------------------F"
client = Wit(wit_access_token)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

def put_png(img_main,png_file,xp,yp,wp,hp):
    img_png = cv2.imread(png_file,cv2.IMREAD_UNCHANGED) #BGRA
    img_png = cv2.resize(img_png,(wp,hp))
    b,g,r,a = cv2.split(img_png)
    a_inv = cv2.bitwise_not(a)
    roi = img_main[yp:yp+hp,xp:xp+wp].copy()
    bg = cv2.bitwise_or(roi,roi,mask=a_inv)
    fg = cv2.bitwise_and(img_png[:,:,:3],img_png[:,:,:3],mask=a)
    dst = cv2.add(bg,fg)
    img_main[yp:yp+hp,xp:xp+wp] = dst    
    return img_main
#---------------------------------------------------------------------------------------
scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Bangkok'))
scheduler.start()

def send_hello_message():
    # ส่งข้อความ "สวัสดี" เมื่อเวลา 07:00
    current_time = datetime.now(pytz.timezone('Asia/Bangkok'))
    if current_time.hour == 7 and current_time.minute == 0:
        send_message("มอนิ่งค้าบบ")

def send_lunch_message():
    # ส่งข้อความ "กินข้าวด้วย" เมื่อเวลา 12:00
    current_time = datetime.now(pytz.timezone('Asia/Bangkok'))
    if current_time.hour == 12 and current_time.minute == 0:
        send_message("กินข้าวด้วยนะครับ")

def send_goodnight_message():
    # ส่งข้อความ "บอกฝันดี" เมื่อเวลา 21:00
    current_time = datetime.now(pytz.timezone('Asia/Bangkok'))
    if current_time.hour == 21 and current_time.minute == 0:
        send_message("ฝันดีนะครับบ")

def send_birthday_greeting():
    # ส่งข้อความ "สุขสันต์วันเกิด" เมื่อวันที่ปัจจุบันเป็น 5 ธันวาคม
    current_date = datetime.now(pytz.timezone('Asia/Bangkok'))
    if current_date.month == 12 and current_date.day == 5:
        send_message("สุขสันต์วันเกิดครับ/ค่ะ")
        
def send_test_message():
    
    print("ส่งข้อความ ""เทส"" เมื่อเวลา 22:10 ในวันที่ 6 เมษายน 2567")  
    # ส่งข้อความ ""เทส"" เมื่อเวลา 22:10 ในวันที่ 6 เมษายน 2567
    current_time = datetime.now(pytz.timezone('Asia/Bangkok'))
    if current_time.year == 2024 and current_time.month == 4 and current_time.day == 6 and current_time.hour == 22 and current_time.minute == 30:
        send_message("เทสระบบส่งอัตโนมัติ")

def send_message(text):
    # ส่งข้อความกลับไปยังผู้ใช้
    message = TextSendMessage(text)
    line_bot_api.push_message(user_id, message)

# ตั้งเวลาในการส่งข้อความ
scheduler.add_job(send_hello_message, 'cron', hour=7, minute=0)
scheduler.add_job(send_lunch_message, 'cron', hour=12, minute=0)
scheduler.add_job(send_goodnight_message, 'cron', hour=21, minute=0)
scheduler.add_job(send_birthday_greeting, 'cron', month=12, day=5)
scheduler.add_job(send_test_message, 'cron', year=2024, month=4, day=6, hour=22, minute=30)


# ปิด Scheduler เมื่อทำงานเสร็จสิ้น
atexit.register(lambda: scheduler.shutdown())

#------------------------------------------------------------------------------------------

answer_greeting = ["มอนิ่งงับแฟน","มอนิ่งงับ","มอนิ่งง้าบบ","มอนิ่งคับบ","สวัสดีงับแฟน","มอนิ่งนะยั้ยตัวเล็ก","มอนิ่งค้าบบ"]
answer_Goodnight = ["ฝันดีงับ","ฝันดีค้าบบ","ฝันดีนะแฟน","ฝันดีค้าบที่รัก","ฝันหวานงับ","ฝันดีครับ","ฝันดีง้าบบ","ฝันถึงเค้าด้วยน้า"]
#answer_where = ["ภาคไฟฟ้า ศิลปากร","ภาควิชาวิศวกรรมไฟฟ้า","ภาคไฟฟ้า","ภาควิชาวิศวกรรมไฟฟ้า มหาวิทยาลัยศิลปากร"]
answer_love = ["รักจิ","รักงับ","รักน้าา","รักมากๆเลยย","รักที่สุดด","รักนะยั้ยตัวเล็ก","รักคนเดียวง้าบบ","รักที่สุดในโลกเลย"]
answer_Cute = ["ที่รักสวยมากงับ","น่ารักมาก","สวยที่สุดง้าบบ","น่ารักน่าหอมงับบ","น่ารักจิ","สวยงับบ","สวยมากๆๆงับ"]
answer_Doingwhat = ["เค้าทำงานงับบ","เล่นเกมง้าบบ","เค้ากินข้าวงับบ","เค้าคิดถึงอยู่งับ","เค้าฝึกอยู่งับ"]
answer_missyou = ["เค้าคิดถึงมากๆเลย","เค้าก็คิดถึงงับ","เค้าคิดถึงที่สุดดด","เค้าคิดถึงนะ","เค้าคิดถึงจัง"]
answer_eat = ["กินแล้วครับ","กินแล้วงับ","กินแล้วครับบ อิ่มมาก","กินแล้ววว","กินแล้ว","ยังไม่ได้กินเลย","ยังเลย","ยังไม่ได้กิน","ยัง"]
answer_next = ["วันนี้นอนอิ่มไหมแฟน","กินข้าวด้วยน้า","เค้าคิดถึงนะ","อาบน้ำด้วยน้าจะได้หอมๆ","อยากเจอแฟนจังง","แฟนรอเค้าด้วยนะ","เค้ารักแฟนนะ"]
answer_next2 = ["หอมๆน้า","จุ๊บๆ ","กอดๆ","มาอุ้มๆ","คนเก่งง","สู้ๆน้า","จุ๊บๆน้าาคนเก่ง","จูบๆๆ","หอม","love love นะ"]

@handler.add(MessageEvent, message=TextMessage)     #ส่วนนี้เกี่ยวกับการรับข้อความ
def handle_text_message(event):
    text = event.message.text
    print(text)    
    current_time = time.localtime()
    Date = f"{current_time.tm_mday} {thai_months[current_time.tm_mon-1]} {current_time.tm_year + 543} "
    print(Date)
    print(type(Date))
    if (text == 'ความรัก'):
        text_show = 'คุณต้องการความรักแบบใด'
        img_url = request.url_root + '/static/A.jpg'
        buttons_template = ButtonsTemplate(
            title='Thun Cafe ยินดีให้บริการ', text=text_show,thumbnail_image_url = img_url,actions=[
                MessageAction(label='รักมากกก', text='รักมากกก'),
                MessageAction(label='รักที่สุด', text='รักที่สุด'),
                MessageAction(label='รัก', text='รัก'),
                URIAction(label='เข้าฟังเพลง',uri='https://www.youtube.com/watch?v=URNttPi5Iio')])
        template_message = TemplateSendMessage(alt_text=text_show, template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        
    elif (text == 'เพลงรัก'):
        text_show = 'สุ่มเพลงเลย'
        img_url = request.url_root + '/static/heart1.jpg'
        buttons_template = ButtonsTemplate(
            title='Thun ยินดีให้บริการ', text=text_show,thumbnail_image_url = img_url,actions=[
                URIAction(label='เข้าฟังเพลง',uri='https://www.youtube.com/watch?v=faccKGHl5jM'),
                URIAction(label='เข้าฟังเพลง',uri='https://www.youtube.com/watch?v=czvDyFfVoVU'),
                URIAction(label='เข้าฟังเพลง',uri='https://www.youtube.com/watch?v=SDvYqwJ0Vy0'),
                URIAction(label='เข้าฟังเพลง',uri='https://www.youtube.com/watch?v=URNttPi5Iio')])
        template_message = TemplateSendMessage(alt_text=text_show, template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == 'เทส':
        print("เทสส")
        # ส่ง StickerMessage ไปยังผู้ใช้
        #line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=p_id,sticker_id=s_id))
        current_time = time.localtime()
        Date = f"{current_time.tm_mday} {thai_months[current_time.tm_mon-1]} {current_time.tm_year + 543}"
        print(Date)
        if Date == "31 ตุลาคม 2566":
            print('ผ่านนนนน')
            text_message = TextSendMessage(text="วันที่ 5 พฤศจิกายน 2566")
            
            # สร้างข้อความสติกเกอร์
            sticker_message = StickerSendMessage(package_id='1', sticker_id='106')
            
            # เพิ่มข้อความเข้าไปใน messages
            messages = [text_message, sticker_message]
            
            # ส่งข้อความทั้งหมดในการสนทนาเดียว
            line_bot_api.reply_message(event.reply_token, messages)
            
    elif text == 'วันเกิด':
        print("วววววววว")
        # ส่ง StickerMessage ไปยังผู้ใช้
        #line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=p_id,sticker_id=s_id))
        current_time = time.localtime()
        Date = f"{current_time.tm_mday} {thai_months[current_time.tm_mon-1]} {current_time.tm_year + 543}"
        print(Date)
        if Date == "5 พฤศจิกายน 2566":
            print('ผ่านนนนน')
            text_message = TextSendMessage(text="วันนี้วันเกิดแฟนน้า เค้าไม่ได้อยู่ด้วยนะ แฟนไม่ต้องร้องไห้ไม่ต้องหวงเค้านะ เค้าจะรีบออกมา เค้ารักแฟนนะ ขอให้มีความสุขมากนะแฟนเดียวเค้าพาไปเที่ยวนะเดียวก็ได้คุยกันนะแฟน สู้ไปด้วยกันนะ รักนะ")
                
            # สร้างข้อความสติกเกอร์
            sticker_message = StickerSendMessage(package_id='3', sticker_id='257')
                
            # เพิ่มข้อความเข้าไปใน messages
            messages = [text_message, sticker_message]
                
            # ส่งข้อความทั้งหมดในการสนทนาเดียว
            line_bot_api.reply_message(event.reply_token, messages)
        else:
            text_message = TextSendMessage(text=f"วันนี้วันที่ {current_time.tm_mday} {thai_months[current_time.tm_mon-1]} {current_time.tm_year + 543} ยังไม่ถึงน้า" )
                
            # สร้างข้อความสติกเกอร์
            sticker_message = StickerSendMessage(package_id='3', sticker_id='243')
                
            # เพิ่มข้อความเข้าไปใน messages
            messages = [text_message, sticker_message]
                
            # ส่งข้อความทั้งหมดในการสนทนาเดียว
            line_bot_api.reply_message(event.reply_token, messages)

    elif text == 'สำรวจ':
        ask_text = 'คุณชอบทานผัดกระเพราหรือไม่'
        confirm_template = ConfirmTemplate(text=ask_text,actions=[
            MessageAction(label='Yes', text='ชอบทาน'),
            MessageAction(label='No', text='ไม่ชอบทาน')])
        template_message = TemplateSendMessage(alt_text=ask_text,template=confirm_template)
        line_bot_api.reply_message(event.reply_token,template_message)
        
    elif text == 'สำเร็จ':
        ask_text = 'คุณชอบทำงานไหมหรือไม่'
        confirm_template = ConfirmTemplate(text=ask_text,actions=[
            MessageAction(label='Yes', text='ชอบทำ'),
            MessageAction(label='No', text='ไม่ชอบทำ')])
        template_message = TemplateSendMessage(alt_text=ask_text,template=confirm_template)
        line_bot_api.reply_message(event.reply_token,template_message)

    elif (text != ""):
        ret = client.message(text)
        if len(ret["intents"]) > 0:
            confidence = ret["intents"][0]['confidence']
            print("confidence : ",str(confidence))
            if (confidence > 0.8):
                intents_name = ret["intents"][0]['name']        
                print("intent = ",intents_name)

                if (intents_name == "greeting"):
                        idx_greeting = random.randint(0, len(answer_greeting) - 1)
                        text_out_greeting = answer_greeting[idx_greeting]
                        
                        # สุ่มจำนวนข้อความระหว่าง 0 ถึง 5
                        num_messages = random.randint(0, 5)
                        
                        # สุ่มข้อความที่ไม่ซ้ำกัน
                        random_messages = random.sample(answer_next, num_messages)
                        
                        # สร้างข้อความในรายการ
                        messages = [TextSendMessage(text=text_out_greeting)]
                        for message in messages:
                            print(message.text)
                        for message in random_messages:
                            messages.append(TextSendMessage(text=message))
                        '''    # ส่งสติกเกอร์
                        p_id = 1
                        s_id = 106
                        sticker_message = StickerSendMessage(package_id=p_id, sticker_id=s_id)
                        messages.append(sticker_message)'''
                        for message in messages:
                            print(message.text)
                        # ส่งข้อความทั้งหมดในการสนทนาเดียว
                        line_bot_api.reply_message(event.reply_token, messages)
                        
                elif (intents_name == "Goodnight"):
                        idx_Goodnight = random.randint(0, len(answer_Goodnight) - 1)
                        text_out_Goodnight = answer_Goodnight[idx_Goodnight]
                        
                        # สุ่มจำนวนข้อความระหว่าง 0 ถึง 2
                        num_messages = random.randint(0, 2)
                        
                        # สุ่มข้อความที่ไม่ซ้ำกัน
                        random_messages = random.sample(answer_next2, num_messages)
                        
                        # สร้างข้อความในรายการ
                        messages = [TextSendMessage(text=text_out_Goodnight)]
                        for message in messages:
                            print(message.text)
                        for message in random_messages:
                            messages.append(TextSendMessage(text=message))
                        for message in messages:
                            print(message.text)
                        # ส่งข้อความทั้งหมดในการสนทนาเดียว
                        line_bot_api.reply_message(event.reply_token, messages)

                elif (intents_name == "love"):
                        idx_love = random.randint(0, len(answer_love) - 1)
                        text_out_love = answer_love[idx_love]
                        
                        # สุ่มจำนวนข้อความระหว่าง 0 ถึง 2
                        num_messages = random.randint(0, 2)
                        
                        # สุ่มข้อความที่ไม่ซ้ำกัน
                        random_messages = random.sample(answer_next2, num_messages)
                        
                        # สร้างข้อความในรายการ
                        messages = [TextSendMessage(text=text_out_love)]
                        for message in messages:
                            print(message.text)
                        for message in random_messages:
                            messages.append(TextSendMessage(text=message))
                        for message in messages:
                            print(message.text)
                        # ส่งข้อความทั้งหมดในการสนทนาเดียว
                        line_bot_api.reply_message(event.reply_token, messages)        

                elif (intents_name == "Cute"):
                        idx_Cute = random.randint(0, len(answer_Cute) - 1)
                        text_out_Cute = answer_Cute[idx_Cute]
                        
                        # สุ่มจำนวนข้อความระหว่าง 0 ถึง 1
                        num_messages = random.randint(0, 1)
                        
                        # สุ่มข้อความที่ไม่ซ้ำกัน
                        random_messages = random.sample(answer_next2, num_messages)
                        
                        # สร้างข้อความในรายการ
                        messages = [TextSendMessage(text=text_out_Cute)]
                        for message in messages:
                            print(message.text)
                        for message in random_messages:
                            messages.append(TextSendMessage(text=message))
                        for message in messages:
                            print(message.text)
                        # ส่งข้อความทั้งหมดในการสนทนาเดียว
                        line_bot_api.reply_message(event.reply_token, messages)

                elif (intents_name == "Doingwhat"):
                        idx_Doingwhat = random.randint(0, len(answer_Doingwhat) - 1)
                        text_out_Doingwhat = answer_Doingwhat[idx_Doingwhat]
                        
                        # สุ่มจำนวนข้อความระหว่าง 0 ถึง 2
                        num_messages = random.randint(0, 2)
                        #print(" num_messages : "+ str(num_messages))
                        # สุ่มจำนวนข้อความระหว่าง 0 ถึง 2
                        num_messages2 = random.randint(0, 2)
                        #print(" num_messages2 : "+ str(num_messages2))
                        # สุ่มข้อความที่ไม่ซ้ำกัน
                        random_messages = random.sample(answer_next2, num_messages)
                        # สุ่มข้อความที่ไม่ซ้ำกัน
                        random_messages2 = random.sample(answer_next, num_messages2)
                        # สร้างข้อความในรายการ
                        messages = [TextSendMessage(text=text_out_Doingwhat)]
                        for message in messages:
                            print(message.text)
                        for message in random_messages:
                            messages.append(TextSendMessage(text=message))
                        for message in random_messages2:
                            messages.append(TextSendMessage(text=message))
                        for message in messages:
                            print(message.text)
                        # ส่งข้อความทั้งหมดในการสนทนาเดียว
                        line_bot_api.reply_message(event.reply_token, messages)
                        
                elif (intents_name == "missyou"):
                        idx_missyou = random.randint(0, len(answer_missyou) - 1)
                        text_out_missyou = answer_missyou[idx_missyou]
                        
                        # สุ่มจำนวนข้อความระหว่าง 0 ถึง 1
                        num_messages = random.randint(0, 1)
                        
                        # สุ่มข้อความที่ไม่ซ้ำกัน
                        random_messages = random.sample(answer_next2, num_messages)
                        
                        # สร้างข้อความในรายการ
                        messages = [TextSendMessage(text=text_out_missyou)]
                        for message in messages:
                            print(message.text)
                        for message in random_messages:
                            messages.append(TextSendMessage(text=message))
                        for message in messages:
                            print(message.text)
                        # ส่งข้อความทั้งหมดในการสนทนาเดียว
                        line_bot_api.reply_message(event.reply_token, messages)
                        
                elif (intents_name == "eat"):
                        idx_eat = random.randint(0, len(answer_eat) - 1)
                        text_out_eat = answer_eat[idx_eat]
                        
                        # สุ่มจำนวนข้อความระหว่าง 0 ถึง 1
                        num_messages = random.randint(0, 1)
                        
                        # สุ่มข้อความที่ไม่ซ้ำกัน
                        random_messages = random.sample(answer_next2, num_messages)
                        
                        # สร้างข้อความในรายการ
                        messages = [TextSendMessage(text=text_out_eat)]
                        for message in messages:
                            print(message.text)
                        for message in random_messages:
                            messages.append(TextSendMessage(text=message))
                        for message in messages:
                            print(message.text)
                        # ส่งข้อความทั้งหมดในการสนทนาเดียว
                        line_bot_api.reply_message(event.reply_token, messages)
                        
                elif (intents_name == "date") :
                        current_time = time.localtime()
                        thai_time = f"{thai_days[current_time.tm_wday]} {current_time.tm_mday} {thai_months[current_time.tm_mon-1]} {current_time.tm_year + 543} เวลา {current_time.tm_hour:02}:{current_time.tm_min:02}:{current_time.tm_sec:02} น."
                        print(thai_time)
                        Date = f"{current_time.tm_mday} {thai_months[current_time.tm_mon-1]} {current_time.tm_year + 543} "
                        print(Date)
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=thai_time))

                                                                                                         
        else :
                print("intent = unknow")
                text_out = "ง่ะ เจ้านายธันไม่ได้ตั้งคำถามนี้ กรุณาถามใหม่อีกครั้งครับ"
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))


if __name__ == "__main__":
    app.run()

