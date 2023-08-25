EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:myLibrary
LIBS:MF_Aesthetics
LIBS:Rgb7Hat-cache
EELAYER 25 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 3 4
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L AD-121F2 D1
U 1 1 59B77441
P 7900 3900
AR Path="/59D957A3/59B77441" Ref="D1" Part="1"
AR Path="/59D95871/59B77441" Ref="D3" Part="1"
F 0 "D3" H 7050 4750 50 0000 L CNN
F 1 "AD-121F2" H 7050 4650 50 0000 L CNN
F 2 "myLibrary:AD-121F2" H 7900 3900 50 0001 C CNN
F 3 "" H 7900 3900 50 0001 C CNN
F 4 "Single Digit 7-segment RGB LED Display, 1-inch digit height, common anode" H 7900 3900 60 0001 C CNN "description"
F 5 "AD-121F2" H 7900 3900 60 0001 C CNN "mpn"
	1    7900 3900
	1    0    0    -1  
$EndComp
$Comp
L TLC5947DAP U4
U 1 1 59B77464
P 3500 4000
AR Path="/59D957A3/59B77464" Ref="U4" Part="1"
AR Path="/59D95871/59B77464" Ref="U5" Part="1"
F 0 "U5" H 2950 5500 50 0000 L CNN
F 1 "TLC5947DAP" H 2950 5400 50 0000 L CNN
F 2 "Housings_SSOP:HTSSOP-32_6.1x11mm_Pitch0.65mm_ThermalPad" H 3500 4000 50 0001 C CNN
F 3 "" H 3500 4000 50 0001 C CNN
F 4 "24-Channel, 12-Bit PWM LED Driver, HTSSOP" H 3500 4000 60 0001 C CNN "description"
F 5 "TLC5947DAP" H 3500 4000 60 0001 C CNN "mpn"
	1    3500 4000
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR8
U 1 1 59B778E2
P 3700 2300
AR Path="/59D957A3/59B778E2" Ref="#PWR8" Part="1"
AR Path="/59D95871/59B778E2" Ref="#PWR12" Part="1"
F 0 "#PWR12" H 3700 2150 50 0001 C CNN
F 1 "VCC" H 3700 2450 50 0000 C CNN
F 2 "" H 3700 2300 50 0001 C CNN
F 3 "" H 3700 2300 50 0001 C CNN
	1    3700 2300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR10
U 1 1 59B77905
P 3500 5600
AR Path="/59D957A3/59B77905" Ref="#PWR10" Part="1"
AR Path="/59D95871/59B77905" Ref="#PWR14" Part="1"
F 0 "#PWR14" H 3500 5350 50 0001 C CNN
F 1 "GND" H 3500 5450 50 0000 C CNN
F 2 "" H 3500 5600 50 0001 C CNN
F 3 "" H 3500 5600 50 0001 C CNN
	1    3500 5600
	1    0    0    -1  
$EndComp
$Comp
L CP1 C9
U 1 1 59B79947
P 6400 1900
AR Path="/59D957A3/59B79947" Ref="C9" Part="1"
AR Path="/59D95871/59B79947" Ref="C11" Part="1"
F 0 "C11" H 6425 2000 50 0000 L CNN
F 1 "100uF" H 6425 1800 50 0000 L CNN
F 2 "Capacitors_SMD:CP_Elec_6.3x7.7" H 6400 1900 50 0001 C CNN
F 3 "" H 6400 1900 50 0001 C CNN
F 4 "Capacitor Aluminum Electrolytic 6.3mm 100uF 20% 35V" H 6400 1900 60 0001 C CNN "description"
F 5 "MF-CAP-6.3MM-100uF" H 6400 1900 60 0001 C CNN "mpn"
	1    6400 1900
	1    0    0    -1  
$EndComp
$Comp
L VCC #PWR9
U 1 1 59B799AD
P 2700 4900
AR Path="/59D957A3/59B799AD" Ref="#PWR9" Part="1"
AR Path="/59D95871/59B799AD" Ref="#PWR13" Part="1"
F 0 "#PWR13" H 2700 4750 50 0001 C CNN
F 1 "VCC" H 2700 5050 50 0000 C CNN
F 2 "" H 2700 4900 50 0001 C CNN
F 3 "" H 2700 4900 50 0001 C CNN
	1    2700 4900
	1    0    0    -1  
$EndComp
$Comp
L C C10
U 1 1 59B79BCD
P 2700 5150
AR Path="/59D957A3/59B79BCD" Ref="C10" Part="1"
AR Path="/59D95871/59B79BCD" Ref="C12" Part="1"
F 0 "C12" H 2725 5250 50 0000 L CNN
F 1 "0.1uF" H 2725 5050 50 0000 L CNN
F 2 "Capacitors_SMD:C_0402" H 2738 5000 50 0001 C CNN
F 3 "" H 2700 5150 50 0001 C CNN
F 4 "Capacitor MLCC 0402 0.1uF 10% 16V" H 2700 5150 60 0001 C CNN "description"
F 5 "MF-CAP-0402-0.1uF" H 2700 5150 60 0001 C CNN "mpn"
	1    2700 5150
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR7
U 1 1 59B79DA4
P 6400 2150
AR Path="/59D957A3/59B79DA4" Ref="#PWR7" Part="1"
AR Path="/59D95871/59B79DA4" Ref="#PWR11" Part="1"
F 0 "#PWR11" H 6400 1900 50 0001 C CNN
F 1 "GND" H 6400 2000 50 0000 C CNN
F 2 "" H 6400 2150 50 0001 C CNN
F 3 "" H 6400 2150 50 0001 C CNN
	1    6400 2150
	1    0    0    -1  
$EndComp
$Comp
L LED_ARGB D2
U 1 1 59E01D76
P 5050 6000
AR Path="/59D957A3/59E01D76" Ref="D2" Part="1"
AR Path="/59D95871/59E01D76" Ref="D4" Part="1"
F 0 "D4" H 5050 6370 50 0000 C CNN
F 1 "LED_ARGB" H 5050 5650 50 0000 C CNN
F 2 "LEDs:LED_Cree-PLCC4_3.2x2.8mm_CCW" H 5050 5950 50 0001 C CNN
F 3 "" H 5050 5950 50 0001 C CNN
F 4 "Tri-Color RGB LED 3228 SMD PLCC-4" H 5050 6000 60 0001 C CNN "description"
F 5 "MF-LED-3228-RGB" H 5050 6000 60 0001 C CNN "mpn"
	1    5050 6000
	1    0    0    -1  
$EndComp
$Comp
L R R7
U 1 1 59E028E7
P 1550 4500
AR Path="/59D957A3/59E028E7" Ref="R7" Part="1"
AR Path="/59D95871/59E028E7" Ref="R9" Part="1"
F 0 "R9" V 1630 4500 50 0000 C CNN
F 1 "4.7K" V 1550 4500 50 0000 C CNN
F 2 "Resistors_THT:R_Axial_DIN0204_L3.6mm_D1.6mm_P5.08mm_Horizontal" V 1480 4500 50 0001 C CNN
F 3 "" H 1550 4500 50 0001 C CNN
F 4 "RES 4.7K OHM 1/4W 1% AXIAL" H 1550 4500 60 0001 C CNN "description"
F 5 "RNMF14FTC4K70" H 1550 4500 60 0001 C CNN "mpn"
	1    1550 4500
	1    0    0    -1  
$EndComp
Text HLabel 6100 1650 0    60   Input ~ 0
VLED
Text HLabel 2100 3800 0    60   Input ~ 0
BLANK
Text HLabel 2100 3900 0    60   Input ~ 0
XLAT
Text HLabel 2100 4000 0    60   Input ~ 0
SCLK
Text HLabel 2100 4100 0    60   Input ~ 0
SIN
Text HLabel 2100 4200 0    60   Output ~ 0
SOUT
Wire Wire Line
	3700 2300 3700 2500
Wire Wire Line
	3400 5500 3400 5400
Wire Wire Line
	1550 5500 3600 5500
Wire Wire Line
	3600 5500 3600 5400
Wire Wire Line
	3500 5600 3500 5500
Wire Wire Line
	2100 4200 2800 4200
Wire Wire Line
	2100 4100 2800 4100
Wire Wire Line
	2100 4000 2800 4000
Wire Wire Line
	2100 3900 2800 3900
Wire Wire Line
	2100 3800 2800 3800
Wire Wire Line
	1550 3700 2800 3700
Wire Wire Line
	4200 2800 6450 2800
Wire Wire Line
	6450 2800 6450 3700
Wire Wire Line
	6450 3700 6900 3700
Wire Wire Line
	4200 2900 6350 2900
Wire Wire Line
	6350 2900 6350 3800
Wire Wire Line
	6350 3800 6900 3800
Wire Wire Line
	4200 3000 6250 3000
Wire Wire Line
	6250 3000 6250 3900
Wire Wire Line
	6250 3900 6900 3900
Wire Wire Line
	4200 3100 6150 3100
Wire Wire Line
	6150 3100 6150 4000
Wire Wire Line
	6150 4000 6900 4000
Wire Wire Line
	4200 3200 6050 3200
Wire Wire Line
	6050 3200 6050 4100
Wire Wire Line
	6050 4100 6900 4100
Wire Wire Line
	4200 3300 5950 3300
Wire Wire Line
	5950 3300 5950 4200
Wire Wire Line
	5950 4200 6900 4200
Wire Wire Line
	4200 3400 5850 3400
Wire Wire Line
	5850 3400 5850 4300
Wire Wire Line
	5850 4300 6900 4300
Wire Wire Line
	4200 3500 5750 3500
Wire Wire Line
	5750 3500 5750 4400
Wire Wire Line
	5750 4400 6900 4400
Wire Wire Line
	4200 3600 5650 3600
Wire Wire Line
	5650 3600 5650 4500
Wire Wire Line
	5650 4500 6900 4500
Wire Wire Line
	4200 3700 5550 3700
Wire Wire Line
	5550 3700 5550 2700
Wire Wire Line
	5550 2700 9050 2700
Wire Wire Line
	9050 2700 9050 3400
Wire Wire Line
	9050 3400 8900 3400
Wire Wire Line
	4200 3800 5450 3800
Wire Wire Line
	5450 3800 5450 2600
Wire Wire Line
	5450 2600 9150 2600
Wire Wire Line
	9150 2600 9150 3500
Wire Wire Line
	9150 3500 8900 3500
Wire Wire Line
	4200 3900 5350 3900
Wire Wire Line
	5350 3900 5350 2500
Wire Wire Line
	5350 2500 9250 2500
Wire Wire Line
	9250 2500 9250 3600
Wire Wire Line
	9250 3600 8900 3600
Wire Wire Line
	4200 4000 5250 4000
Wire Wire Line
	5250 4000 5250 2400
Wire Wire Line
	5250 2400 9350 2400
Wire Wire Line
	9350 2400 9350 3700
Wire Wire Line
	9350 3700 8900 3700
Wire Wire Line
	4200 4100 5550 4100
Wire Wire Line
	5550 4100 5550 4700
Wire Wire Line
	5550 4700 9050 4700
Wire Wire Line
	9050 4700 9050 3800
Wire Wire Line
	9050 3800 8900 3800
Wire Wire Line
	4200 4200 5450 4200
Wire Wire Line
	5450 4200 5450 4800
Wire Wire Line
	5450 4800 9150 4800
Wire Wire Line
	9150 4800 9150 3900
Wire Wire Line
	9150 3900 8900 3900
Wire Wire Line
	4200 4300 5350 4300
Wire Wire Line
	5350 4300 5350 4900
Wire Wire Line
	5350 4900 9250 4900
Wire Wire Line
	9250 4900 9250 4000
Wire Wire Line
	9250 4000 8900 4000
Wire Wire Line
	4200 4400 5250 4400
Wire Wire Line
	5250 4400 5250 5000
Wire Wire Line
	5250 5000 9350 5000
Wire Wire Line
	9350 5000 9350 4100
Wire Wire Line
	9350 4100 8900 4100
Wire Wire Line
	4200 4500 5150 4500
Wire Wire Line
	5150 4500 5150 5100
Wire Wire Line
	5150 5100 9450 5100
Wire Wire Line
	9450 5100 9450 4200
Wire Wire Line
	9450 4200 8900 4200
Wire Wire Line
	4200 4600 5050 4600
Wire Wire Line
	5050 4600 5050 5200
Wire Wire Line
	5050 5200 9550 5200
Wire Wire Line
	9550 5200 9550 4300
Wire Wire Line
	9550 4300 8900 4300
Wire Wire Line
	4200 4700 4950 4700
Wire Wire Line
	4950 4700 4950 5300
Wire Wire Line
	4950 5300 9650 5300
Wire Wire Line
	9650 5300 9650 4400
Wire Wire Line
	9650 4400 8900 4400
Wire Wire Line
	4200 4800 4850 4800
Wire Wire Line
	4850 4800 4850 5400
Wire Wire Line
	4850 5400 9750 5400
Wire Wire Line
	9750 5400 9750 4500
Wire Wire Line
	9750 4500 8900 4500
Wire Wire Line
	2700 4900 2700 5000
Wire Wire Line
	2700 5300 2700 5500
Wire Wire Line
	6900 3300 6800 3300
Wire Wire Line
	6800 3300 6800 1650
Wire Wire Line
	6100 1650 10100 1650
Wire Wire Line
	6400 1750 6400 1650
Wire Wire Line
	6400 2050 6400 2150
Wire Wire Line
	4200 4900 4750 4900
Wire Wire Line
	4750 4900 4750 5800
Wire Wire Line
	4750 5800 4850 5800
Wire Wire Line
	4200 5000 4650 5000
Wire Wire Line
	4650 5000 4650 6000
Wire Wire Line
	4650 6000 4850 6000
Wire Wire Line
	4200 5100 4550 5100
Wire Wire Line
	4550 5100 4550 6200
Wire Wire Line
	4550 6200 4850 6200
Wire Wire Line
	5250 6000 10100 6000
Wire Wire Line
	10100 6000 10100 1650
Wire Wire Line
	1550 3700 1550 4350
Wire Wire Line
	1550 4650 1550 5500
Connection ~ 3500 5500
Connection ~ 3400 5500
Connection ~ 2700 5500
Connection ~ 6400 1650
Connection ~ 6800 1650
$EndSCHEMATC
