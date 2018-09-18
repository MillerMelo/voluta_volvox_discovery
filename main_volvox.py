import pyb
import time
from pyb import Pin, Timer, ExtInt
import motor_wheel


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

conf_fl_srv_vel = (15.0, 95.0, 14.0, 91.0)
conf_fr_srv_vel = (15.0, 95.0, 14.0, 91.0)
conf_bl_srv_vel = (15.0, 95.0, 14.0, 91.0)
conf_br_srv_vel = (15.0, 95.0, 14.0, 91.0)


#timer_2 = Timer(2, freq=1000)

def move(pct_vel):
	motor_fl.run_scale(pct_vel)
	motor_fr.run_scale(pct_vel)
	motor_bl.run_scale(pct_vel)
	motor_br.run_scale(pct_vel)

#Motor Front Left
motor_fl = motor_wheel.MotorWheel('PA0', 5, 1, 'PB6', 4, 1)	
motor_fl.update_config(conf_fl_srv_vel)

#Motor Front Right
motor_fr = motor_wheel.MotorWheel('PA1', 5, 2, 'PB7', 4, 2)	
motor_fr.update_config(conf_fr_srv_vel)

#Motor Back Left
motor_bl = motor_wheel.MotorWheel('PA2', 5, 3, 'PB8', 4, 3)	
motor_bl.update_config(conf_bl_srv_vel)

#Motor Back Right
motor_br = motor_wheel.MotorWheel('PA3', 5, 4, 'PB9', 4, 4)	
motor_br.update_config(conf_br_srv_vel)


while True:

	for vel_temp in range (0, 100, 1):
		move(vel_temp)
		time.sleep_ms(10)

	for vel_temp in range (100, 0, -1):
		move(vel_temp)
		time.sleep_ms(10)

	move(0)
	time.sleep(2)

	for vel_temp in range (0, -100, -1):
		move(vel_temp)
		time.sleep_ms(10)

	for vel_temp in range (-100, 0, 1):
		move(vel_temp)
		time.sleep_ms(10)

	move(0)
	time.sleep(2)
	