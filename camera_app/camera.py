#!/usr/bin/python

import os
import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
from pygame import gfxdraw
import numpy as np
import time
from time import strftime
import datetime
import picamera
import picamera.array
import datetime as dt

from subprocess import call
from subprocess import Popen, PIPE

# Analog read battery level stuff
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


recordButton = 0
photoTaken = 0
mouse = 0

gpio_pin1=18 # The GPIO pin the button is attached to K1
gpio_pin2=23 # The GPIO pin the button is attached to K2
#gpio_pin3=24 # The GPIO pin the button is attached to K3

GPIO.setmode(GPIO.BCM) # Set GPIO mode

GPIO.setup(gpio_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set the up the button. This is for K1 on the screen
GPIO.setup(gpio_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set the up the button. This is for K2 on the screen
#GPIO.setup(gpio_pin3, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set the up the button. This is for K3 on the screen

white = (255,255,255) # White colour
red = (255,0,0) # Colours for the red dot
green = (0,255,0) # Colours for the red dot
blue = (0,0,255) # Colours for the red dot
bright_green = (0,0,255) # Colours for the red dot
black = (0,0,0) # Colours for the red dot

# Screen res
#cam_width = 320 
#cam_height = 240 

# 2X Screen res
cam_width = 640 
cam_height = 480 

# 3X Screen res
#cam_width = 960 
#cam_height = 720 

# QVGA
#cam_width = 800 
#cam_height = 600 

# HD 1080
#cam_width = 1920 
#cam_height = 1080 

# 4X normal res
#cam_width = 1280 
#cam_height = 960 

camera = picamera.PiCamera()
camera.resolution = (cam_width, cam_height)
#camera.hflip = True # Flip the video from the camera
camera.hflip = False # Flip the video from the camera
camera.framerate = 24 # Frame rate
#camera.framerate = 60 # Frame rate

photo_dir = '/home/pi/camera_photos' # Dir for photos
video_dir = '/home/pi/camera_videos' # Dir for videos

#pygame.init() # Start pygame
pygame.display.init()
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('freesansbold.ttf', 30)

pygame.mouse.set_visible(False) # Turned off the mouse pointer
screen = pygame.display.set_mode([cam_width, cam_height],pygame.NOFRAME) # Set up the screen without a window boarder 
video = picamera.array.PiRGBArray(camera)

def buttonStateChanged1(gpio_pin1):

    if(GPIO.input(gpio_pin1) == True):  

        try: # Checks to see if USB drive is there if not saves to SD card 
#            print("USB")
            proc = Popen(["ls /media/pi/"], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
            out, err = proc.communicate()  # Read data from stdout and stderr
            print out
            photo_dir_usb = '/media/pi/%s/camera_photos' % out.rstrip('\n') # Dir for videos on USB
#            print "photo dir %s" % photo_dir_usb
#            else:
#        except:

            if (out == ''):
                raise ValueError('empty string')

            else:
                try:
                    call(["mkdir", "/media/pi/%s/camera_photos" % out.rstrip('\n')])
                    photoFilenameUsb = os.path.join(photo_dir_usb, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.jpg')) # Makes up the file name by adding it all into one string
                    camera.capture(photoFilenameUsb)
    #                print("Photo taken usb")
                    photo(photoFilenameUsb)

                except:
                    photoFilenameUsb = os.path.join(photo_dir_usb, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.jpg')) # Makes up the file name by adding it all into one string
                    camera.capture(photoFilenameUsb)
    #                print("Photo taken usb")
                    photo(photoFilenameUsb)
        except ValueError as e:
            photoFilename = os.path.join(photo_dir, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.jpg')) # Makes up the file name by adding it all into one string
            print("SD CARD")
#            print(e)
            camera.capture(photoFilename)
#            print("Photo taken")
            photo(photoFilename)

#        print('%s.jpg' % strftime("%H:%M:%S"))
        photoTaken = 1
        time.sleep(2)
        photoTaken = 0

GPIO.add_event_detect(gpio_pin1, GPIO.BOTH, callback=buttonStateChanged1)
#GPIO.add_event_detect(gpio_pin1, GPIO.RISING, callback=buttonStateChanged1,bouncetime=400)

state = 0 # State for the button

#def buttonStateChanged2(gpio_pin2):
#
#    global state
#    global recordButton
#    global video_out
#
#
#    if(GPIO.input(gpio_pin2) == True):  
#
#        if (state == 1):
#            state = 0
#
#        elif (state == 0):
#            state = 1
#
#    if (state == 1):
##        print ("start rec")
#
#        try: # Checks to see if USB drive is there if not saves to SD card
#
#            proc = Popen(["ls /media/pi/"], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
#            video_out, err = proc.communicate()  # Read data from stdout and stderr
#            video_dir_usb = '/media/pi/%s/camera_videos' % video_out.rstrip('\n') # Dir for videos on USB
#
#            proc = Popen(["ls /media/pi/%s" % video_out], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
#            video_out_dir, err = proc.communicate()  # Read data from stdout and stderr
#
#            if (video_out == ''):
#                raise ValueError('empty string')
#
#            else:
#                print video_dir
##            if (video_dir == ''):
#                try:
#    #                print video_dir
#                    call(["mkdir", "/media/pi/%s/camera_videos" % video_out.rstrip('\n')]) # Attemps to make a dir 
#                    videoFilenameUsb = os.path.join(video_dir_usb, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264')) # Brings all the elements together to have time and date
#                    camera.start_recording(videoFilenameUsb) # Start recording with time and date as file name
##            else:
#                except: # If it cant make dir then it just uses the one on the flash drive
#
#                    videoFilenameUsb = os.path.join(video_dir_usb, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264')) # Brings all the elements together to have time and date
#                    camera.start_recording(videoFilenameUsb) # Start recording with time and date as file name
#
#        except ValueError as e: # If error happens it falls back to this state and saves to sd card
#            videoFilename = os.path.join(video_dir, dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.h264')) # Brings all the elements together to have time and date
##            print("video taken sd")
#            camera.start_recording(videoFilename) # Start recording with time and date as file name
#
#        recordButton = 1 # Turns on the record red dot
#
#    elif (state == 0):
##        print ("stop rec")
#        camera.stop_recording() # Stop the recording
#        recordButton = 0 # Turns off the record red dot
#
#GPIO.add_event_detect(gpio_pin2, GPIO.BOTH, callback=buttonStateChanged2)
#GPIO.add_event_detect(gpio_pin2, GPIO.RISING, callback=buttonStateChanged2,bouncetime=400)

#def buttonStateChanged3(gpio_pin3):
#
#    if(GPIO.input(gpio_pin3) == True):  
#        print("Button pressed three")
#        pygame.quit() # Quits the python script
#
##GPIO.add_event_detect(gpio_pin3, GPIO.BOTH, callback=buttonStateChanged3)
#GPIO.add_event_detect(gpio_pin3, GPIO.RISING, callback=buttonStateChanged3,bouncetime=400)
#
def rec():

    pygame.gfxdraw.filled_circle(screen, 20, 20, 10, red) # Draw circle
    pygame.gfxdraw.aacircle(screen, 20, 20, 10, red) # Draw an anti alias circle
    textsurface = myfont.render('REC', True, red) # Draw text
    screen.blit(textsurface,(35,10)) # Draw text
#    pygame.display.update() # Update screen

def photo(fileName):

#    screen.fill(white) # Flash screen white
    lastImg = pygame.image.load('%s' % fileName) # Load up the photo you just took
    scalePhoto = pygame.transform.scale(lastImg, (320, 240)) # Scale to fit screen
    screen.blit(scalePhoto, (0,0)) 
    pygame.display.update() # Update screen

for frameBuf in camera.capture_continuous(video, format ="rgb", use_video_port=True):

    frame = np.rot90(frameBuf.array)        
    video.truncate(0)
    frame = pygame.surfarray.make_surface(frame)
    scaleVideo = pygame.transform.scale(frame, (320, 240)) # Scales the video to fit the screen
    flipVideo = pygame.transform.flip(scaleVideo, True, False) # Flip the scaled video horizonatly
    screen.fill([0,0,0]) # Fill the screen
    screen.blit(flipVideo, (0,0)) # Post to the screen

    if recordButton == 1:
        rec() # Puts the red dot on screen when recording


    for event in pygame.event.get(): # Events for the mouse and hit target code

        if(event.type is MOUSEBUTTONDOWN): # If the mouse is clicked
            mouse = pygame.mouse.get_pos() # Get mouse pointer position

        elif(event.type is MOUSEBUTTONUP):# If the mouse click is let go
            mouse = pygame.mouse.get_pos() # Get mouse pointer position

#            if 150+100 > mouse[0] > 150 and 450+50 > mouse[1] > 450:
#                pygame.draw.rect(gameDisplay, bright_green,(150,450,100,50))
            if 270+50 > mouse[0] > 270 and 200+50 > mouse[1] > 200: # Draw a hit target
#                pygame.draw.rect(screen, red,(270,200,50,50)) # Draw a box
#                pygame.quit() # Quits the python script
                call(["sudo", "shutdown", "-h", "now" ])

            if 0+50 > mouse[0] > 0 and 200+50 > mouse[1] > 200: # Draw a hit target
#                pygame.draw.rect(screen, red,(270,200,50,50)) # Draw a box
                pygame.quit() # Quits the python script

            if 270+50 > mouse[0] > 270 and 0+50 > mouse[1] > 0:
                print "un mount"
                proc = Popen(["ls /media/pi/"], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
                out, err = proc.communicate()  # Read data from stdout and stderr
                call(["umount", "/media/pi/%s" % out.rstrip('\n')]) # Attemps to make a dir 

            if 0+160 > mouse[0] > 0 and 50+160 > mouse[1] > 50:
                print "pressed left"

                if (state == 1):
                    state = 0

                elif (state == 0):
                    state = 1

                if (state == 1):
            #        print ("start rec")

                    try: # Checks to see if USB drive is there if not saves to SD card

                        proc = Popen(["ls /media/pi/"], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
                        video_out, err = proc.communicate()  # Read data from stdout and stderr
                        video_dir_usb = '/media/pi/%s/camera_videos' % video_out.rstrip('\n') # Dir for videos on USB

                        proc = Popen(["ls /media/pi/%s" % video_out], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
                        video_out_dir, err = proc.communicate()  # Read data from stdout and stderr

                        if (video_out == ''):
                            raise ValueError('empty string')

                        else:
                            print video_dir
            #            if (video_dir == ''):
                            try:
                #                print video_dir
                                call(["mkdir", "/media/pi/%s/camera_videos" % video_out.rstrip('\n')]) # Attemps to make a dir 
                                videoFilenameUsb = os.path.join(video_dir_usb, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264')) # Brings all the elements together to have time and date
                                camera.start_recording(videoFilenameUsb) # Start recording with time and date as file name
            #            else:
                            except: # If it cant make dir then it just uses the one on the flash drive

                                videoFilenameUsb = os.path.join(video_dir_usb, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264')) # Brings all the elements together to have time and date
                                camera.start_recording(videoFilenameUsb) # Start recording with time and date as file name

                    except ValueError as e: # If error happens it falls back to this state and saves to sd card
                        videoFilename = os.path.join(video_dir, dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.h264')) # Brings all the elements together to have time and date
            #            print("video taken sd")
                        camera.start_recording(videoFilename) # Start recording with time and date as file name

                    recordButton = 1 # Turns on the record red dot

                elif (state == 0):
            #        print ("stop rec")
                    camera.stop_recording() # Stop the recording
                    recordButton = 0 # Turns off the record red dot


            if 160+160 > mouse[0] > 160 and 50+160 > mouse[1] > 50:
                print "pressed right"

                try: # Checks to see if USB drive is there if not saves to SD card 
        #            print("USB")
                    proc = Popen(["ls /media/pi/"], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
                    out, err = proc.communicate()  # Read data from stdout and stderr
                    print out
                    photo_dir_usb = '/media/pi/%s/camera_photos' % out.rstrip('\n') # Dir for videos on USB
        #            print "photo dir %s" % photo_dir_usb
        #            else:
        #        except:

                    if (out == ''):
                        raise ValueError('empty string')

                    else:
                        try:
                            call(["mkdir", "/media/pi/%s/camera_photos" % out.rstrip('\n')])
                            photoFilenameUsb = os.path.join(photo_dir_usb, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.jpg')) # Makes up the file name by adding it all into one string
                            camera.capture(photoFilenameUsb)
            #                print("Photo taken usb")
                            photo(photoFilenameUsb)

                        except:
                            photoFilenameUsb = os.path.join(photo_dir_usb, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.jpg')) # Makes up the file name by adding it all into one string
                            camera.capture(photoFilenameUsb)
            #                print("Photo taken usb")
                            photo(photoFilenameUsb)
                except ValueError as e:
                    photoFilename = os.path.join(photo_dir, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.jpg')) # Makes up the file name by adding it all into one string
                    print("SD CARD")
        #            print(e)
                    camera.capture(photoFilename)
        #            print("Photo taken")
                    photo(photoFilename)

        #        print('%s.jpg' % strftime("%H:%M:%S"))
                photoTaken = 1
                time.sleep(2)
                photoTaken = 0

#    pygame.draw.rect(screen, green,(270,190,50,50)) # Draw a box

    proc = Popen(["ls /media/pi/"], stdout=PIPE, shell=True) # Run comman and send it to stdout and stder
    out, err = proc.communicate()  # Read data from stdout and stderr
#    print out

    if (out == ''):
        pygame.draw.lines(screen, green, True, [[285, 20], [315, 20], [300, 5], [285, 20]], 3) # Draw a triangle
        pygame.draw.rect(screen, green, [285, 25, 30, 7], 3) # Draw a rectangle

    else:
        pygame.draw.lines(screen, red, True, [[285, 20], [315, 20], [300, 5], [285, 20]], 3) # Draw a triangle
        pygame.draw.rect(screen, red, [285, 25, 30, 7], 3) # Draw a rectangle

    # Power shutdown on screen button
    pygame.gfxdraw.aacircle(screen, 295, 215, 15, red) # Draw an anti alias circle
    pygame.gfxdraw.aacircle(screen, 295, 215, 14, red) # Draw an anti alias circle
    pygame.gfxdraw.aacircle(screen, 295, 215, 13, red) # Draw an anti alias circle
    pygame.gfxdraw.aacircle(screen, 295, 215, 12, red) # Draw an anti alias circle
    pygame.draw.lines(screen, red, True, [[295, 215],[295, 192]], 3) # Draw a triangle

# Analog read the battery level and display it on the button left corner of the screen
    values = [0]*4

    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[i] = adc.read_adc(i, gain=GAIN)
#        values[i] = adc.read_adc(i, gain=GAIN, sps)

    mapped_value = translate(values[0], 24000, 30500, 0, 100)
    string_number = "%.f%%" % mapped_value
    
    textsurface = myfont.render(string_number, True, blue) # Draw text
    screen.blit(textsurface,(15,215)) # Draw text

    if values[0] <= 24000: # If the battery level drops too low it will issue the shutdown command
        screen.fill(white) # Flash screen white
        textsurface = myfont.render('Low Battery', True, black) # Draw text
        screen.blit(textsurface,(35,10)) # Draw text
        time.sleep(5)
        call(["sudo", "shutdown", "-h", "now" ]) # Shutdown command
        

    pygame.display.update() # Update screen

