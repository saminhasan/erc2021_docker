#!/usr/bin/env python
import rospy

from geometry_msgs.msg import Vector3Stamped, PoseStamped, PoseWithCovarianceStamped


rospy.init_node("pose_msg")


pose_pub = rospy.Publisher("wheel_pose_with_covariance", PoseWithCovarianceStamped, queue_size=5)

pose_msg = PoseWithCovarianceStamped()

wheel_pose_cov = rospy.get_param("~wheel_pose_covariance_diagonal")


for i in range(6):
    pose_msg.pose.covariance[i*6] = wheel_pose_cov[i] 







def pose_callback(pose):
    pose_msg.header.stamp = pose.header.stamp
    pose_msg.pose.pose = pose.pose
    pose_pub.publish(pose_msg)




pose_sub = rospy.Subscriber("wheel_pose", PoseStamped, pose_callback)



rospy.spin()
