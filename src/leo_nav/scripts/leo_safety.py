#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import Bool
import tkinter as tk
import os
from threading import Thread


ARMED = False


running = True




class Application(tk.Frame):
	
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.master.geometry("400x100")
		self.pack()
		self.create_widgets()
		self.master.title("Mode manager")

	def create_widgets(self):

		self.arm = tk.Button(self)
		self.arm["text"] = "Start"
		self.arm["command"] = self.armed
		self.arm.pack(fill = "both", expand = True)

		self.unarm = tk.Button(self)
		self.unarm["text"] = "Pause"
		self.unarm["command"] = self.unarmed
		self.unarm.pack(fill = "both", expand = True)





	def armed(self):
		global ARMED
		self.arm.configure(bg="green")
		self.unarm.configure(bg="white")

		ARMED = False
		print("Current State: ARMED" + str(ARMED))

	def unarmed(self):
		global ARMED
		self.arm.configure(bg="white")
		self.unarm.configure(bg="red")
		ARMED = True

		print("Current State: ARMED" + str(ARMED))









if __name__ == '__main__':
	
	root = tk.Tk()
	app = Application(master=root)

	try:
		rospy.init_node('safety')
		pub = rospy.Publisher('arm_state', Bool, queue_size=10)

		rate = rospy.Rate(50) # 10hz
		while not rospy.is_shutdown() and running:
			rospy.loginfo(ARMED)
			pub.publish(ARMED)
			app.update_idletasks()
			app.update()
			rate.sleep()
	except rospy.ROSInterruptException or KeyboardInterrupt:
		pass



