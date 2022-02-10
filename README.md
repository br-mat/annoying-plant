# anoying_plant

## About
 <p>
 This is a talking plant project with RaspberryPi Pico and a DF-mini player module as well as an DS-3231 RTC-module (Real time clock).
 The main purpose of the project is a beginner friendly diy experience.
 Using Python as a quite easy to learn language and very simple basic modules and circuits.
 It should give a small insight into the world of microcontrollers and what they are capable of.
 <br>
 I provided a short BASICS summary, to explain briefly basic functionalities in Python and electronics.
 </p>
## Basics
### Electronic Basics
<p>
Probably the most common basic is that electric energy flow in form of electrons from higher to lower Voltage levels. The amount of current flowing through your wires is depending on the Resistance of the path the electrones are traveling. This leads to a well known and Basic formula: U=R*I.
<br>
<pre><code>
U=R*I -- U is our Voltage, R is the value of our Resistance in Ohm and I stands for the amount of current in Ampere.
</code></pre>
That to be said lets think about that law quickly, everything including wires have a certain value for Resistance. With a shorted wire from Voltage source to ground we usually can expect almost infinite amount of energy to flow (wire resistance really low - close to 0). When we add an Resistor with lets say 1000 Ohm and our source provides 5V like every USB plug a current of 0.001 Ampere should flow (1mA). The formula used for this comes from Ohm's law I=U/R as you can see this simple formula is quite easy to use and will apear quite ofthen from now on. <br>
I want too add a short reminder on how to calculate resistance. Resistors in series can be added together. For paralell resistors its a little different, ******************
</p>

### Savety
<p>
 
</p>

### RaspberryPi Pico
<p>
Raspberry Pi Foundation entrance in the world of microcontrollers. The company itself is well known for its single board computers. This much smaller module comes with a fairly good price. The difference between the bigger RaspberryPi's is that not supposed to be a whole computer. Therfor it comes with less computing power and programmable memory space and probably more important no Operating system. That to be said you programm the function of the module on your own. It is also suitable for low power aplications because it does not need that much power.
<br>
The technical aspects can be found in the Datasheet linked below:
The board itself is powered by a MicroUSB connection this refers also as VBUS Pin and need to be 5V or it can be powered by or directily at the VSYS Pin in the range of 1.8-5.5 V. It is important to strictly folowing the datasheet here to avoid damage to our controller. <br>
The Pico is powered by the RP-2040 Chip sitting in the middle of the board, avoid touching the Pins of the Chip itself directly because electrostatic charge from your hands can damage it. Tho controll the processor microPython or with a little effort C++ can be used, more to that later.
<br>
We can now programm the Pins's of the module to switch HIGH/LOW or read analog Signals (Voltage levels). This offers a wide range of possible applications which can be easy realised, we just need to be aware of some basic concepts to not risk damaging the module itself. Altough it is usually quite resistant to little acidents in a certain extent.

</p>
Pinout source: "http://land-boards.com/blwiki/images/thumb/5/56/Raspberry-Pi-Pico-Pinout.jpg/730px-Raspberry-Pi-Pico-Pinout.jpg"
Datasheet source: "https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf"

### microPython
<p>
 
</p>
