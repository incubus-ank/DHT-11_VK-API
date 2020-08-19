import vk_api 
from vk_api.longpoll import VkLongPoll, VkEventType
import RPi.GPIO as GPIO
import Adafruit_DHT


GPIO.setmode(GPIO.BCM)

gpio4_pin7 = 4

gpio17_pin11 = 17
gpio27_pin13 = 27
gpio22_pin15 = 22

sensor = Adafruit_DHT.DHT11

GPIO.setup(gpio4_pin7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)

GPIO.setup(gpio17_pin11, GPIO.OUT) 
GPIO.output(gpio17_pin11, 0)
GPIO.setup(gpio27_pin13, GPIO.OUT) 
GPIO.output(gpio27_pin13, 0)
GPIO.setup(gpio22_pin15, GPIO.OUT) 
GPIO.output(gpio22_pin15, 0)


vk_session = vk_api.VkApi(token='')

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():    

    
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

        
        if event.text.lower() == 'проверка' :
                vk.messages.send(user_id=event.user_id,random_id=event.random_id,message='Успешно!')

        if event.text.lower() == 'вкл_красный' :
                vk.messages.send(user_id=event.user_id,random_id=event.random_id,message='Включен красный светодиод')
                GPIO.output(gpio17_pin11, 1)               
        if event.text.lower() == 'выкл_красный' :
                vk.messages.send(user_id=event.user_id,random_id=event.random_id,message='Красный светодиод выключен')
                GPIO.output(gpio17_pin11, 0)
                
        if event.text.lower() == 'вкл_зеленый' :
                vk.messages.send(user_id=event.user_id,random_id=event.random_id,message='Включен зелёный светодиод')
                GPIO.output(gpio27_pin13, 1)          
        if event.text.lower() == 'выкл_зеленый' :
                vk.messages.send(user_id=event.user_id,random_id=event.random_id,message='Зелёный светодиод выключен')
                GPIO.output(gpio27_pin13, 0)

        if event.text.lower() == 'вкл_синий' :
                vk.messages.send(user_id=event.user_id,random_id=event.random_id,message='Включен синий светодиод')
                GPIO.output(gpio22_pin15, 1)                               
        if event.text.lower() == 'выкл_синий' :
                vk.messages.send(user_id=event.user_id,random_id=event.random_id,message='Синий светодиод выключен')
                GPIO.output(gpio22_pin15, 0)
        
        if event.text.lower() == 'показания' :
                humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio4_pin7)
                if humidity is not None and temperature is not None:
                    s = ('Температура={0:0.1f}*C  Влажность={1:0.1f}%'.format(temperature, humidity))
                else:
                    s = ('Ошибка. Попробуйте снова!')
                vk.messages.send(user_id=event.user_id,random_id=event.random_id,message=s)                
