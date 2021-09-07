#!/usr/bin/env python

import time
import tkinter as tk
import rospy
from std_msgs.msg import String, UInt8, Empty

class muffinbutton:
	def __init__(self):
		self.root = tk.Tk()
		self.label = tk.Label(self.root, fg="dark green")
		self.button = tk.Button(self.root, text='Deploy Probe', width=25, command=self.deploy_probe)
		self.data = None
		rospy.init_node('listener', anonymous=True)
		rospy.Subscriber("probe_deployment_unit/probes_dropped", UInt8, self.callback)
		self.pub = rospy.Publisher('probe_deployment_unit/drop', Empty, queue_size=10)

	def callback(self,data):

		self.data = data.data

	def title(self, str):
		self.root.title(str)

	def deploy_probe(self):
		msg =Empty()
		self.pub.publish(msg)

	def run(self):
		self.label.pack()
		self.button.pack()
		self.counter_label()
		self.root.mainloop()

	def function_to_display(self, fun):
		self.func = fun
	def count(self):
		st = self.func()
		self.label.config(text=st)
		self.label.after(100, self.count)

	def counter_label(self):
		self.counter = 0
		self.count()

	def fun(self):
		return self.data

if __name__ == "__main__":
	A = muffinbutton()
	A.title("Probe Deployment Manager") 
	A.root.geometry("400x100")
	A.function_to_display(A.fun)
	A.run()
