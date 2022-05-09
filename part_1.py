import cv2 
import matplotlib.pyplot as plt
import numpy as np
import rospy
from ackermann_msgs.msg import AckermannDriveStamped

# 1. Flag Detection

def get_flag_color(img):
    height = round(img.shape[0]/2)
    width = round(img.shape[1]/2)

    color = img[height, width, :]

    print(color)
    return color

def detect_flag(img, color):
    blur = cv2.GaussianBlur(img, (9, 9), cv2.BORDER_DEFAULT)
    range = 30
    max = color.copy()
    min = color.copy()
    np.putmask(max, 255-range < max, 255-range)
    np.putmask(min, range > min, range )
    max += range
    min -= range
    print(max, min)
    mask = cv2.inRange(blur, min, max) 
    edges = cv2.Canny(mask, 50, 150)
    edge = cv2.findNonZero(edges)
    # mid = (edge[:,0,0].max() + edge[:,0,0].min())/2
    mid = edge[:,0,0].mean()
    print(mid)
    plt.imshow(edges)
    plt.savefig('draw.png')


flag = cv2.imread('Flag.png')
cam = cv2.imread('CaptureTheFlag.png')

color = get_flag_color(flag)
detect_flag(cam, color)

# 2. Controller
# TODO: Compute steering_angle based on the position of the flag in each frame
# Update the values with change_vals() and they will be published every 2 seconds

max_speed = 1
max_steering = 1.03

# 3. Message Publishing
steering_angle = 0
steering_angle_velocity = 0
speed = 0
acceleration = 0

def change_vals(SA, SAV, S, A):
    global steering_angle 
    global steering_angle_velocity
    global speed
    global acceleration
    
    steering_angle = SA
    steering_angle_velocity = SAV
    speed = S
    acceleration = A

def controller(evt):
    msg = AckermannDriveStamped()
    msg.header.stamp = rospy.Time.now()
    msg.drive.steering_angle = steering_angle
    msg.drive.steering_angle_velocity = steering_angle_velocity
    msg.drive.speed = speed
    msg.drive.acceleration = acceleration
    print(msg.drive)
    ack_publisher.publish(msg)

def cb(evt):
    # Contruct an AckermannDriveStamped message
    msg = AckermannDriveStamped()
    msg.header.stamp = rospy.Time.now()
    # msg.header.frame_id = '???'
    msg.drive.steering_angle = 0.5 * max_steering
    msg.drive.steering_angle_velocity = 0.1 * max_steering
    msg.drive.speed = 0.5 * max_speed
    msg.drive.acceleration = 0.01
    print(msg.drive)
    ack_publisher.publish(msg)


rospy.init_node('MsgPublish')
ack_publisher = rospy.Publisher('mux/ackermann_cmd_mux/input/navigation', AckermannDriveStamped, queue_size=1)

change_vals(0.01, 0.02, 0.03, 0.04)
#rospy.Timer(rospy.Duration(2), cb)
rospy.Timer(rospy.Duration(2), controller)
while not rospy.is_shutdown():
    rospy.spin()