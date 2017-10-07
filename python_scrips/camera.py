import os
import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
import numpy as np
import time
from time import strftime
import datetime
import picamera
import picamera.array
import datetime as dt

recordButton = 0

gpio_pin1=18 # The GPIO pin the button is attached to K1
gpio_pin2=23 # The GPIO pin the button is attached to K2
gpio_pin3=24 # The GPIO pin the button is attached to K3
GPIO.setmode(GPIO.BCM) # Set GPIO mode
GPIO.setup(gpio_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set the up the button. This is for K1 on the screen
GPIO.setup(gpio_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set the up the button. This is for K2 on the screen
GPIO.setup(gpio_pin3, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set the up the button. This is for K3 on the screen

white = (255,255,255) # White colour
red = (255,0,0) # Colours for the red dot

#screen_width = 320
#screen_height = 240 

#screen_width = 1920 
#screen_height = 1080 

#screen_width = 1280 
#screen_height = 720 

#screen_width = 640 
#screen_height = 480 

cam_width = 800 
cam_height = 600 
#cam_width = 320 
#cam_height = 240

camera = picamera.PiCamera()
camera.resolution = (cam_width, cam_height)
camera.hflip = True # Flip the video from the camera
camera.framerate = 24 # Frame rate
#os.chdir ("/home/pi/camera_photos")
photo_dir = '/home/pi/camera_photos' # Dir for photos
video_dir = '/home/pi/camera_videos' # Dir for videos

pygame.init() # Start pygame
#pygame.display.set_caption("OpenCV camera stream on Pygame")

pygame.mouse.set_visible(False) # Turned off the mouse pointer
screen = pygame.display.set_mode([cam_width, cam_height],pygame.NOFRAME) # Set up the screen without a window boarder 
video = picamera.array.PiRGBArray(camera)

def buttonStateChanged1(gpio_pin1):

    if not (GPIO.input(gpio_pin1)):
        photoFilename = os.path.join(photo_dir, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.jpg'))

        print("Photo taken")
        camera.capture(photoFilename)
        print('%s.jpg' % strftime("%H:%M:%S"))
        screen.fill(white)
        pygame.display.update() 

GPIO.add_event_detect(gpio_pin1, GPIO.BOTH, callback=buttonStateChanged1)

state = 0

def buttonStateChanged2(gpio_pin2):

    global state
    global recordButton
    videoFilename = os.path.join(video_dir, dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.h264')) # Brings all the elements together to have time and date

    if(GPIO.input(gpio_pin2) == True):  
        if (state == 1):
            state = 0
        elif (state == 0):
            state = 1
    if (state == 1):
        print ("start rec")
        camera.start_recording(videoFilename) # Start recording with time and date as file name
        recordButton = 1 # Turns on the record red dot
    elif (state == 0):
        print ("stop rec")
        camera.stop_recording() # Stop the recording
        recordButton = 0 # Turns off the record red dot

#GPIO.add_event_detect(gpio_pin2, GPIO.BOTH, callback=buttonStateChanged2)
GPIO.add_event_detect(gpio_pin2, GPIO.RISING, callback=buttonStateChanged2,bouncetime=200)

def buttonStateChanged3(gpio_pin3):

    if not (GPIO.input(gpio_pin3)):
        print("Button pressed three")
        pygame.quit() # Quits the python script

GPIO.add_event_detect(gpio_pin3, GPIO.BOTH, callback=buttonStateChanged3)

#try:
for frameBuf in camera.capture_continuous(video, format ="rgb", use_video_port=True):

    if recordButton == 1:
        pygame.draw.circle(screen, red, [30, 30], 10, 10) # Draws a red record dot
        pygame.display.update() # Updates the screen

    else:
        pass # Does nothing
 #       pygame.display.update() 

    frame = np.rot90(frameBuf.array)        
    video.truncate(0)
    frame = pygame.surfarray.make_surface(frame)
    scaleVideo = pygame.transform.scale(frame, (320, 240)) # Scales the video to fit the screen
    screen.fill([0,0,0])
    screen.blit(scaleVideo, (0,0))
    pygame.display.update() # Update screen

#    if GPIO.input(gpio_pin1) == False: # Listen for the press, the loop until it steps
#        print "button one"
#
#    if GPIO.input(gpio_pin2) == False: # Listen for the press, the loop until it steps
#        print "button two"
#
#    if GPIO.input(gpio_pin3) == False: # Listen for the press, the loop until it steps
#        print "button three"
#    
#    for event in pygame.event.get():
#        if event.type == KEYDOWN:
#            camera.capture('image.jpg')
