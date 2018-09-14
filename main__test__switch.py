import pyb

in_c6_flanco = False
acu_in_c6 = 0

out_a0 = pyb.Pin('PA0', pyb.Pin.OUT_PP)

def irq_in_c6(line):
	global acu_in_c6, in_c6_flanco
	if in_c6_flanco == False:
		acu_in_c6 +=1
		in_c6_flanco = True
		print(acu_in_c6)
		tim.callback(t_on)
		out_a0.on()

def t_on(timer):
	global in_c6_flanco
	in_c6_flanco = False
	tim.deinit()
	print(in_c6_flanco)
	out_a0.off()

tim = pyb.Timer(8, freq=10)
tim.init(freq=1)
in_c6 = pyb.Pin('PC6', pyb.Pin.IN)
extint = pyb.ExtInt(in_c6, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_UP,irq_in_c6)

