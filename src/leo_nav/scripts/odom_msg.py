#!/usr/bin/env python
import rospy

from geometry_msgs.msg import Vector3Stamped, TwistStamped, TwistWithCovarianceStamped


rospy.init_node("odom_msg")


odom_pub = rospy.Publisher("wheel_odom_with_covariance", TwistWithCovarianceStamped, queue_size=5)

odom_msg = TwistWithCovarianceStamped()

wheel_odom_cov = rospy.get_param("~wheel_odom_covariance_diagonal")


for i in range(6):
    odom_msg.twist.covariance[i*6] = wheel_odom_cov[i]







def odom_callback(odom):
    odom_msg.header.stamp = odom.header.stamp
    odom_msg.twist.twist = odom.twist
    odom_pub.publish(odom_msg)




odom_sub = rospy.Subscriber("wheel_odom", TwistStamped, odom_callback)



rospy.spin()
