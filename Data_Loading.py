#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 18:01:41 2021

@author: aditya
"""

import yaml
import time
import datetime
import math
import mysql.connector
import os
import threading

def Team_Entry(tname,mydb,mycursor) :
    tid1=0
    mycursor.execute("SELECT * FROM team where tname=\""+tname+"\"")
    output=mycursor.fetchall()
    if (output==[]) :
        mycursor.execute("select max(tid) from team")
        output=mycursor.fetchall()
        if (output[0][0]==None) :
            sql = "INSERT INTO team (tid, tname) VALUES (%s,%s)"
            val = (str(1),str(tname))
            tid1=1
            mycursor.execute(sql,val)
        else :
            sql = "INSERT INTO team (tid, tname) VALUES (%s,%s)"
            val = (str(int(output[0][0])+1),str(tname))
            tid1=int(output[0][0])+1
            mycursor.execute(sql,val)
    else :
        tid1=output[0][0]
    
    #print(tname+" Inserted In Team")
    return tid1

def Match_Metadata_Entry(Info,i1,i2,mydb,mycursor) :
    #city=Info["city"]
    teams=Info["teams"]
    date=str(Info["dates"][0]).split("-")
    year=date[0]
    month=date[1]
    date=date[2]
    Winner=Info["outcome"]["winner"]
    Man_of_Match=Info["player_of_match"]
    ground=Info["venue"]
    #print(Man_of_Match)
    
    mid=0
    mycursor.execute("select max(mid) from ipl_match")
    output=mycursor.fetchall()
    if (output[0][0]==None) :
        mid=1
    else :
        mid=int(output[0][0])+1
    
    tid1=Team_Entry(teams[0],mydb,mycursor)
    tid2=Team_Entry(teams[1],mydb,mycursor)
    
    wid=0
    mycursor.execute("SELECT * FROM team where tname=\""+Winner+"\"")
    output=mycursor.fetchall()
    wid=output[0][0]
    
    MOM=0
    mycursor.execute("SELECT * FROM player where pname=\""+Man_of_Match[0]+"\"")
    output=mycursor.fetchall()
    MOM=output[0][0]
    
    sql = "INSERT INTO ipl_match (mid,year,month,d,tid1,tid2,venue,wid,MOM,first_i,second_i ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (str(mid),str(year),str(month),str(date),str(tid1),str(tid2),str(ground),str(wid),str(MOM),str(i1),str(i2))
    
    mycursor.execute(sql,val)
    
    
    #mydb.commit()
    return mid;
    
def Batsman_Data() :
    D={}
    D["Runs"]=0
    D["Four"]=0
    D["Six"]=0
    D["Balls"]=0
    D["Out_Type"]="Not_Out"
    
    return D    

def Bowler_Data() :
    D={}
    D["Balls"]=0
    D["Wickets"]=0
    D["Extra"]=0
    D["Runs"]=0
    D["Four"]=0
    D["Six"]=0
    
    return D

def Inning(Inn) :
    team=Inn["team"]
    deliveries=Inn["deliveries"]
    #print(deliveries)
    batsman={}
    bowler={}
    Extra=0
    
    for d in deliveries :
        ball=list(d.keys())[0]
        
        bman=d[ball]["batsman"]
        
        if bman not in batsman:
            batsman[bman]=Batsman_Data()
        
        boler=d[ball]["bowler"]
        if boler not in bowler :
            bowler[boler]=Bowler_Data()
        
        if(d[ball]["runs"]["extras"]==0):
            batsman[bman]["Balls"]+=1
            bowler[boler]["Balls"]+=1
        
        if "runs" in d[ball] :
            batsman[bman]["Runs"]+=d[ball]["runs"]["batsman"]
            if (d[ball]["runs"]["batsman"]== 4):
                batsman[bman]["Four"]+=1
                bowler[boler]["Four"]+=1
            
            if (d[ball]["runs"]["batsman"]== 6):
                batsman[bman]["Six"]+=1
                bowler[boler]["Six"]+=1
                
        
        
        #if ball-Over == 0.5 :
         #   bowler[boler]["Overs"]+=1
        
        if "runs" in d[ball] :
            bowler[boler]["Extra"]+=d[ball]["runs"]["extras"]
            bowler[boler]["Runs"]+=d[ball]["runs"]["total"]
            Extra+=d[ball]["runs"]["extras"]
        
        if "wicket" in d[ball] :
            bowler[boler]["Wickets"]+=1
            batsman[bman]["Out_Type"]=d[ball]["wicket"]["kind"]
            #batsman[bman]["Out"]+=1
            
        
    return batsman,bowler,Extra
def Inning_Entry_Database(First_Inning,mydb,mycursor) :
    iid=0
    mycursor.execute("select max(iid) from Innings")
    output=mycursor.fetchall()
    if (output[0][0]==None) :
        sql = "INSERT INTO Innings (iid, extra) VALUES (%s,%s)"
        val = (str(1),str(First_Inning[2]))
        iid=1
        mycursor.execute(sql,val)
    else :
        sql = "INSERT INTO Innings (iid, extra) VALUES (%s,%s)"
        val = (str(int(output[0][0])+1),str(First_Inning[2]))
        iid=int(output[0][0])+1
        mycursor.execute(sql,val)
    #print(str(iid)+" Inserted")
    
    
    for b in First_Inning[0] :
        mycursor.execute("SELECT * FROM Player where pname=\""+b+"\"")
        output=mycursor.fetchall()
        if (output==[]) :
            mycursor.execute("select max(pid) from player")
            output=mycursor.fetchall()
            if (output[0][0]==None) :
                sql = "INSERT INTO Player (pid, pname) VALUES (%s,%s)"
                val = (str(1),str(b))
                mycursor.execute(sql,val)
            else :
                sql = "INSERT INTO Player (pid, pname) VALUES (%s,%s)"
                val = (str(int(output[0][0])+1),str(b))
                mycursor.execute(sql,val)
            #print(b+" Inserted In player")
            
        mycursor.execute("SELECT * FROM Player where pname=\""+b+"\"")
        output=mycursor.fetchall()
        sql = "INSERT INTO Batting (iid, pid,runs,fours,six,balls,out_type) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (str(iid),str(output[0][0]),str(First_Inning[0][b]["Runs"]),str(First_Inning[0][b]["Four"]),str(First_Inning[0][b]["Six"]),str(First_Inning[0][b]["Balls"]),str(First_Inning[0][b]["Out_Type"]))
        mycursor.execute(sql,val)
        
        #print(str(b)+" Entry Inserted")
   
    
    
    for b in First_Inning[1] :
        mycursor.execute("SELECT * FROM Player where pname=\""+b+"\"")
        output=mycursor.fetchall()
        if (output==[]) :
            mycursor.execute("select max(pid) from player")
            output=mycursor.fetchall()
            if (output[0][0]==None) :
                sql = "INSERT INTO Player (pid, pname) VALUES (%s,%s)"
                val = (str(1),str(b))
                mycursor.execute(sql,val)
            else :
                sql = "INSERT INTO Player (pid, pname) VALUES (%s,%s)"
                val = (str(int(output[0][0])+1),str(b))
                mycursor.execute(sql,val)
            #print(b+" Inserted In player")
        mycursor.execute("SELECT * FROM Player where pname=\""+b+"\"")
        output=mycursor.fetchall()
        
        
        sql = "INSERT INTO Bowling (iid, pid,balls,wickets,extra,runs,four,sixes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (str(iid),str(output[0][0]),str(First_Inning[1][b]["Balls"]),str(First_Inning[1][b]["Wickets"]),str(First_Inning[1][b]["Extra"]),str(First_Inning[1][b]["Runs"]),str(First_Inning[1][b]["Four"]),str(First_Inning[1][b]["Six"]))
        mycursor.execute(sql,val)
        
        #print(str(b)+" Entry Inserted")
    
    #mycursor.execute(sql,val)
    
    #mydb.commit()
    return iid;

def sortfunc(e) :
    e=e.split(".")[0]
    return int(e)

def DBMS_Entry(filename) :
    f=open(os.path.join("../ipl1/", filename), 'r')
    docs = yaml.load(f, Loader=yaml.FullLoader)
    First_Inning=Inning(docs["innings"][0]["1st innings"])
    Second_Inning=Inning(docs["innings"][1]["2nd innings"])
    #print(First_Inning[0])
    
    mydb = mysql.connector.connect(host="ipl-server.mysql.database.azure.com",user="nmsc@ipl-server",password="nm@12345",database="IPL")
    mycursor = mydb.cursor()
    '''
    #iid=1
    #sql = "INSERT INTO Innings (iid, extra) VALUES (%s,%s)"
    #val = (str(iid),str(First_Inning[2]))
    '''
    i1=Inning_Entry_Database(First_Inning, mydb, mycursor)
    print("Inning 1 Over")
    
    i2=Inning_Entry_Database(Second_Inning, mydb, mycursor)
    print("Inning 2 Over")
    
    mid=Match_Metadata_Entry(docs["info"],i1,i2,mydb,mycursor)
    print(str(mid)+ " Inserted")
    print(filename+" Completed\n\n")
    mydb.commit()
    mydb.close()
    f.close()
T=[]
def main() :
    #start the loop from here below for every match file 
    # Match Files Loop #Make the following given code iterative for every yml file for one season
    
    files=[]
    
    for filename in os.listdir("../ipl1/"):
        files.append(filename)
    files.sort(key=sortfunc)
    print(files)
    
    for i in range(len(files)) :
        DBMS_Entry(files[i])
    print("Over")
        
        
            
            
        
    
    
    
    
    '''
    #print("First Inning :")
    #print ("Batting:gg")
    for v in First_Inning[0]:
        if v not in Batsman_List:
            Batsman_List[v] = First_Inning[0][v]
            
        else:
            Batsman_List[v]["Runs"]+=First_Inning[0][v]["Runs"]
            Batsman_List[v]["Four"]+=First_Inning[0][v]["Four"]
            Batsman_List[v]["Six"]+=First_Inning[0][v]["Six"]
            Batsman_List[v]["Balls"]+=First_Inning[0][v]["Balls"]
            Batsman_List[v]["Out"]+=First_Inning[0][v]["Out"]
        if(First_Inning[0][v]["Runs"]>=100):
            Batsman_List[v]["100's"]+=1
        elif(First_Inning[0][v]["Runs"]>=50):
            Batsman_List[v]["50's"]+=1
    #print(Batsman_List)
        
    #print("/*********************************/")
    #print ("Bowling:\n\n")
    
    for v in First_Inning[1]:
        if v not in Bowler_List:
            Bowler_List[v] = First_Inning[1][v]
            
        else:
            Bowler_List[v]["Runs"]+=First_Inning[1][v]["Runs"]
            Bowler_List[v]["Four"]+=First_Inning[1][v]["Four"]
            Bowler_List[v]["Six"]+=First_Inning[1][v]["Six"]
            Bowler_List[v]["Balls"]+=First_Inning[1][v]["Balls"]
            Bowler_List[v]["Extra"]+=First_Inning[1][v]["Extra"]
            Bowler_List[v]["Wickets"]+=First_Inning[1][v]["Wickets"]
        if(First_Inning[1][v]["Wickets"]>=5):
            Bowler_List[v]["5 Wickets"]+=1
        elif(First_Inning[1][v]["Wickets"]>=3):
            Bowler_List[v]["3 Wickets"]+=1
    #print(Bowler_List)
    #print("/*********************************/")
    #Extra+=First_Inning[2]
    #print("Extras:"+str(First_Inning[2]))    
    #print("\n\n")
    
    #print("/*********************************/")
    #print("Second Inning :")
    #print ("Batting:\n\n")
    for v in Second_Inning[0]:
        if v not in Batsman_List:
            Batsman_List[v] = Second_Inning[0][v]
            
        else:
            Batsman_List[v]["Runs"]+=Second_Inning[0][v]["Runs"]
            Batsman_List[v]["Four"]+=Second_Inning[0][v]["Four"]
            Batsman_List[v]["Six"]+=Second_Inning[0][v]["Six"]
            Batsman_List[v]["Balls"]+=Second_Inning[0][v]["Balls"]
            Batsman_List[v]["Out"]+=Second_Inning[0][v]["Out"]
        if(Second_Inning[0][v]["Runs"]>=100):
            Batsman_List[v]["100's"]+=1
        elif(Second_Inning[0][v]["Runs"]>=50):
            Batsman_List[v]["50's"]+=1
            
    #print(Batsman_List)   
    #print("/*********************************/")
    #print ("Bowling:\n\n")
    for v in Second_Inning[1]:
        if v not in Bowler_List:
            Bowler_List[v] = Second_Inning[1][v]
            
        else:
            Bowler_List[v]["Runs"]+=Second_Inning[1][v]["Runs"]
            Bowler_List[v]["Four"]+=Second_Inning[1][v]["Four"]
            Bowler_List[v]["Six"]+=Second_Inning[1][v]["Six"]
            Bowler_List[v]["Balls"]+=Second_Inning[1][v]["Balls"]
            Bowler_List[v]["Extra"]+=Second_Inning[1][v]["Extra"]
            Bowler_List[v]["Wickets"]+=Second_Inning[1][v]["Wickets"]
        if(Second_Inning[1][v]["Wickets"]>=5):
            Bowler_List[v]["5 Wickets"]+=1
        elif(Second_Inning[1][v]["Wickets"]>=3):
            Bowler_List[v]["3 Wickets"]+=1
            
    ##removw this print bowler_list statement in the below line
    #print(Bowler_List)
        
    #print("\n/*********************************/")
    #Extra+=Second_Inning[2]
    #print("Extras:"+str(Second_Inning[2]))
    #print("\n\n")
    #print("Total Extras",Extra)
    
    
    
    ## End the loop started for each match file here
    for v in Batsman_List:
        Batsman_List[v]["Strike Rate"] = Batsman_List[v]["Runs"]*100/Batsman_List[v]["Balls"]
        if (Batsman_List[v]["Out"]>0):
            Batsman_List[v]["Average"] = Batsman_List[v]["Runs"]/Batsman_List[v]["Out"]
        else:
            Batsman_List[v]["Average"] = Batsman_List[v]["Runs"]
    for v in Bowler_List:
        
        if(Bowler_List[v]["Wickets"]>0):
            Bowler_List[v]["Economy"] = 6*Bowler_List[v]["Runs"]/Bowler_List[v]["Balls"]
            Bowler_List[v]["Average"] = Bowler_List[v]["Runs"]/Bowler_List[v]["Wickets"]
            Bowler_List[v]["Strike Rate"] = Bowler_List[v]["Balls"]/Bowler_List[v]["Wickets"]
        else:
            Bowler_List[v]["Average"] = Bowler_List[v]["Runs"]
            Bowler_List[v]["Strike Rate"] = Bowler_List[v]["Balls"]
            
    print("Batsman:\n")
    for v in Batsman_List:
        print(v,Batsman_List[v])
    print("\n\n Bowling: \n")
    for v in Bowler_List:
        print(v,Bowler_List[v])
    '''       
if __name__=="__main__" :
    main()