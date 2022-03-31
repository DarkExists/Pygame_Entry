# Pygame_Entry
------------------------------------------------------------------------
This Pygame Module Will Help You To Make Entry Box in Pygame Very Easily
------------------------------------------------------------------------

Entry Types Supported :
------------------------------
  **.** Alphabetic Entry\
  **.** AlphaNumeric with Special Characters Entry\
  **.** Numeric Entry\
  **.** Phone Number Entry\
  **.** Password Entry
 
 # Module Name entrybox.py 
 # class name inside module "entrybox.py" >>> Entry 
# How to Use
 import entrybox\
 import pygame
 
 screen = pygame.display.set_mode(300,400)\
 entry = entrybox.Entry(screen)
# ~~~~
 
 // gameloop\
 entry.update() or If you want to update all the entries you can use entrybox.Entry.update_all()
 
 To learn more see demo.py file
 
# ~~~~
 
Attributes of Module:
-------------------------------

**screen** : Where You Want To Blit Your Entry\
**font** : Which type of font you want in your Entry text (by default uses System Default Font)\
**text** : By default Set to None in case you want some text in your entry in starting you can change it\
**width,height** : size of your entry (by default set to 100,20)\
**left,top** : left and right position of your entry (by default set to 0,0)\
**activecl** : active color of your entry when entry touches the cursor (by default nickle_grey)\
**inactivecl** : inactive color of your entry when entry not touches the cursor or entry is selected (by default platinum)\
**depth** : depth of the entry (by default set to 0)\
**edge** : edges of the entry (by default value is a tuple -> (0,0,0,0) {bottom_right,top_left,top_right,bottom_left})\
**staticalpha** : alpha value of the entry when not selected (by default set to 255)\
**dynamicalpha** : alpha value of the entry when selected (by default set to 255)\
**textcl** : text color of the entry\
**cursorcl** : cursor color of entry\
**show** : If you want to hide the main text and show some other text like you do in passwords *** in this manner you can change its value by default it is set to None\
**lock** : It you want to make Password Type Entry set lock = True (by default set to False)\
# type : Supported type ("alnum","alpha","digit","phone") In which type you want your entry (by default set to "alnum")
**limit** : To limit the characters of your entry (by default set to -1)\
**msg** : In case your want to show Any Message when your Entry is empty (by default No Msg)
# mindigvalue,maxdigvalue : Supports only when entry is "digit" type In case if you want to set the range of entry then use these attributes e g. Date,Month,Year
**blink** : If set to True the cursor will blink (by default set to False)\
**lock_open_img** : If You set lock attribute to True and you want to show your lock open image use this attribute attribute takes a tuple -> ("image path","image name","image extention")\
**lock_img** : If You set lock attribute to True and you want to show your lock image use this attribute attribute takes a tuple -> ("image path","image name","image extention")

# If You Are Not Downloading The Whole Package We Prefer You to download the two given images "eye.png" and "eye_lock.png" and put these images in the directory where your put the Module File.
