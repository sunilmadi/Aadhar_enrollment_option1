import sqlite3 as sq
from pymongo import MongoClient
from Modules_Packages.aadhar_project import smst as smt,emailt as emt,otpcheck as otpt,sms1 as sma,emaila as ema
class generateaadhar:
    def __init__(self,pancard,name,dob,age,city,state,phone):
        self.pancard=pancard
        self.name=name 
        self.dob=dob 
        self.age=age 
        self.city=city 
        self.state=state 
        self.phone=phone 
    def createaadhar(self):
        z,y=generateaadhar.generate_token()
        y1=int(y) + 1
        z1=generateaadhar.generate_aadhar(int(y1))
        cr=input("DO YOU WANT TO CONTINUE WITH AADHAR REGISTRATION(Y) OR USE TOKEN NUMBER TO CONTINUE WITH AADHAR REGISTRATION LATER(N)? :")
        if cr=='N':
            rt=otpt.otpcheck()
            if rt==1:
                generateaadhar.inserttoken(z,self.pancard,z1,'N')
            else:
                print("invalid OTP or time out")
                return
        else:
            rt=otpt.otpcheck()
            if rt==1:
                generateaadhar.insertaadhar(self.pancard,self.name,self.dob,self.age,self.city,self.state,self.phone,z1)
            else:
                print("invalid OTP or time out")
            

    def generate_token():
        new_token=0
        conn=sq.connect("PANCARD.db")
        query1="SELECT MAX(TOKEN),AADHARNUM,TOEKN_USED FROM TOKEN"
        result=conn.execute(query1)
        for i in result:
            new_token=i[0]+1
        conn.commit()
        conn.close()        
        return new_token,i[1]
    def generate_aadhar(aadharnum):
        conn=MongoClient('localhost',27017)
        db=conn['AADHAR']
        AADHARINFO=db.AADHARINFO
        result=AADHARINFO.aggregate([{'$group':{'_id':'AADHARNUM','MAXAADHAR':{'$max':'$AADHARNUM'}}}])
        for i in result:
            max_aadhar= i['MAXAADHAR'] + 1   
        if int(max_aadhar) > int(aadharnum):
            return int(max_aadhar)
        else:
            return int(aadharnum)
        
    def inserttoken(token,pann,aadharn,tokenu):
        conn=sq.connect("PANCARD.db")
        query1="SELECT * FROM TOKEN WHERE PANNUM='{0}' AND TOEKN_USED='{1}'"
        query=query1.format(pann,'N')
        result=conn.execute(query)
        result1=result.fetchall()
        if len(result1)==0:
            query1="INSERT INTO TOKEN VALUES({0},'{1}',{2},'{3}')"
            query=query1.format(token,pann,aadharn,tokenu)
            result=conn.execute(query)  
            smt.sendsms(token,'N')
            email1=input("enter your email :")
            emt.emailfunc(email1,token,'N')
        else: 
            for i in result1:   
                if i[1]==pann:
                    token=i[0]
                    smt.sendsms(token,'E')
                    email1=input("enter your email :")
                    emt.emailfunc(email1,token,'E')
              
        print("YOUR AADHAR REGISTRATION TOKEN NUMBER IS GENERATED AND SENT TO YOUR REGISTERED MOBILE NUMBER.KEEP IT SAFE TO CONTINUE WITH AADHAR REGISTRATION LATER")    
        conn.commit()
        conn.close()

    def insertaadhar(pann,name,dob,age,city,state,phone,z1):
        conn=MongoClient('localhost',27017)
        db=conn['AADHAR']
        AADHARINFO=db.AADHARINFO
        result=AADHARINFO.insert_one({'PANNUM':pann,'NAME':name,'DOB':dob,'AGE':age,'CITY':city,'STATE':state,'PHONENUM':phone,'AADHARNUM':z1})
        sma.sendsms(z1,'N')
        email1=input("enter your email :")
        ema.emailfunc(email1,z1,'N')
