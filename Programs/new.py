import mindwave, time, subprocess


import RPi.GPIO as gpio

 
def init():
 gpio.setmode(gpio.BCM)
 gpio.setup(17, gpio.OUT)
 gpio.setup(22, gpio.OUT)
 gpio.setup(23, gpio.OUT)
 gpio.setup(24, gpio.OUT)
 
def reverse(tf):
 init()
 gpio.output(17, True)
 gpio.output(22, False)
 gpio.output(23, True) 
 gpio.output(24, False)
 time.sleep(tf)
 gpio.cleanup()
 
def forward(tf):
 init()
 gpio.output(17, False)
 gpio.output(22, True)
 gpio.output(23, False) 
 gpio.output(24, True)
 time.sleep(tf)
 gpio.cleanup()
 
def right(tf):
 init()
 gpio.output(17, False)
 gpio.output(22, False)
 gpio.output(23, True) 
 gpio.output(24, False)
 time.sleep(tf)
 gpio.cleanup()

def left(tf):
 init()
 gpio.output(17, True)
 gpio.output(22, False)
 gpio.output(23, False) 
 gpio.output(24, False)
 time.sleep(tf)
 gpio.cleanup()




headset = mindwave.Headset('COM12')
time.sleep(2)

headset.connect()
print "Connecting"

while headset.status != 'connected':
  time.sleep(3)
  print"Trying to connect headset"
  if headset.status == 'standby':
    headset.connect()
    print "Retrying"

print "connected"
forward(2)
headset.blinked=0

def single_blink(headset):
  print "Single blink"
  left(2)
  headset.single_blink=False

def double_blink(headset):
  print "Double blink"
  right(2)
  headset.double_blink=False
def on_blink(headset):
  print"Blinked."
  
headset.single_blink=False
headset.double_blink=False
def checkblink(headset):
  while True:
    if headset.blinked==1 and not headset.single_blink:
      headset.single_blink=True
      mindwave.threading.Thread(target=single_blink,args=(headset,)).start()
    elif headset.blinked==2 and not headset.double_blink:
      headset.double_blink=True
      mindwave.threading.Thread(target=double_blink,args=(headset,)).start()
    headset.blinked=0    
    time.sleep(2)

blnk = mindwave.threading.Thread(target=checkblink,args=(headset,))
blnk.daemon = True
blnk.start()
    
def on_raw(headset,raw):
    if headset.poor_signal==0:
        if raw>400 and headset.listener.initial==0:
            headset.listener.initial=mindwave.datetime.datetime.now()
        elif raw<-90 and headset.listener.timer()>20 and headset.listener.timer()<300:
            print "got it"
            headset.blinked+=1
            print headset.blinked
            #mindwave.threading.Thread(target=on_blink,args=(headset,)).start()
            headset.listener.initial=0
        elif headset.listener.timer()>500:
            headset.listener.initial=0
headset.raw_value_handlers.append(on_raw)



while True:
  #print headset.raw_value
  try:
    if headset.poor_signal:
      print headset.poor_signal
   
    #print 'raw '+str(headset.raw_value)
    print "Attention: %s, Meditation: %s" % (headset.attention, headset.meditation)
    
    if headset.attention >= 50:
      print "car is moving in maximum speed...."
      forward(5)
    else:
      if headset.attention >=70:
        print "car is moving 70 miles/sec...."
      else:
        if headset.attention >=60:
          print "car is moving 60 miles/sec...."
        else:
          if headset.attention >=45:
            print "car is going to start...."
          else:
            print "Sorry Your concentration level is low...."
                  
            
    
              
    time.sleep(3)
  except KeyboardInterrupt:
    headset.disconnect()
    #GPIO.cleanup()
    #p.stop()
    break  
  
