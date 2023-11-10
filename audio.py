import paho.mqtt.client as paho
import json
import os
import streamlit as st
import time
import glob
import numpy as np
import pytesseract
from PIL import Image
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from gtts import gTTS
values = 0.0
act1="OFF"
act2="Cerrao"
text=""

st.markdown('<style>' + open('estilo.css').read() + '</style>', unsafe_allow_html=True)

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)
    
st.title("Bienvenido a tu casa inteligente")

image = Image.open('smartHouse.png')
st.image(image,caption='Tu casa inteligente',width=200)

if 5==5:
        
        stt_button = Button(label=" Inicio ", width=200)
        st.write("Da una instrucción")
        
        stt_button.js_on_event("button_click", CustomJS(code="""
            var recognition = new webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
         
            recognition.onresult = function (e) {
                var value = "";
                for (var i = e.resultIndex; i < e.results.length; ++i) {
                    if (e.results[i].isFinal) {
                        value += e.results[i][0].transcript;
                    }
                }
                if ( value != "") {
                    document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
                }
            }
            recognition.start();
            """))
        
        result = streamlit_bokeh_events(
            stt_button,
            events="GET_TEXT",
            key="listen",
            refresh_on_update=False,
            override_height=75,
            debounce_time=0)
        
        if result:
            if "GET_TEXT" in result:
                st.write(result.get("GET_TEXT"))
            try:
                os.mkdir("temp")
            except:
                pass
            st.title("Texto a Audio")            
            text = str(result.get("GET_TEXT"))
            text = text.lower()
            print(text)

broker="157.230.214.127"
port=1883
client1= paho.Client("ESTE_ES_MAURI2")
client1.on_message = on_message





if text=="encender":
    act1="Encendido"
    client1= paho.Client("ESTE_ES_MAURI2")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client1.publish("mauri1", message)
    st.write("Se han encendido las luces")
    image = Image.open('bombillo.png')
    st.image(image,caption=' ',width=200)
    #client1.subscribe("Sensores")
    
    
else:
    st.write('')

if text=="apagar":
    act1="Apagado"
    client1= paho.Client("ESTE_ES_MAURI2")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client1.publish("mauri1", message)
    st.write("Se han apagado las luces")
    image = Image.open('bombillo.png')
    st.image(image,caption=' ',width=200)
  
    
else:
    st.write('')



if text=="abrir":
    act2="Abrido"
    client1= paho.Client("ESTE_ES_MAURI2")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)   
    message =json.dumps({"Act2": act2})
    ret= client1.publish("mauri1", message)
    st.write("Se ha abierto la puerta")
    image = Image.open('puerta.png')
    st.image(image,caption=' ',width=200)
    
 
else:
    st.write('')

if text=="cerrar":
    act2="Cerrao"
    client1= paho.Client("ESTE_ES_MAURI2")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)   
    message =json.dumps({"Act2": act2})
    ret= client1.publish("mauri1", message)
    st.write("Se ha cerrado la puerta")
    image = Image.open('puerta.png')
    st.image(image,caption=' ',width=200)
    
 
else:
    st.write('')
