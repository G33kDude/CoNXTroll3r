import math

def int_in_range(num, min=None, max=None):
	try:
		num = int(num)
	except ValueError:
		raise Exception("must be integer")
	
	if type(min) is int and num < min:
		raise Exception("below lower bound {0}".format(min))
	if type(max) is int and num > max:
		raise Exception("above upper bound {0}".format(max))
	
	return num

def float_in_range(num, min=None, max=None):
	try:
		num = float(num)
	except ValueError:
		raise Exception("must be number")
	
	if type(min) in (int,float) and num < min:
		raise Exception("below lower bound {0}".format(min))
	if type(max) in (int,float) and num > max:
		raise Exception("above upper bound {0}".format(max))
	
	return num

class Wrapper:
	def __init__(self, robot, left, right, diameter, track):
		self.robot = robot
		self.wheels = Wheels(left, right, diameter, track)
	
	def step_sync(self, speed, turn, degrees):
		try:
			speed = int_in_range(speed, -100, 100)
		except Exception as e:
			raise Exception("Speed {0}".format(e))
		
		try:
			degrees = int_in_range(degrees, None, None)
		except Exception as e:
			raise Exception("Distance {0}".format(e))
		if degrees < 0:
			degrees *= -1
			speed *= -1
		
		try:
			turn = int_in_range(turn, -200, 200)
		except Exception as e:
			raise Exception("Turn {0}".format(e))
		if self.wheels.invert:
			turn *= 1
		
		self.robot.motordevice.step_sync(self.wheels.ports, speed, turn, degrees, 1)
	
	def move(self, speed, amount=0, in_units=True):
		if in_units:
			amount = float_in_range(amount) * 360.0/self.wheels.circumference
		self.step_sync(speed, 0, amount)
	
	def pivot(self, speed, amount, direction):
		if direction == "right":
			turn = 100
		elif direction == "left":
			turn = -100
		else:
			raise Exception("Invalid direction {0}".format(direction))
		
		self.step_sync(speed, turn, int_in_range(amount) * self.wheels.track/self.wheels.radius)
	
	def spin(self, speed, amount, direction):
		if direction == "right":
			turn = 200
		elif direction == "left":
			turn = -200
		else:
			raise Exception("Invalid direction {0}".format(direction))
		
		self.step_sync(speed, turn, int_in_range(amount) * self.wheels.track/self.wheels.diameter)

class Wheels:
	def __init__(self, left, right, diameter, track):
		self.ports = left | right
		self.invert = left < right
		self.diameter = diameter * 1.0
		self.radius = diameter / 2.0
		self.track = track * 1.0
		self.circumference = diameter * math.pi