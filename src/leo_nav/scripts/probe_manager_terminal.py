#!/usr/bin/env python

import rospy
import time
from std_msgs.msg import String, UInt8, Empty

number_of_probe_deployed = 0
def callback(data):
	global number_of_probe_deployed
	number_of_probe_deployed = data.data
	print("Number_of_probe_deployed:", number_of_probe_deployed)

def main():
	global number_of_probe_deployed

	rospy.init_node('probing', anonymous=True)
	rospy.Subscriber("probe_deployment_unit/probes_dropped", UInt8, callback)
	pub = rospy.Publisher('probe_deployment_unit/drop', Empty, queue_size=10)
	while True:
		data = raw_input("Press Enter to deploy a probe:")
		msg =Empty()
		pub.publish(msg)
		time.sleep(1)

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException or KeyboardInterrupt:
		exit()
