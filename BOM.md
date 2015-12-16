# Bill of Materials for dap42 revision 2 (dap42v2)
Unless otherwise specified, all resistors, capacitors, and LEDs are in 0603 packages.

Unspecified part numbers are either generic with (virtually) no design constraints, or were not sourced from a distributor with an offical part number.

RefDes | P/N | Notes
---|------------------------|------------
U1 | STM32F042F6            | STM32F042F6
U2 | MIC5504-3.3YM5         | 5V -> 3.3V LDO, SOT-23-5
S1 | ADTSM31NV              | Momentary pushbutton, bootloader enable
S2 | ADTSM31NV              | Momentary pushbutton, reset
J1 | | Mini-USB type B connector
J2 | GoPortHeader_th_10pack<sup>[1](#f1)</sup> | 0.05" pitch, 2x5 shrouded male socket, SWD debug header for the dap42
J3 | GoPortHeader_th_10pack<sup>[1](#f1)</sup> | 0.05" pitch, 2x5 shrouded male socket, SWD debug header for the target
J4 | | 0.1" pitch, 4-pin header for external UART
J5 | | 0.1" pitch, 4-pin header for 3.3V and 5V power and ground
D1 | | LED, LED0/Connected
D2 | | LED, LED1/Running
D3 | | LED, LED2/USB activity
R1 | | 1kOhm
R2 | | 1kOhm
R3 | | 1kOhm
R4 | | 10kOhm
C1 | | 0.1uF
C2 | | 0.1uF
C3 | | 0.1uF
C4 | | 1uF
C5 | | 1uF

---
<sup id="f1">1. P/N is for a 10-pack of shrouded headers, can also substitute unshrouded male headers</sup>
