#!/usr/bin/env python
# license removed for brevity
__author__ = 'fiorellasibona'
import rospy
import math
import yaml
import time
import actionlib
import tf_conversions
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion
from tf.transformations import quaternion_from_euler


class MoveBaseSeq():

	def __init__(self):
		rospy.init_node('move_base_sequence')
		## Load tag_info parameters from yaml file
		# Get a parameter from our private namespace
		param_path = rospy.get_param("~wp_poses_param_path")
		rospy.loginfo("Waypoint poses : %s", param_path)
		f = open(param_path, 'r')
		params_raw = f.read()
		f.close()

		params = yaml.load(params_raw)
		# Dictionary with tag poses: [x, y, z, Roll, Pitch, Yaw]
		wp_info = params['wp_info'] 
		rospy.loginfo("Tag info dict: %s", wp_info)

		self.pose_seq = list()
		self.goal_cnt = 0

  		for tag_id, tf_data in wp_info.iteritems():
			p = Pose()

			p.position.x =  tf_data[0]
			p.position.y =  tf_data[1]
			p.position.z =  tf_data[2]
			q = tf_conversions.transformations.quaternion_from_euler(tf_data[3], tf_data[4], tf_data[5])
			p.orientation.x = q[0]
			p.orientation.y = q[1]
			p.orientation.z = q[2]
			p.orientation.w = q[3]
			self.pose_seq.append(p)
		time.sleep(5)
		#Create action client
		self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
		time.sleep(5)
		rospy.loginfo("Waiting for move_base action server...")
		time.sleep(5)
		wait = self.client.wait_for_server(rospy.Duration(10.0))
		time.sleep(5)
		if not wait:
			rospy.logerr("Action server not available!")
			rospy.signal_shutdown("Action server not available!")
			return
		rospy.loginfo("Connected to move base server")
		rospy.loginfo("Starting goals achievements ...")
		self.movebase_client()

	def active_cb(self):
		rospy.loginfo("Goal pose "+str(self.goal_cnt+1)+" is now being processed by the Action Server...")

	def feedback_cb(self, feedback):
		#To print current pose at each feedback:
		#rospy.loginfo("Feedback for goal "+str(self.goal_cnt)+": "+str(feedback))
		rospy.loginfo("Feedback for goal pose "+str(self.goal_cnt+1)+" received")

	def done_cb(self, status, result):
		self.goal_cnt += 1
		# Reference for terminal status values: http://docs.ros.org/diamondback/api/actionlib_msgs/html/msg/GoalStatus.html
		if status == 2:
			rospy.loginfo("Goal pose "+str(self.goal_cnt)+" received a cancel request after it started executing, completed execution!")

		if status == 3:
			rospy.loginfo("Goal pose "+str(self.goal_cnt)+" reached") 
		if self.goal_cnt< len(self.pose_seq):
			next_goal = MoveBaseGoal()
			next_goal.target_pose.header.frame_id = "map"
			next_goal.target_pose.header.stamp = rospy.Time.now()
			next_goal.target_pose.pose = self.pose_seq[self.goal_cnt]
			rospy.loginfo("Sending goal pose "+str(self.goal_cnt+1)+" to Action Server")
			rospy.loginfo(str(self.pose_seq[self.goal_cnt]))
			self.client.send_goal(next_goal, self.done_cb, self.active_cb, self.feedback_cb) 
		else:
			rospy.loginfo("Final goal pose reached!")
			rospy.signal_shutdown("Final goal pose reached!")
			return

		if status == 4:
			rospy.loginfo("Goal pose "+str(self.goal_cnt)+" was aborted by the Action Server")
			rospy.signal_shutdown("Goal pose "+str(self.goal_cnt)+" aborted, shutting down!")
			return

		if status == 5:
			rospy.loginfo("Goal pose "+str(self.goal_cnt)+" has been rejected by the Action Server")
			rospy.signal_shutdown("Goal pose "+str(self.goal_cnt)+" rejected, shutting down!")
			return

		if status == 8:
			rospy.loginfo("Goal pose "+str(self.goal_cnt)+" received a cancel request before it started executing, successfully cancelled!")
	
	def movebase_client(self):
		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now() 
		goal.target_pose.pose = self.pose_seq[self.goal_cnt]
		rospy.loginfo("Sending goal pose "+str(self.goal_cnt+1)+" to Action Server")
		rospy.loginfo(str(self.pose_seq[self.goal_cnt]))
		self.client.send_goal(goal, self.done_cb, self.active_cb, self.feedback_cb)
		rospy.spin()




if __name__ == '__main__':
	try:
		MoveBaseSeq()

	except rospy.ROSInterruptException:
		rospy.loginfo("Navigation finished.")
