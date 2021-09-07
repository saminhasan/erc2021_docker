#!/usr/bin/env python

import rospy
import time
from std_msgs.msg import Bool
PAUSED = False

def main():
	global PAUSED
	rospy.init_node('safety')
	pub = rospy.Publisher('arm_state', Bool, queue_size=10)
	while True:
		data = raw_input("PAUSED:" + str(PAUSED))
		PAUSED = not PAUSED
		rospy.loginfo(PAUSED)
		for i in range(5):
			pub.publish(PAUSED)
if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException or KeyboardInterrupt:
		exit()
