from Modules_Packages.aadhar_project import readpan as rp 
import datetime as dt 
import time as tt
class validation:
    def __init__(self):
        pass
    def funcvalidation():
        flagdob='N'
        ss=dt.datetime.today()
        print("open an aadhar function")
        name1=input("enter your name: ")
        dob1=input("enter your age in mm/dd/yyyy format: ")
        dobd=dob1[3:5]
        dob2=dob1[0:2]
        dob3=dob1[2:3]
        dob4=dob1[5:6]
        dob5=dob1[6:10]
        if int(dob2) in [1,2,3,4,5,6,7,8,9,10,11,12] and dob3=='/' and dob4 =='/':
            if int(dob5) % 4 ==0:
                if int(dob2)==2 and int(dob1[3:5]) in range(1,30):
                    flagdob='Y'

                elif int(dob2) in [1,3,5,7,8,10,12] and int(dob1[3:5]) in range(1,32):
                    flagdob='Y'
                elif int(dob2) in [4,6,9,11] and int(dob1[3:5]) in range(1,31):
                    flagdob='Y'
                else:
                    flagdob='N'
            else:
                if int(dob2)==2 and int(dob1[3:5]) in range(1,29):
                    flagdob='Y'

                elif int(dob2) in [1,3,5,7,8,10,12] and int(dob1[3:5]) in range(1,32):
                    flagdob='Y'
                elif int(dob2) in [4,6,9,11] and int(dob1[3:5]) in range(1,31):
                    flagdob='Y'
                else:
                    flagdob='N' 
        else:
            flagdob='N'
        if flagdob=='N':
            s='Invalid date of birth'
            s1=s+ " " + dob1
            return s1
        pancard1=input("enter your 10 digit pan card number: ")
        if len(pancard1) !=10:
            s='Invalid pancard number'
            s1=s+ " " + pancard1
            return s1
        city1=input("enter your city: ")
        state1=input("enter your state: ")
        phone1=input("enter your 10 digit mobile number: ")
        for i in phone1:
            if i not in ['0','1','2','3','4','5','6','7','8','9'] or len(phone1)!=10:
                s='Invalid mobile number'
                s1=s+ " " + phone1
                return s1
        #calculate age.first get the number of days and then age in years
        z=dt.date.today() - dt.date(int(dob5),int(dob2),int(dobd))
        age1=(z.days//365)
        return [10,name1,dob1,pancard1,city1,state1,phone1,age1]
class pandb:
    def __init__(self,name,dob,pancard,city,state,phone,age):
        self.name=name
        self.dob=dob
        self.pancard=pancard
        self.city=city
        self.state=state
        self.phone=phone
        self.age=age
    def read_pandb(self):
        z=rp.pandb(self.name,self.dob,self.pancard,self.city,self.state,self.phone,self.age)
        z1=z.checkpandb()
        if z1==1:
            z.readaadhardb(self.pancard)   # exiting pancard customer will go to read aadhar database
            return
        elif z1==2:
            print("Invalid / No  OTP entered.")
            return
        elif z1==3:
            print("OTP time out error")
            return
        elif z1=='Y':
            z2=z.panregistration()   # pancard not existing and want to open pancard 
            if z2[0]==1:
                z.sendsms(z2[1],'N')
                z.sendemail(z2[1],'N')
                z.readaadhardb(z2[1])   # newly registered pan users will go to read aadhar database
            return
        elif z1=='N':  # pancard not existing and do not want to open pancard
            return


        

    



        
    






    