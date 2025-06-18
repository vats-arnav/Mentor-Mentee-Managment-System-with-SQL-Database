import time
import datetime
import tabulate
from  tabulate import tabulate
from datetime import datetime
import mysql.connector
from mysql.connector import Error

mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="tiger", buffered=True)
if mydb.is_connected():
    print("Ok....Connection Made....")
    print(mydb)

    try:
        mycursor = mydb.cursor()
        mycursor.execute("create database if not exists MENTOR_MENTEE_PORTAL")
        mycursor.execute('use MENTOR_MENTEE_PORTAL')

        # Create Mentee_Master table
        sql_create = """CREATE TABLE IF NOT EXISTS mentee_master (
                            me_id INT(5) UNSIGNED ZEROFILL NOT NULl AUTO_INCREMENT,
                            me_name VARCHAR(30) NOT NULL,
                            me_class VARCHAR(3) NOT NULL,
                            me_interest VARCHAR(100) NOT NULL,
                            me_region VARCHAR(20),
                            me_email VARCHAR(30),
                            me_mob CHAR(10) NOT NULL,
                            me_username VARCHAR(10) NOT NULL,
                            me_pwd VARCHAR(10) NOT NULL,
                            PRIMARY KEY(me_id)
                        )
                     """
        mycursor.execute(sql_create)

        # # Alter Mentee_Master table for Mentee_ID auto generation
        # sql_alter = """ALTER TABLE mentee_master AUTO_INCREMENT = 1"""
        # mycursor.execute(sql_alter)

        # Populate Mentee_Master table
        sql_insert = """INSERT INTO mentee_master
                    (me_name, me_class, me_interest, me_region, me_email, me_mob, me_username, me_pwd)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        mycursor.execute(sql_insert, ("Arnav Vats", "XII", "Robotics", "North Delhi", "1@ab.com", "9898989898", "u1", "pw1"))
        mycursor.execute(sql_insert, ("Ansh Vats", "XI", "AI", "North Delhi", "a2@bc.com", "9898989898", "u2", "pw2"))
        mycursor.execute(sql_insert, ("Aryan Dhingra", "XI", "Creative Writing", "West Delhi", "a23@gc.com", "9797979798", "u3", "pw3"))
        mycursor.execute(sql_insert, ("Sharanya Gupta", "XI", "Career Counselling", "North Delhi", "123@gc.com", "9891122330", "u4", "pw4"))
        mycursor.execute(sql_insert, ("Mayank Rathi", "XI", "Management", "East Delhi", "12@gc.com", "9898989898", "u5", "pw5"))
        mycursor.execute(sql_insert, ("Rashmi Narang", "XII", "Entrepreneurship", "South Delhi", "1a23@gc.com", "9889098760", "u6", "pw6"))
        mycursor.execute(sql_insert, ("Neera Sharma", "XI", "Engineering", "North Delhi", "hg45@gc.com", "8500120034", "u7", "pw7"))
        mycursor.execute(sql_insert, ("Akshay Chauhan", "XII", "Entrepreneurship", "North Delhi", "fra23@gc.com", "9800987679", "u8", "pw8"))
        mycursor.execute(sql_insert, ("Priya Dhingra", "XI", "Creative Writing", "West Delhi", "afs@gc.com", "8797979798", "u19", "pw9"))
        mycursor.execute(sql_insert, ("Garima Vohra", "XII", "Career Counselling", "East Delhi", "nm23@gc.com", "9891122330", "u10", "pw10"))
        mycursor.execute(sql_insert, ("Manya Jain", "XI", "Teaching", "South Delhi", "a2bb@gc.com", "9898989898", "u11", "pw11"))
        mycursor.execute(sql_insert, ("Pawan Nagpal", "XII", "Fashion Tech", "East Delhi", "aaa@gc.com", "8890987690", "u12", "pw12"))
        mycursor.execute(sql_insert, ("Dheeraj Agrawal", "XII", "Finance", "South Delhi", "ggg@gc.com", "9890546534", "u13", "pw13"))
        mycursor.execute(sql_insert, ("Ambika Bhargava", "XI", "Soft Engg", "West Delhi", "ab@ab.com", "9811223344", "u14", "pw14"))
        mycursor.execute(sql_insert, ("Ravi Mishra", "XII", "Volunteering", "North Delhi", "rm@rm.com", "9812334123", "u15", "pw15"))

        # Create Mentor_Master table
        sql_create = """CREATE TABLE IF NOT EXISTS mentor_master (
                            mo_id INT(5) UNSIGNED ZEROFILL NOT NULl AUTO_INCREMENT,
                            mo_name VARCHAR(30) NOT NULL,
                            mo_qual VARCHAR(20) NOT NULL,
                            mo_class VARCHAR(20) NOT NULL,
                            mo_interest VARCHAR(100) NOT NULL,
                            mo_region VARCHAR(20),
                            mo_meetingmode VARCHAR(20),
                            mo_email VARCHAR(30),
                            mo_mob CHAR(10) NOT NULL,
                            mo_username VARCHAR(10) NOT NULL,
                            mo_pwd VARCHAR(10) NOT NULL,
                            PRIMARY KEY(mo_id)
                        )
                     """
        mycursor.execute(sql_create)

        # # Alter Mentor_Master table for Mentor_ID auto generation
        # sql_alter = """ALTER TABLE mentee_master AUTO_INCREMENT = 1"""
        # mycursor.execute(sql_alter)

        # Populate Mentor_Master table
        sql_insert = """INSERT INTO mentor_master
                                (mo_name, mo_qual, mo_class, mo_interest, mo_region, mo_meetingmode, mo_email, mo_mob, mo_username, mo_pwd)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        mycursor.execute(sql_insert, ("Asmita Sharma", "MS", "XI, XII", "AI, Robotics, Teaching", "North Delhi", "Online", "av@gc.com", "9123456222", "u1", "pw1"))
        mycursor.execute(sql_insert, ("Shekhar Tyagi", "MA", "XI, XII", "Creative Writing, Teaching, Career Counselling", "East Delhi", "Offline", "av@gc.com", "9345678922", "u2", "pw2"))
        mycursor.execute(sql_insert, ("Madhu Bhatia", "MBA", "XI, XII", "Entrepreneurship, Management, Volunteering", "North Delhi", "Online, Offline", "av@gc.com", "9234567891", "u3", "pw3"))
        mycursor.execute(sql_insert, ("Rishabh Jain", "BTech", "XI, XII", "AI, Soft Engg, App Development", "West Delhi", "Online, Offline", "av@gc.com", "9434567893", "u4", "pw4"))
        mycursor.execute(sql_insert, ("Kavya Sridhar", "PhD", "XI, XII", "Creative Writing, Career Counselling, Teaching", "South Delhi", "Online", "av@gc.com", "9987127893", "u5", "pw5"))
        mycursor.execute(sql_insert, ("Vikrant Kundu", "MCom", "XI, XII", "Finance, Management, Startups", "West Delhi", "Online", "av@gc.com", "8789231209", "u6", "pw6"))
        mycursor.execute(sql_insert, ("Nayan Malhotra", "PhD", "XI, XII", "Soft Engg, Robotics, Startups", "North Delhi", "Online, Offline", "nm@gm.com", "9120981256", "u7", "pw7"))

        # Create Mentor_Availability table
        sql_create = """CREATE TABLE IF NOT EXISTS mentor_availability (
                                mto_id INT(5) UNSIGNED ZEROFILL NOT NULL,
                                meet_available_day VARCHAR(10) NULL,
                                meet_available_date DATE NOT NULL,
                                meet_available_time TIME NOT NULL,
                                meet_mode VARCHAR(7) NULL,
                                PRIMARY KEY(mto_id, meet_available_date, meet_available_time),
                                CONSTRAINT fk_mentor_availability FOREIGN KEY (mto_id) REFERENCES mentor_master(mo_id))
                         """
        mycursor.execute(sql_create)

        # Populate Mentor_Mentee_Availability table
        sql_insert = """INSERT INTO mentor_availability
                                        (mto_id, meet_available_day, meet_available_date, meet_available_time, meet_mode)
                                        VALUES (%s, %s, %s, %s, %s)"""

        mycursor.execute(sql_insert, (1, "", "2022-09-18", "16:00:00", "Online"))
        mycursor.execute(sql_insert, (1, "", "2022-09-20", "16:00:00", "Online"))
        mycursor.execute(sql_insert, (1, "", "2022-09-20", "18:00:00", "Online"))
        mycursor.execute(sql_insert, (1, "", "2022-09-24", "18:00:00", "Online"))
        mycursor.execute(sql_insert, (1, "", "2022-09-24", "20:00:00", "Online"))

        mycursor.execute(sql_insert, (2, "", "2022-09-20", "16:00:00", "Online"))
        mycursor.execute(sql_insert, (2, "", "2022-09-22", "18:00:00", "Offline"))
        mycursor.execute(sql_insert, (2, "", "2022-09-23", "19:00:00", "Offline"))
        mycursor.execute(sql_insert, (2, "", "2022-09-24", "20:00:00", "Offline"))

        mycursor.execute(sql_insert, (3, "", "2022-09-20", "16:00:00", "Offline"))
        mycursor.execute(sql_insert, (3, "", "2022-09-21", "19:00:00", "Online"))
        mycursor.execute(sql_insert, (3, "", "2022-09-21", "20:00:00", "Online"))

        mycursor.execute(sql_insert, (4, "", "2022-09-20", "16:00:00", "Online"))
        mycursor.execute(sql_insert, (4, "", "2022-09-22", "17:00:00", "Offline"))
        mycursor.execute(sql_insert, (4, "", "2022-09-23", "19:00:00", "Online"))

        mycursor.execute(sql_insert, (5, "", "2022-09-20", "20:00:00", "Online"))
        mycursor.execute(sql_insert, (5, "", "2022-09-25", "17:00:00", "Online"))

        mycursor.execute(sql_insert, (6, "", "2022-09-21", "16:00:00", "Online"))
        mycursor.execute(sql_insert, (6, "", "2022-09-21", "19:00:00", "Online"))
        mycursor.execute(sql_insert, (6, "", "2022-09-25", "17:00:00", "Online"))

        mycursor.execute(sql_insert, (7, "", "2022-09-21", "18:00:00", "Online"))
        mycursor.execute(sql_insert, (7, "", "2022-09-22", "19:00:00", "Offline"))
        mycursor.execute(sql_insert, (7, "", "2022-09-23", "19:00:00", "Offline"))

        # Fetching records from Mentor Availability table
        print("\n*** MENTOR AVAILABILITY TABLE ***".center(30))
        sql_all = """SELECT * FROM mentor_availability"""
        mycursor.execute(sql_all)
        records = mycursor.fetchall()
        if len(records) == 0:
            print("\nTable is empty! ")
            # input("Click enter to proceed...")
        else:
            # Converting MySQL date object (day of the week) into string format
            sql_dayname = """UPDATE mentor_availability SET meet_available_day = DAYNAME(%s) WHERE meet_available_date = %s"""
            for row in records:
                inputdata = (str(row[2]), str(row[2]))
                mycursor.execute(sql_dayname, inputdata)

        # Fetching records using INNER JOIN on Mentor Availability and Mentor Master tables
        sql_all = """SELECT ma.mto_id, ms.mo_name, ma.meet_available_day, DATE_FORMAT(ma.meet_available_date, '%M %d %Y'), LOWER(DATE_FORMAT(ma.meet_available_time,'%l:%i %p')), ma.meet_mode 
                         FROM mentor_availability AS ma 
                         INNER JOIN mentor_master AS ms
                         ON ma.mto_id = ms.mo_id
                         """
        mycursor.execute(sql_all)
        records = mycursor.fetchall()
        print(tabulate(records, headers=["Mentor ID", "Mentor Name", "Available Day", "Available Date", "Available Time",
                                         "Meeting Mode"],
                       tablefmt='pretty'))

        # Create Mentor_Mentee_Schedule table
        sql_create = """CREATE TABLE IF NOT EXISTS mentor_mentee_schedule (
                        meeting_id INT(5) UNSIGNED ZEROFILL NOT NULl AUTO_INCREMENT,
                        mto_id INT(5) UNSIGNED ZEROFILL NOT NULL,
                        mte_id INT(5) UNSIGNED ZEROFILL NOT NULL,
                        meet_day VARCHAR(10) NULL,
                        meet_date DATE NOT NULL,
                        meet_time TIME NOT NULL,
                        meet_mode VARCHAR(7) NOT NULL,
                        PRIMARY KEY(meeting_id),
                        CONSTRAINT uq_mentor_mentee_mo UNIQUE (mto_id, mte_id, meet_date, meet_time),
                        CONSTRAINT fk1_mentor_mentee_mo FOREIGN KEY (mto_id) REFERENCES mentor_master(mo_id),
                        CONSTRAINT fk2_mentor_mentee_me FOREIGN KEY (mte_id) REFERENCES mentee_master(me_id));
                     """
        mycursor.execute(sql_create)

        # Populate Mentor_Mentee_Schedule table
        sql_insert = """INSERT INTO mentor_mentee_schedule
                                (meeting_id, mto_id, mte_id, meet_day, meet_date, meet_time, meet_mode)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        mycursor.execute(sql_insert, (1, 1, 1, "", "2022-09-17", "16:00:00", "Online"))
        mycursor.execute(sql_insert, (2, 1, 2, "", "2022-09-28", "18:00:00", "Online"))
        mycursor.execute(sql_insert, (3, 4, 2, "", "2022-09-19", "17:00:00", "Offline"))
        mycursor.execute(sql_insert, (4, 5, 3, "", "2022-09-30", "20:00:00", "Online"))
        mycursor.execute(sql_insert, (5, 1, 3, "", "2022-09-17", "16:00:00", "Online"))
        mycursor.execute(sql_insert, (6, 1, 1, "", "2022-09-19", "18:00:00", "Online"))
        mycursor.execute(sql_insert, (7, 1, 1, "", "2022-09-28", "20:00:00", "Online"))
        mycursor.execute(sql_insert, (8, 5, 4, "", "2022-09-26", "17:00:00", "Online"))
        mycursor.execute(sql_insert, (9, 2, 4, "", "2022-09-19", "16:00:00", "Online"))

        # Fetching records from Mentor Mentee Schedule table
        print("\n*** MENTOR MENTEE SCHEDULE TABLE ***".center(30))
        sql_all = """SELECT * FROM mentor_mentee_schedule"""
        mycursor.execute(sql_all)
        records = mycursor.fetchall()
        if len(records) == 0:
            print("\nTable is empty! ")
        else:
            # Converting MySQL date object (day of the week) into string format
            sql_dn = """UPDATE mentor_mentee_schedule SET meet_day = DAYNAME(%s) WHERE meet_date = %s"""
            for row in records:
                inputdata = (str(row[4]), str(row[4]))
                mycursor.execute(sql_dn, inputdata)

        # Fetching records using INNER JOIN on Mentor Availability and Mentor Master tables
        sql_all = """SELECT mms.meeting_id, mto_id, mte_id, meet_day, DATE_FORMAT(meet_date, '%M %d %Y'), LOWER(DATE_FORMAT(meet_time,'%l:%i %p')), meet_mode 
                     FROM mentor_mentee_schedule AS mms
                     INNER JOIN mentor_master AS mom
                     ON mms.mto_id = mom.mo_id
                  """
        mycursor.execute(sql_all)
        records = mycursor.fetchall()
        print(tabulate(records, headers=["Meeting ID", "Mentor ID", "Mentee ID", "Day", "Date", "Time", "Mode"], tablefmt='pretty'))
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        mydb.commit()
        mycursor.close()

