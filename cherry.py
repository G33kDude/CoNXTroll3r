print "importing os"
import os

print "importing cherrypy"
import cherrypy

print "importing ev3"
from ev3 import robot
print "importing wrapper"
from wrapper import Wrapper

print "done importing"

class Root:
	def __init__(self, robot):
		self.robot = robot
		with open(os.path.join(_template_dir, "index.htm"), "r") as f:
			self.index_template = f.read().format(move_speed=30, move_degrees=90, move_distance=robot.wheels.track)
		print "Website initialized"
	
	@cherrypy.expose
	def index(self):
		return self.index_template
	
	@cherrypy.expose
	def move(self, kind="move", speed="20", direction="forward", amount="10"):
		if amount == "0":
			raise Exception("Invalid amount 0")
		if kind == "move":
			if direction == "forward":
				self.robot.move(speed, amount)
			elif direction == "backward":
				self.robot.move(speed, "-" + amount)
			else:
				raise Exception("Unkown direction {0}".format(direction))
		elif kind == "pivot":
			self.robot.pivot(speed, amount, direction)
		elif kind == "spin":
			self.robot.spin(speed, amount, direction)
		else:
			raise Exception("Unkown movement type {0}".format(kind))

_root_dir = os.path.join(os.getcwd(), "www")
_static_dir = os.path.join(_root_dir, "root")
_template_dir = os.path.join(_root_dir, "templates")

print "opening"
robot.open_all_devices()

try:
	cherrypy.config.update({
		'server.socket_host': '0.0.0.0',
		'server.socket_port': 80,
		'engine.autoreload.on': False
	})
	cherrypy.tree.mount(Root(Wrapper(robot, robot.MOTOR_B_BIT, robot.MOTOR_C_BIT, 5.6, 17)), "/", {
		'/': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': _static_dir
		}
	})
	cherrypy.engine.start()
	cherrypy.engine.block()
finally:
	print "closing"
	robot.close_all_devices()