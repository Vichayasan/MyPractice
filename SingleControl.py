import machine
import time

# -------------------------
# Pin setup
# -------------------------

butt = machine.Pin(20, machine.Pin.IN)
Motor_M1A = machine.PWM(machine.Pin(8))
Buz = machine.PWM(machine.Pin(22))

# -------------------------
# PWM configuration
# -------------------------

print("Start PWM Config")

MOTOR_DUTY = 40000 # Motor Speed
Motor_M1A.freq(20000)   	 # 20 kHz
print("Motor Off")
Motor_M1A.duty_u16(0)	#Start Motor OFF

BUZZER_FREQ = 3000      # 3 kHz audible tone
BUZZER_DUTY = 2500     # ~50% duty


Buz.freq(BUZZER_FREQ)
Buz.duty_u16(0)      # Start silent

def Motor_on():
    print("Motor ON")
    Motor_M1A.duty_u16(MOTOR_DUTY) # control motor speed
    Buz.duty_u16(BUZZER_DUTY)
    
def Motor_off():
    print("Motor Off")
    Motor_M1A.duty_u16(0)
    Buz.duty_u16(0)
    
# -------------------------
# Main loop
# -------------------------
print("Start Main Loop")
while True:
    
    
    if not butt.value():
        Motor_on()
    else:
        Motor_off()
        
    time.sleep_ms(20)