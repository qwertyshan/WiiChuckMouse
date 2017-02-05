# Import the required libraries for this script
import math, string, time, serial, sys, time
from Quartz.CoreGraphics import * # imports all of the top-level symbols in the module

# The port to which your Arduino board is connected
port = '/dev/cu.usbmodem1421'

# Invert y-axis (True/False)
invertY = False

# The cursor speed
cursorSpeed = 5000

# The baudrate of the Arduino program
baudrate = 19200

# Variables indicating whether the mouse buttons are pressed or not
leftDown = False
rightDown = False

# Variables indicating the center position (no movement) of the controller
midAccelX = 530 # Accelerometer X
midAccelY = 510 # Accelerometer Y
midAnalogY = 134 # Analog Y

if port == 'arduino_port':
    print 'Please set up the Arduino port.'
    while 1:
        time.sleep(1)

# Connect to the serial port
ser = serial.Serial(port=port, baudrate=baudrate)
# ser = serial.Serial(port, baudrate, timeout = 1)

# Wait 1s for things to stabilize
time.sleep(1)

# While the serial port is open
while ser.isOpen():

    # Read one line
    line = ser.readline()

    # Strip the ending (\r\n)
    line = string.strip(line, '\r\n')

    # Split the string into an array containing the data from the Wii Nunchuk
    line = string.split(line, ' ')

    # Set variables for each of the values
    analogX = int(line[0])
    analogY = int(line[1])
    accelX = int(line[2])
    accelY = int(line[3])
    accelZ = int(line[4])
    zButton = int(line[5])
    cButton = int(line[6])

    # Set mouse event methods
    def mouseEvent(type, posx, posy):
        theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, theEvent)

    def mousemove(posx,posy):
        mouseEvent(kCGEventMouseMoved, posx,posy)

    def leftmouseclickdn(posx,posy):
        mouseEvent(kCGEventLeftMouseDown, posx,posy)

    def leftmouseclickup(posx,posy):
        mouseEvent(kCGEventLeftMouseUp, posx,posy)

    def leftmousedrag(posx,posy):
        mouseEvent(kCGEventLeftMouseDragged, posx,posy)

    def rightmouseclickdn(posx,posy):
        mouseEvent(kCGEventRightMouseDown, posx,posy)

    def rightmouseclickup(posx,posy):
        mouseEvent(kCGEventRightMouseUp, posx,posy)

    def scrollup():
        event = CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitLine, 1, -1)
        CGEventPost(kCGHIDEventTap, event)

    def scrolldown():
        event = CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitLine, 1, 1)
        CGEventPost(kCGHIDEventTap, event)

    # Left Mouse Button
    # If the Wii Nunchuk Z Button is pressed, but wasn't previously
    if(zButton and not leftDown):
        # Simulate a mouse pressing the left mouse button
        leftDown = True
        ourEvent = CGEventCreate(None)
        currentpos = CGEventGetLocation(ourEvent)
        leftmouseclickdn(int(currentpos.x),int(currentpos.y))
    # Else if it was pressed, but isn't anymore
    elif(leftDown and not zButton):
        # Simulate a mouse releasing the left mouse button
        leftDown = False
        ourEvent = CGEventCreate(None)
        currentpos = CGEventGetLocation(ourEvent)
        leftmouseclickup(int(currentpos.x),int(currentpos.y))


    # Right Mouse Button
    # Do the same with the C Button, simulating the right mouse button
    if(cButton and not rightDown):
        rightDown = True
        ourEvent = CGEventCreate(None)
        currentpos = CGEventGetLocation(ourEvent)
        rightmouseclickdn(int(currentpos.x),int(currentpos.y))
    elif(rightDown and not cButton):
        rightDown = False
        ourEvent = CGEventCreate(None)
        currentpos = CGEventGetLocation(ourEvent)
        rightmouseclickup(int(currentpos.x),int(currentpos.y))
        

    # Mouse Wheel
    # If the analog stick is not centered
    if(analogY > midAnalogY+5):
        scrollup()
    elif(analogY < midAnalogY-5):
        scrolldown()


    # Mouse Movement
    # Create variables indicating how much the mouse cursor should move in each direction
    dx = 0
    dy = 0

    # If the Wii Nunchuk is rotated around the x-axis
    if(abs(accelX - midAccelX) > 20):
        # Calculate how much the cursor should move horizontally
        dx = int(math.floor((accelX - midAccelX))*cursorSpeed/500)

    # If the Wii Nunchuk is rotated around the y-axis
    if(abs(accelY - midAccelY) > 20):
        # Calculate how much the cursor should move vertically
        dy = int(math.floor((accelY - midAccelY))*cursorSpeed/500)
        # Invert the y-axis
        if invertY:
            dy = dy*-1

    # Simulate mouse movement with the values calculated above
    mousemove(dx,dy)
    

# After the program is over, close the serial port connection
ser.close()
