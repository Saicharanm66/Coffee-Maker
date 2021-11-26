import paho.mqtt.client as mqtt
import sched, time
import timeit
import json
import datetime 

coffee_temperature=0
coffee_status=0
set_time=int(timeit.default_timer())
duration=1
CurTime=0
PWcons=0

# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.subscribe("G6")
    Parameters = '{ "Time":"Time","OnTime":"time", "Temp":30, "Consumption":"Low", "Status":"ON"}'

    #client.publish("G6", Parameters)

# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    global coffee_temperature
    global coffee_status
    try:
        ifjson=json.loads(str(msg.payload.decode("utf-8","ignore")))
        coffee_temperature= ifjson["Temp"]
        coffee_status= ifjson["Status"]
    except:
        print(str(msg.payload))
    #print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("155.4.118.2", 1883, 60)

def setsec(n): 
    return str(datetime.timedelta(seconds = n))

while True:

    if(timeit.default_timer()-set_time)>duration:
        set_time = int(timeit.default_timer())
        #sec=int(timeit.default_timer()) - int(initial_time)
        if(coffee_status=="OFF"):
            secto = "0.0 Sec"
            coffee_temperature = "0.0"
            PWcons="0.0 W"
            initial_time = timeit.default_timer()
            sec = int(timeit.default_timer()) - int(initial_time)
        else:
            sec = int(timeit.default_timer()) - int(initial_time)
            #print(sec)
            #sec=sec+1
            #print(sec)         
            secto=setsec(sec)
            PWcons=str(round((sec/3600)*900,2)) + "W"
            #print(PWcons)

        t=time.localtime()
        CurTime=time.strftime("%H : %M : %S",t)
        #print(CurTime)

        Payload = {            
                "Time" : CurTime,
                "OnTime" : secto,
                "Temp" : coffee_temperature,
                "Consumption" : PWcons,
                "Status" : coffee_status
                    }
        print(json.dumps(Payload))
        client.publish("G6", json.dumps(Payload))
    client.loop()
#client.loop_forever()










  





