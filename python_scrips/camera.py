import os
import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
#import cv2
import numpy as np
import time
from time import strftime
import datetime
import picamera
import picamera.array
import datetime as dt

#global startRecord 
startRecord = 0

gpio_pin1=18 # The GPIO pin the button is attached to
gpio_pin2=23 # The GPIO pin the button is attached to
gpio_pin3=24 # The GPIO pin the button is attached to
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gpio_pin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)



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
#camera.resolution = (cam_width, cam_height)
camera.hflip = True
camera.framerate = 24
#os.chdir ("/home/pi/camera_photos")
photo_dir = '/home/pi/camera_photos' 
video_dir = '/home/pi/camera_videos'



pygame.init()
#pygame.display.set_caption("OpenCV camera stream on Pygame")

pygame.mouse.set_visible(False) # Turned off the mouse pointer
screen = pygame.display.set_mode([cam_width, cam_height],pygame.NOFRAME) # Set up the screen without a window boarder 
video = picamera.array.PiRGBArray(camera)
#video = picamera.array.PiArrayOutput(camera)

#video = picamera.array.PiArrayOutput(camera, size=None)

def buttonStateChanged1(gpio_pin1):

    if not (GPIO.input(gpio_pin1)):
        photoFilename = os.path.join(photo_dir, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.jpg'))

        print("Photo taken")
        camera.capture(photoFilename)
        print('%s.jpg' % strftime("%H:%M:%S"))

GPIO.add_event_detect(gpio_pin1, GPIO.BOTH, callback=buttonStateChanged1)

def buttonStateChanged2(gpio_pin2):

    global startRecord 
    if not (GPIO.input(gpio_pin2)):
        print("Button pressed two")
#        camera.start_recording('video.h264')
        startRecord += 1
        print(startRecord)
        videoFilename = os.path.join(video_dir, dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.h264'))

        if (startRecord == 2):
            startRecord = 0

        if startRecord == 1:
#            camera.start_recording('video.mp4')
            camera.start_recording(videoFilename)
        if startRecord == 2:
#            camera.stop_recording('video.mp4')
            camera.stop_recording(videoFilename)

#        firstButtonOnly = 0;
#        weighing = 0;
#        weighingFirstButton = 0;
#    camera.start_recording('video.h264')


GPIO.add_event_detect(gpio_pin2, GPIO.BOTH, callback=buttonStateChanged2)

def buttonStateChanged3(gpio_pin3):

    if not (GPIO.input(gpio_pin3)):
        print("Button pressed three")
        pygame.quit()

GPIO.add_event_detect(gpio_pin3, GPIO.BOTH, callback=buttonStateChanged3)

#try:
for frameBuf in camera.capture_continuous(video, format ="rgb", use_video_port=True):
    frame = np.rot90(frameBuf.array)        
    video.truncate(0)
    
    frame = pygame.surfarray.make_surface(frame)
    scaleVideo = pygame.transform.scale(frame, (320, 240))
    screen.fill([0,0,0])
#    screen.blit(frame, (0,0))
    screen.blit(scaleVideo, (0,0))
    pygame.display.update()

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
#
##                raise KeyboardInterrupt
#        elif event.type == KEYUP:
##                raise KeyboardInterrupt
#            pass

#except KeyboardInterrupt,SystemExit:
#    pass
#pygame.quit()
#    cv2.destroyAllWindows()
