# annoying_plant
---
## About
<p>
This is a talking plant project requiring a RaspberryPi Pico a DF-mini player module as well as a DS-3231 RTC-module (Real time clock).
 The main purpose of the project is a beginner friendly diy experience.
 Using Python as a quite easy to learn language and very simple basic modules and circuits.
 It should give a small insight into the world of microcontrollers and what they are capable of.
 <br>
 I provided a short BASICS summary, to explain briefly basic functionalities in Python and electronics.
 </p>

---
## Basics
---
### Modules & ICs
---
#### DS3231 RTC Module
<p>
The DS3231 is a low-cost, extremely accurate I²C real-time clock (RTC) with an integrated temperature-compensated crystal oscillator (TCXO) and crystal. The device incorporates a batteryslott. When running this Module on active supply voltage it is advised to cut XXXXXXXX if you use a battery. Recharging a non-rechargeable battery is dangerous. It should be avoided at all costs.
CMOS Open-Drain
</p>

#### NAND Gate
<p>
 text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text 
</p>

#### DF-mini-player
<p>
 text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text 
</p>

---
### Electronic Basics
---
If you are somewhat experienced you can skip this part, as it is mainly to explain the basic function of commonly used electronic parts.

#### ***Ohm's law:***
<p>
Probably the most common basic is that electric energy flow in form of electrons from higher to lower Voltage levels. The amount of current flowing through your wires is depending on the Resistance of the path the electrons are traveling. This leads to a well-known and Basic formula: U=R*I.
<br>
<pre><code>U=R*I
U is our Voltage, R is the value of our Resistance in Ohm and I stand for the amount of current in Ampere.
</code></pre>
That to be said let’s think about that law quickly, everything including wires have a certain value for Resistance. With a shorted wire from Voltage source to ground we usually can expect almost infinite amount of energy to flow (wire resistance really low - close to 0). <br> When we add an Resistor with let’s say 1000 Ohm and our source provides 5V like every USB plug a current of 0.001 Ampere should flow (1mA). The formula used for this comes from Ohm's law I=U/R as you can see this simple formula is quite easy to use and will appear quite often from now on. <br>
I want to add a short reminder on how to calculate resistance. Resistors in series can be added together. For parallel resistors it’s a little different, ******************
</p>


#### ***Electronic components:***
Only some important parts are listed for this project.
- **Resistor:** As it can be found above, this part have a resistance in Ohm. Often used to limit the current flowing through a path. <br>
*Example:*  Limiting the amount of current flowing through LED's or Pulling Wires to a certain level while not shorting the circuit. For example, if something needs a signal default High on the input it can be realized with a Pull-up resistor to the supply voltage. When the Input is pulled low then only limited current from the source flows through the resistor.
- **Transistor:** The electronic equivalent of a switch. With two main categories, MOSFET YYYYYYYYYYYYYY and Bipolar YYYYYYYY. Both of them comes with N- and P-doped variants. The range of application is wide. They can be used as amplifier or simply as switches. For our purpose only the use of as switch (in saturation) is relevant. <br>
*Example:* Using an Npn bipolar transistor we could switch High currents directly from the source. Without risk to damage a Pin of the microcontroller due to overload.
- **Diode:** Is an electrical component that allow current to flow only in one direction. <br>
*Example:* Often used as rectifiers. A special case among diodes are LED, when current flows through them they emit light of a certain wave length.
- **Capacitor:** Capacitors are Conducting plates parallel to each other. They are able to draw energy from a source and store it. Inside the two metal plates separated by a non-conducting substance. When activated, a capacitor quickly releases electricity in a tiny fraction of a second. <br>
*Example:* They can be used to flatten fluctuation supply. Placed close to the supply Pins of any IC (integrated circuit) a capacitor stabilize the IC’s voltage supply.

---
### Savety
---

<p>
Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text Text  
</p>

---
### RaspberryPi Pico
---
<p>
Raspberry Pi Foundation entrance in the world of microcontrollers. The company itself is well known for its single board computers. This much smaller module comes with a fairly good price. The difference between the bigger RaspberryPi's is that not supposed to be a whole computer. Therefore it comes with less computing power and programmable memory space and probably more important no Operating system. That to be said you program the function of the module on your own. It is also suitable for low power applications because it does not need that much power.
<br>
The technical aspects can be found in the Datasheet linked below:
The board itself is powered by a MicroUSB connection this refers also as VBUS Pin and need to be 5V or it can be powered by or directly at the VSYS Pin in the range of 1.8-5.5 V. It is important to strictly following the datasheet here to avoid damage to our controller. <br>
The Pico is powered by the RP-2040 Chip sitting in the middle of the board, avoid touching the Pins of the Chip itself directly because electrostatic charge from your hands can damage it. To control the processor microPython or with a little effort C++ can be used, more to that later.
<br>
We can now program the Pin’s of the module to switch HIGH/LOW or read analog Signals (Voltage levels). This offers a wide range of possible applications which can be easy realized, we just need to be aware of some basic concepts to not risk damaging the module itself. Although it is usually quite resistant to little accidents in a certain extent. <br>
The Output capability of the Pico is limited, for switching higher loads its important to not exceed the parts limits. Measure negative voltages is neither a good idea because it can damage the part.
</p>

<br>

[Pinout source](http://land-boards.com/blwiki/images/thumb/5/56/Raspberry-Pi-Pico-Pinout.jpg/730px-Raspberry-Pi-Pico-Pinout.jpg) <br>
[Datasheet source](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)

<br>

---
### microPython
---

MicroPython is a efficient implementation of the Python 3 programming language and is optimised to run on microcontrollers and in constrained environments, like our Pico. It includes a small subset of the Python standard librarys, but its more than sufficient to the needs of this project. <br>
We will use Thonny to write our python code. Its a beginnerfriendly easy to use IDE perfectly fitting the needs to run all kinds of electronic projects. <br>
<br>

latest version of [Thonny](https://thonny.org/)
<br>



