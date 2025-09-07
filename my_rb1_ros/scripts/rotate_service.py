#! /usr/bin/env python

import rospy
import math
from my_rb1_ros.srv import Rotate, RotateResponse
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion

class RotateRB1Service():
    
    def __init__(self):
        self.world_yaw = 0.0
        self.rb1_odom_subscriber = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.rb1_vel_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.service = rospy.Service('/rotate_robot', Rotate, self.rotate_callback)
        self.ctrl_c = False
        self.rotate_speed = 0.5 # 0.5 radians/sec
        self.cmd = Twist()
        self.rate = rospy.Rate(10) # 10Hz
        rospy.on_shutdown(self.shutdownhook)
    
    def odom_callback(self, odom_msg):
        quaternion = odom_msg.pose.pose.orientation
        _, _, yaw = euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
        self.world_yaw = yaw

    def rotate_callback(self, request):
        rospy.loginfo("Service Requested")
        initial_yaw = self.world_yaw
        turn_degrees = request.degrees
        turn_radians = math.radians(turn_degrees)
        new_world_yaw = self._normalize_angle(initial_yaw + turn_radians) # shortest path [-pi, pi]

        rospy.logdebug(f"Turn rb1 robot {turn_degrees} degrees.")
        rospy.logdebug(f"Current yaw {initial_yaw}, new yaw {new_world_yaw}")
        error = self._normalize_angle(new_world_yaw - self.world_yaw)
        rospy.logdebug(f"Error {error}")
        while abs(error) > 0.01 and not rospy.is_shutdown():
            # define the new angular velocity in short direction
            self.cmd.angular.z = self.rotate_speed * math.copysign(1, error)
            self.publish_once_in_cmd_vel()
            rospy.logdebug("%.3f, %.3f", self.world_yaw, new_world_yaw)
            self.rate.sleep()
            error = self._normalize_angle(new_world_yaw - self.world_yaw)
        
        # stop turning robot
        self.stop_rb1()
        rospy.logdebug(f"New yaw {self.world_yaw}.")

        rospy.loginfo("Service Completed")
        return RotateResponse(result=f"Robot successfully turned.")
    
    def publish_once_in_cmd_vel(self):
        """
        This is because publishing in topics sometimes fails the first time you publish.
        In continuous publishing systems there is no big deal but in systems that publish only
        once it IS very important.
        """
        while not self.ctrl_c:
            connections = self.rb1_vel_publisher.get_num_connections()
            if connections > 0:
                self.rb1_vel_publisher.publish(self.cmd)
                break
            else:
                self.rate.sleep()
    
    def stop_rb1(self):
        rospy.loginfo("Stop the robot")
        self.cmd.linear.x = 0.0
        self.cmd.angular.z = 0.0
        self.publish_once_in_cmd_vel()
        
    def shutdownhook(self):
        # works better than the rospy.is_shutdown()
        self.stop_rb1()
        self.ctrl_c = True
    
    def _normalize_angle(self, angle):
        return math.atan2(math.sin(angle), math.cos(angle))  # Equivalent to (angle + pi) % (2*pi) - pi
        # angle = angle % (2 * math.pi)  # Wrap to [0, 2π)
        # if angle > math.pi:
        #     angle -= 2 * math.pi  # Shift to [-π, π]
        # return angle
            
if __name__ == '__main__':
    rospy.init_node('rotate_service_server', anonymous=True, log_level=rospy.DEBUG)
    rotate_service = RotateRB1Service()
    rospy.loginfo("Service Ready")
    rospy.spin()