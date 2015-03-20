import os
import pipes
import SimpleHTTPServer
import SocketServer
import subprocess
import sys
import urllib
import urlparse

import pyev3

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_POST(self):
		mname = "action_" + self.path[1:]
		if not hasattr(self, mname):
			return self.send_response(404)
		method = getattr(self, mname)
		
		if "content-type" not in self.headers:
			return self.send_response(415) # Unsupported Media Type
		
		required_ctype = "application/x-www-form-urlencoded"
		if required_ctype not in self.headers["content-type"]:
			return self.send_response(415) # Unsupported Media Type
		
		if "content-length" not in self.headers:
			return self.send_response(411) # Length Required
		
		try:
			clength = int(self.headers["content-length"])
		except ValueError:
			return self.send_response(400) # Bad Request
		
		form_data = self.rfile.read(clength)
		
		# Similar to parse_qs, but only gives 1 value per key
		query = dict(urlparse.parse_qsl(form_data, keep_blank_values=True))
		
		print query
		
		try:
			response = method(**query)
		except: # Naughty, I know
			return self.send_response(500) # Internal Server Error
		
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(response)
	
	def action_speak(self, text):
		command = "espeak -a 200 -s 80 --stdout {} | aplay".format(pipes.quote(text))
		subprocess.Popen(command, shell=True)
	
	def action_move(self, kind="move", speed="20", direction="forward", amount="10"):
		global motors
		
		amount = int(amount) # Exceptions get handled in move caller
		
		if amount == 0:
			raise Exception("Invalid amount 0")
		if motors.left_motor.run or motors.right_motor.run:
			raise Exception("Robot already in motion")
		
		motors.pulses_per_second_sp = speed
		motors.position = 0
		if kind == "move":
			if direction == "forward":
				motors.position_sp = amount
			elif direction == "backward":
				motors.position_sp = -amount
			else:
				raise Exception("Unknown direction {}".format(direction))
		elif kind == "pivot":
			if direction == "left":
				motors.left_motor.position_sp = 0
				motors.right_motor.position_sp = amount
			elif direction == "right":
				motors.left_motor.position_sp = amount
				motors.right_motor.position_sp = 0
			else:
				raise Exception("Unknown direction {}".format(direction))
		elif kind == "spin":
			if direction == "left":
				motors.right_motor.position_sp = amount
				motors.left_motor.position_sp = -amount
			elif direction == "right":
				motors.right_motor.position_sp = -amount
				motors.left_motor.position_sp = amount
			else:
				raise Exception("Unknown direction {}".format(direction))
		elif kind == "wave":
			motors.position_sp = 0
			arm.position_sp = -45
			arm.run = 1
			while arm.run:
				pass
			arm.position_sp = 45
			arm.run = 1
			while arm.run:
				pass
			arm.position_sp = 0
			arm.run = 1
		else:
			raise Exception("Unknown movement type {}".format(kind))
		
		motors.run = 1

class Motors(object):
	def __init__(self, left_motor_port, right_motor_port):
		object.__setattr__(self, 'left_motor', pyev3.Motor(left_motor_port))
		object.__setattr__(self, 'right_motor', pyev3.Motor(right_motor_port))
	
	def __getattr__(self, attr):
		return self.left_motor.__getattr__(attr)
	
	def __setattr__(self, attr, value):
		self.left_motor.__setattr__(attr, value)
		self.right_motor.__setattr__(attr, value)
	
	def are_running(self):
		return self.left_motor.run or self.right_motor.run
	
	def reset(self):
		self.left_motor.reset()
		self.right_motor.reset()

motors = Motors(pyev3.OUTPUT_B, pyev3.OUTPUT_C)

motors.reset()
motors.run_mode = "position"
motors.regulation_mode = "on"
motors.pulses_per_second_sp = 0

arm = pyev3.Motor(pyev3.OUTPUT_A)
arm.reset()
arm.run_mode = "position"
arm.regulation_mode = "on"
arm.position = 0
arm.position_sp = 0
arm.pulses_per_second_sp = 180
arm.stop_mode = 'hold'

PORT = 8081

os.chdir("./www/root")

SocketServer.TCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(("", PORT), MyHandler)
try:
	httpd.serve_forever()
finally:
	motors.run = 0