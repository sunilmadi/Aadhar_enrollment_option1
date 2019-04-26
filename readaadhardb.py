from pymongo import MongoClient
from Modules_Packages.aadhar_project import sms1 as sm,emaila as em,otpcheck as otpc,generateaadhar as ga 
def readaadhardb(pancard,name,dob,age,city,state,phone):
    Flagadb='N'
    client=MongoClient('localhost',27017)
    db=client['AADHAR']
    AADHARINFO=db.AADHARINFO
    result=AADHARINFO.find_one({'PANNUM':pancard})
    if result is None:
        pass
    else:
        for i,j in result.items():
            if j==pancard:
                aadhartemp=result['AADHARNUM']
                Flagadb='Y'
        else:
            pass
    if Flagadb=='Y':
        val=otpc.otpcheck()
        if val==1:
            sm.sendsms(aadhartemp,'E')
            email1=input("enter your email :")
            em.emailfunc(email1,aadhartemp,'E')
        else:
            print("otp invalid or time out error")
    else:
        aadhar_return=ga.generateaadhar(pancard,name,dob,age,city,state,phone).createaadhar()



