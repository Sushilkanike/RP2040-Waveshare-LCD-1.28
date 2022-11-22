#Ben10_Omnitrix
from machine import Pin,I2C,SPI,PWM,ADC
import framebuf
import time
import array
import math



I2C_SDA = 6
I2C_SDL = 7

DC = 8
CS = 9
SCK = 10
MOSI = 11
RST = 12

count = 0
peak = 0
Gval = [0, 0, 0]
PI = 3.14

push_button = Pin(13,Pin.IN, Pin.PULL_DOWN)

BL = 25

Vbat_Pin = 29


class LCD_1inch28(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 240
        
        
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1,100_000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        self.grey  =   0x0000
        
        for j in range (0,3):
            self.fill(self.green)
                
            self.line(0,0,90,120,self.black)
            for i in range (1,20):
                self.line(0-i,0,90-i,120,self.black)
            for i in range (0,75):
                self.line(-20-i,0,70-i,120,self.grey)            

            self.line(90,120,0,240,self.black)
            for i in range (1,20):
                self.line(90-i,120,0-i,240,self.black)
            for i in range (0,75):
                self.line(70-i,120,-20-i,240,self.grey)            
                
                
            self.line(240,0,150,120,self.black)
            for i in range (1,20):
                self.line(240+i,0,150+i,120,self.black)
            for i in range (0,75):
                self.line(260+i,0,170+i,120,self.grey)
                    
            self.line(150,120,240,240,self.black)
            for i in range (1,20):
                self.line(150+i,120,240+i,240,self.black)
            for i in range (0,75):
                self.line(170+i,120,260+i,240,self.grey)
                    
            self.show()
            
            time.sleep(0.5)
            self.fill(self.red)
                
            self.line(0,0,90,120,self.black)
            for i in range (1,20):
                self.line(0-i,0,90-i,120,self.black)
            for i in range (0,75):
                self.line(-20-i,0,70-i,120,self.grey)            

            self.line(90,120,0,240,self.black)
            for i in range (1,20):
                self.line(90-i,120,0-i,240,self.black)
            for i in range (0,75):
                self.line(70-i,120,-20-i,240,self.grey)            
                
                
            self.line(240,0,150,120,self.black)
            for i in range (1,20):
                self.line(240+i,0,150+i,120,self.black)
            for i in range (0,75):
                self.line(260+i,0,170+i,120,self.grey)
                    
            self.line(150,120,240,240,self.black)
            for i in range (1,20):
                self.line(150+i,120,240+i,240,self.black)
            for i in range (0,75):
                self.line(170+i,120,260+i,240,self.grey)
                    
            self.show()
            
            time.sleep(0.5)
        
        self.pwm = PWM(Pin(BL))
        self.pwm.freq(5000)
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)
    def set_bl_pwm(self,duty):
        self.pwm.duty_u16(duty)#max 65535
    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        time.sleep(0.01)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        time.sleep(0.05)
        
        self.write_cmd(0xEF)
        self.write_cmd(0xEB)
        self.write_data(0x14) 
        
        self.write_cmd(0xFE) 
        self.write_cmd(0xEF) 

        self.write_cmd(0xEB)
        self.write_data(0x14) 

        self.write_cmd(0x84)
        self.write_data(0x40) 

        self.write_cmd(0x85)
        self.write_data(0xFF) 

        self.write_cmd(0x86)
        self.write_data(0xFF) 

        self.write_cmd(0x87)
        self.write_data(0xFF)

        self.write_cmd(0x88)
        self.write_data(0x0A)

        self.write_cmd(0x89)
        self.write_data(0x21) 

        self.write_cmd(0x8A)
        self.write_data(0x00) 

        self.write_cmd(0x8B)
        self.write_data(0x80) 

        self.write_cmd(0x8C)
        self.write_data(0x01) 

        self.write_cmd(0x8D)
        self.write_data(0x01) 

        self.write_cmd(0x8E)
        self.write_data(0xFF) 

        self.write_cmd(0x8F)
        self.write_data(0xFF) 


        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(0x20)

        self.write_cmd(0x36)
        self.write_data(0x98)

        self.write_cmd(0x3A)
        self.write_data(0x05) 


        self.write_cmd(0x90)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08) 

        self.write_cmd(0xBD)
        self.write_data(0x06)
        
        self.write_cmd(0xBC)
        self.write_data(0x00)

        self.write_cmd(0xFF)
        self.write_data(0x60)
        self.write_data(0x01)
        self.write_data(0x04)

        self.write_cmd(0xC3)
        self.write_data(0x13)
        self.write_cmd(0xC4)
        self.write_data(0x13)

        self.write_cmd(0xC9)
        self.write_data(0x22)

        self.write_cmd(0xBE)
        self.write_data(0x11) 

        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)

        self.write_cmd(0xDF)
        self.write_data(0x21)
        self.write_data(0x0c)
        self.write_data(0x02)

        self.write_cmd(0xF0)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF1)    
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37)  
        self.write_data(0x6F)


        self.write_cmd(0xF2)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF3)   
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37) 
        self.write_data(0x6F)

        self.write_cmd(0xED)
        self.write_data(0x1B) 
        self.write_data(0x0B) 

        self.write_cmd(0xAE)
        self.write_data(0x77)
        
        self.write_cmd(0xCD)
        self.write_data(0x63)


        self.write_cmd(0x70)
        self.write_data(0x07)
        self.write_data(0x07)
        self.write_data(0x04)
        self.write_data(0x0E) 
        self.write_data(0x0F) 
        self.write_data(0x09)
        self.write_data(0x07)
        self.write_data(0x08)
        self.write_data(0x03)

        self.write_cmd(0xE8)
        self.write_data(0x34)

        self.write_cmd(0x62)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x71)
        self.write_data(0xED)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x0F)
        self.write_data(0x71)
        self.write_data(0xEF)
        self.write_data(0x70) 
        self.write_data(0x70)

        self.write_cmd(0x63)
        self.write_data(0x18)
        self.write_data(0x11)
        self.write_data(0x71)
        self.write_data(0xF1)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x13)
        self.write_data(0x71)
        self.write_data(0xF3)
        self.write_data(0x70) 
        self.write_data(0x70)

        self.write_cmd(0x64)
        self.write_data(0x28)
        self.write_data(0x29)
        self.write_data(0xF1)
        self.write_data(0x01)
        self.write_data(0xF1)
        self.write_data(0x00)
        self.write_data(0x07)

        self.write_cmd(0x66)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0xCD)
        self.write_data(0x67)
        self.write_data(0x45)
        self.write_data(0x45)
        self.write_data(0x10)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_cmd(0x67)
        self.write_data(0x00)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x54)
        self.write_data(0x10)
        self.write_data(0x32)
        self.write_data(0x98)

        self.write_cmd(0x74)
        self.write_data(0x10)
        self.write_data(0x85)
        self.write_data(0x80)
        self.write_data(0x00) 
        self.write_data(0x00) 
        self.write_data(0x4E)
        self.write_data(0x00)
        
        self.write_cmd(0x98)
        self.write_data(0x3e)
        self.write_data(0x07)

        self.write_cmd(0x35)
        self.write_cmd(0x21)

        self.write_cmd(0x11)
        time.sleep(0.12)
        self.write_cmd(0x29)
        time.sleep(0.02)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xef)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)


class QMI8658(object):
    def __init__(self,address=0X6B):
        self._address = address
        self._bus = I2C(id=1,scl=Pin(I2C_SDL),sda=Pin(I2C_SDA),freq=100_000)
        bRet=self.WhoAmI()
        if bRet :
            self.Read_Revision()
        else    :
            return NULL
        self.Config_apply()

    def _read_byte(self,cmd):
        rec=self._bus.readfrom_mem(int(self._address),int(cmd),1)
        return rec[0]
    def _read_block(self, reg, length=1):
        rec=self._bus.readfrom_mem(int(self._address),int(reg),length)
        return rec
    def _read_u16(self,cmd):
        LSB = self._bus.readfrom_mem(int(self._address),int(cmd),1)
        MSB = self._bus.readfrom_mem(int(self._address),int(cmd)+1,1)
        return (MSB[0] << 8) + LSB[0]
    def _write_byte(self,cmd,val):
        self._bus.writeto_mem(int(self._address),int(cmd),bytes([int(val)]))
        
    def WhoAmI(self):
        bRet=False
        if (0x05) == self._read_byte(0x00):
            bRet = True
        return bRet
    def Read_Revision(self):
        return self._read_byte(0x01)
    def Config_apply(self):
        # REG CTRL1
        self._write_byte(0x02,0x60)
        # REG CTRL2 : QMI8658AccRange_8g  and QMI8658AccOdr_1000Hz
        self._write_byte(0x03,0x23)
        # REG CTRL3 : QMI8658GyrRange_512dps and QMI8658GyrOdr_1000Hz
        self._write_byte(0x04,0x53)
        # REG CTRL4 : No
        self._write_byte(0x05,0x00)
        # REG CTRL5 : Enable Gyroscope And Accelerometer Low-Pass Filter 
        self._write_byte(0x06,0x11)
        # REG CTRL6 : Disables Motion on Demand.
        self._write_byte(0x07,0x00)
        # REG CTRL7 : Enable Gyroscope And Accelerometer
        self._write_byte(0x08,0x03)

    def Read_Raw_XYZ(self):
        xyz=[0,0,0,0,0,0]
        raw_timestamp = self._read_block(0x30,3)
        raw_acc_xyz=self._read_block(0x35,6)
        raw_gyro_xyz=self._read_block(0x3b,6)
        raw_xyz=self._read_block(0x35,12)
        timestamp = (raw_timestamp[2]<<16)|(raw_timestamp[1]<<8)|(raw_timestamp[0])
        for i in range(6):
            # xyz[i]=(raw_acc_xyz[(i*2)+1]<<8)|(raw_acc_xyz[i*2])
            # xyz[i+3]=(raw_gyro_xyz[((i+3)*2)+1]<<8)|(raw_gyro_xyz[(i+3)*2])
            xyz[i] = (raw_xyz[(i*2)+1]<<8)|(raw_xyz[i*2])
            if xyz[i] >= 32767:
                xyz[i] = xyz[i]-65535
        return xyz
    def Read_XYZ(self):
        xyz=[0,0,0,0,0,0]
        raw_xyz=self.Read_Raw_XYZ()  
        #QMI8658AccRange_8g
        acc_lsb_div=(1<<12)
        #QMI8658GyrRange_512dps
        gyro_lsb_div = 64
        for i in range(3):
            xyz[i]=raw_xyz[i]/acc_lsb_div#(acc_lsb_div/1000.0)
            xyz[i+3]=raw_xyz[i+3]*1.0/gyro_lsb_div
        return xyz


if __name__=='__main__':
  
    LCD = LCD_1inch28()
    LCD.set_bl_pwm(65535)
    qmi8658=QMI8658()
    Vbat= ADC(Pin(Vbat_Pin))   
    
    while(True):
        #read QMI8658
        xyz=qmi8658.Read_XYZ()
        LCD.fill(LCD.red)
        
        #if push_button.value(): #uncomment this line to use pushbutton at GPIO13 and add the indentation for the if condition
        #count += 1                
        #ime.sleep(2) #replace 2 with 0.1 if push button is used
        count = 1   #uncomment this line to stay on a paricular page
            
        if count == 1:
            
            LCD.fill(LCD.green)
            
            LCD.line(0,0,90,120,LCD.black)
            for i in range (1,20):
                LCD.line(0-i,0,90-i,120,LCD.black)
            for i in range (0,75):
                LCD.line(-20-i,0,70-i,120,LCD.grey)            

            LCD.line(90,120,0,240,LCD.black)
            for i in range (1,20):
                LCD.line(90-i,120,0-i,240,LCD.black)
            for i in range (0,75):
                LCD.line(70-i,120,-20-i,240,LCD.grey)            
            
            
            LCD.line(240,0,150,120,LCD.black)
            for i in range (1,20):
                LCD.line(240+i,0,150+i,120,LCD.black)
            for i in range (0,75):
                LCD.line(260+i,0,170+i,120,LCD.grey)
                
            LCD.line(150,120,240,240,LCD.black)
            for i in range (1,20):
                LCD.line(150+i,120,240+i,240,LCD.black)
            for i in range (0,75):
                LCD.line(170+i,120,260+i,240,LCD.grey)
                
            LCD.show()
            time.sleep(0.1)
            
        elif count == 2:
            LCD.fill(LCD.red)
            LCD.fill_rect(0,0,240,60,LCD.red)
            LCD.text("lvlAlpha",90,25,LCD.white)
        
            LCD.fill_rect(0,40,240,40,LCD.blue)
            LCD.text("Environment",80,57,LCD.white)
            
            LCD.fill_rect(0,200,240,40,0x180f)
            reading = Vbat.read_u16()*3.3/65535*2
            LCD.text("Vbat={:.2f}".format(reading),80,215,LCD.white)
            LCD.show()
            time.sleep(0.1)
            
        elif count == 3:
            LCD.fill_rect(0,0,240,60,LCD.red)
            LCD.text("lvlAlpha",90,25,LCD.white)
        
            LCD.fill_rect(0,40,240,40,LCD.blue)
            LCD.text("IMU Impact Injury",60,57,LCD.white)
            
            LCD.fill_rect(0,80,120,120,0x1805)
            LCD.text("GForce",35,105,LCD.red)
            
            for i in range(0,2):
            
                Accel_X = xyz[0]
                Accel_Y = xyz[1]
                Accel_Z = xyz[2]
            
                G = pow((pow(xyz[0],2) + pow(xyz[1],2) + pow(xyz[2],2)),0.5)
                G = G/10
                
                Gval[i] = G
                time.sleep(0.1)
            
            if Gval[1] > Gval[0] :
                peak = Gval[1]
            else:
                peak = Gval[0]
            
            LCD.text("{:+.2f}".format(G),35,120,LCD.red)
            LCD.text("Peak Hold",25,155,LCD.red)
            LCD.text("{:+.2f}".format(peak),35,175,LCD.red)
            
            
            
            LCD.fill_rect(120,80,120,120,0xF073)
            LCD.text("Eular Angles",130,105,LCD.white)
            
            Gyro_X = xyz[3]
            Gyro_Y = xyz[4]
            Gyro_Y = xyz[5]
            
            pitch = 180 * math.atan2(Accel_X, math.sqrt(Accel_Y*Accel_Y + Accel_Z*Accel_Z))/PI;
            roll = 180 * math.atan2(Accel_Y, math.sqrt(Accel_X*Accel_X + Accel_Z*Accel_Z))/PI;
            
            LCD.text("Pitch={:+3.2f}".format(pitch),125,130,LCD.white)
            LCD.text("Roll ={:+3.2f}".format(roll),125,150,LCD.white)
            
            
            LCD.fill_rect(0,200,240,40,0x180f)
            reading = Vbat.read_u16()*3.3/65535*2
            LCD.text("Vbat={:.2f}".format(reading),80,215,LCD.white)        

            LCD.show()
            time.sleep(0.1)

        elif count == 4:
            LCD.fill_rect(0,0,240,60,LCD.red)
            LCD.text("lvlAlpha",90,25,LCD.white)
        
            LCD.fill_rect(0,40,240,40,LCD.blue)
            LCD.text("Location",91,57,LCD.white)
            
            LCD.fill_rect(0,200,240,40,0x180f)
            reading = Vbat.read_u16()*3.3/65535*2
            LCD.text("Vbat={:.2f}".format(reading),80,215,LCD.white)        

            LCD.show()
            time.sleep(0.1)
            
            count = 0
            
        else:
            count = 0

