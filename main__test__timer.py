from pyb import Pin, Timer

p = Pin('PA0')

acu_pulso = 0

def tick(timer):
	global acu_pulso
	acu_pulso += 1


tim = Timer(2, freq=400)
ch = tim.channel(1, Timer.PWM, pin=p)
ch.pulse_width_percent(50)
tim.callback(tick)
