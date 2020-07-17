# alarm
I need an alarm for my garage.

## Prerequisites

You need to have:
- **Risco ShockTec** [RK601SM0000B](https://www.riscogroup.com/italy/products/product/2694) sismic sensor
- [**Raspberry Pi**](https://www.raspberrypi.org/)

## Electronics

The circuit is built using a Raspberry Pi as controller, and a Risco ShockTec RK601SM0000B as thief detection sensor.

### Sensor

**Risco ShockTec RK601SM0000B** is a NC (Normally Closed) sensor. If you give him a 3.3v tension so, you'll read 3.3v on the other side if is all ok, 0v if the sensor triggered (or the sensor is broken).

Risco ShockTec RK601SM0000B has 3 switches to determine why the alarm flag is raised:
- **Tamper**: There is a switch with a spring on the PCB inside the sensor. If someone tries to open it, it triggers. This triggers even if someone tries to use a magnet to "confuse" the sensor.
- **Reed**: A Reed sensor is placed on the PCB. This detects the presence of the magnet given with the sensor.
- **Alarm**: Triggers when the frequency of the vibrancy is inside the "thief" range (there is someone hammering on the window for example).

### Overall circuit

To wire this circuit you have to choose 3 free GPIO on your Raspberry Pi, and wire that as shown in the figure below.
The sensor requires external power supply (in the manual is said between 9v and 16v, i used a 12v power supply), you need to wire it as shown in the figure below.

- GPIO_X: Is the pin to wire on Raspberry Pi for reading the Alarm Switch.
- GPIO_Y: Is the pin to wire on Raspberry Pi for reading the Reed Switch.
- GPIO_Z: Is the pin to wire on Raspberry Pi for reading the Tamper Switch.

![wiring](https://raw.githubusercontent.com/thanh-guong/alarm/master/image/circuit.jpg)