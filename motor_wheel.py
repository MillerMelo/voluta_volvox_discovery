import pyb
import time
from pyb import Pin, Timer, ExtInt

class MotorWheel:

	# lrv_pct_vel (Low Range Value)
	# urv_pct_vel (Upper Range Value)
	# srv_pct_vel (Scale Range Value)

	def __init__(self, pin_cw, timer_cw, channel_cw, pin_ccw, timer_ccw, channel_ccw):
		out_cw = Pin(pin_cw, Pin.OUT_PP)
		out_ccw = Pin(pin_ccw, Pin.OUT_PP)

		self.t_conf_cw = Timer(timer_cw, freq=1000)
		self.t_conf_ccw = Timer(timer_ccw, freq=1000)
		self.pwm_cw = self.t_conf_cw.channel(channel_cw, Timer.PWM, pin=out_cw)
		self.pwm_ccw = self.t_conf_ccw.channel(channel_ccw, Timer.PWM, pin=out_ccw)
	
		self.lrv_pct_vel_cw = 0.0
		self.urv_pct_vel_cw = 100.0
		self.srv_pct_vel_cw = 0.0
		self.lrv_pct_vel_ccw = 0.0
		self.urv_pct_vel_ccw = 100.0
		self.srv_pct_vel_ccw = 0.0

	def update_config(self, conf_srv_vel):
		self.lrv_pct_vel_cw = conf_srv_vel[0]
		self.urv_pct_vel_cw = conf_srv_vel[1]
		self.lrv_pct_vel_ccw = conf_srv_vel[2]
		self.urv_pct_vel_ccw = conf_srv_vel[3]

	def run_scale(self, pct_vel):
		vel_pct_cw = (abs(pct_vel*-1)-(pct_vel*-1))/2
		vel_pct_ccw = (abs(pct_vel)-pct_vel)/2
		
		if vel_pct_cw > 0:
			self.srv_pct_vel_cw = (vel_pct_cw * ((self.urv_pct_vel_cw - self.lrv_pct_vel_cw) / 100)) + self.lrv_pct_vel_cw
		else:
			self.srv_pct_vel_cw = 0

		if vel_pct_ccw > 0:
			self.srv_pct_vel_ccw = (vel_pct_ccw * ((self.urv_pct_vel_ccw - self.lrv_pct_vel_ccw) / 100)) + self.lrv_pct_vel_ccw
		else:
			self.srv_pct_vel_ccw = 0

		self.pwm_cw.pulse_width_percent(self.srv_pct_vel_cw)
		self.pwm_ccw.pulse_width_percent(self.srv_pct_vel_ccw)

		#print(pct_vel)
		#print("Avance = %.2f Retorno = %.2f" %(self.srv_pct_vel_cw, self.srv_pct_vel_ccw))
		return self.srv_pct_vel_cw, self.srv_pct_vel_ccw

