from twilio.rest import Client
import datetime as dt 
from Modules_Packages.aadhar_project import email as em,readaadhardb as radb
class pandb:
    def __init__(self,name,dob,pancard,city,state,phone,age):
        self.name=name
        self.dob=dob
        self.pancard=pancard
        self.city=city
        self.state=state
        self.phone=phone
        self.age=age
    def sqlconnect(self):
        import sqlite3 as sq 
        conn=sq.connect("pancard.db")
        return conn
    def checkpandb(self):
        flagcpdb='N'
        z=self.sqlconnect()
        e=z.execute("SELECT * FROM PANCARD")
        for i in e:
            if i[0]==self.pancard and i[6]==int(self.phone):
                self.name=i[1]
                self.dob=i[2]
                self.city=i[4]
                self.state=i[5]
                self.age=i[3]
                flagcpdb='Y'  
            else:
                pass
        if flagcpdb=='Y':
            val=self.otpcheck(self.phone)
            if val==1:
                self.sendsms(self.pancard,'E')
                self.sendemail(self.pancard,'E')
            z.close()
            return val
        else:
            print("your pancard not in pan database")
            p1=input("DO YOU WANT TO REGISTER A PANCARD FOR AADHAR(Y/N)? :")
            z.close()
            return p1

    def otpcheck(self,phone):
        import sqlite3 as sq
        conn=sq.connect("pancard.db")
        cursor=conn.execute("SELECT max(OTP) FROM OTP")
        for i in cursor:    
             new_otp=int(i[0])+1         
        number='+917507483508'
        account_sid = 'AC9ca57309561dff05e457f51f0d40370a'
        auth_token = 'd5a27293ea20119e6a61f540983efb30'
        client = Client(account_sid, auth_token)
        body1="your otp number is {0}"
        body2=body1.format(new_otp)
        message = client.messages.create(
                     body=body2,
                     from_='+17065100684',
                     to=number,
                 )
        t1=dt.datetime.today()
        t11=(t1.hour*3600+ t1.minute*60 + t1.second)
        verify_otp=int(input("enter your otp received on your registered mobile number which is valid for only 2 minutes : "))
        t2=dt.datetime.today()
        t22=(t2.hour*3600+ t2.minute*60 + t2.second)
        t3=t22-t11
        query1="INSERT INTO OTP (OTP,USED) VALUES({0},'Y')"
        query2=query1.format(new_otp)
        cursor=conn.execute(query2)
        conn.commit()
        conn.close()
        if t3 <=120:  # setting 120 seconds of otp vaidity
            if int(verify_otp)==int(new_otp):
                return 1  # proceed with aadhar regsitration/ pan card registration
            else:
                return 2   # invalid user due to otp/no otp  mismatch
        else:
            return 3    #OTP time out
    def panregistration(self):
        flagr='N'
        print("entered into pancard registration function")
        import sqlite3 as sq 
        conn=sq.connect("pancard.db")
        cursor1=conn.execute("SELECT max(COUNTER),PANNUM FROM PANCARD")
        for i in cursor1:
            new_counter=int(i[0])+1
        new_pannum=('AZXPM'+ str(int(i[1][5:9])+1) + self.state[0:1])
        query1="INSERT INTO PANCARD VALUES('{0}','{1}','{2}','{3}','{4}','{5}',{6},{7})"
        val=self.otpcheck(self.phone)
        if val==1:
            query2=query1.format(new_pannum,self.name,self.dob,self.age,self.city,self.state,self.phone,new_counter)
            cursor=conn.execute(query2)
            flagr='Y'
        else:
            print("invalid otp or time out")
            pass
        conn.commit()
        conn.close()
        if flagr=='Y':
            return [1 , new_pannum]
        else:
            return 2
    def sendsms(self,pancard,action):
        number='+917507483508'
        account_sid = 'AC9ca57309561dff05e457f51f0d40370a'
        auth_token = 'd5a27293ea20119e6a61f540983efb30'
        client = Client(account_sid, auth_token)
        if action=='E':
            body1="Your pancard number already exists and pancard number is: '{0}'"
        elif action =='N':
            body1="Your pancard number generated successfully  and pancard number is: '{0}'"
        body2=body1.format(pancard)
        message = client.messages.create(
                     body=body2,
                     from_='+17065100684',
                     to=number,
                 )
    def sendemail(self,pancard,action):
        email1=input("enter your email :")
        em.emailfunc(email1,pancard,action)
    def readaadhardb(self,pancard):
        radb.readaadhardb(pancard,self.name,self.dob,self.age,self.city,self.state,self.phone)
        


        
        


        





