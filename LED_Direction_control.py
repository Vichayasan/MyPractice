import machine # call all function in Library
import time

# -------------------------
# Pin setup
# -------------------------

buttNum = [20, 21] # config pin number
press = [machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for pin in buttNum] # Initialize GPIO pin modes (active-low)

LED_freq = 20000
ledNum = [9, 8, 11, 10, 15, 14, 13, 12] 							# config pin number
LED = [machine.PWM(machine.Pin(pin), LED_freq) for pin in ledNum] 	# Initialize GPIO pin modes

# -------------------------
# PWM configuration
# -------------------------

print("Start PWM Config")										# debug process
LED_DUTY = 40000
print('LED_DUTY: %d, LED_freq: %d'%(LED_DUTY, LED_freq))		# debug process

# -------------------------
# declare global variable for setup machine
# -------------------------

stopCK = False
statButt = 0 # config status of pressing

# -------------------------
# LED step functions
# -------------------------

# config variable outside for avoiding reset step function proscess
cw_count = 0					# LED index for clockwise direction start at 0 of list[]
cc_count = len(LED) - 1			# LED index for Counterclockwise direction start at -1 of list[]

def ccDir():									# create Function control for Counterclockwise direction
    
    global cc_count								# declare global variable
        
        # 🔴 interrupt condition
    if cc and cw:   # both buttons are pressed					
        print("STOP 03")				# debug process
        return 3
    if cw:					# GPIO 21 is pressed
        print("Interrupted by CW button")		# debug process
        return 2
        
    LED[cc_count].duty_u16(LED_DUTY)			# LEDs to ON state
    time.sleep_ms(150)							# Delay for human visibility
    print(f"LED No.{ledNum[cc_count]} : ON")   	# debug process
    LED[cc_count].duty_u16(0)					# LEDs to OFF state
        
    cc_count = (cc_count - 1) % len(LED)		# Move to previous LED index with wrap-around
    return 1
        
        
def cwDir():									# create Function control for clockwise direction
    
    global cw_count								# declare global variable
        
        # 🔴 interrupt condition
    if cc and cw:   # both buttons are pressed
        print("STOP 02")				# debug process
        return 3
    if cc:					# GPIO 20 is pressed
        print("Interrupted by CC button")		# debug process
        return 1
        
    LED[cw_count].duty_u16(LED_DUTY)			# LEDs to ON state
    time.sleep_ms(150)							# Delay for human visibility
    print(f"LED No.{ledNum[cw_count]} : ON")   	# debug process
    LED[cw_count].duty_u16(0)					# LEDs to OFF state
        
    cw_count = (cw_count + 1) % len(LED)		# Move to forward LED index with wrap-around
    return 2

def offAll():
    for led in LED:
        led.duty_u16(0)
    return 3
        

# -------------------------
# Main loop
# -------------------------

while True:
    
    cc = not press[1].value()
    cw = not press[0].value()
    
    # detect status of pressing
    if cc and cw:
        print("STOP 01")
        stopCK = False

    elif cc:
        print('Start counter-clockwise direction')	# debug process
        statButt = 1
        stopCK = True
        
    elif cw:
        print('Start clockwise direction')			# debug process
        statButt = 2
        stopCK = True
        
    if stopCK:
        # ---- run according to state ----
        if statButt == 1:
            statButt = ccDir()

        elif statButt == 2:
            statButt = cwDir()
        
        elif statButt == 3:
            statButt = offAll()
        
        
    time.sleep_ms(1) # avoid CPU clock knock out at 1 ms
