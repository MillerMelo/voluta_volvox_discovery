
import time
import motor_wheel
from ws2812 import WS2812
from pyb import Pin, Timer, ExtInt, ADCAll


#out_m5_cw = Pin('PA5', Pin.OUT_PP)

# 12 bit resolution, internal channels On
adcall = ADCAll(12, 0x70000) 
neo_pixel = WS2812(spi_bus=2, intensity=0.1)


in_btn_play 	= Pin('PB12', Pin.IN)
in_btn_home 	= Pin('PB13', Pin.IN)
in_btn_pos_0 	= Pin('PB14', Pin.IN)
in_home_x 		= Pin('PC6', Pin.IN)
in_home_y 		= Pin('PC7', Pin.IN)
in_home_z 		= Pin('PB8', Pin.IN)

out_dir_x 		= Pin('PE1', Pin.OUT_PP)
out_dir_y 		= Pin('PE2', Pin.OUT_PP)
out_dir_z 		= Pin('PE3', Pin.OUT_PP)
out_enable_x	= Pin('PE4', Pin.OUT_PP)
out_enable_y	= Pin('PE5', Pin.OUT_PP)
out_enable_z	= Pin('PE6', Pin.OUT_PP)


#Scale Range Value Velocity Motors
conf_fl_srv_vel = (15.0, 85.0, 14.0, 81.0)
conf_fr_srv_vel = (15.0, 85.0, 14.0, 81.0)
conf_bl_srv_vel = (15.0, 85.0, 14.0, 81.0)
conf_br_srv_vel = (15.0, 85.0, 14.0, 81.0)


adc_temp = 0.0
adc_vbatt = 0.0
upd_leds = False
led_direction_r = False
led_direction_l = False
led_id = 0
led_state = 0
led_state_acc_on = 0
led_state_acc_off = 0





#timer_2 = Timer(2, freq=1000)
#pot_value = int(pot_pin_adc.read())

def move(pct_vel, direction=0):

	if direction = 0:
		motor_fl.run_scale(pct_vel)
		motor_fr.run_scale(pct_vel)
		motor_bl.run_scale(pct_vel)
		motor_br.run_scale(pct_vel)
	

def update_states():
	global adc_temp, adc_vbatt, led_state
	adc_temp = adcall.read_core_temp()
	adc_vbatt = adcall.read_core_vbat()
	#print("%.2f V %.2f °C" %(adc_vbatt, adc_temp))
	
	if adc_vbatt < 3.3:
		led_state = 2
	elif adc_temp > 40.0:
		led_state = 3



def update_leds(timer):
	global upd_leds, led_direction_r, led_direction_l, led_state, led_state_acc_on, led_state_acc_off
	
	if upd_leds:
		upd_leds = False
		neo_pixel.id = led_id

		#Switching led direction right
		if led_direction_r:
			neo_pixel.direction_r = not neo_pixel.direction_r
		else:
			neo_pixel.direction_r = False
		
		#Switching led direction left
		if led_direction_l:
			neo_pixel.direction_l = not neo_pixel.direction_l
		else:
			neo_pixel.direction_l = False

		#Switching led state indicate the number of fault
		if led_state > 0:

			if led_state_acc_on < led_state:
				if neo_pixel.state != 5:
					neo_pixel.state = 5
					led_state_acc_on += 1
				else:
					neo_pixel.state = 0
			else:
				neo_pixel.state = 0
				led_state_acc_off +=1

			if led_state_acc_off > 9:
				led_state_acc_on = 0
				led_state_acc_off = 0
		else:
			neo_pixel.state = 0
			led_state_acc_on = 0
			led_state_acc_off = 0
			

		



#Config Hardware Motor Front Left
motor_fl = motor_wheel.MotorWheel('PA0', 5, 1, 'PB6', 4, 1)	
motor_fl.update_config(conf_fl_srv_vel)

#Config Hardware Motor Front Right
motor_fr = motor_wheel.MotorWheel('PA1', 5, 2, 'PB7', 4, 2)	
motor_fr.update_config(conf_fr_srv_vel)

#Config Hardware Motor Back Left
motor_bl = motor_wheel.MotorWheel('PA2', 5, 3, 'PB8', 4, 3)	
motor_bl.update_config(conf_bl_srv_vel)

#Config Hardware Motor Back Right
motor_br = motor_wheel.MotorWheel('PA3', 5, 4, 'PB9', 4, 4)	
motor_br.update_config(conf_br_srv_vel)


timer_9 = Timer(9, freq=5)
timer_9.callback(update_leds)






while True:

	update_states()
	
	if not upd_leds:
		neo_pixel.show()
		upd_leds = True

	#if go_forward and not in_move:









	'''
	neo_pixel.headlights = True
	neo_pixel.stops = False
	#neo_pixel.show()
	

	for vel_temp in range (0, 100, 1):
		move(vel_temp)
		time.sleep_ms(10)

	for vel_temp in range (100, 0, -1):
		move(vel_temp)
		time.sleep_ms(10)

	neo_pixel.headlights = False
	neo_pixel.stops = True
	#neo_pixel.show()

	move(0)
	time.sleep(2)

	neo_pixel.headlights = True
	neo_pixel.stops = False
	#neo_pixel.show()

	for vel_temp in range (0, -100, -1):
		move(vel_temp)
		time.sleep_ms(10)

	for vel_temp in range (-100, 0, 1):
		move(vel_temp)
		time.sleep_ms(10)

	neo_pixel.headlights = False
	neo_pixel.stops = True
	#neo_pixel.show()

	move(0)
	time.sleep(2)
	'''
	
