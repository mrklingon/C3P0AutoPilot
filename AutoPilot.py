import time
import usb_hid
import random
import board
import neopixel
import touchio

# Play a browser based arcade game, like: https://makecode.com/_JfAKKf2EUcLv

# pad #1 shoots laser / flashes red
# pad #2 toggles on/off C3P0 - moves ship at random and fires lasers - flashes
#                 multi-colored lights. / turns red when toggled off
# touch #1 and #2 to end program - lights flash gold.



touch1 = touchio.TouchIn(board.TOUCH1)
touch2 = touchio.TouchIn(board.TOUCH2)

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)


pixels = neopixel.NeoPixel(board.NEOPIXEL, 4, auto_write=True)


#Define colors
pink = (12,10,12)
gold = (50, 40, 5)
blue = (0,0,8)
orange = (25, 10, 0)
blank = (0,0,0)
grn = (0,20,0)
green  = (0,20,0)
red = (20,0,0)
zero = (2,2,2)
colors = [pink, gold, blue, orange,green,red]

#define cursor keycodes
moves = [Keycode.DOWN_ARROW,Keycode.UP_ARROW,Keycode.LEFT_ARROW,Keycode.RIGHT_ARROW]
REPL = False


def shoot():
    #send random stream of " "  - to fire laser
    pixels.fill(blue)
    for x in range(1+random.randrange(4)):
        keyboard_layout.write(" ")
    time.sleep(.1)
    pixels.fill(blank)

def jiggle():
    #random cursor movement
    steps = 3 + random.randrange(5)
    for i in range(steps):
        pixels.fill(random.choice(colors))
        dir = moves[random.randrange(4)]
        for x in range(10):
            keyboard.send(dir)
    pixels.fill(blank)

C3P0 = False
Done = False


while not Done:
    Val = 0
    if touch1.value:
        Val = Val + 1
    if touch2.value:
        Val = Val + 2
    if Val == 1 :
        print("shoot")
        shoot()

    if Val == 2 :
        if C3P0:
            print("droid deactivated")
            C3P0 = False
            pixels.fill(red)
            time.sleep(2)

            
        else :
            print("droid engaged")
            C3P0 = True
            pixels.fill(green)
            time.sleep(.5)
        
    if Val == 3 :
        Done = True
    if C3P0:
        for r in range(random.randrange(5)):
            shoot() # fire laser
            time.sleep(.25)
            jiggle() # move ship
            time.sleep(.25)
            
    time.sleep(.1)
print("End of the Line")
pixels.fill(gold)
time.sleep(5)


