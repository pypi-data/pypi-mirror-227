# version: Python3
from DobotEDU import *
import tkinter as tk
from tkinter import *
import customtkinter as ct

#Dobot Configuration
dobot_magician.set_iomultiplexing("DO_01", 3)
magician.set_multiplexing(io="DO_01", multiplex=3)
magician.set_multiplexing(io="DO_02", multiplex=3)
magician.set_multiplexing(io="DO_03", multiplex=3)
magician.set_multiplexing(io="DO_04", multiplex=3)
magician.set_multiplexing(io="DO_05", multiplex=3)
magician.set_multiplexing(io="DO_06", multiplex=3)
magician.set_multiplexing(io="DO_07", multiplex=3)
magician.set_multiplexing(io="DO_08", multiplex=3)
magician.set_multiplexing(io="DO_09", multiplex=3)
magician.set_multiplexing(io="DO_10", multiplex=3)
magician.set_multiplexing(io="DO_11", multiplex=3)
magician.set_multiplexing(io="DO_12", multiplex=3)
magician.set_multiplexing(io="DO_13", multiplex=3)
magician.set_multiplexing(io="DO_14", multiplex=3)
magician.set_multiplexing(io="DO_14", multiplex=2)
magician.set_multiplexing(io="DO_15", multiplex=3)
magician.set_multiplexing(io="DO_15", multiplex=1)
magician.set_multiplexing(io="DO_16", multiplex=3)
magician.set_multiplexing(io="DO_17", multiplex=3)
magician.set_multiplexing(io="DO_18", multiplex=3)
magician.set_multiplexing(io="DO_19", multiplex=3)
magician.set_multiplexing(io="DO_20", multiplex=3)

magician.set_pwm(io="DO_14", freq=0, cycle=50)
magician.set_do(io="DO_15", level=0)
#Functions definitions
def slider_event_RT(value):
    valRT=tk.StringVar(value=int(value))
    labelRT = ct.CTkLabel(master=root,
                               textvariable=valRT,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
    labelRT.place(relx=0.3, rely=0.27)
    labelRTM.place_forget()
    freq=(value-0.352)/0.003
    if freq<0:
        freq=0
    magician.set_pwm(io="DO_14", freq=freq, cycle=50)
    valPWMS = tk.StringVar(value=int(freq))
    labelPWMS = ct.CTkLabel(master=root,
                               textvariable=valPWMS,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
    labelPWMS.place(relx=0.43, rely=0.27)
    labelPWMM.place_forget()
def slider_event_CB(value):
    global v
    if v==0:
        value=abs(int(value))
    if v==1:
        value=int(value)*(-1)
    magician.set_converyor(index=magician.Stepper1,enable=True,speed=value)
    valCB=tk.StringVar(value=value)
    labelCB = ct.CTkLabel(master=root,
                               textvariable=valCB,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
    labelCB.place(relx=0.3, rely=0.69)
    labelCBM.place_forget()

    
def stopRT():
    magician.set_pwm(io="DO_14", freq=0, cycle=50)
    valRT=tk.StringVar(value=0)
    labelRT = ct.CTkLabel(master=root,
                               textvariable=valRT,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
    labelRT.place(relx=0.3, rely=0.27)
    sliderRT.set(0)
    print("Stop RT")
    valPWM = tk.StringVar(value=0)
    labelPWM = ct.CTkLabel(master=root,
                               textvariable=valPWM,
                               width=50,
                               height=25,
                               fg_color=("#ececec", "white"),
                               corner_radius=8)
    labelPWM.place(relx=0.43, rely=0.27)
    labelPWMM.place_forget()
def stopCB():
    magician.set_converyor(index=magician.Stepper1,enable=True,speed=0)
    valCBM=tk.StringVar(value=0)
    labelCBM = ct.CTkLabel(master=root,
                               textvariable=valCBM,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
    labelCBM.place(relx=0.3, rely=0.69)
    sliderCB.set(0)
    print("Stop CB")
def GoFront():
    global v
    v=0
    print("CB Front")
def GoBack():
    global v
    v=1
    print("CB Back")    
def GoLeft():
    magician.set_do(io="DO_15", level=1)
    print("RT Left")
def GoRight():
    magician.set_do(io="DO_15", level=0)    
    print("RT Right")   

def X_P():
    global x
    global y
    global z
    global r
    global s
    x=x+s
    magician.ptp(mode=1, x=x, y=y, z=z, r=r)
    PXC = tk.StringVar(value=x)
    labelPXC = ct.CTkLabel(master=root,
                            textvariable=PXC,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
    labelPXC.place(relx=0.65, rely=0.15)
    labelPX.place_forget()

    print(x)
def A_V():
    magician.set_endeffector_gripper(enable=True, on=True)
def SS_V():
    magician.set_endeffector_gripper(enable=True, on=False)
def D_V():
    magician.set_endeffector_gripper(enable=False, on=False)
def S_U():
    global s
    s=1
def S_D():
    global s
    s=10
def S_V():
    global s
    s=20
def X_N():
    global x
    global y
    global z
    global r
    global s
    x=x-s
    magician.ptp(mode=1, x=x, y=y, z=z, r=r)  
    PXC = tk.StringVar(value=x)
    labelPXC = ct.CTkLabel(master=root,
                            textvariable=PXC,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
    labelPXC.place(relx=0.65, rely=0.15)
    labelPX.place_forget()
    print(x)
def Y_P():
    global x
    global y
    global z
    global r
    global s
    y=y+s
    magician.ptp(mode=1, x=x, y=y, z=z, r=r)  
    PYC = tk.StringVar(value=y)
    labelPYC = ct.CTkLabel(master=root,
                            textvariable=PYC,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
    labelPYC.place(relx=0.72, rely=0.15)
    labelPY.place_forget()
    print(y)
def Y_N():
    global x
    global y
    global z
    global r
    global s
    y=y-s
    magician.ptp(mode=1, x=x, y=y, z=z, r=r)
    PYC = tk.StringVar(value=y)
    labelPYC = ct.CTkLabel(master=root,
                            textvariable=PYC,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
    labelPYC.place(relx=0.72, rely=0.15)
    labelPY.place_forget()
    print(y)
def Z_P():
    global x
    global y
    global z
    global r
    global s
    z=z+s
    magician.ptp(mode=1, x=x, y=y, z=z, r=r)
    PZC = tk.StringVar(value=z)
    labelPZC = ct.CTkLabel(master=root,
                            textvariable=PZC,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
    labelPZC.place(relx=0.9, rely=0.15)
    print(z)
def Z_N():
    global x
    global y
    global z
    global r
    global s
    z=z-s
    magician.ptp(mode=1, x=x, y=y, z=z, r=r)
    PZC = tk.StringVar(value=z)
    labelPZC = ct.CTkLabel(master=root,
                            textvariable=PZC,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
    labelPZC.place(relx=0.9, rely=0.15)

    print(z)
def R_P():
    global x
    global y
    global z
    global r
    global s
    r=r+s
    magician.ptp(mode=1, x=x, y=y, z=z, r=r)
    PRC = tk.StringVar(value=r)
    labelPRC = ct.CTkLabel(master=root,
                            textvariable=PRC,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
    labelPRC.place(relx=0.97, rely=0.15)
    labelPR.place_forget()
    print(r)
def R_N():
    global x
    global y
    global z
    global r
    global s
    r=r-s
    magician.ptp(mode=1, x=x, y=y, z=z, r=r)    
    PRC = tk.StringVar(value=r)
    labelPRC = ct.CTkLabel(master=root,
                            textvariable=PRC,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
    labelPRC.place(relx=0.97, rely=0.15)
    labelPR.place_forget()

    print(r)
def HOME():
    global x
    global y
    global z
    global r
    x=200
    y=0
    z=50
    r=0
    magician.set_home()
    PX = tk.StringVar(value=x)
    labelPX = ct.CTkLabel(master=root,
                                textvariable=PX,
                                width=20,
                                height=12,
                                fg_color=("#ececec", "#ececec"),
                                corner_radius=8)
    labelPX.place(relx=0.65, rely=0.15)
    PY = tk.StringVar(value=y)
    labelPY = ct.CTkLabel(master=root,
                                textvariable=PY,
                                width=20,
                                height=12,
                                fg_color=("#ececec", "#ececec"),
                                corner_radius=8)
    labelPY.place(relx=0.72, rely=0.15)
    PZ = tk.StringVar(value=z)
    labelPZ = ct.CTkLabel(master=root,
                                textvariable=PZ,
                                width=20,
                                height=12,
                                fg_color=("#ececec", "#ececec"),
                                corner_radius=8)
    labelPZ.place(relx=0.9, rely=0.15)
    PR = tk.StringVar(value=r)
    labelPR = ct.CTkLabel(master=root,
                                textvariable=PR,
                                width=20,
                                height=12,
                                fg_color=("#ececec", "#ececec"),
                                corner_radius=8)
    labelPR.place(relx=0.97, rely=0.15)
    print(x,y,z,r)
    
    
    
    
#GUI configuration
x=200
y=0
z=50
r=0
v=0
s=1
ct.set_appearance_mode('white')

ct.set_default_color_theme("green")
root= ct.CTk()
root.title("Dobot Didactech")
root.geometry("1100x400")
text_var = tk.StringVar(value="Welcome! You will then be able to select the conveyor belt or the rotary table,\n in order to test the speed and performance of both. ")

label = ct.CTkLabel(master=root,
                               textvariable=text_var,
                               width=80,
                               height=40,
                               font=('Comic Sans MS', 15),
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
label.place(relx=0.28, rely=0.05, anchor=tk.CENTER)

text_var2 = tk.StringVar(value="In this part, you can test the Dobot Magician's movements\n and observe the value of its entries.")

label2 = ct.CTkLabel(master=root,
                               textvariable=text_var2,
                               width=80,
                               height=40,
                               font=('Comic Sans MS', 15),
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
label2.place(relx=0.8, rely=0.05, anchor=tk.CENTER)


#Rotary table configuration

#imgRT= tk.PhotoImage(file="./images/RT.png")
#lbl_imgRT= tk.Label(root, image=imgRT)
#lbl_imgRT.place(relx=0.08,rely=0.15)
RTtitle = tk.StringVar(value="Rotary Table DDT for Dobot ")

labelTRT = ct.CTkLabel(master=root,
                            textvariable=RTtitle,
                            width=80,
                            height=40,
                            font=('Times', 20),
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelTRT.place(relx=0.14, rely=0.15)
buttonRTL = ct.CTkButton(master=root, text="Clockwise", fg_color="green", command=GoLeft)
buttonRTL.place(relx=0.14, rely=0.33, anchor=CENTER)
buttonRTR = ct.CTkButton(master=root, text="Counterclockwise", fg_color="green", command=GoRight)
buttonRTR.place(relx=0.14, rely=0.43, anchor=CENTER)
buttonRT = ct.CTkButton(master=root, text="Stop", fg_color="red", command=stopRT)
buttonRT.place(relx=0.33, rely=0.43, anchor=CENTER)
sliderRT = ct.CTkSlider(master=root, from_=0, to=40, command=slider_event_RT)
sliderRT.place(relx=0.33, rely=0.36, anchor=tk.CENTER)
sliderRT.set(0)
valRTM=tk.StringVar(value=0)
labelRTM = ct.CTkLabel(master=root,
                            textvariable=valRTM,
                            width=20,
                            height=25,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelRTM.place(relx=0.3, rely=0.27)
VarURT = tk.StringVar(value="rpm")

labelURT = ct.CTkLabel(master=root,
                            textvariable=VarURT,
                            width=20,
                            height=25,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelURT.place(relx=0.32, rely=0.27)
valPWMM = tk.StringVar(value=0)
labelPWMM = ct.CTkLabel(master=root,
                            textvariable=valPWMM,
                            width=20,
                            height=25,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelPWMM.place(relx=0.43, rely=0.27)
UPWM = tk.StringVar(value=" Hz with 50% Duty cicle")
labelUPWM = ct.CTkLabel(master=root,
                            textvariable=UPWM,
                            width=20,
                            height=25,
                            fg_color=("#ececec", "black"),
                            corner_radius=8)
labelUPWM.place(relx=0.47, rely=0.27)


#Conveyor Belt configuration
#imgCB= tk.PhotoImage(file="images/CB.png")
#lbl_imgCB= tk.Label(root, image=imgCB)
#lbl_imgCB.place(relx=0.36,rely=0.15)
CBtitle = tk.StringVar(value="Conveyor Belt Dobot ")

labelCBT = ct.CTkLabel(master=root,
                            textvariable=CBtitle,
                            width=80,
                            height=40,
                            font=('Times', 20),
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelCBT.place(relx=0.14, rely=0.55)
buttonCBDF = ct.CTkButton(master=root, text="Go fordward", fg_color="green", command=GoFront)
buttonCBDF.place(relx=0.14, rely=0.75, anchor=CENTER)
buttonCBDB = ct.CTkButton(master=root, text="Go backward", fg_color="green", command=GoBack)
buttonCBDB.place(relx=0.14, rely=0.85, anchor=CENTER)
buttonCB = ct.CTkButton(master=root, text="Stop", fg_color="red", command=stopCB)
buttonCB.place(relx=0.33, rely=0.85, anchor=CENTER)

sliderCB = ct.CTkSlider(master=root, from_=0, to=75, command=slider_event_CB)
sliderCB.set(0)
sliderCB.place(relx=0.33, rely=0.78, anchor=tk.CENTER)
valCBM=tk.StringVar(value=0)

labelCBM = ct.CTkLabel(master=root,
                            textvariable=valCBM,
                            width=20,
                            height=25,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelCBM.place(relx=0.3, rely=0.69)
VarUCB = tk.StringVar(value="mm/s")

labelUCB = ct.CTkLabel(master=root,
                            textvariable=VarUCB,
                            width=20,
                            height=25,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelUCB.place(relx=0.33, rely=0.69)

#Dobot Configuration GUI
buttonXP = ct.CTkButton(master=root, text="X +",height=15, width=15, fg_color="black",text_color="white", command=X_P)
buttonXP.place(relx=0.7, rely=0.2)
buttonYP = ct.CTkButton(master=root, text="Y +",height=15, width=15, fg_color="black",text_color="white", command=Y_P)
buttonYP.place(relx=0.65, rely=0.25)
buttonXN = ct.CTkButton(master=root, text="X -", height=15, width=15,fg_color="black",text_color="white", command=X_N)
buttonXN.place(relx=0.7, rely=0.3)
buttonYN = ct.CTkButton(master=root, text="Y -", height=15, width=15,fg_color="black",text_color="white", command=Y_N)
buttonYN.place(relx=0.75, rely=0.25)

buttonZP = ct.CTkButton(master=root, text="Z +", height=15, width=15,fg_color="black",text_color="white", command=Z_P)
buttonZP.place(relx=0.9, rely=0.2)
buttonZN = ct.CTkButton(master=root, text="Z -", height=15, width=15, fg_color="black",text_color="white", command=Z_N)
buttonZN.place(relx=0.9, rely=0.3)
buttonRP = ct.CTkButton(master=root, text="R +", height=15, width=15,fg_color="black",text_color="white", command=R_P)
buttonRP.place(relx=0.85, rely=0.25)
buttonRN = ct.CTkButton(master=root, text="R -", height=15, width=15, fg_color="black",text_color="white", command=R_N)
buttonRN.place(relx=0.95, rely=0.25)

#magician.ptp(mode=0, x=x, y=y, z=z, r=r)
buttonSU = ct.CTkButton(master=root, text="Avanzar en 1", height=15, width=15, fg_color="green",text_color="white", command=S_U)
buttonSU.place(relx=0.55, rely=0.6)
buttonSD = ct.CTkButton(master=root, text="Avanzar en 10", height=15, width=15,fg_color="green",text_color="white", command=S_D)
buttonSD.place(relx=0.55, rely=0.67)
buttonSV = ct.CTkButton(master=root, text="Avanzar en 20", height=15, width=15, fg_color="green",text_color="white", command=S_V)
buttonSV.place(relx=0.55, rely=0.74)

buttonAV = ct.CTkButton(master=root, text="Absorver", height=15, width=15, fg_color="gray",text_color="white", command=A_V)
buttonAV.place(relx=0.55, rely=0.4)
buttonSV = ct.CTkButton(master=root, text="Soplar", height=15, width=15, fg_color="gray",text_color="white", command=SS_V)
buttonSV.place(relx=0.55, rely=0.47)
buttonDV = ct.CTkButton(master=root, text="Desactivar", height=15, width=15, fg_color="red",text_color="white", command=D_V)
buttonDV.place(relx=0.55, rely=0.54)

buttonH = ct.CTkButton(master=root, text="Home", height=15, width=30, fg_color="blue",text_color="white", command=HOME)
buttonH.place(relx=0.79, rely=0.15)
PXT = tk.StringVar(value="x: ")
labelPXT = ct.CTkLabel(master=root,
                            textvariable=PXT,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelPXT.place(relx=0.62, rely=0.15)
PX = tk.StringVar(value=x)
labelPX = ct.CTkLabel(master=root,
                            textvariable=PX,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelPX.place(relx=0.65, rely=0.15)
PYT = tk.StringVar(value="y: ")
labelPYT = ct.CTkLabel(master=root,
                            textvariable=PYT,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelPYT.place(relx=0.69, rely=0.15)
PY = tk.StringVar(value=y)
labelPY = ct.CTkLabel(master=root,
                            textvariable=PY,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelPY.place(relx=0.72, rely=0.15)
PZT = tk.StringVar(value="z: ")
labelPZT = ct.CTkLabel(master=root,
                            textvariable=PZT,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelPZT.place(relx=0.87, rely=0.15)
PZ = tk.StringVar(value=z)
labelPZ = ct.CTkLabel(master=root,
                            textvariable=PZ,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelPZ.place(relx=0.9, rely=0.15)
PRT = tk.StringVar(value="r: ")
labelPRT = ct.CTkLabel(master=root,
                            textvariable=PRT,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelPRT.place(relx=0.94, rely=0.15)
PR = tk.StringVar(value=r)
labelPR = ct.CTkLabel(master=root,
                            textvariable=PR,
                            width=20,
                            height=12,
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelPR.place(relx=0.97, rely=0.15)

TI = tk.StringVar(value="INPUTS DOBOT")

labelTI = ct.CTkLabel(master=root,
                            textvariable=TI,
                            width=20,
                            height=25,
                            font=('Times',15),
                            fg_color=("#ececec", "#ececec"),
                            corner_radius=8)
labelTI.place(relx=0.75, rely=0.37)

check_D1 = tk.StringVar(value=magician.get_di(io="DI_01")['level'])
check_D2 = tk.StringVar(value=magician.get_di(io="DI_03")['level'])
check_D3 = tk.StringVar(value=magician.get_di(io="DI_03")['level'])
check_D4 = tk.StringVar(value=magician.get_di(io="DI_04")['level'])
check_D5 = tk.StringVar(value=magician.get_di(io="DI_05")['level'])
check_D6 = tk.StringVar(value=magician.get_di(io="DI_06")['level'])
check_D7 = tk.StringVar(value=magician.get_di(io="DI_07")['level'])
check_D8 = tk.StringVar(value=magician.get_di(io="DI_08")['level'])
check_D9 = tk.StringVar(value=magician.get_di(io="DI_09")['level'])
check_D10 = tk.StringVar(value=magician.get_di(io="DI_10")['level'])
check_D11 = tk.StringVar(value=magician.get_di(io="DI_11")['level'])
check_D12 = tk.StringVar(value=magician.get_di(io="DI_12")['level'])
check_D13 = tk.StringVar(value=magician.get_di(io="DI_13")['level'])
check_D14 = tk.StringVar(value=magician.get_di(io="DI_14")['level'])
check_D15 = tk.StringVar(value=magician.get_di(io="DI_15")['level'])
check_D16 = tk.StringVar(value=magician.get_di(io="DI_16")['level'])
check_D17 = tk.StringVar(value=magician.get_di(io="DI_17")['level'])
check_D18 = tk.StringVar(value=magician.get_di(io="DI_18")['level'])
check_D19 = tk.StringVar(value=magician.get_di(io="DI_19")['level'])
check_D20 = tk.StringVar(value=magician.get_di(io="DI_20")['level'])

checkbox1 = ct.CTkCheckBox(master=root, variable=check_D1,state=DISABLED, text="Digital 1" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox1.place(relx=0.7,rely=0.45)
checkbox2 = ct.CTkCheckBox(master=root, variable=check_D2,state=DISABLED, text="Digital 2" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox2.place(relx=0.7,rely=0.5)
checkbox3 = ct.CTkCheckBox(master=root, variable=check_D3,state=DISABLED, text="Digital 3" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox3.place(relx=0.7,rely=0.55)
checkbox4 = ct.CTkCheckBox(master=root, variable=check_D4,state=DISABLED, text="Digital 4" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox4.place(relx=0.7,rely=0.6)
checkbox5 = ct.CTkCheckBox(master=root, variable=check_D5,state=DISABLED, text="Digital 5" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox5.place(relx=0.7,rely=0.65)
checkbox6 = ct.CTkCheckBox(master=root, variable=check_D6,state=DISABLED, text="Digital 6" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox6.place(relx=0.7,rely=0.7)
checkbox7 = ct.CTkCheckBox(master=root, variable=check_D7,state=DISABLED, text="Digital 7" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox7.place(relx=0.7,rely=0.75)
checkbox8 = ct.CTkCheckBox(master=root, variable=check_D8,state=DISABLED, text="Digital 8" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox8.place(relx=0.7,rely=0.8)
checkbox9 = ct.CTkCheckBox(master=root, variable=check_D9,state=DISABLED, text="Digital 9" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox9.place(relx=0.7,rely=0.85)
checkbox10 = ct.CTkCheckBox(master=root, variable=check_D10,state=DISABLED, text="Digital 10" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox10.place(relx=0.7,rely=0.9)

checkbox11 = ct.CTkCheckBox(master=root, variable=check_D11,state=DISABLED, text="Digital 11" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox11.place(relx=0.85,rely=0.45)
checkbox12 = ct.CTkCheckBox(master=root, variable=check_D12,state=DISABLED, text="Digital 12" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox12.place(relx=0.85,rely=0.5)
checkbox13 = ct.CTkCheckBox(master=root, variable=check_D13,state=DISABLED, text="Digital 13" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox13.place(relx=0.85,rely=0.55)
checkbox14 = ct.CTkCheckBox(master=root, variable=check_D14,state=DISABLED, text="Digital 14" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox14.place(relx=0.85,rely=0.6)
checkbox15 = ct.CTkCheckBox(master=root, variable=check_D15,state=DISABLED, text="Digital 15" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox15.place(relx=0.85,rely=0.65)
checkbox16 = ct.CTkCheckBox(master=root, variable=check_D16,state=DISABLED, text="Digital 16" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox16.place(relx=0.85,rely=0.7)
checkbox17 = ct.CTkCheckBox(master=root, variable=check_D17,state=DISABLED, text="Digital 17" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox17.place(relx=0.85,rely=0.75)
checkbox18 = ct.CTkCheckBox(master=root, variable=check_D18,state=DISABLED, text="Digital 18" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox18.place(relx=0.85,rely=0.8)
checkbox19 = ct.CTkCheckBox(master=root, variable=check_D19,state=DISABLED, text="Digital 19" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox19.place(relx=0.85,rely=0.85)
checkbox20 = ct.CTkCheckBox(master=root, variable=check_D20,state=DISABLED, text="Digital 20" ,checkbox_height=15, checkbox_width=15, onvalue="1", offvalue="0")
checkbox20.place(relx=0.85,rely=0.9)

#root.iconbitmap('images/logo.ico')
root.mainloop()
























