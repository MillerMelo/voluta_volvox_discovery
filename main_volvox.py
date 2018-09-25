
import time
import motor_wheel
from neopixel import WS2812
from math import pi, exp
from pyb import Pin, Timer, ExtInt, ADCAll

#Configure Hardware
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
# 12 bit resolution, internal channels On
adcall = ADCAll(12, 0x70000) 
#Config Hardware Leds NeoPixel
neo_pixel = WS2812(spi_bus=2, intensity=0.1)
#Confir Timer Switching Leds NeoPixel
timer_9 = Timer(9, freq=5)
#Confir Timer Used in Positioning
timer_14 = Timer(14, freq=1000)

#timer_2 = Timer(2, freq=1000)
#pot_value = int(pot_pin_adc.read())

#out_m5_cw = Pin('PA5', Pin.OUT_PP)
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

#Declare Globals Variable
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#Scale Range Value Velocity Motors
conf_fl_srv_vel = (15.0, 85.0, 14.0, 81.0)
conf_fr_srv_vel = (15.0, 85.0, 14.0, 81.0)
conf_bl_srv_vel = (15.0, 85.0, 14.0, 81.0)
conf_br_srv_vel = (15.0, 85.0, 14.0, 81.0)
#Velocity Parameters
encoder_ppr = 20
motor_max_rpm = 150
wheel_diameter = 19.5
wheel_perimeter = pi * wheel_diameter
speed_max = (motor_max_rpm / 60) * wheel_perimeter #(mm*seg)
#Position Parameters
distance_sp = 200.0
distance_traveled = 0.1
time_pos_sp = 0
time_pos_used = 0
time_pos_used_mem = 0
speed_sp = 0.0
speed_temp = 0.0
#Movement Variables
go_forward = False
on_move = False
#Neopixel Variables
upd_leds = False
led_direction_r = False
led_direction_l = False
led_id = 0
led_state = 0
led_state_acc_on = 0
led_state_acc_off = 0

adc_temp = 0.0
adc_vbatt = 0.0

#Define Funtions
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#
def move_wheel(pct_vel, direction=0):
	if direction == 0:
		motor_fl.run_scale(pct_vel)
		motor_fr.run_scale(pct_vel)
		motor_bl.run_scale(pct_vel)
		motor_br.run_scale(pct_vel)
	
#
def update_states():
	global adc_temp, adc_vbatt, led_state
	adc_temp = adcall.read_core_temp()
	adc_vbatt = adcall.read_core_vbat()
	#print("%.2f V %.2f °C" %(adc_vbatt, adc_temp))
	
	if adc_vbatt < 3.3:
		led_state = 2
	elif adc_temp > 40.0:
		led_state = 3

#Update leds neopixel
def update_leds(timer):
	global upd_leds, led_direction_r, led_direction_l, led_state, led_state_acc_on, led_state_acc_off, go_forward
	
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
				go_forward = True

		else:
			neo_pixel.state = 0
			led_state_acc_on = 0
			led_state_acc_off = 0

#Update Time Used in Positioning
def time_positioning(timer):
	global time_pos_used, time_pos_used_mem, time_pos_sp, go_forward

	if go_forward:
		if time_pos_used < time_pos_sp:
			time_pos_used = time_pos_used_mem + 1
			time_pos_used_mem = time_pos_used

 #Calculate instant speed (distance(mm), speed(mm/seg))
def calculate_speed(sp_distance=0.0, sp_time=0.0, traveled_distance=0.0, used_time=0.0, acc=0.2, dacc=0.2):
	speed_instant = 0.0
	speed_uniform = 1-acc-dacc
	time_acc = sp_time * acc
	time_dacc = sp_time * dacc
	time_speed_uniform = sp_time * speed_uniform
	
	speed_average = sp_distance / (sp_time*(acc*0.5 + speed_uniform + dacc*0.5))

	distance_acc = time_acc * speed_average * 0.5
	distance_dacc = time_dacc * speed_average * 0.5
	distance_speed_uniform = time_speed_uniform * speed_average
	distance_run_dacc = distance_acc + distance_speed_uniform

	if traveled_distance < distance_run_dacc:
		scale_time = -1 * (((20 / time_acc) * used_time) - 10)
		neo_pixel.stops = False
	else:
		used_time_dacc = traveled_distance - distance_run_dacc
		scale_time = scale_time = ((20 / time_acc) * used_time_dacc) - 10
		neo_pixel.stops = True

	speed_instant = (1 / (1 + (exp(scale_time)))) * speed_average
	return speed_instant


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

#Run Timer Switching Leds NeoPixel
timer_9.callback(update_leds)
#Run Timer Update Speed
timer_14.callback(time_positioning)





while True:
	#
	update_states()
	
	#
	if not upd_leds:
		neo_pixel.show()
		upd_leds = True
		#print(speed_temp)

	#
	if go_forward:

		if not on_move:
			on_move = True
			speed_sp = 1.0
			distance_sp = 3.0
			distance_traveled = 0.0
			time_total = distance_sp / speed_sp
			time_pos_sp = int(time_total * 1000)
			time_pos_used = 0
			time_pos_used_mem = 0
			neo_pixel.headlights = True

		if distance_sp > distance_traveled:

			time_move = time_pos_used / 1000
			distance_traveled = time_move
			speed_temp = calculate_speed(sp_distance=distance_sp, sp_time=time_total, traveled_distance=distance_traveled, used_time=time_move, acc=0.25, dacc=0.25)
			move_wheel(speed_temp*60)

		else:
			move_wheel(0)
			neo_pixel.headlights = False
			neo_pixel.stops = False
			go_forward = False
			on_move = False


#time.sleep_ms(10)
#time.sleep(2)