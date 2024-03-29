# annoying_plant

Project is WIP

---

## About
---

<p>

This is a talking plant project requiring a RaspberryPi Pico a DFPlayer-mini module as well as a DS-3231 RTC-module (Real time clock).
The main purpose of the project is a beginner friendly DIY experience.
Using Python as a quite easy language to learn and very simple basic modules and circuits.
It should give a small insight into the world of microcontrollers and what they are capable of.
<br>

I provided a short BASICS summary, to explain briefly basic functionalities in Python and electronics. If you not really experienced i give a quick introduction into the most important things for the main project.

![drawing](./docs/draw.png)

</p>


---
## Content
---

- [Parts](#parts)
- [Main Project](#main-project)
- [Basic](#basic)
    * [Safety](#safety)
    * [Electronic Basics](#electronic-basics)
    * [Modules & ICs](#modules--ics)
    * [RaspberryPi Pico](#raspberrypi-pico)

- [Lection 1](#lection-1-installation--blink-sketch)
- [Lection 2](#lection-2-flip-flop)
- [Lection 3](#lection-3-dfplayer-mini)
- [Lection 4](#lection-4-analog-input)


---

## Parts

---

- RaspberryPi Pico
- Zs-042 (DS3231 RTC)
- CD40107BE (2x NAND IC)
- DFPlayer-mini, speaker & microSD-card
- capacitive soil moisture sensor
- Basic components:
    * IRF4905 P-Mos
    * IRFZ44N N-Mos
    * 2x 100nF Capacitor
    * Resistors
    * LED's (optional)


---
## Main project
---

<p>

Main goal of this project is to realize a speaking plant. The existing code should give a framework to customize according to your needs. As the project was originally oriented towards beginners i try to keep the code easy readable and understandable. The circuit works stable after some testing, nontheless some improvements might follow in future. <br>

Main code:
Upload the [main.py](./code/main.py) file to your Pico and build the circuit following the scematic below.

Main sketch:
![annoying plant circuit](./docs/main_v1.png)



<br>

**Circuit description:**
As power supply in this version a 9V block battery or accumulator is used. The circuit is protected by a fuse and a diode agains reversed polarity. An improvement to this would probably be a [P-Mosfet](https://components101.com/articles/design-guide-pmos-mosfet-for-reverse-voltage-polarity-protection). <br>

The next part is a Buck-converter to regulate voltage down to 5V, it is important to first adjust the convterter to about 5V output bevore soldering it in. Doublecheck the Voltage in order to avoid damaging parts! <br>
On the right bottom of the sketch sits the Dfplayer module with our SD card. <br>

Above the buck converter the module in red is a level shifter module. The Pico is not 5V tolerant at its GPIO (general purpose input output) Pins, we risk damaging the part. The ds3231 serial communication is pulled HIGH to 5V level. This is the reason why we must shift down the signal to 3.3V of the Pico. At the shifter module we apply the higher 5V voltage level (red wire) at **'HV'** and 3.3V (orange wire) to **'LV'**. Then module will automatically shift any binary (0 or 1) to its coresponding sides voltage level. <br>

Now we talk about a whole group of parts, which should save some energy in the long run. The Pico is able to cut off its own power supply with a Flip-flop formed by the NAND Gates. In the picture above it ist orientated with the small engraved dot on the bottom left side. It also controlls the RTC and set alarms to flip it on again to wake up the whole system. In the middle we see the CD401007BE IC it holds two NAND Gates. This part works together with the RTC module, at the top of the sketch and the two Mosfet transistors on the right. This group controlls the power of the microcontroller and the dfplayer module, as said saving energy by turning them of while waiting. <br>

The last thing is a capacitive moisture sensor, it brings us the ability to monitor the plant condition and play sounds when the plant pot seems to be dry. Don't forgett to calibrate the moisture sensors values, as it can be seen in [Lection 4](#lection-4-analog-input).
<br>

<br>

You need to upload [main.py](./code/main.py) to the Pico. We import some additional code, therefor you need to upload [dfplayermini.py](./code/dfplayermini.py) and [ds3231_impl.py](./code/ds3231_impl.py) as well. <br>

<br>

**Code description:**
Now lets take a quick look at the coding part. As mentioned above too keep things simple I try to avoid complicated structures in order to reach a good beginnerfriendly readability. <br>
First we start as always with imports of important modules such as the DFplayer-mini  or DS3231 RTC. Importing some additional hardware and software modules such as I2C or random.

<pre><code>
from dfplayermini import Player
from ds3231_impl import ds3231
from machine import Pin, I2C, ADC
import time
import binascii
import sys
import random
</code></pre>

Some variables wont change throughout the operating process therefor we define some constants and initialize some Pin's. We also define a function to handle playing random sounds:
<pre><code>
I2C_PORT = 0
I2C_SDA = 16
I2C_SCL = 17

dry_baseline = 600

ALARM_PIN = 14

led2 = Pin(15, Pin.OUT)
test=0
led = Pin(25, Pin.OUT)
reset = Pin(20, Pin.OUT)

#define a function to handle random tracks of specific folders, list from the dictionary need to be passed accessed by key
def pick_random_track(content_list):
    number=random.randint(1, content_list[1]) #select random number from dictionary
    music = Player(pin_TX=machine.Pin(0), pin_RX=machine.Pin(1)) #init player module
    time.sleep_ms(10)
    music.volume(40)
    #music.play(12,2)
    music.play(number, content_list[0]) #play track 1
    time.sleep(25)
    music.stop()

</code></pre>

Now we come to the main funciton of our programm. At first we will establish the serial communication to the RTC module to get access to date and time. Next step is to confirm the correct value for minute to make sure we didn't woke up due to some outside caused error. Then with 'if analog read > baseline' we want to check if the measurement exceds our defined baseline. <br>
If this condition is true we will play a random sound. For example from the sounds dictionary we select a random number from the 'voiceline_thirsty_at' and play it. The modules goes to sleep after 25 seconds, which is defined in the '*pick_random_track*' function. Some if conditions below are just set **True** to debug the functionality of our code, you may look into '*main.py*' for the actual code to deploy:
<pre><code>
if __name__ == '__main__':
    led.value(0) # activate onboard LED
    rtc = ds3231(I2C_PORT,I2C_SCL,I2C_SDA) #init serial communication with RTC module
    time.sleep_ms(20) #give init process some time
    #rtc.set_time('13:26:25,Tuesday,2022-02-17') #set rtc time uncomment if needed
    #time.sleep_ms(1)
    
    #match_min=[0, 15, 30, 32, 45] #wake every list entry, keep 2 min distance!
    match_min=range(0, 59, 3) #wake every 3 min
    
    print(rtc.read_time())
    y, month, day, h, min1, sec1, wday=rtc.read_time()
    if min1 in match_min: #check for correct time
    #if True:
        print('check plant condition')
        sounds={'music': [1, 2], 'voicline_thirsty_aut': [2, 16], 'voiceline_random_aut': [3, 22]} # dictionary containing lists [folder, num tracks]
        
        #take measurement
        vals=[0]*50
        for index, element in enumerate(vals):
            vals[index]=analog_value.read_u16()
        a_read = sum(vals)/len(vals)
        
        #if _low <= a_read <= _up: #check for reasonable values
        if True:
            #if a_read > dry_baseline: #check if plant is dry
            if False:
                print('AAH! Saufen!')
                #using dictionarys as workaround for problems with folder system on the module
                pick_random_track(sounds['voicline_thirsty_aut'])
            else:
                print('plant fine!')
                #do something at random events?
                pick_random_track(sounds['voiceline_random_aut'])
                    
        else:
            print('Warning: measurement went wrong')
            #do something when measurement not working?

</code></pre>

The last steps are to set a new wake up alarm. Therefor we take our 'min1' measurement and select the next larger number from the array. If no larger number can be found we break no value would be set and the 'next_index' variable will remain at predefined value 0, picking the first index of our list. Then we can shutdown the whole thing by reseting the Flip-flop. <br>
<br> I added some time delays (sleep) here and there to make give the controller some time to initialize Serial conection and make sure it reached a stable state:
<pre><code>
    #set next wakeup-alarm
    next_index=0
    for index, element in enumerate(match_min):
        if element > min1:
            next_index=index
            break
    rtc.set_alarm1(f"{h:02}:{match_min[next_index]:02}:{sec1:02},{wday},{y:04}-{month:02}-{day:02}")
    time.sleep_ms(10)
    
    #reset FF and shutdown pico's supply
    print('shutdown')
    led.value(0)
    time.sleep_ms(10)
    reset.value(1)
</code></pre>


</p>

<br>

---
## Basics
---

---
### Safety
---

<p>

The project is powered by a 5V USB cable or a 9V Block-battery. With this Voltages you don't need to worry when touching something active powered. The resistance of our skin is typically high enough so you wont feel any effects of the small current flowing through your boddy. <br>
Wrongly connect or shorting the circuit can ruin some parts, but you typically will notice them gettin warm first which leaves you sometimes enough time to unplug whatever you might have missconnected. If you follow the instructions you should be on the save side, althugh i garuantee nothing.

</p>

---
### Electronic Basics
---
If you are somewhat experienced you can skip this part, as it is mainly to explain the basic function of commonly used electronic parts.

#### ***Ohm's law:***

<p>

Probably the most common basic is that electric energy flow in form of electrons from higher to lower voltage levels. The amount of current flowing through your wires is depending on the resistance of the path the electrons are traveling. This leads to a well-known and basic formula:

<br>

<pre><code>U=R*I
U is our voltage, R is the value of our resistance in ohm and I stand for the amount of current in ampere.

</code></pre>

That to be said let’s think about that law quickly, everything including wires have a certain value for resistance. With a shorted wire from voltage source to ground we usually can expect almost infinite amount of energy to flow (wire resistance really low - close to 0) dependend of outputcapability of the source. <br> When we add a resistor with let’s say 1000 ohm and our source provides 5V like every USB plug, a current of 0.001 ampere should flow (1mA). The formula used for this comes from Ohm's law I=U/R as you can see this simple formula is quite easy to use and will appear quite often from now on. <br>
I want to add a short reminder on how to calculate resistance. Resistors in series can be added together. For parallel resistors it’s a little different and more complicated, [see](https://en.wikipedia.org/wiki/Resistor).
</p>


#### ***Electronic components:***

<p>

Only some important parts are listed for this project.
- [**Resistor:**](https://en.wikipedia.org/wiki/Resistor) A resistor is a passive electrical component that implements electrical resistance as a circuit element. In electronic circuits, resistors are used to reduce current flow, adjust signal levels, to divide voltages and many other uses. <br>
The resistance value of the part is given in ohm. <br>
*Example:*  Limiting the amount of current flowing through LED's or Pulling Wires to a certain level while not shorting the circuit. For example, if something needs a signal default High on the input it can be realized with a Pull-up resistor to the supply voltage. This prevent a short circuit if the pin is switched low.
- [**Transistor:**](https://en.wikipedia.org/wiki/Transistor) The electronic equivalent of a switch. With two main categories, MOSFET  and Bipolar. Both come with N- and P-doped variants. The range of application is wide. They can be used as amplifier or simply as switches. For our purpose only the use of as switch (in saturation) is relevant. <br>
*Example:* Using an Npn bipolar transistor we could switch High currents directly from the source. Without risk to damage a Pin of the microcontroller due to overload.
- [**Diode:**](https://en.wikipedia.org/wiki/Diode) Is an electrical component that allow current to flow only in one direction. <br>
*Example:* Often used as rectifiers. A special case among diodes are LED, when current flows through them they emit light of a certain wave length.
- [**Capacitor:**](https://en.wikipedia.org/wiki/Capacitor) Capacitors are Conducting plates parallel to each other. They can draw energy from a source and store it. Inside the two metal plates separated by a non-conducting substance. When activated, a capacitor quickly releases electricity in a tiny fraction of a second. <br>
*Example:* They can be used to flatten fluctuation supply. Placed close to the supply Pins of any IC (integrated circuit) a capacitor stabilize the IC’s voltage supply.

</p>

---
### Modules & ICs
---
#### DS3231 RTC Module
<p>

The DS3231 is a low-cost, extremely accurate I²C real-time clock (RTC) with an integrated temperature-compensated crystal oscillator. The device incorporates a batteryslott. <br>
The module is quite consistent over long time periods, it is temperature compensated so it should keep a quite acurate time even in rough circumstances. The serial communication standard used by the device is called [I²C](https://en.wikipedia.org/wiki/I%C2%B2C) or inter-integraterd-circuits. When running this Module on active supply voltage and a battery, it is advised to remove either Resistor or the Diode itself or cut the wire inbetween them. Recharging a non-rechargeable battery is dangerous. It should be avoided at all costs. <br>

The Output Pins of the module are CMOS Open-Drain, so we need to add a Pull-up resistor to pull it on an active HIGH level for our microcontroller to notice it. In our case this would be the **SQW** pin. <br>

This would be true for our serial communication pins too (**SDA**, **SCL**) usually this is already implemented with the intern pullup of the microcontroller.

</p>

![battery security](./docs/battery_protection_ds3231.PNG)

The picture shows our module, with the diode and resistor mentioned above marked with a red arrow. <br>
- **32K** outputs a 32kHz signal
- **SQW/INT** outputs either a square wave signal or an interupt signal to wakeup our microController
- **SCL** Serial Clock, communication: i²c (inter integrated circuit)
- **SDA** Serial Data, communication: i²c
- **VCC** Supply Pin
- **GND** Ground Pin

<br>

#### NAND Gate

<p>

The signal levels 1 and 0 are ofthen called HIGH or LOW at some point, all of these are refering to the same levels (Supplay Voltage and GND). <br>

NAND stands for **not** **and**, what this mean can be shown in the truth table of this gate. Basically, the output is always HIGH except when both inputs are HIGH. In the picture below A and B are the inputs while C is the output. The output also requires a pullup resistor to pull the signal level to HIGH as its cmos-open-drain nature. <br>

![battery security](./docs/truthtable.PNG)

We use a CD40107BE IC the datasheet can be found in the docs folder, the truth table was also taken from the datasheet. <br>

A special use case for the NAND Gate is to invert incomming signals, when we combine the pins A and B it's inverting the signal. You also can see this in first and last lane of the truth table, where A and B are equal. <br>

We can now use this gate to create a flip flop. This is a special circuit designed to store a specific state as to 1 or 0 (HIGH or LOW) representing supply voltage level and ground level in most cases.

</p>

<br>

#### DF-mini-player

<p>

This module is able to drive an analoge speaker. It needs to be supplied with 3.2 - 5 Volts.
The file system supports up to 32GB on the microSD card. It can be controlled either by buttons on the hardware side or with commands through software.

<br>

![DFPlayer mini pinout](./docs/dfplayer1.png)

![DFPlayer specs](./docs/dfplayer2.png)
  
1. Main directory
Up to 3000 wav or mp3 files can be stored in the main directory of the SD card. They must be saved as 0001.mp3 (or 0001.wav), 0002.mp3 …. 3000.mp3. The files are copied in the exact order of their names. Since they are there by creation time.

2. Default directories
You can create 99 standard directories, which follow the scheme 01, 02, 03 .... 99 must be named. In each of these folders, 255 files can be addressed directly using commands.

</p>



---
### RaspberryPi Pico
---

<p>

Raspberry Pi Foundation entrance in the world of microcontrollers. The company itself is well known for its single board computers. This much smaller module comes with a fairly good price. The difference between the bigger RaspberryPi's is that not supposed to be a whole computer. Therefore, it comes with less computing power and programmable memory space and probably more important no Operating system. That to be said you program the function of the module on your own. It is also suitable for low power applications because it does not need that much power.
<br>

The technical aspects can be found in the Datasheet linked below:
The board itself is powered by a MicroUSB connection this refers also as VBUS Pin and need to be 5V. Powering directly at VSYS Pin in the range of 1.8-5.5 V is also possible. It is important to strictly following the datasheet here to avoid damage to our controller. <br>

The Pico is powered by the RP-2040 Chip sitting in the middle of the board, avoid touching the Pins of the Chip itself directly because electrostatic charge from your hands can damage it. To control the processor microPython or with a little effort C++ can be used, more to that later.
<br>

We can now program the Pin’s of the module to switch HIGH/LOW or read analog Signals (Voltage levels). This offers a wide range of possible applications which can be easy realized, we just need to be aware of some basic concepts to not risk damaging the module itself. Although it is usually quite resistant to little accidents in a certain extent. <br>

The Output capability of the Pico is limited (~20mA), for switching higher loads its important to not exceed the parts limits. For switching higher currents use rellais or transistors. Measure or apply negative voltages is neither a good idea because it can damage the part too. This should not be achievable without a propper voltage supply, except for accidentally mistake GND and VCC. <br>

Another possible mistake could be applying 5V to the General purpose Input/Output pins of the Pico. The chip is not 5V tolerant! Use a level-shifter to convert the voltage levels down or a [voltage devider](https://en.wikipedia.org/wiki/Voltage_divider) , simple circuit made out of two resistors. <br>

For more information look at the Datasheet provided below, but more Important is the Pinout scematic, as it is shown there the number and type of our Pins.

</p>

<br>

[Pinout RaspberryPi Pico](./docs/pinoutpico.png)

[Datasheet source](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)

---
### microPython
---

MicroPython is a efficient implementation of the Python 3 programming language it is optimised to run on microcontrollers, like our Pico. It includes a small subset of the Python standard librarys, but its more than sufficient to the needs of this project. <br>
We will use Thonny to write our python code. Its a beginnerfriendly easy to use IDE perfectly fitting the needs to run all kinds of basic electronic projects. <br>
In order to not further stretch this tutorial, you can find tons of good content online such as [this](https://www.programiz.com/python-programming/first-program) or [that](https://www.youtube.com/watch?v=RBpK8C3N-Y8&t=6968s) explaining the basics of programming in Python. If you are not that familiar with programming simply take the codes provided, you may play around with it and learn by doing. <br>

latest version of [Thonny](https://thonny.org/)

<br>


---
## Lection 1: Installation & Blink sketch
---

### Lection 1.1: Installation
A nice and simple tutorial for the following can also be found [here](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/0), every step is well written and illustrated. You may look at it if something went wrong. <br>

<p>

If you have not already downloaded & installed [Thonny](https://thonny.org/) you should do this now. <br>
After the installation is complete click on **Run - select interpreter** like shown below.
![Thonny select interpreter](./docs/thonny1.png)

Now select **MicroPython (Raspberry Pi Pico)** <br>
(In Case you seting up your Pico for the first time you need to hit the **'install or update firmware'** button on the lower right of following window.)
![micropython Pico](./docs/thonny2.png)

---
### Lection 1.2: Blink sketch

Now we can start to write the actual programm. Starting with a simple sketch to show basic functionality. Make sure your Pico is connected for the next steps. It should be select automatically the right port.
<pre><code>
#Hello World!

# import existing code
import time
from machine import Pin

ledpin = Pin(25, Pin.OUT) # here we declare the 'ledpin' as Pin 25 in output mode, variables in python can be anything basically (type will be handled automatically)

print("Hello World!") # this will print "Hello World!" to the console in our IDE, the message will be sent by the Pico over USB-serial interface
message='Test!123'
print(message) #this will print the variable message (which is a string in this case)


ledpin.value(1) # now we output a HIGH signal on the defined ledpin (anything except 0 is counted as HIGH)
time.sleep(1) # wait for 1 second, the controller wont do ANYTHING while this period of time
time.sleep_ms(1) # wait for 1 millisecond

ledpin.value(0) # pull ledpin LOW
</code></pre>

For more details on [time library](https://docs.micropython.org/en/latest/library/time.html) click the link.

Now click on save, there should now apper a window asking you where u want to save. Hit the button to save on the Pico like shown below. **Important** use the file ending .py when saving your programm!

![save on Pico](./docs/thonny3.png)

![Run sketch](./docs/thonny4.png)

When you hit the **Run** button the programm should start to execute on the Pico, if you want to stop the code hit the red **STOP**. The Led should blink from now until you stop the code from executing. But the code wont execute as soon as the board is powered on in order to achieve that see bellow. <br>

<br>

**Additional:** <br>
A better and maybee more 'pythonic' way to implement something similar is shown in blink.py from the code folder. Load it or copy the code manually into your ThonnyIDE.

<pre><code>
#import existing code
from machine import Pin, Timer

#declare pins & variables
led = Pin(25, Pin.OUT)  #initialize pin 25 and set it to output
LED_state = True        #declare a boolean variable
tim = Timer()           #initialize a timer module

#define a function to execute code at a certain callback event
def tick(timer):
    global led, LED_state       #get access to the global variables in function space
    LED_state = not LED_state   #inverting bool value
    led.value(LED_state)        #output the new state to our pin

#use Timer object to execute our callback function at 1Hz (1 per second)
tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)
</code></pre>

When you save the code to your Pico this time give the file the name **main.py** , now the Pico will execute the code everytime it is powered on automatically. You should still be able to controll it by the **STOP** and **RUN** button while pluged to your PC. <br>


</p>

<br>

---
## Lection 2: Flip flop
---

<p>

**Theory:** <br>
A Flip-flop is a bistable circuit saving a electronic state. It's fundamental circuit to store digital information. In games like Minecraft, you can build such a thing pretty quickly. <br>
In the game you can build an inverter out of a redstone wire and a redstone torch attached to the block. When we connect two inverters this will form a Bistable state. Switching one of the buttons will cause the system to flip side and will stay that way untill the other button is pressed. <br>

![Minecraft FF](./docs/mc_ff.png)

In real world application the way this works is basically the same. This time wie connect two NAND-Gates together, which eventually forms our Flip-flop. There is one more important thing, a forbidden state exists when both inputs are activated at the same time. This state is not really dangerous in our case but you simply cant really tell how the circuit is gonna react to it, loosing correct state of the machine could cause problems. <br>

In the picture below the raw scematic of a real world Flip-flop is shown. The basic element of the circuit are 2 NAND-Gates, which we can see marked in red. <br>

![Real FF](./docs/realFF.jpg)

**Circuit:** <br>
Now we gona build a small circuit to test this functionality. Our real-world implementatin of the FF reacts when one of the inputs is pulled low. So we simulate the press of a button by simply attatching lose wires, which we can connect manually to simulate a button press. In order to flip we must pick the correct wire, either pink or violet and hold it onto the ground rail (black). <br> This could theoretically also achieved with our Pico. When we connect those two wires to output pins and set them to HIGH state. As soon as we pull the correct one LOW the FF should switch and the other LED should light up. <br>

<br>

**Tipps&Info:**

1. **Resistor values:** The Resistors to protect the LED should be around 300 Ohm, they can be calculated according the formula or with online [tools](https://www.elektronik-kompendium.de/sites/bau/1109111.htm).
<br> The other two Resistors are 100kOhm to pull the signal level of the Nand output HIGH. This need to be done because of the open Drain nature of the NAND IC (Integrated Circuit). <br>

<pre><code>
protection Resistor = Voltage drop over R / I on LED
#Voltage drop over R can be obtained by subtracting forward drop Voltage of the Diode itself from source Voltage 
</code></pre>

2. **LED orientation:** Orientation matters, because when you put them in wrong direction they will simply stop any flow of current try to pass through them. The Anode (+) side needs to be at the side with the higher potential (Voltage) and the Kathode on the GND side. Usually the **longer foot** is the Anode. The position of the protection Resistor doesn't matter.

3. **Breadboard:** On the breadboard the side rails marked with red and blue stripes are connected on the horizontal axis. This color sceme is used as red for positive Voltage level (3.3V in this case) and blue as ground (GND) potential. <br>
The inside of the breadboard is connected vertical a-e and f-j. You can see this in the green highlighted holes which forming a path in vertical direction for every connection. <br>

4. **IC Chip:** On the IC (CD40107BE) there is a dot. This dot usually referes to pin 1 on the Chip. In the scematic pin number 1 is on the bottom left side. Directly above you see the red VCC (source Voltage) wire and in the bottom right with the black wire sits the GND connection. More details in the [datasheet](https://html.alldatasheet.com/html-pdf/26840/TI/CD40107/73/3/CD40107.html), on page 3 you can find the pinout sceme.

![Circuit FF](./docs/lec2.png)

<br>

**Important** If you play around and try to connect the circuit with the Pico keep in mind using the 3.3V Output. Otherwise you might damage your controller when applying 5V to its input pins. Therefor lookup the [pinout](./docs/pinoutpico.png) diagram of the pico. Either from internet search or take the link from the above section on of the Pico. (It's the 5th pin on the same side as the VBUS Pin, VBUS is 1st)

<br>
<pre><code>
#code may look like
from machine import Pin
import time

#declare pins & variables
state=True
s = Pin(20, Pin.OUT)  #initialize pin 20 and set it on output
r = Pin(21, Pin.OUT)  #initialize pin 21 and set it on output
led = Pin(25, Pin.OUT)

s.value(1)
r.value(1)
led.value(0) #output low (GND)

#s while loop will loop as long as the condition (True in this cause) will get false (wont happen in this case)
while True:
    s.value(not state)
    r.value(state)
    time.sleep_ms(1) #sleeps a millisecond
    s.value(1)
    r.value(1)
    #this is an if statement simply it triggers the if-part when state is true or hops in else-part otherwise
    if state:
        state=False #if true set false
    else:
        state=True #else set true
    time.sleep(5) #sleep 5 sec
    #hopps to the top of the while loop

</code></pre>

</p>

<br>

---
## Lection 3: DFPlayer-mini
---
For more detailed information on the module visit [here](https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299). I already provided some information about it at the the Basics part, it is not mandatory to know all the details. <br>

Now we gona test the function of the DFPlayer module. Build your circuit on the breadboard according the scematic. There is no shifting of voltage level required, the DFplayer-mini outputs 3.3V for its communication. <br>


![Circuit DFPlayer](./docs/lec3.png)

Then you have to upload the 0001.mp3 file from the mp3 folder to the SD-card. The naming of the file is important to work with the selected library for this module. <br>
Load the dfplayer_example.py onto the Pico. When you look at the code you will notice that we import something, in this case this is not part of the standard library so we will need to deploy that code too on the Pico. Again simply save it with the correct name dfplayermini.py onto the controller. <br>
If you hit the play sign again it should start with the programm, in this case it should play the beginning of a song for about 15 seconds and then lower the volume until it reaches 0. Then the song should stop and the device should go back to sleep. <br>

See the code here: [dfplayer_example.py](./code/dfplayer_example.py) <br>

Changing the code is pretty simple i'll provide an example of some functions from the library and how to use them: <br>
<pre><code>
code here follow soon!
# In order to use the functions we need to use the created object instance of the dfplayer library
# first we need to initialize our Player class object
player123 = Player(pin_TX=machine.Pin(0), pin_RX=machine.Pin(1)) # player123 naming is not relevant an can be changed
player123.awake() # wakeup the module

# how to play tracks
# folder id is optional, keep in mind that files without folder are played in order of their creation not by the actuall number!
# to avoid interupt playing we may set a delay, or use an aditional wire to indicate if the module is busy or not (i'll use delay, for now)
player123.play(track_id, folder_id)

# this will pause the sound
player123.pause()

# we can resume to play
player123.resume()

# volume change
player123.volume(40) #value can be adjusted

# module options
player123.module_reset()
player123.module_wake()
player123.module_sleep()

# there are more options available but these are the most important ones
</code></pre>

It is also possible to use this device manually. Take a loose wire (grey in the sketch) connected to GND and tipp shortly on the **IO_2** Pin to select the next track. The corresponding Pin you can find [above](#df-mini-player). This will play the whole song. When holding this pin we can adjust the Volume, therefor look up the functions from the table in the "Notes". When working with the loose wire avoid connecting it directly to VCC, this will short the circuit. To avoid this problem you might add a resistor of any value above 1k to this wire in series. <br>

---
## Lection 4: Analog Input
---

<p>
This section is a short reminder on how to use the ADC (Analog digital conveter) of the Pico. Altough a potentiometer would be perfectly suited for this task we need to calibrate our moiture sensor anyway. <br>
Now were gona prepare our capacitive moisture sensor. The sensor will be powered from the 3.3V output of the Pico. This way we do not need a voltage devider to convert the analog signal into save range for our controller (not 5V tollerant). We need to calibrate the sensors threshold values, to estimate if the plant pot is dry or wet.
Therefore we will need a cup of water, the plant pot could also help as well. We want to define boarders for our measured values to decide if the measurement was ok or we got some kind of error. <br>

Build up the circuit according to the following: <br>
![moisture sensor](./docs/lec4.png)

<br>
Now upload the code to the Pico:

<br>

When these steps are completed we can start with our calibration. Don't forgett to hit the run button as soon as you have uploaded this code below onto the Pico. First take a measurement of the sensor while in air. Writte down this value somewhere as we need it later. Measurements higher than this value are neglectable so they mark the upper boarder of our sensor values. Now hold the sensor into the cup of water, it is important to instert the sensor only up to the white line! Hit the run button again, the measurements now represent the lower boarder. <br>
With these two boarder values we defined our measurement range. When you put the sensor into the plant pot we get a feeling on realistic values. In order to prevent future problems set the boarder boundary a bit wider than the measured values might be a good idea. <br>
Later when we try to decide if our plant pot is dry or not we will define a boarder value within the measurement range. When the measurement passes this value we can decide on how to react in the final goal we will, then play a random track to signal the plants needs. <br>

Upload the [code](./code/lec4_0.py):
<pre><code>
from machine import Pin, I2C, ADC

#set analog pin
analog_value = ADC(28)

#defined global variables
_up = 44068.67 #represent analog reading in air
_low = 17736.8 #analog reading while in water

#take multiple measurements, for better accuracy
vals=[0] * 60 #create empty ist with 60 positions
for index, element in enumerate(vals): #iterate over list
    vals[index]=analog_value.read_u16() #fill list with readings
#derive the average analog measurement
val_raw = sum(vals) / len(vals)

print(val_raw)
</code></pre>

When you replaced my values we can now think about a more practical example on how to use this sensor. You might read through and get the basic idea of the [code](./code/lec4.py): below, or upload and thest the sensor under real conditions in a plant.

<pre><code>
from machine import Pin, I2C, ADC
import time

#defined global variables
_up = 44068.67 #represent analog reading
_low = 17736.8

#boundarys for plant condition (percent of soil moisture)
limit_u = 65 #upper boundary (100% --> pure water)
limit_l = 45 #lower boundary (0% --> air)

#set analog pin
analog_value = ADC(28)

# function calculate relative moisture in percent
def rel_moisture(val):
    #sanity check
    if val > _up:
        print(f'Warning: measured value ({val}) greater than upper boarder ({_up})')
        val=_up
    if val < _low:
        print(f'Warning: measured value ({val}) smaller than lower boarder ({_low})')
        val=_low
    #calculate percent value
    perc = int((val-_low)*100/(_up-_low)) #between 0 and 100
    perc = 100-perc #invert the result for better readability
    print(f"Soil Moisture: {perc}% ")
    return perc

#take multiple measurements, for better accuracy
vals=[0] * 60 #create empty ist with 60 positions
for index, element in enumerate(vals): #iterate over list
    vals[index]=analog_value.read_u16() #fill list with readings
#derive the average analog measurement
val_raw = sum(vals) / len(vals)

#pass raw measurement value in relative mositure funciton to get percent value
val = rel_moisture(val_raw)
print(val)

if val < limit_u:
    #do something
    print('I need water!')
elif val > limit_l:
    #do something
    print('I am drowning!')
else:
    print('I feel fine')
</code></pre>

</p>


---
## Lection 5: Real-time-clock DS3231
---

<p>

In this lection we take a short look on the [RTC](#ds3231-rtc-module) module and check its functionality. We will initially set the clock time, as long as its battery is connected the device should be synchronous. The module should be able to keep track of accurate time ofer long periods. <br> Keep in mind if you use a different Microcontroller that you have to shift the Voltage levels. Because our Pico outputs 3.3V on its Digital pins we do not risk damaging the RTC Module or the Pico. <br>
Now upload the following code snipet, it should simply set the given time and then print the time every 5 seconds. If we just want to read the time afterwards uncoment the statment where we set the time of the device.

Build up the circuit according to the following: <br>
![ds3231 module](./docs/lec5.png)

<br>

Usually you just have to set the time once, when a battery is inserted it should be able to keep the time for long periods.
Upload the [code](./code/lec5.py) and the used [library](./code/ds3231_impl.py):
<pre><code>
from ds3231_impl import ds3231
import time

I2C_PORT = 0
I2C_SDA = 16
I2C_SCL = 17

rtc = ds3231(I2C_PORT,I2C_SCL,I2C_SDA) #init serial communication with RTC module
time.sleep_ms(20) #give init process some time
rtc.set_time('13:26:25,Tuesday,2022-03-22') #set rtc time uncomment if not wanted
time.sleep_ms(20)

while 1:
    print(rtc.read_time()) #read time and print it
    time.sleep(5) #sleep 5 seconds
</code></pre>




</p>
