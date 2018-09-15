import pyb
import time
from pyb import Pin, Timer, ExtInt


out_m1_cw = Pin('PA0', Pin.OUT_PP)
out_m2_cw = Pin('PA1', Pin.OUT_PP)
out_m3_cw = Pin('PA2', Pin.OUT_PP)
out_m4_cw = Pin('PA3', Pin.OUT_PP)
out_m5_cw = Pin('PA5', Pin.OUT_PP)
out_m1_ccw = Pin('PB6', Pin.OUT_PP)
out_m2_ccw = Pin('PB7', Pin.OUT_PP)
out_m3_ccw = Pin('PB8', Pin.OUT_PP)
out_m4_ccw = Pin('PB9', Pin.OUT_PP)


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


vel_pct = 0


def update_vel(vel):
	
	vel_pct_cw = (abs(vel*-1)-(vel*-1))/2
	vel_pct_ccw = (abs(vel)-vel)/2

	pwm_m1_cw.pulse_width_percent(vel_pct_cw)
	pwm_m1_ccw.pulse_width_percent(vel_pct_ccw)

	print("Avance = %d Retorno = %d" %(vel_pct_cw, vel_pct_ccw))





#timer_2 = Timer(2, freq=1000)
timer_4 = Timer(4, freq=1000)
timer_5 = Timer(5, freq=1000)


pwm_m1_cw = timer_5.channel(1, Timer.PWM, pin=out_m1_cw)
pwm_m2_cw = timer_5.channel(2, Timer.PWM, pin=out_m2_cw)
pwm_m3_cw = timer_5.channel(3, Timer.PWM, pin=out_m3_cw)
pwm_m4_cw = timer_5.channel(4, Timer.PWM, pin=out_m4_cw)
pwm_m1_ccw = timer_4.channel(1, Timer.PWM, pin=out_m1_ccw)
pwm_m2_ccw = timer_4.channel(2, Timer.PWM, pin=out_m2_ccw)
pwm_m3_ccw = timer_4.channel(3, Timer.PWM, pin=out_m3_ccw)
pwm_m4_ccw = timer_4.channel(4, Timer.PWM, pin=out_m4_ccw)


while True:

	for vel_pct in range (0, 100):
		update_vel(vel_pct)
		#time.sleep_ms(100)
		time.sleep(1)

	for vel_pct in range (99, -100):
		update_vel(vel_pct)
		#time.sleep_ms(100)
		time.sleep(1)

	for vel_pct in range (-99, -1):
		update_vel(vel_pct)
		#time.sleep_ms(100)
		time.sleep(1)

