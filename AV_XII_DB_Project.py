# THE MENTOR_MENTEE_PORTAL
import os
import time
import re
import pwinput
import random
import mysql.connector
from tabulate import tabulate
from mysql.connector import Error
from os import system, name
from datetime import datetime

# Establishing a connection to the database 'MENTOR_MENTEE_PORTAL' in MySQL
mydb = mysql.connector.connect(host="127.0.0.1",user="root",password="tiger", buffered=True)
if mydb.is_connected():
    mycursor = mydb.cursor()
    mycursor.execute("create database if not exists MENTOR_MENTEE_PORTAL")
    mycursor.execute('use MENTOR_MENTEE_PORTAL')

def clear():                        # To clear the screen
    # for windows the name is 'nt'
    if name == 'nt':
        _ = system('cls')
    # and for mac and linux, the os.name is 'posix'
    else:
        _ = system('clear')
def welcome():
    clear()
    print('*' * 180)
    print(' ' * 180)
    print('WELCOME TO THE MENTOR-MENTEE PORTAL'.center(180))
    print(' ' * 180)
    print('*' * 180)
    print()
def make_directory(path):                # To create a directory, if not exixts
    if not os.path.exists(path):
        # if the demo_folder directory is not present
        # then create it.
        os.makedirs(path)
def isValidMob(mob):                # To check validity of a 10-digit mobile number
    if mob.isdigit() and (mob.startswith('7') or mob.startswith('8') or mob.startswith('9')) and len(mob) == 10:
        return True
    else:
        return False
def isValidEMail(email):            # To check validity of an email address
    """
    Both the local part and the domain name can contain one or more dots, but no two dots can appear right next to each other.
    The first and last characters in the local part and in the domain name must not be dots.
    Domain name must include at least one dot, and that the part of the domain name after the last dot can only consist of letters.
    Domain name must include at least one dot, and that the part of the domain name after the last dot can only consist of letters.
    The top-level domain (.com in these examples) must consist of two to three letters only.
    """
    regex = "^[a-zA-Z0-9_!#$%&'*+/=?`{|}~^-]+(?:\\.[\\w!#$%&'*+/=?`{|}~^-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,3}$"
    if(re.search(regex,email)):
        return True
    else:
        return False

def view_mentee_schd_meetings(username, pwd):
    sql_all = """SELECT mms.meeting_id, mem.me_name, mom.mo_name, mms.meet_day, DATE_FORMAT(mms.meet_date, '%M %d %Y'), LOWER(DATE_FORMAT(mms.meet_time,'%l:%i %p')), mms.meet_mode 
                  FROM mentor_mentee_schedule AS mms 
                  INNER JOIN mentor_master AS mom
                  INNER JOIN mentee_master AS mem
                  ON mms.mto_id = mom.mo_id 
                  AND mms.mte_id = mem.me_id
                  WHERE mem.me_username = %s
                  AND mem.me_pwd = %s 
                  ORDER BY mms.meet_date, mms.meet_time
               """
    inputdata = (username, pwd)
    mycursor = mydb.cursor()
    try:
        mycursor.execute(sql_all, inputdata)
        records_meet = mycursor.fetchall()
        if len(records_meet) == 0:
            print("\nSorry, no record found!")
            input("Click enter to proceed...")
            print("Returning to Mentee Menu...")
            time.sleep(2)
        else:
            print("Displaying your meeting details...")
            print('-' * 180)
            print("SCHEDULED MEETING APPOINTMENTS".center(100))
            print(tabulate(records_meet,
                           headers=["Meeting ID", "Mentee Name", "Mentor Name", "Day", "Date", "Time", "Mode"],
                           tablefmt='pretty'))
            print('-' * 180)
            print(mycursor.rowcount, "record(s) fetched.")
            print()
            input("Click enter to proceed...")
            print("Returning to Mentee Menu...")
            time.sleep(2)
    except mysql.connector.Error:
        print("Failed to delete record from table. Record may no longer exists!")
        input("Click enter to proceed...")
        print("Returning to Mentee Menu...")
        time.sleep(2)
    finally:
        if mydb.is_connected():
            mycursor.close()
def del_a_meeting_with_mentor(username):
    try:
        del_meet_id = int(input("Enter the ID of the meeting you want to cancel: "))
        sql_all = """SELECT * FROM mentor_mentee_schedule AS mms
                     INNER JOIN mentee_master AS mem 
                     ON mms.mte_id = mem.me_id
                     WHERE mem.me_username = %s
                     AND mms.meeting_id = %s
                  """
        mycursor = mydb.cursor()
        inputdata = (username, del_meet_id)
        try:
            mycursor.execute(sql_all, inputdata)
            record_meet = mycursor.fetchone()
            if record_meet is None:
                print("\nNo record found!")
                input("Click enter to proceed...")
                print("Returning to Mentee Menu...")
                time.sleep(2)
            else:
                ch_del = input("Are you sure to delete the meeting? (Y/N): ").title()
                if ch_del == 'Y':
                    sql_delete = """DELETE FROM mentor_mentee_schedule WHERE meeting_id = %s"""
                    try:
                        mycursor = mydb.cursor()
                        mycursor.execute(sql_delete, (del_meet_id,))
                        mydb.commit()
                        print("Deleting record...")
                        time.sleep(2)
                        print(mycursor.rowcount, " record(s) deleted successfully!")
                        input("Click enter to proceed...")
                        print("Returning to Mentee Menu....")
                        time.sleep(2)
                    except mysql.connector.Error:
                        print("Failed to delete record from table. Record may no longer exists!")
                        input("Click enter to proceed...")
                        print("Returning to Meeting Cancellation Menu...")
                        time.sleep(2)
        except mysql.connector.Error as e:
            print("Failed to delete record from table. Record may no longer exists!", e)
            input("Click enter to proceed...")
            print("Returning to Meeting Cancellation Menu...")
            time.sleep(2)
        finally:
            if mydb.is_connected():
                mycursor.close()
    except ValueError:
        print("INVALID CHOICE!")
        choice = 0
        input("Click enter to proceed...")
        print("Returning to Meeting Cancellation Menu...")
        time.sleep(2)
def del_all_meetings_with_mentor(username):
    ch_del = input("Are you sure to delete all records? (Y/N): ").title()
    if ch_del == 'Y':
        sql_all = """SELECT mms.mte_id FROM mentor_mentee_schedule AS mms
                     INNER JOIN mentee_master AS mem 
                     ON mms.mte_id = mem.me_id
                     WHERE mem.me_username = %s
                  """
        mycursor = mydb.cursor()
        try:
            mycursor.execute(sql_all, (username,))
            record_meet = mycursor.fetchone()
            if len(record_meet) == 0:
                print("\nNo record found!")
                input("Click enter to proceed...")
                print("Returning to Mentee Menu...")
                time.sleep(2)
            else:
                sql_delete = """DELETE FROM mentor_mentee_schedule WHERE mte_id = %s"""
                try:
                    mycursor = mydb.cursor()
                    mycursor.execute(sql_delete, (record_meet[0],))
                    mydb.commit()
                    print("Deleting record...")
                    time.sleep(2)
                    print(mycursor.rowcount, " record(s) deleted successfully!")
                    input("Click enter to proceed...")
                    print("Returning to Mentee Menu....")
                    time.sleep(2)
                except mysql.connector.Error:
                    print("Failed to delete record from table. Record may no longer exists!")
                    input("Click enter to proceed...")
                    print("Returning to Meeting Cancellation Menu...")
                    time.sleep(2)
        except mysql.connector.Error:
            print("Failed to delete record from table. Record may no longer exists!")
            input("Click enter to proceed...")
            print("Returning to Meeting Cancellation Menu...")
            time.sleep(2)
        finally:
            if mydb.is_connected():
                mycursor.close()
    elif ch_del == 'N':
        print("No problem...")
        print("Returning to Mentee Menu...")
        time.sleep(2)
    else:
        print("INVALID CHOICE!")
        input("Click enter to proceed...")
        print("Returning to Meeting Cancellation Menu...")
        time.sleep(2)
def cancel_meeting(username, pwd):
    sql_meet = """SELECT mms.meeting_id, mem.me_name, mom.mo_name, mms.meet_day, DATE_FORMAT(mms.meet_date, '%M %d %Y'), LOWER(DATE_FORMAT(mms.meet_time,'%l:%i %p')), mms.meet_mode 
                  FROM mentor_mentee_schedule AS mms 
                  INNER JOIN mentor_master AS mom
                  INNER JOIN mentee_master AS mem
                  ON mms.mto_id = mom.mo_id 
                  AND mms.mte_id = mem.me_id
                  WHERE mem.me_username = %s
                  AND mem.me_pwd = %s
               """
    inputdata = (username, pwd)
    mycursor = mydb.cursor()
    try:
        mycursor.execute(sql_meet, inputdata)
        records_meet = mycursor.fetchall()
        if len(records_meet) == 0:
            print("\nNo record found!")
            input("Click enter to proceed...")
            print("Returning to Mentee Menu...")
            time.sleep(2)
        else:
            choice = 0
            while choice != 3:
                welcome()
                print("Displaying your meeting details...")
                print('-' * 180)
                print("MEETING APPOINTMENTS".center(100))
                print(tabulate(records_meet,
                               headers=["Meeting ID", "Mentee Name", "Mentor Name", "Day", "Date", "Time", "Mode"],
                               tablefmt='pretty'))
                print('-' * 180)
                print(mycursor.rowcount, "record(s) fetched.")
                print()
                print("----------------------------------".ljust(100))
                print("MEETING CANCELLATION MENU".center(30))
                print("----------------------------------".ljust(100))
                print("1. Cancel all meetings")
                print("2. Cancel a meeting")
                print("3. Return to Mentee Menu")
                try:
                    choice = int(input("Enter your choice: "))
                    if choice == 1:
                        del_all_meetings_with_mentor(username)
                        break
                    elif choice == 2:
                        del_a_meeting_with_mentor(username)
                        break
                    elif choice == 3:
                        print("Returning to Mentee Menu...")
                        time.sleep(2)
                        break
                    else:
                        print("INVALID CHOICE!")
                        input("Click enter to proceed...")
                        print("Returning to Meeting Cancellation Menu...")
                        time.sleep(2)
                except ValueError:
                    print("INVALID CHOICE!")
                    choice = 0
                    input("Click enter to proceed...")
                    print("Returning to Meeting Cancellation Menu...")
                    time.sleep(2)
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
        input("Click enter to proceed...")
        print("Returning to Mentee Menu...")
        time.sleep(2)
    finally:
        if mydb.is_connected():
            mycursor.close()
def del_availability_record(mto_id, meet_date, meet_time):
    sql_delete = """DELETE FROM mentor_availability 
                    WHERE mto_id = %s AND meet_available_date = %s AND meet_available_time = %s"""
    inputdata = (mto_id, meet_date, meet_time)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql_delete, inputdata)
        mydb.commit()
    except mysql.connector.Error as e:
        print("Failed to delete record from table. Record may no longer exists!", e)
        input("Click enter to proceed...")
def gen_appointment_slip(username, pwd):
    sql_print = """SELECT mms.meeting_id, mem.me_name, mom.mo_name, mms.meet_day, DATE_FORMAT(mms.meet_date, '%M %d %Y'), LOWER(DATE_FORMAT(mms.meet_time,'%l:%i %p')), mms.meet_mode 
                      FROM mentor_mentee_schedule AS mms 
                      INNER JOIN mentor_master AS mom
                      INNER JOIN mentee_master AS mem
                      ON mms.mto_id = mom.mo_id 
                      AND mms.mte_id = mem.me_id
                      WHERE mem.me_username = %s
                      AND mem.me_pwd = %s
                      ORDER BY mms.meet_date, mms.meet_time
                   """
    inputdata = (username, pwd)
    mycursor = mydb.cursor()
    try:
        mycursor.execute(sql_print, inputdata)
        record_meet = mycursor.fetchone()
        if record_meet is None:
            print("\nSorry, no record found!")
            input("Click enter to proceed...")
            print("Returning to Mentee Menu...")
            time.sleep(2)
        else:
            print("----------------------------------".ljust(100))
            print("PRINT APPOINTMENT SLIP".center(30))
            print("----------------------------------".ljust(100))
            # print("Displaying your meeting details...")
            # print('-' * 180)
            # print("SCHEDULED MEETING APPOINTMENTS".center(100))
            # print(tabulate(record_meet,
            #                headers=["Meeting ID", "Mentee Name", "Mentor Name", "Day", "Date", "Time", "Mode"],
            #                tablefmt='pretty'))
            # print('-' * 180)
            # print(mycursor.rowcount, "record(s) fetched.")
            print()
            try:
                meet_id_print = int(input("Enter the Meeting ID for which appointment slip is to be generated: "))
                if record_meet[0] == meet_id_print:
                    print("Generating appointment slip...")
                    now = datetime.now()
                    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
                    dir = 'B:\\MentorMenteePortal\\Reports\\Mentee\\' + username + '\\AppointmentSlip'
                    make_directory(dir)
                    filename = 'B:\\MentorMenteePortal\\Reports\\Mentee\\' + username + '\\AppointmentSlip' + '\\AS_'+str(record_meet[0]).zfill(4)+'.txt'
                    try:
                        with open(filename, 'w+') as fin:
                            fin.write('*' * 100 + '\n')
                            fin.write('\n')
                            fin.write('APPOINTMENT SLIP'.center(100))
                            fin.write('\n')
                            fin.write(('Generated on: ' + date_time).rjust(100))
                            fin.write('\n')
                            fin.write('*' * 100 + '\n')
                            fin.write("Meeting ID:                  " + str(record_meet[0]).zfill(4) + '\n')
                            fin.write("Mentee Name:                 " + str(record_meet[1]) + '\n')
                            fin.write("Mentor Name:                 " + str(record_meet[2]) + '\n')
                            fin.write("Day of Appointment:          " + str(record_meet[3]) + '\n')
                            fin.write("Date of Appointment:         " + str(record_meet[4]) + '\n')
                            fin.write("Time of Appointment:         " + str(record_meet[5]) + '\n')
                            fin.write("Mode of the Meeting          " + str(record_meet[6]) + '\n')
                            fin.write("*" * 42 + " END OF REPORT " + "*" * 43)
                        print("Appointment slip generated successfully!")
                        input("Click enter to proceed...")
                        print("Returning to Mentee Menu....")
                        time.sleep(2)
                    except FileNotFoundError:
                        print("Failed to open file!")
                else:
                    print("Sorry, no record found!")
                    input("Click enter to proceed...")
                    print("Returning to Mentee Menu....")
                    time.sleep(2)
            except ValueError:
                print("INVALID CHOICE!")
                choice = 0
                input("Click enter to proceed...")
                print("Returning to Mentee Menu...")
                time.sleep(2)
    except mysql.connector.Error:
        print("Failed to delete record from table. Record may no longer exists!")
        input("Click enter to proceed...")
        print("Returning to Mentee Menu...")
        time.sleep(2)
    finally:
        if mydb.is_connected():
            mycursor.close()
def fix_meeting(mto_id, mte_id, meet_day, meet_date, meet_time, meet_mode):
    try:
        sql_insert = """INSERT INTO mentor_mentee_schedule
                        (mto_id, mte_id, meet_day, meet_date, meet_time, meet_mode)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
        recordTuple = (mto_id, mte_id, meet_day, meet_date, meet_time, meet_mode)
        try:
            mycursor.execute(sql_insert, recordTuple)
            mydb.commit()
            del_availability_record(mto_id, meet_date, meet_time)
            print("CONGRATULATIONS! Your meeting has been scheduled.\n")
            sql_all = """SELECT mms.meeting_id, mem.me_name, mom.mo_name, mms.meet_day, DATE_FORMAT(mms.meet_date, '%M %d %Y'), LOWER(DATE_FORMAT(mms.meet_time,'%l:%i %p')), mms.meet_mode 
                         FROM mentor_mentee_schedule AS mms 
                         INNER JOIN mentor_master AS mom
                         INNER JOIN mentee_master AS mem
                         ON mms.mto_id = mom.mo_id 
                         AND mms.mte_id = mem.me_id
                         WHERE mom.mo_id = %s AND mem.me_id = %s
                         AND mms.meet_date = %s AND mms.meet_time = %s AND mms.meet_mode = %s
                     """
            recordTuple = (mto_id, mte_id, meet_date, meet_time, meet_mode)
            print("Here are the meeting details: \n")
            mycursor.execute(sql_all,recordTuple)
            records_meet = mycursor.fetchall()
            if len(records_meet) == 0:
                print("\nSorry, no meeting record found!")
                input("Click enter to proceed...")
                print("Returning to Mentee Menu...")
                time.sleep(2)
            else:
                # mm.mo_name, mm.mo_qual, mm.mo_interest,
                # mm.mo_region, mo_email, mo_mob, ma.meet_available_day, ma.meet_available_date, ma.meet_available_time
                print('-' * 180)
                print(tabulate(records_meet, headers=["Meeting ID", "Mentor ID", "Mentee ID", "Day", "Date", "Time", "Mode"],
                             tablefmt='pretty'))
                print('-' * 180)
                input("Click enter to proceed...")
                print("Returning to Mentee Menu...")
                time.sleep(2)
        except mysql.connector.IntegrityError:
            print("\nA meeting is already scheduled on same day at same time! Try Again!!!")
            input("Click enter to proceed...")
            print("Returning to Mentee Menu...")
            time.sleep(2)
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
        input("Click enter to proceed...")
        print("Returning to Mentee Menu...")
        time.sleep(2)
    finally:
        if mydb.is_connected():
            mycursor.close()
def schedule_meeting(username, pwd):
    # (me_id, me_name, me_class, me_interest, me_region, me_meetingmode, me_email, me_mob, me_username, me_pwd)
    sql_me = """SELECT * FROM mentee_master WHERE me_username = %s AND me_pwd = %s"""
    inputdata_me = (username, pwd)

    # (mo_id, mo_name, mo_qual, mo_class, mo_interest, mo_region, mo_meetingmode, mo_email, mo_mob, mo_username, mo_pwd)
    sql_mo = """SELECT mm.mo_id, mm.mo_name, mm.mo_qual, mm.mo_interest, mm.mo_region, mo_email, mo_mob, ma.meet_available_day, ma.meet_available_date, ma.meet_available_time, ma.meet_mode
                FROM mentor_availability AS ma
                INNER JOIN mentor_master AS mm
                ON ma.mto_id = mm.mo_id
                WHERE mm.mo_interest LIKE CONCAT('%', %s, '%')
            """
    mycursor = mydb.cursor()
    try:
        mycursor.execute(sql_me, inputdata_me)
        record_me = mycursor.fetchone()
        if len(record_me) == 0:
            print("\nIncorrect username or password. Try Again!!!")
            input("Click enter to proceed...")
            print("Returning to Mentee Menu...")
            time.sleep(2)
        else:
            valid = 0
            while valid != 1:
                welcome()
                print("----------------------------------".ljust(100))
                print("CHECK MENTOR AVAILABILITY".center(30))
                print("----------------------------------".ljust(100))
                print("Displaying your details...")
                print(record_me)
                print()
                input("Click enter to proceed...")

                mycursor = mydb.cursor()
                # record_me[3] is Mentee interest
                mycursor.execute(sql_mo, (record_me[3],))
                records_mo = mycursor.fetchall()
                if len(records_mo) == 0:
                    print("\nSorry, no mentor matches your interests!")
                    input("Click enter to proceed...")
                    print("Returning to Mentee Menu...")
                    time.sleep(2)
                    break
                else:
                    # mm.mo_name, mm.mo_qual, mm.mo_interest,
                    # mm.mo_region, mo_email, mo_mob, ma.meet_available_day, ma.meet_available_date, ma.meet_available_time
                    print("Displaying details of mentors matching your interests...")
                    print('-' * 180)
                    print(tabulate(records_mo,
                                   headers=["ID", "Name", "Qualification", "Interests", "Region", "eMail", "Mobile Number",
                                            "Day", "Date", "Time", "Meeting Mode"],
                                   tablefmt='pretty'))
                    print('-' * 180)
                    print()
                    print("Please enter meeting details: ")
                    try:
                        meet_date = input("Enter date of meeting (yyyy-mm-dd): ")
                        datetime.strptime(meet_date, '%Y-%m-%d')
                    except ValueError:
                        print("INVALID CHOICE!")
                        input("Click enter to proceed...")
                        print("Returning to Check Mentor Availability Menu...")
                        time.sleep(2)
                        break
                    try:
                        meet_time = int(input("Enter preferred time slot for the meeting."
                                   "Enter preferred time slot for the meeting."
                                      "\nChoose from:\n  Press 1 for 4:00 pm (16:00:00)\n  Press 2 for 5:00 pm (17:00:00)\n  Press 3 for 6:00 pm (18:00:00)\n  Press 4 for 7:00 pm (19:00:00)\n  Press 5 for 8:00 pm (20:00:00)\n"))
                        if meet_time == 1:
                            meet_time = '4:00 pm'
                        elif meet_time == 2:
                            meet_time = '5:00 pm'
                        elif meet_time == 3:
                            meet_time = '6:00 pm'
                        elif meet_time == 4:
                            meet_time = '7:00 pm'
                        elif meet_time == 5:
                            meet_time = '8:00 pm'
                        else:
                            print("INVALID CHOICE!")
                            input("Click enter to proceed...")
                            print("Returning to Check Mentor Availability Menu...")
                            time.sleep(2)
                            break
                        meet_time = datetime.strptime(meet_time, '%I:%M %p')
                        meet_time = meet_time.time()
                    except ValueError:
                        print("INVALID CHOICE!")
                        input("Click enter to proceed...")
                        print("Returning to Check Mentor Availability Menu...")
                        time.sleep(2)
                        break
                    try:
                        meet_mode = int(input("Enter preferred mode of meeting.\nPress 1 for Online and 2 for Offline): "))
                        if meet_mode == 1:
                            meet_mode = 'Online'
                        elif meet_mode == 2:
                            meet_mode = 'Offline'
                        else:
                            print("INVALID CHOICE!")
                            input("Click enter to proceed...")
                            print("Returning to Check Mentor Availability Menu...")
                            time.sleep(2)
                            break
                    except ValueError:
                        print("INVALID CHOICE!")
                        input("Click enter to proceed...")
                        print("Returning to Check Mentor Availability Menu...")
                        time.sleep(2)
                        break
                    sql_search = """SELECT mom.mo_id, mom.mo_name, mom.mo_qual, mom.mo_interest, mom.mo_region, mom.mo_email, mom.mo_mob, ma.meet_available_day, ma.meet_mode
                                    FROM mentor_availability AS ma
                                    INNER JOIN mentor_master AS mom
                                    ON ma.mto_id = mom.mo_id
                                    WHERE ma.meet_available_date = %s
                                    AND ma.meet_available_time = %s
                                    AND mom.mo_interest LIKE CONCAT('%', %s, '%')
                                    AND mom.mo_meetingmode LIKE CONCAT('%', %s, '%')
                                """
                    # record_me[3] is Mentee interest
                    inputdata_mo = (meet_date, meet_time, record_me[3], meet_mode)
                    mycursor.execute(sql_search, inputdata_mo)
                    records_mo = mycursor.fetchall()
                    if len(records_mo) == 0:
                        print("\nSorry, either no mentor matches your interests or is not free at this date and time!")
                        input("Click enter to proceed...")
                        print("Returning to Check Mentor Availability Menu...")
                        time.sleep(2)
                    else:
                        valid = 1
                        print("Matched: ", records_mo)
                        print("MATCHED MENTOR DETAILS".center(180))
                        print('-' * 180)
                        print(tabulate(records_mo,
                                       headers=["ID", "Name", "Qualification", "Interests",
                                                "Region", "eMail", "Mobile Number", "Meeting Day", "Meeting Mode"],
                                       tablefmt='pretty'))
                        print('-' * 180)
                        print(mycursor.rowcount, "record(s) fetched successfully!")
                        ch_meeting = input("Do you want to schedule meeting with the mentor? (Y/N): ").title()
                        if ch_meeting == 'Y':
                            ch_mo_id = int(input("Enter ID of the mentor you want to meet: "))
                            for row in records_mo:
                                if row[0] == ch_mo_id:
                                    meet_day = row[7]
                                    fix_meeting(ch_mo_id, record_me[0], meet_day, meet_date, meet_time, meet_mode)
                                    break
                                else:
                                    continue
                        elif ch_meeting == 'N':
                            print("No problem...")
                            print("Returning to Mentee Menu...")
                            time.sleep(2)
                            break
                        else:
                            print("INVALID CHOICE!")
                            input("Click enter to proceed...")
                            print("Returning to Mentee Menu...")
                            time.sleep(2)
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
        input("Click enter to proceed...")
        print("Returning to Mentee Menu...")
        time.sleep(2)
    finally:
        if mydb.is_connected():
            mycursor.close()
def update_mentee_account(username, pwd):                   # Updating a mentee account in the database
    sql_username = """SELECT * FROM mentee_master WHERE me_username = %s"""
    mycursor = mydb.cursor()
    try:
        mycursor.execute(sql_username, (username,))
        record = mycursor.fetchone()
        if len(record) == 0:
            print("\nUsername does not exists...Try Again!!!")
            input("Click enter to proceed...")
            print("Returning to Mentee Menu...")
            time.sleep(2)
        else:
            if record[8] == pwd:
                choice = 0
                while choice != 4:
                    welcome()
                    print("----------------------------------".ljust(100))
                    print("MENTEE UPDATE MENU".center(30))
                    print("----------------------------------".ljust(100))
                    print("1. Update eMail and Mobile Number")
                    print("2. Update Username and Password")
                    print("3. Update Class")
                    print("4. Return to Mentee Menu")
                    print()
                    try:
                        print("Displaying Mentee details before updation...")
                        print(record)
                        input("Click enter to proceed...")
                        choice = int(input("Enter your choice: "))
                        if choice == 1:
                            new_email = input("Enter new email id: ")
                            new_mob = input("Enter new mobile number: ")
                            sql_update = """UPDATE mentee_master SET me_email = %s, me_mob = %s WHERE me_username = %s AND me_pwd = %s"""
                            inputdata = (new_email, new_mob, username, pwd)
                            mycursor.execute(sql_update, inputdata)
                            mydb.commit()
                            print(mycursor.rowcount, " record updated successfully!")
                            print("Displaying Mentee details after updation...")
                            mycursor.execute(sql_username, (username,))
                            record = mycursor.fetchone()
                            print(record)
                            input("Click enter to proceed...")
                            print("Returning to Mentee Update Menu...")
                            time.sleep(2)
                        elif choice == 2:
                            new_un = input("Enter new username: ")
                            new_pwd = input("Enter new password: ")
                            sql_update = """UPDATE mentee_master SET me_username = %s, me_pwd = %s WHERE me_username = %s AND me_pwd = %s"""
                            inputdata = (new_un, new_pwd, username, pwd)
                            mycursor.execute(sql_update, inputdata)
                            mydb.commit()
                            print(mycursor.rowcount, " record updated successfully!")
                            print("Displaying Mentee details after updation...")
                            username = new_un
                            pwd = new_pwd
                            mycursor.execute(sql_username, (username,))
                            record = mycursor.fetchone()
                            print(record)
                            input("Click enter to proceed...")
                            print("Returning to Mentee Update Menu...")
                            time.sleep(2)
                        elif choice == 3:
                            new_qual = input("Enter new class: ")
                            sql_update = """UPDATE mentee_master SET me_class = %s WHERE me_username = %s AND me_pwd = %s"""
                            inputdata = (new_qual.title(), username, pwd)
                            mycursor.execute(sql_update, inputdata)
                            mydb.commit()
                            print(mycursor.rowcount, " record updated successfully!")
                            print("Displaying Mentor details after updation...")
                            mycursor.execute(sql_username, (username,))
                            record = mycursor.fetchone()
                            print(record)
                            input("Click enter to proceed...")
                            print("Returning to Mentee Update Menu...")
                            time.sleep(2)
                        elif choice == 4:
                            print("Returning to Mentee Menu...")
                            time.sleep(2)
                            break
                        else:
                            print("INVALID CHOICE!")
                            input("Click enter to proceed...")
                            print("Returning to Mentee Update Menu...")
                            time.sleep(2)
                    except ValueError:
                        print("INVALID CHOICE!")
                        choice = 0
                        input("Click enter to proceed...")
                        print("Returning to Mentee Update Menu...")
                        time.sleep(2)
            else:
                print("INCORRECT PASSWORD!")
                input("Click enter to proceed...")
                print("Returning to Login Menu...")
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
        input("Click enter to proceed...")
        print("Returning to Login Menu...")
        time.sleep(2)
    finally:
        if mydb.is_connected():
            mycursor.close()
def view_mentee_account(username, pwd):
    print("----------------------------------".ljust(100))
    print("MENTEE ACCOUNT".center(30))
    print("----------------------------------".ljust(100))
    mycursor = mydb.cursor()
    try:
        sql_username = """SELECT * FROM mentee_master WHERE me_username = %s"""
        mycursor.execute(sql_username, (username,))
        records = mycursor.fetchall()
        if len(records) == 0:
            print("\nUsername does not exists...Try Again!!! ")
            input("Click enter to proceed...")
        else:
            for row in records:
                if row[8] == pwd:
                    print('-' * 180)
                    print("MENTEE DETAILS".center(180))
                    print(tabulate(records, headers=["ID", "Name", "Class", "Interests", "Region",
                                             "eMail", "Mobile Number", "Username", "Password"], tablefmt='pretty'))
                    print('-' * 180)
                    print(mycursor.rowcount, "records fetched.")
                    input("Click enter to proceed...")
                    print("Returning to Mentee Menu...")
                    time.sleep(2)
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if mydb.is_connected():
            mycursor.close()
def login_mentee():                 # To let an existing mentee log into the 'MENTOR-MENTEE PORTAL'
    print("Enter username and password. If new user, please signup first.")
    username = input("\nEnter username: ")
    if username != "":
        mycursor = mydb.cursor()
        try:
            sql_username = """SELECT me_pwd FROM mentee_master WHERE me_username = %s"""
            mycursor.execute(sql_username, (username,))
            records = mycursor.fetchall()
            if len(records) == 0:
                    print("\nUsername does not exists...Try Again!!! ")
                    input("Click enter to proceed...")
                    print("Returning to Login Menu...")
                    time.sleep(2)
            else:
                pwd = pwinput.pwinput()
                for row in records:
                    if row[0] == pwd:
                        choice = 0
                        while choice != 7:
                            welcome()
                            print("----------------------------------".ljust(100))
                            print("MENTEE MENU".center(30))
                            print("----------------------------------".ljust(100))
                            print("1. View Account")
                            print("2. Update Account")
                            print("3. Schedule Meeting With A Mentor")
                            print("4. Generate Appointment Slip")
                            print("5. View Scheduled Meetings")
                            print("6. Cancel Meeting With A Mentor")
                            print("7. Return to Login Menu")
                            print()
                            try:
                                choice = int(input("Enter your choice: "))
                                if choice == 1:
                                    view_mentee_account(username, pwd)
                                elif choice == 2:
                                    update_mentee_account(username, pwd)
                                elif choice == 3:
                                    schedule_meeting(username, pwd)
                                elif choice == 4:
                                    gen_appointment_slip(username, pwd)
                                elif choice == 5:
                                    view_mentee_schd_meetings(username, pwd)
                                elif choice == 6:
                                    cancel_meeting(username, pwd)
                                elif choice == 7:
                                    print("Returning to Login Menu...")
                                    time.sleep(2)
                                    break
                                else:
                                    print("INVALID CHOICE!")
                                    input("Click enter to proceed...")
                                    print("Returning to Mentee Menu...")
                                    time.sleep(2)
                            except ValueError:
                                print("INVALID CHOICE!")
                                choice = 0
                                input("Click enter to proceed...")
                                print("Returning to Mentee Menu...")
                                time.sleep(2)
                    else:
                        print("INCORRECT PASSWORD!")
                        input("Click enter to proceed...")
                        print("Returning to Login Menu...")
                        time.sleep(2)
                        break
        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
            input("Click enter to proceed...")
            print("Returning to Login Menu...")
            time.sleep(2)
        finally:
            mycursor.close()
    else:
        print("INVALID CHOICE!")
        input("Click enter to proceed...")
        print("Returning to Login Menu...")
        time.sleep(2)

def view_mentor_schd_meetings(username, pwd):
    sql_all = """SELECT mms.meeting_id, mom.mo_name, mem.me_name, mms.meet_day, DATE_FORMAT(mms.meet_date, '%M %d %Y'), LOWER(DATE_FORMAT(mms.meet_time,'%l:%i %p')), mms.meet_mode 
                  FROM mentor_mentee_schedule AS mms 
                  INNER JOIN mentor_master AS mom
                  INNER JOIN mentee_master AS mem
                  ON mms.mto_id = mom.mo_id 
                  AND mms.mte_id = mem.me_id
                  WHERE mom.mo_username = %s
                  AND mom.mo_pwd = %s 
                  ORDER BY mms.meet_date, mms.meet_time
               """
    inputdata = (username, pwd)
    mycursor = mydb.cursor()
    try:
        mycursor.execute(sql_all, inputdata)
        records_meet = mycursor.fetchall()
        if len(records_meet) == 0:
            print("\nSorry, no record found!")
            input("Click enter to proceed...")
            print("Returning to Mentor Menu...")
            time.sleep(2)
        else:
            print("Displaying your meeting details...")
            print('-' * 180)
            print("SCHEDULED MEETING APPOINTMENTS".center(100))
            print(tabulate(records_meet,
                           headers=["Meeting ID", "Mentor Name", "Mentee Name", "Day", "Date", "Time", "Mode"],
                           tablefmt='pretty'))
            print('-' * 180)
            print(mycursor.rowcount, "record(s) fetched.")
            print()
            input("Click enter to proceed...")
            print("Returning to Mentor Menu...")
            time.sleep(2)
    except mysql.connector.Error:
        print("Failed to delete record from table. Record may no longer exists!")
        input("Click enter to proceed...")
        print("Returning to Mentor Menu...")
        time.sleep(2)
    finally:
        if mydb.is_connected():
            mycursor.close()
def del_a_mentor_meeting(username):
    try:
        del_meet_id = int(input("Enter the ID of the meeting you want to cancel: "))
        sql_all = """SELECT * FROM mentor_mentee_schedule AS mms
                     INNER JOIN mentor_master AS mom
                     ON mms.mto_id = mom.mo_id
                     WHERE mom.mo_username = %s
                     AND mms.meeting_id = %s
                  """
        mycursor = mydb.cursor()
        inputdata = (username, del_meet_id)
        try:
            mycursor.execute(sql_all, inputdata)
            record_meet = mycursor.fetchone()
            if record_meet is None:
                print("\nNo record found!")
                input("Click enter to proceed...")
                print("Returning to Mentor Menu...")
                time.sleep(2)
            else:
                ch_del = input("Are you sure to delete the meeting? (Y/N): ").title()
                if ch_del == 'Y':
                    sql_delete = """DELETE FROM mentor_mentee_schedule WHERE meeting_id = %s"""
                    try:
                        mycursor = mydb.cursor()
                        mycursor.execute(sql_delete, (del_meet_id,))
                        mydb.commit()
                        print("Deleting record...")
                        time.sleep(2)
                        print(mycursor.rowcount, " record(s) deleted successfully!")
                        input("Click enter to proceed...")
                        print("Returning to Mentor Menu....")
                        time.sleep(2)
                    except mysql.connector.Error:
                        print("Failed to delete record from table. Record may no longer exists!")
                        input("Click enter to proceed...")
                        print("Returning to Meeting Cancellation Menu...")
                        time.sleep(2)
        except mysql.connector.Error as e:
            print("Failed to delete record from table. Record may no longer exists!", e)
            input("Click enter to proceed...")
            print("Returning to Meeting Cancellation Menu...")
            time.sleep(2)
        finally:
            if mydb.is_connected():
                mycursor.close()
    except ValueError:
        print("INVALID CHOICE!")
        choice = 0
        input("Click enter to proceed...")
        print("Returning to Meeting Cancellation Menu...")
        time.sleep(2)
def del_all_mentor_meetings(username):
    ch_del = input("Are you sure to delete all records? (Y/N): ").title()
    if ch_del == 'Y':
        sql_all = """SELECT mms.mto_id FROM mentor_mentee_schedule AS mms
                     INNER JOIN mentor_master AS mom
                     ON mms.mto_id = mom.mo_id
                     WHERE mom.mo_username = %s
                  """
        mycursor = mydb.cursor()
        try:
            mycursor.execute(sql_all, (username,))
            record_meet = mycursor.fetchone()
            if len(record_meet) == 0:
                print("\nNo record found!")
                input("Click enter to proceed...")
                print("Returning to Mentee Menu...")
                time.sleep(2)
            else:
                sql_delete = """DELETE FROM mentor_mentee_schedule WHERE mto_id = %s"""
                try:
                    mycursor = mydb.cursor()
                    mycursor.execute(sql_delete, (record_meet[0],))
                    mydb.commit()
                    print("Deleting record(s)...")
                    time.sleep(2)
                    print(mycursor.rowcount, " record(s) deleted successfully!")
                    input("Click enter to proceed...")
                    print("Returning to Mentee Menu....")
                    time.sleep(2)
                except mysql.connector.Error:
                    print("Failed to delete record from table. Record may no longer exists!")
                    input("Click enter to proceed...")
                    print("Returning to Meeting Cancellation Menu...")
                    time.sleep(2)
        except mysql.connector.Error:
            print("Failed to delete record from table. Record may no longer exists!")
            input("Click enter to proceed...")
            print("Returning to Meeting Cancellation Menu...")
            time.sleep(2)
        finally:
            if mydb.is_connected():
                mycursor.close()
    elif ch_del == 'N':
        print("No problem...")
        print("Returning to Mentee Menu...")
        time.sleep(2)
    else:
        print("INVALID CHOICE!")
        input("Click enter to proceed...")
        print("Returning to Meeting Cancellation Menu...")
        time.sleep(2)
def cancel_meeting_with_mentee(username, pwd):
    sql_meet = """SELECT mms.meeting_id, mom.mo_name, mem.me_name, mms.meet_day, DATE_FORMAT(mms.meet_date, '%M %d %Y'), LOWER(DATE_FORMAT(mms.meet_time,'%l:%i %p')), mms.meet_mode 
                  FROM mentor_mentee_schedule AS mms 
                  INNER JOIN mentor_master AS mom
                  INNER JOIN mentee_master AS mem
                  ON mms.mto_id = mom.mo_id 
                  AND mms.mte_id = mem.me_id
                  WHERE mom.mo_username = %s
                  AND mom.mo_pwd = %s
               """
    inputdata = (username, pwd)
    mycursor = mydb.cursor()
    try:
        mycursor.execute(sql_meet, inputdata)
        records_meet = mycursor.fetchall()
        if len(records_meet) == 0:
            print("\nNo record found!")
            input("Click enter to proceed...")
            print("Returning to Mentor Menu...")
            time.sleep(2)
        else:
            choice = 0
            while choice != 3:
                welcome()
                print("Displaying your meeting details...")
                print('-' * 180)
                print("MEETING APPOINTMENTS".center(100))
                print(tabulate(records_meet,
                               headers=["Meeting ID", "Mentor Name", "Mentee Name", "Day", "Date", "Time", "Mode"],
                               tablefmt='pretty'))
                print('-' * 180)
                print(mycursor.rowcount, "record(s) fetched.")
                print()
                print("----------------------------------".ljust(100))
                print("MEETING CANCELLATION MENU".center(30))
                print("----------------------------------".ljust(100))
                print("1. Cancel all meetings")
                print("2. Cancel a meeting")
                print("3. Return to Mentor Menu")
                try:
                    choice = int(input("Enter your choice: "))
                    if choice == 1:
                        del_all_mentor_meetings(username)
                        break
                    elif choice == 2:
                        del_a_mentor_meeting(username)
                        break
                    elif choice == 3:
                        print("Returning to Mentor Menu...")
                        time.sleep(2)
                        break
                    else:
                        print("INVALID CHOICE!")
                        input("Click enter to proceed...")
                        print("Returning to Meeting Cancellation Menu...")
                        time.sleep(2)
                except ValueError:
                    print("INVALID CHOICE!")
                    choice = 0
                    input("Click enter to proceed...")
                    print("Returning to Meeting Cancellation Menu...")
                    time.sleep(2)
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
        input("Click enter to proceed...")
        print("Returning to Mentor Menu...")
        time.sleep(2)
    finally:
        if mydb.is_connected():
            mycursor.close()
def update_availability(username, pwd):
    sql_id = """SELECT mo_id FROM mentor_master WHERE mo_username = %s AND mo_pwd = %s"""
    inputdata = (username, pwd)
    mycursor = mydb.cursor()
    meet_date = datetime.min
    meet_time = datetime.min
    meet_mode = ""
    try:
        mycursor.execute(sql_id, inputdata)
        record = mycursor.fetchone()
        if len(record) == 0:
            print("\nInvalid username or password. Try Again!!!")
            input("Click enter to proceed...")
            print("Returning to Mentor Menu...")
            time.sleep(2)
        else:
            valid = 0
            while valid != 1:
                welcome()
                print("----------------------------------".ljust(100))
                print("UPDATE MENTOR AVAILABILITY MENU".center(30))
                print("----------------------------------".ljust(100))

                print("Enter the meeting details:  ")
                try:
                    meet_date = input("Enter date of meeting (yyyy-mm-dd): ")
                    datetime.strptime(meet_date, '%Y-%m-%d')
                except ValueError:
                    print("INVALID CHOICE!")
                    input("Click enter to proceed...")
                    print("Returning to Update Mentor Availability Menu...")
                    time.sleep(2)
                    # break
                try:
                    meet_time = int(input("Enter preferred time slot for the meeting."
                                          "\nChoose from:\n  Press 1 for 4:00 pm (16:00:00)\n  Press 2 for 5:00 pm (17:00:00)\n  Press 3 for 6:00 pm (18:00:00)\n  Press 4 for 7:00 pm (19:00:00)\n  Press 5 for 8:00 pm (20:00:00)\n"))
                    if meet_time == 1:
                        meet_time = '4:00 pm'
                    elif meet_time == 2:
                        meet_time = '5:00 pm'
                    elif meet_time == 3:
                        meet_time = '6:00 pm'
                    elif meet_time == 4:
                        meet_time = '7:00 pm'
                    elif meet_time == 5:
                        meet_time = '8:00 pm'
                    else:
                        print("INVALID CHOICE!")
                        input("Click enter to proceed...")
                        print("Returning to Check Mentor Availability Menu...")
                        time.sleep(2)
                        # break
                    meet_time = datetime.strptime(meet_time, '%I:%M %p')
                    meet_time = meet_time.time()
                except ValueError:
                    print("INVALID CHOICE!")
                    input("Click enter to proceed...")
                    print("Returning to Check Mentor Availability Menu...")
                    time.sleep(2)
                    # break
                try:
                    meet_mode = int(input("Enter preferred mode of meeting.\nPress 1 for Online and 2 for Offline): "))
                    if meet_mode == 1:
                        meet_mode = 'Online'
                    elif meet_mode == 2:
                        meet_mode = 'Offline'
                    else:
                        print("INVALID CHOICE!")
                        input("Click enter to proceed...")
                        print("Returning to Check Mentor Availability Menu...")
                        time.sleep(2)
                        # break
                except ValueError:
                    print("INVALID CHOICE!")
                    input("Click enter to proceed...")
                    print("Returning to Check Mentor Availability Menu...")
                    time.sleep(2)
                    # break
                sql_insert = """INSERT INTO mentor_availability
                                (mto_id, meet_available_day, meet_available_date, meet_available_time, meet_mode)
                                VALUES (%s, %s, %s, %s, %s)"""
                recordTuple = (record[0], "", meet_date, meet_time, meet_mode)
                mycursor.execute(sql_insert, recordTuple)

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
                mydb.commit()
                print("Record saved successfully to the Mentor Availability table.")
                mycursor.close()
                print("Returning to Mentor Menu....")
                time.sleep(2)
                return 100
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
        input("Click enter to proceed...")
        print("Returning to Login Menu...")
        time.sleep(2)
    finally:
        if mydb.is_connected():
            mycursor.close()
def update_mentor_account(username, pwd):                  # Updating a mentor account in the database
    sql_username = """SELECT * FROM mentor_master WHERE mo_username = %s"""
    mycursor = mydb.cursor()
    try:
        mycursor.execute(sql_username, (username,))
        record = mycursor.fetchone()
        if len(record) == 0:
            print("\nUsername does not exists...Try Again!!!")
            input("Click enter to proceed...")
            print("Returning to Mentor Menu...")
            time.sleep(2)
        else:
            if record[10] == pwd:
                choice = 0
                while choice != 6:
                    welcome()
                    print("----------------------------------".ljust(100))
                    print("MENTOR UPDATE MENU".center(30))
                    print("----------------------------------".ljust(100))
                    print("1. Update eMail and Mobile Number")
                    print("2. Update Username and Password")
                    print("3. Update Qualification")
                    print("4. Return to Mentor Menu")
                    print()
                    try:
                        print("Displaying Mentor details before updation...")
                        print(record)
                        input("Click enter to proceed...")
                        choice = int(input("Enter your choice: "))
                        if choice == 1:
                            new_email = input("Enter new email id: ")
                            new_mob = input("Enter new mobile number: ")
                            sql_update = """UPDATE mentor_master SET mo_email = %s, mo_mob = %s WHERE mo_username = %s AND mo_pwd = %s"""
                            inputdata = (new_email, new_mob, username, pwd)
                            mycursor.execute(sql_update, inputdata)
                            mydb.commit()
                            print(mycursor.rowcount, " record updated successfully!")
                            print("Displaying Mentor details after updation...")
                            mycursor.execute(sql_username, (username,))
                            record = mycursor.fetchone()
                            print(record)
                            input("Click enter to proceed...")
                            print("Returning to Mentor Update Menu....")
                            time.sleep(2)
                        elif choice == 2:
                            new_un = input("Enter new username: ")
                            new_pwd = input("Enter new password: ")
                            sql_update = """UPDATE mentor_master SET mo_username = %s, mo_pwd = %s WHERE mo_username = %s AND mo_pwd = %s"""
                            inputdata = (new_un, new_pwd, username, pwd)
                            mycursor.execute(sql_update, inputdata)
                            mydb.commit()
                            print(mycursor.rowcount, " record updated successfully!")
                            print("Displaying Mentor details after updation...")
                            username = new_un
                            pwd = new_pwd
                            mycursor.execute(sql_username, (username,))
                            record = mycursor.fetchone()
                            print(record)
                            input("Click enter to proceed...")
                            print("Returning to Mentor Update Menu....")
                            time.sleep(2)
                        elif choice == 3:
                            new_qual = input("Enter new qualification: ")
                            sql_update = """UPDATE mentor_master SET mo_qual = %s WHERE mo_username = %s AND mo_pwd = %s"""
                            inputdata = (new_qual.title(), username, pwd)
                            mycursor.execute(sql_update, inputdata)
                            mydb.commit()
                            print(mycursor.rowcount, " record updated successfully!")
                            print("Displaying Mentor details after updation...")
                            mycursor.execute(sql_username, (username,))
                            record = mycursor.fetchone()
                            print(record)
                            input("Click enter to proceed...")
                            print("Returning to Mentor Update Menu....")
                            time.sleep(2)
                        elif choice == 4:
                            print("Returning to Mentor Menu...")
                            time.sleep(2)
                            break
                        else:
                            print("INVALID CHOICE!")
                            input("Click enter to proceed...")
                            print("Returning to Mentor Update Menu...")
                            time.sleep(2)
                    except ValueError:
                        print("INVALID CHOICE!")
                        choice = 0
                        input("Click enter to proceed...")
                        print("Returning to Mentor Update Menu...")
                        time.sleep(2)
            else:
                print("INCORRECT PASSWORD!")
                input("Click enter to proceed...")
                print("Returning to Login Menu...")
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
        input("Click enter to proceed...")
        print("Returning to Login Menu...")
        time.sleep(2)
    finally:
        if mydb.is_connected():
            mycursor.close()
def view_mentor_account(username, pwd):
    print("----------------------------------".ljust(100))
    print("MENTOR ACCOUNT".center(30))
    print("----------------------------------".ljust(100))
    mycursor = mydb.cursor()
    try:
        sql_username = """SELECT * FROM mentor_master WHERE mo_username = %s"""
        mycursor.execute(sql_username, (username,))
        records = mycursor.fetchall()
        if len(records) == 0:
            print("\nUsername does not exists...Try Again!!! ")
        else:
            for row in records:
                if row[10] == pwd:
                    print('-' * 180)
                    print("MENTOR DETAILS".center(180))
                    print(tabulate(records, headers=["ID", "Name", "Qualification", "Class Taught", "Interests", "Region",
                                                     "Preferred Mode of Meeting", "eMail", "Mobile Number", "Username", "Password"], tablefmt='pretty'))
                    print('-' * 180)
                    print(mycursor.rowcount, "records fetched.")
                    input("Click enter to proceed...")
                    print("Returning to Mentor Menu....")
                    time.sleep(2)
                else:
                    print("INCORRECT PASSWORD!")
                    input("Click enter to proceed...")
                    print("Returning to Login Menu...")
                    break
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if mydb.is_connected():
            mycursor.close()
def login_mentor():                 # To let an existing mentor log into the 'MENTOR-MENTEE PORTAL'
    print("Enter username and password. If new user, please signup first.")
    username = input("Enter username: ")
    if username != "":
        mycursor = mydb.cursor()
        try:
            sql_username = """SELECT mo_pwd FROM mentor_master WHERE mo_username = %s"""
            mycursor.execute(sql_username, (username,))
            records = mycursor.fetchall()
            mycursor.close()
            if len(records) == 0:
                print("\nUsername does not exists...Try Again!!!")
                input("Click enter to proceed...")
                print("Returning to Login Menu...")
                time.sleep(2)
            else:
                pwd = pwinput.pwinput()
                for row in records:
                    if row[0] == pwd:
                        choice = 0
                        while choice != 6:
                            welcome()
                            print("----------------------------------".ljust(100))
                            print("MENTOR MENU".center(30))
                            print("----------------------------------".ljust(100))
                            print("1. View Account")
                            print("2. Update Account")
                            print("3. Update Availability")
                            print("4. Cancel Meeting With A Mentee")
                            print("5. View Scheduled Meetings")
                            print("6. Return to Login Menu")
                            print()
                            try:
                                choice = int(input("Enter your choice: "))
                                if choice == 1:
                                    view_mentor_account(username, pwd)
                                elif choice == 2:
                                    update_mentor_account(username, pwd)
                                elif choice == 3:
                                    update_availability(username, pwd)
                                elif choice == 4:
                                    cancel_meeting_with_mentee(username, pwd)
                                elif choice == 5:
                                    view_mentor_schd_meetings(username, pwd)
                                elif choice == 6:
                                    print("Returning to Login Menu...")
                                    time.sleep(2)
                                    break
                                else:
                                    print("INVALID CHOICE!")
                                    input("Click enter to proceed...")
                                    print("Returning to Mentor Menu...")
                                    time.sleep(2)
                            except ValueError:
                                print("INVALID CHOICE!")
                                choice = 0
                                input("Click enter to proceed...")
                                print("Returning to Mentor Menu...")
                                time.sleep(2)
                    else:
                        print("INCORRECT PASSWORD!")
                        input("Click enter to proceed...")
                        print("Returning to Login Menu...")
                        break
        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
            input("Click enter to proceed...")
            print("Returning to Login Menu...")
            time.sleep(2)
        finally:
            mycursor.close()
    else:
        print("INVALID CHOICE!")
        input("Click enter to proceed...")
        print("Returning to Login Menu...")
        time.sleep(2)

def publish_mentee_report():        # Generating report of a mentee's details
    print("----------------------------------".ljust(100))
    print("PUBLISH MENTEE REPORT".center(30))
    print("----------------------------------".ljust(100))
    rep_me_un = input("Enter username of the mentee to be published: ")
    if rep_me_un != "":
        print("Displaying mentee details before publishing...")
        sql_select = """SELECT me_id, me_name, me_class, me_interest, me_region, me_email, me_mob
                            FROM mentee_master 
                            WHERE me_username = %s"""
        mycursor = mydb.cursor()
        try:
            mycursor.execute(sql_select, (rep_me_un,))
            record = mycursor.fetchone()
            if record:
                print("Transferring record to file...")

                now = datetime.now()
                date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
                make_directory(r'B:\MentorMenteePortal\Reports\Mentee')
                filename = r'B:\MentorMenteePortal\Reports\Mentee\MenteeReport_' + str(record[0]).zfill(4) + '.txt'

                try:
                    with open(filename, 'w+') as fin:
                        fin.write('*' * 100 + '\n')
                        fin.write('\n')
                        fin.write('MENTEE REPORT'.center(100))
                        fin.write('\n')
                        fin.write(('Created on: ' + date_time).rjust(100))
                        fin.write('\n')
                        fin.write('*' * 100 + '\n')
                        fin.write("ID:                          " + str(record[0]).zfill(4) + '\n')
                        fin.write("Name:                        " + str(record[1]) + '\n')
                        fin.write("Class:                       " + str(record[2]) + '\n')
                        fin.write("Interests:                   " + str(record[3]) + '\n')
                        fin.write("Region:                      " + str(record[4]) + '\n')
                        fin.write("eMail ID:                    " + str(record[6]) + '\n')
                        fin.write("Mobile Number:               " + str(record[7]) + '\n')
                        fin.write("*" * 42 + " END OF REPORT " + "*" * 43)
                    print("Record written to report successfully!")
                    input("Click enter to proceed...")
                    print("Returning to Admin Menu....")
                    time.sleep(2)
                except FileNotFoundError:
                    print("Failed to open file!")
            else:
                print("Sorry, no record found!")
                input("Click enter to proceed...")
                print("Returning to Admin Menu....")
                time.sleep(2)
        except mysql.connector.Error as error:
            print("Failed to fetch record from table!")
            time.sleep(2)
        finally:
            if mydb.is_connected():
                mycursor.close()
    else:
        print("INVALID CHOICE!")
        input("Click enter to proceed...")
        print("Returning to Admin Menu....")
        time.sleep(2)
def del_mentee():                   # Deleting a mentee account from the database
    print("----------------------------------".ljust(100))
    print("DELETE MENTEE".center(30))
    print("----------------------------------".ljust(100))
    del_me_un = input("Enter username of the mentee to be deleted: ")
    if del_me_un != "":
        sql_select = """SELECT me_id, me_name, me_class, me_interest, me_region, me_meetingmode, me_email, me_mob
                            FROM mentee_master 
                            WHERE me_username = %s"""
        mycursor = mydb.cursor()
        try:
            mycursor.execute(sql_select, (del_me_un,))
            record = mycursor.fetchone()
            if (record):
                print("Displaying mentee details before deletion...")
                print(record)
                sql_delete = """DELETE FROM mentee_master WHERE me_username = %s"""
                mycursor.execute(sql_delete, (del_me_un,))
                mydb.commit()
                print("Deleting record...")
                time.sleep(2)
                print(mycursor.rowcount, " record deleted successfully!")
                input("Click enter to proceed...")
                print("Returning to Admin Menu....")
                time.sleep(2)
            else:
                print("Sorry, no record found!")
                input("Click enter to proceed...")
                print("Returning to Admin Menu....")
                time.sleep(2)
        except mysql.connector.Error:
            print("Failed to delete record from table. Record no longer exists!")
        finally:
            if mydb.is_connected():
                mycursor.close()
    else:
        print("INVALID CHOICE!")
        input("Click enter to proceed...")
        print("Returning to Admin Menu....")
        time.sleep(2)
def search_mentee():                # Searching mentees in the database using pattern matching query and printing records
    print("----------------------------------".ljust(100))
    print("VIEW MENTEE DETAILS".center(30))
    print("----------------------------------".ljust(100))
    enq_me_name = input("Enter mentee's name or a pattern in mentee's name: ").title()
    if enq_me_name != '' and all(chr.isalpha() or chr.isspace() for chr in enq_me_name):
        sql_select = """SELECT me_id, me_name, me_class, me_interest, me_region, me_meetingmode, me_email, me_mob
                        FROM mentee_master
                        WHERE me_name LIKE CONCAT('%', %s, '%')"""
        mycursor = mydb.cursor()
        try:
            mycursor.execute(sql_select, (enq_me_name,))
            records = mycursor.fetchall()
            if records:
                print("The total number of mentors with the name ", enq_me_name, " is: ", mycursor.rowcount)
                print()
                print('-' * 180)
                print("MENTEE DETAILS".center(180))
                print(tabulate(records, headers=["ID", "Name", "Class", "Interests", "Region",
                                                 "Preferred Mode of Meeting", "eMail", "Mobile Number"], tablefmt='pretty'))
                print('-' * 180)
                print(mycursor.rowcount, "record(s) fetched.")
                input("Click enter to proceed...")
                print("Returning to Admin Menu....")
                time.sleep(2)
            else:
                print("Sorry, no record found!")
                input("Click enter to proceed...")
                print("Returning to Admin Menu....")
                time.sleep(2)
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if mydb.is_connected():
                mycursor.close()
    else:
        print("INVALID CHOICE!")
        input("Click enter to proceed...")
        print("Returning to Admin Menu....")
        time.sleep(2)
def view_mentees():                 # View details of all mentees
    print("----------------------------------".ljust(100))
    print("VIEW ALL MENTEES".center(30))
    print("----------------------------------".ljust(100))
    sql_select = """SELECT me_id, me_name, me_class, me_interest, me_region, me_email, me_mob
                    FROM mentee_master"""
    mycursor = mydb.cursor()
    try:
        mycursor.execute(sql_select)
        records = mycursor.fetchall()
        if len(records) != 0:
            print()
            print('-' * 180)
            print("MENTEE RECORDS".center(180))
            print(tabulate(records, headers=["ID", "Name", "Class", "Interests", "Region",
                                             "eMail", "Mobile Number"], tablefmt='pretty'))
            print('-' * 180)
            print(mycursor.rowcount, "records fetched.")
            input("Click enter to proceed...")
            print("Returning to Admin Menu....")
            time.sleep(2)
        else:
            print("Sorry, no record found!")
            input("Click enter to proceed...")
            print("Returning to Admin Menu....")
            time.sleep(2)
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if mydb.is_connected():
            mycursor.close()

def publish_mentor_report():        # Generating report of a mentor's details
    print("----------------------------------".ljust(100))
    print("PUBLISH MENTOR REPORT".center(30))
    print("----------------------------------".ljust(100))
    rep_mo_un = input("Enter username of the mentor to be published: ")
    if rep_mo_un != "":
        sql_select = """SELECT mo_id, mo_name, mo_qual, mo_class, mo_interest, mo_region, mo_meetingmode, mo_email, mo_mob
                        FROM mentor_master 
                        WHERE mo_username = %s"""
        mycursor = mydb.cursor()
        try:
            mycursor.execute(sql_select, (rep_mo_un,))
            record = mycursor.fetchone()
            if (record):
                print("Transferring record to file...")

                now = datetime.now()
                date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
                make_directory(r'B:\MentorMenteePortal\Reports\Mentor')
                filename = r'B:\MentorMenteePortal\Reports\Mentor\MentorReport_' + str(record[0]).zfill(4) + '.txt'

                try:
                    with open(filename, 'w+') as fin:
                        fin.write('*' * 120 +'\n')
                        fin.write('\n')
                        fin.write('MENTOR REPORT'.center(120))
                        fin.write('\n')
                        fin.write(('Created on: ' + date_time).rjust(100))
                        fin.write('\n')
                        fin.write('*' * 120 + '\n')
                        fin.write("ID:                          " + str(record[0]).zfill(4) + '\n')
                        fin.write("Name:                        " + str(record[1]) + '\n')
                        fin.write("Qualification:               " + str(record[2]) + '\n')
                        fin.write("Class Taught:                " + str(record[3]) + '\n')
                        fin.write("Interests:                   " + str(record[4]) + '\n')
                        fin.write("Region:                      " + str(record[5]) + '\n')
                        fin.write("Preferred Mode of Meeting:   " + str(record[6]) + '\n')
                        fin.write("eMail ID:                    " + str(record[7]) + '\n')
                        fin.write("Mobile Number:               " + str(record[8]) + '\n')
                        fin.write("*" * 52 + " END OF REPORT " + "*" * 53)
                    print("Record written to report successfully!")
                    input("Click enter to proceed...")
                    print("Returning to Admin Menu....")
                    time.sleep(2)
                except FileNotFoundError:
                    print("Failed to open file!")
            else:
                print("Sorry, no record found!")
        except mysql.connector.Error as error:
            print("Failed to fetch record from table!")
            time.sleep(2)
        finally:
            if mydb.is_connected():
                mycursor.close()
    else:
        print("INVALID CHOICE!")
        input("Click enter to proceed...")
        print("Returning to Admin Menu....")
        time.sleep(2)
def del_mentor():                   # Deleting a mentor account from the database
    print("----------------------------------".ljust(100))
    print("DELETE MENTOR".center(30))
    print("----------------------------------".ljust(100))
    del_mo_un = input("Enter username of the mentor to be deleted: ")
    if del_mo_un != '':
        sql_select = """SELECT mo_id, mo_name, mo_qual, mo_class, mo_interest, mo_region, mo_meetingmode, mo_email, mo_mob
                        FROM mentor_master 
                        WHERE mo_username = %s"""
        mycursor = mydb.cursor()
        try:
            mycursor.execute(sql_select, (del_mo_un,))
            record = mycursor.fetchone()
            if (record):
                print("Displaying mentor details before deletion...")
                print(record)
                sql_delete = """DELETE FROM  mentor_master WHERE mo_username = %s"""
                mycursor.execute(sql_delete, (del_mo_un,))
                mydb.commit()
                print("Deleting record...")
                time.sleep(2)
                print(mycursor.rowcount, " record deleted successfully!")
                input("Click enter to proceed...")
                print("Returning to Admin Menu....")
                time.sleep(2)
            else:
                print("Sorry, no record found!")
                input("Click enter to proceed...")
                print("Returning to Admin Menu....")
                time.sleep(2)
        except mysql.connector.Error as error:
            print("Failed to delete record from table. Record no longer exists!")
        finally:
            if mydb.is_connected():
                mycursor.close()
    else:
        print("INVALID CHOICE!")
        input("Click enter to proceed...")
        print("Returning to Admin Menu....")
        time.sleep(2)
def search_mentor():                # Searching mentors in the database using pattern matching query and printing records
    print("----------------------------------".ljust(100))
    print("SEARCH MENTOR".center(30))
    print("----------------------------------".ljust(100))
    enq_mo_name = input("Enter mentor's name or a pattern in mentor's name: ").title()
    if enq_mo_name != '' and all(chr.isalpha() or chr.isspace() for chr in enq_mo_name):
        sql_select = """SELECT mo_id, mo_name, mo_qual, mo_class, mo_interest, mo_region, mo_meetingmode, mo_email, mo_mob
                        FROM mentor_master
                        WHERE mo_name LIKE CONCAT('%', %s, '%')"""
        mycursor = mydb.cursor()
        try:
            mycursor.execute(sql_select, (enq_mo_name,))
            records = mycursor.fetchall()
            if (records):
                print("The total number of mentors with the name ", enq_mo_name, " is: ", mycursor.rowcount)
                print()
                print('-' * 180)
                print("MENTOR DETAILS".center(180))
                print(tabulate(records, headers=["ID", "Name", "Qualification", "Class Taught", "Interests", "Region",
                                                  "Preferred Mode of Meeting", "eMail", "Mobile Number"], tablefmt='pretty'))
                print('-' * 180)
                print(mycursor.rowcount, "record(s) fetched.")
                input("Click enter to proceed...")
                print("Returning to Admin Menu....")
                time.sleep(2)
            else:
                print("Sorry, no record found!")
                input("Click enter to proceed...")
                print("Returning to Admin Menu....")
                time.sleep(2)
        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if mydb.is_connected():
                mycursor.close()
    else:
        print("INVALID CHOICE!")
        input("Click enter to proceed...")
        print("Returning to Admin Menu....")
        time.sleep(2)
def view_mentors():                 # View details of all mentors
    print("----------------------------------".ljust(100))
    print("VIEW ALL MENTORS".center(30))
    print("----------------------------------".ljust(100))
    sql_select = """SELECT mo_id, mo_name, mo_qual, mo_class, mo_interest, mo_region, mo_meetingmode, mo_email, mo_mob
                        FROM mentor_master"""
    mycursor = mydb.cursor()
    try:
        mycursor.execute(sql_select)
        records = mycursor.fetchall()
        if len(records) != 0:
            print()
            print('-' * 180)
            print("MENTOR RECORDS".center(180))
            print(tabulate(records, headers=["ID", "Name", "Qualification", "Class Taught", "Interests", "Region",
                                              "Preferred Mode of Meeting", "eMail", "Mobile Number"], tablefmt='pretty'))
            print('-' * 180)
            print(mycursor.rowcount, "records fetched.")
            input("Click enter to proceed...")
            print("Returning to Admin Menu...")
            time.sleep(2)
        else:
            print("Sorry, no record found!")
            input("Click enter to proceed...")
            print("Returning to Admin Menu....")
            time.sleep(2)
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if mydb.is_connected():
            mycursor.close()
def login_admin():                  # To let Admin log into the 'MENTOR-MENTEE PORTAL'
    password = pwinput.pwinput()
    if (password == "admin"):
        choice = 0
        while choice != 9:
            welcome()
            print("----------------------------------".ljust(100))
            print("ADMIN MENU".center(30))
            print("----------------------------------".ljust(100))
            print("1. View Mentors")
            print("2. Search a Mentor")
            print("3. Delete a Mentor")
            print("4. Publish Mentor Details")
            print("5. View Mentees")
            print("6. Search a Mentee")
            print("7. Delete a Mentee")
            print("8. Publish Mentee Details")
            print("9. Return to Main Menu")
            print()
            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    view_mentors()
                elif choice == 2:
                    search_mentor()
                elif choice == 3:
                    del_mentor()
                elif choice == 4:
                    publish_mentor_report()
                elif choice == 5:
                    view_mentees()
                elif choice == 6:
                    search_mentee()
                elif choice == 7:
                    del_mentee()
                elif choice == 8:
                    publish_mentee_report()
                elif choice == 9:
                    print("Returning to Main Menu...")
                    time.sleep(2)
                else:
                    print("INVALID CHOICE!")
                    input("Click enter to proceed...")
                    print("Returning to Admin Menu...")
                    time.sleep(2)
            except ValueError:
                print("INVALID CHOICE!")
                choice = 0
                input("Click enter to proceed...")
                print("Returning to Admin Menu....")
                time.sleep(2)
    else:
        print("Password Incorrect!!")
        input("Click enter to proceed...")
        print("Returning to Login Menu...")
        time.sleep(2)

def login():                        # Opening login facility for the existing users
    name = input('Please enter your name.\n').title()
    if name.isalpha():
        role = 0
        while role != 4:
            welcome()
            print(f'Hello {name}.')
            print()
            print("----------------------------------".ljust(100))
            print("LOGIN MENU".center(30))
            print("----------------------------------".ljust(100))
            print("1. Login as Admin")
            print("2. Login as a Mentor")
            print("3. Login as a Mentee")
            print("4. Return to Main Menu")
            print()
            try:
                role = int(input('Please enter your choice: '))
                if role == 1:
                    login_admin()
                elif role == 2:
                    login_mentor()
                elif role == 3:
                    login_mentee()
                elif role == 4:
                    print("Returning to Main Menu...")
                    time.sleep(2)
                    break
                else:
                    print("INVALID CHOICE!")
                    input("Click enter to proceed...")
                    print("Returning to Login Menu...")
                    time.sleep(2)
            except ValueError:
                print("INVALID CHOICE!")
                role = 0
                input("Click enter to proceed...")
                print("Returning to Login Menu...")
                time.sleep(2)
    else:
        print("INVALID CHOICE!")
        input("Click enter to proceed...")
        print("Returning to Main Menu...")
        time.sleep(2)

def new_mentee():                   # Adding a new mentee account to the table 'mentee_master' in the database
    welcome()
    print("----------------------------------".ljust(100))
    print("MENTEE SIGNUP".center(30))
    print("----------------------------------".ljust(100))
    print("Enter the following details:  ")
    me_name = input('Please enter your full name.\n').title()
    while me_name != '' and all(chr.isalpha() or chr.isspace() for chr in me_name):
        me_class = input('Please enter your class.\n')
        me_interest = input('Please enter the area of interest for which you require mentoring.\n').title()
        me_region = input('Please enter your location.\n').title()
        me_email = input('Enter Email Id.\n')
        while (not isValidEMail(me_email)):
            me_email = input('Invalid email id! Please enter a valid email id.\n')
            input("Click enter to proceed...")
        me_mob = input('Please enter your 10-digit mobile number.\n')
        ##    phone='+91'+ phone
        while (not isValidMob(me_mob)):
            me_mob = input('Invalid mobile number! Please enter your 10-digit mobile number.\n')
            input("Click enter to proceed...")
        me_username = input("Enter username for this account: ")
        me_pwd = input("Enter password for this account: ")
        try:
            mycursor = mydb.cursor()
            sql_insert = """INSERT INTO mentee_master 
                        (me_name, me_class, me_interest, me_region, me_email, me_mob, me_username, me_pwd)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            recordTuple = (me_name, me_class, me_interest, me_region, me_email, me_mob, me_username, me_pwd)
            mycursor.execute(sql_insert, recordTuple)
            mydb.commit()
            print("Record inserted successfully into Mentee table")
            mycursor.close()
            print("Returning to Main Menu....")
            time.sleep(2)
            return 100
        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
    else:
        print("INVALID CHOICE!")
        input("Click enter to proceed...")
        print("Returning to Signup Menu...")
        time.sleep(2)
        clear()
        return -1
def new_mentor():                   # Adding a new mentor account to the table 'mentor_master' in the database
    welcome()
    print("----------------------------------".ljust(100))
    print("MENTOR SIGNUP".center(30))
    print("----------------------------------".ljust(100))
    print("Enter the following details:  ")
    mo_name = input('Please enter your full name.\n').title()
    if mo_name != '' and all(chr.isalpha() or chr.isspace() for chr in mo_name):
        mo_qual = input('Please enter your highest qualification.\n')
        mo_class = input('Please enter the classes you mentor.\n')
        mo_interest = input('Please enter the area of interest for which you provide mentoring.\n').title()
        mo_region = input('Please enter your location.\n').title()
        mo_meetingmode = input('Please enter mode of the classes (Offline/Online).\n').title()
        mo_email = input('Enter Email Id.\n')
        while (not isValidEMail(mo_email)):
            mo_email = input('Invalid email id! Please enter a valid email id.\n')
        mo_mob = input('Please enter your 10-digit mobile number.\n')
        ##    phone='+91'+ phone
        while (not isValidMob(mo_mob)):
            mo_mob = input('Invalid mobile number! Please enter your 10-digit mobile number.\n')
        mo_username = input("Enter username for this account: ")
        mo_pwd = input("Enter password for this account: ")
        mycursor = mydb.cursor()
        try:
            sql_insert = """INSERT INTO mentor_master 
                            (mo_name, mo_qual, mo_class, mo_interest, mo_region, mo_meetingmode, mo_email, mo_mob, mo_username, mo_pwd)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            recordTuple = (mo_name, mo_qual, mo_class, mo_interest, mo_region, mo_meetingmode, mo_email, mo_mob, mo_username, mo_pwd)
            mycursor.execute(sql_insert, recordTuple)
            mydb.commit()
            print( "Record saved successfully to the Mentor table.")
            mycursor.close()
            print("Returning to Main Menu....")
            time.sleep(2)
            return 100
        except mysql.connector.Error as e:
            print("Error reading data from MySQL table", e)
            mycursor.close()
    else:
        print("INVALID CHOICE!")
        input("Click enter to proceed...")
        print("Returning to Signup Menu...")
        time.sleep(2)
        clear()
        return -1

def signup():                       # Opening signup facility for new users
    role = 0
    while role != 3:
        welcome()
        print("----------------------------------".ljust(100))
        print("SIGNUP MENU".center(30))
        print("----------------------------------".ljust(100))
        print("1. Role: Mentor")
        print("2. Role: Mentee")
        print("3. Return to Main Menu")
        try:
            role = int(input("Dear User, please enter your choice: "))
            if role == 1:
                status = new_mentor()
                if status == 100:
                    break
                else:
                    role = 0
                    continue
            elif role == 2:
                status = new_mentee()
                if status == 100:
                    break
                else:
                    role = 0
                    continue
            elif role == 3:
                print("Returning to Main Menu...")
                time.sleep(2)
                break
            else:
                print("INVALID CHOICE!")
                role = 0
                input("Click enter to proceed...")
                print("Returning to Signup Menu....")
                time.sleep(2)
        except ValueError:
            print("INVALID CHOICE!")
            role = 0
            input("Click enter to proceed...")
            print("Returning to Signup Menu....")
            time.sleep(2)

def menuMain():                     # To display Main Menu of the 'MENTOR-MENTEE PORTAL'
    index = 0
    while index != 3:
        welcome()
        print("----------------------------------".ljust(100))
        print("MAIN MENU".center(30))
        print("----------------------------------".ljust(100))
        try:
            index = int(input('Dear User, enter your choice (1 for signup, 2 for login, 3 for exit): '))
            if index == 1:
                signup()
            elif index == 2:
                login()
            elif index == 3:
                print("HAVE A GOOD DAY. BYE FOR NOW!!".center(80))
                break
            else:
                print("INVALID CHOICE!")
                input("Click enter to proceed...")
                print("Starting again....")
                time.sleep(2)
        except ValueError:
            print("INVALID CHOICE!")
            index = 0
            input("Click enter to proceed...")
            print("Starting again....")
            time.sleep(2)

# The main function: Program begins here
if __name__ == '__main__':
    menuMain()