
class Motor:

	# lrv_pct_vel (Low Range Value)
	# urv_pct_vel (Upper Range Value)
	# srv_pct_vel (Scale Range Value)

	def __init__(self):
		self.lrv_pct_vel = 0.0
		self.urv_pct_vel = 100.0
		self.srv_pct_vel = 0.0

	def update_config(self, lrv_pct_vel, urv_pct_vel):
		self.lrv_pct_vel = lrv_pct_vel
		self.urv_pct_vel = urv_pct_vel

	def scale(self, pct_vel):
		self.srv_pct_vel = (pct_vel * ((self.urv_pct_vel - self.lrv_pct_vel) / 100)) + self.lrv_pct_vel
		return self.srv_pct_vel

	def test(self):
		delta = self.urv_pct_vel - self.lrv_pct_vel
		d_delta = delta / 100
		m_delta = pct_vel * d_delta
		a_delta = m_delta + self.lrv_pct_vel

		print(pct_vel)
		print(delta)
		print(d_delta)
		print(m_delta)
		print(a_delta)

