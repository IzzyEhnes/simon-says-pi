# Izzy Ehnes
# simon_says.py
# 12/15/2019
# CS12, Section 0656
#
# This is a simple Simon Says game for the Raspberry Pi. 
# Once run, either the red, yellow, greed or blue LED will light up briefly.
# The white LED will then light up, indicating that the user can select a button.
# If the correct colored button is selected, the original LED will light up again
# followed by another randomly chosen LED, and then the white LED to indicate the 
# user can select buttons. Each time the user selects the correct sequence of buttons 
# corresponding to the light sequence, a new light will be added to the sequence 
# until the number of rounds declared in numRounds have been completed.
#
# If the user selects an incorrect button at any point the player loses, and the 
# white LED will flash three times and the program ends. The player will also 
# lose if they don't select the correct number of buttons in the alotted time. 
#
# If the user passes each round, then all of the colored lights will flash up and 
# down the line and turn on and off again twice to let the user know they won the game.


import RPi.GPIO as GPIO
import sys
import time
import random

# LED GPIO pin numbers
redLED = 18
yellowLED = 23
greenLED = 17
blueLED = 10
whiteLED = 16

# Button GPIO pin numbers
redButton = 25
yellowButton = 24
greenButton = 27
blueButton = 9

#GPIO configs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(whiteLED, GPIO.OUT)

#GPIO.setup(redButton, GPIO.IN)
GPIO.setup(redLED, GPIO.OUT)
GPIO.setup(redButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIO.setup(yellowButton, GPIO.IN)
GPIO.setup(yellowLED, GPIO.OUT)
GPIO.setup(yellowButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIO.setup(greenButton, GPIO.IN)
GPIO.setup(greenLED, GPIO.OUT)
GPIO.setup(greenButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIO.setup(blueButton, GPIO.IN)
GPIO.setup(blueLED, GPIO.OUT)
GPIO.setup(blueButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lights = [redLED, yellowLED, greenLED, blueLED]
buttons = [redButton, yellowButton, greenButton, blueButton]
lightSequence = []
buttonsPressed = []

#In case LEDS were on for some reason
GPIO.output(whiteLED, False)
GPIO.output(redLED, False)
GPIO.output(yellowLED, False)
GPIO.output(greenLED, False)
GPIO.output(blueLED, False)

time.sleep(1)

def redPressed(channel):
    buttonsPressed.append(redLED)
    #print ("Red button pressed")
    
def yellowPressed(channel):
    buttonsPressed.append(yellowLED)
    #print ("Yellow button pressed")
    
def greenPressed(channel):
    buttonsPressed.append(greenLED)
    #print ("Green button pressed")
    
def bluePressed(channel):
    buttonsPressed.append(blueLED)
    #print ("Blue button pressed")
    
#Turns all LEDs on
def turnAllOn():
    GPIO.output(redLED, True)
    GPIO.output(yellowLED, True)
    GPIO.output(greenLED, True)
    GPIO.output(blueLED, True)
    time.sleep(0.25)

#Turns all LEDs off
def turnAllOff():
    GPIO.output(redLED, False)
    GPIO.output(yellowLED, False)
    GPIO.output(greenLED, False)
    GPIO.output(blueLED, False)
    time.sleep(0.1)
    
def gameWon():
    print ("You won!")
    for LED in lights:
        GPIO.output(LED, True)
        time.sleep(0.1)
        GPIO.output(LED, False)
        time.sleep(0.05)
        
    for LED in reversed(lights):
        GPIO.output(LED, True)
        time.sleep(0.1)
        GPIO.output(LED, False)
        time.sleep(0.05)
        
    turnAllOn()
    turnAllOff()
    turnAllOn()
    turnAllOff()
    sys.exit()
    
    
def gameLost():
    print ("Sorry, you lost!")
    for i in range(5):
        GPIO.output(whiteLED, True)
        time.sleep(0.1)
        GPIO.output(whiteLED, False)
        time.sleep(0.1)
    sys.exit()
    
    
GPIO.add_event_detect(redButton, GPIO.BOTH, callback=redPressed, bouncetime=300)
GPIO.add_event_detect(yellowButton, GPIO.BOTH, callback=yellowPressed, bouncetime=300)
GPIO.add_event_detect(greenButton, GPIO.BOTH, callback=greenPressed, bouncetime=300)
GPIO.add_event_detect(blueButton, GPIO.BOTH, callback=bluePressed, bouncetime=300)

#Max number of LEDs in final sequence
numRounds = 3

for roundCount in range(numRounds):
        randomNum = random.randint(0,3)
        newLED = lights[randomNum]
        
        lightSequence.append(newLED)
        
        #print (newLED) #for testing purposes
        
        #Displays random light for 1 second
        for LEDCount in range(len(lightSequence)):
            GPIO.output(lightSequence[LEDCount], True)
            time.sleep(.5)
            GPIO.output(lightSequence[LEDCount], False)
            time.sleep(.5)
            
        buttonsPressed.clear()
        
        #Displays white LED to indicate the user that they can begin selecting buttons
        GPIO.output(whiteLED, True)
        time.sleep(.5)
        GPIO.output(whiteLED, False)
        time.sleep(.5)
        
        #Waits for button presses
        time.sleep(roundCount+1)
        
        #print ('\n')
        
        if (len(buttonsPressed) != len(lightSequence)):
            print ("You took too long to select the button(s)!")
            sys.exit()

        for buttonCount in range(0, len(buttonsPressed)):
            if (lightSequence[buttonCount] != buttonsPressed[buttonCount]):
                gameLost()
                
#If the player beat every round              
gameWon()