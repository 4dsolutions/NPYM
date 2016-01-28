# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 18:42:43 2015

@author: kurner

@author: kurner
(copyleft) MIT License, 2015
"""

import sqlite3 as sql
import modeling_1_v2 as model
import datetime
import time
import os

class DB:
    backend  = 'sqlite3'
    user_initials  = 'NPYM IT'
    timezone = int(time.strftime("%z", time.localtime()))
    target_path = '/Users/kurner/Documents/classroom_labs'
    db_name = ":memory:"    
    db_name = os.path.join(target_path, 'npym.db')

    @classmethod
    def mod_date(cls):
        return time.mktime(time.gmtime())  # GMT time
        
    @classmethod
    def connect(cls):
        if cls.backend == 'sqlite3':
            DB.conn = sql.connect(DB.db_name)
            DB.c = DB.conn.cursor()
        elif cls.backend == 'mysql':
            DB.conn = sql.connect(host='localhost', 
                                  user='root', port='8889')
            DB.c = DB.conn.cursor()           
    
    @classmethod
    def disconnect(cls):
        DB.conn.close()
    
    @classmethod    
    def load_meeting(cls, the_code):
        query = ("SELECT mtg_code, mtg_name, mtg_quarter, mtg_type " 
                 "FROM Meetings "
                 "WHERE Meetings.mtg_code = '{}'".format(the_code))
        DB.c.execute(query)
        result = DB.c.fetchone()
        meeting = model.Meeting(*result[0:4])
        for group_data in DB.c.fetchall():
            meeting.add_group(DB.load_group(**group_data))       
        return meeting
    
    @classmethod
    def save_meeting(cls, meeting): 
        query = ("INSERT INTO Meetings"
        "(mtg_code, mtg_name, mtg_type) "
        "VALUES ('{}','{}', {})")
        #DB.c.execute(query.format(meeting.mtg_code, 
        #                          meeting.mtg_name, meeting.mtg_type))
        #DB.conn.commit()        
        for group in meeting.the_groups:
            DB.save_group(group)

    @classmethod
    def import_meetings(cls):
        recs = []       
        with open(os.path.join(DB.target_path, 'meetings.txt')) as f:
            for line in f.readlines():
                cols = line.split("|")
                m = model.Meeting( *cols[0:4] )
                recs.append((m.mtg_code, m.mtg_quarter, 
                             m.mtg_name, int(m.mtg_type)))
                             
        DB.c.executemany('''INSERT INTO Meetings(mtg_code, mtg_name, 
        mtg_quarter, mtg_type) VALUES (?, ?, ?, ?)'''  , recs)
        DB.conn.commit()
    
    @classmethod
    def load_roles(cls):
        query = ("SELECT role_name FROM Roles")
        DB.c.execute(query)    
        r = model.Roles()
        for group in DB.c.fetchall:
            r.add_role(group[0])
        return r
            
    @classmethod
    def save_roles(cls, roles):
        for role in roles.the_roles:
            query = ("INSERT INTO Roles"
            "(role_name) "
            "VALUES ({})")
            DB.c.execute(query.format("'{}'".format(role)))
        DB.conn.commit()

    @classmethod
    def load_mtg_types(cls):
        query = ("SELECT mtg_type, mtg_type_desc FROM Meeting_Types")
        DB.c.execute(query)    
        mt = model.Meeting_Types()
        for rec in DB.c.fetchall:
            mt.add_type(*rec)
        return mt
            
    @classmethod
    def save_mtg_types(cls, mtg_types):
        for mtg_type in mtg_types.the_types:
            query = ("INSERT INTO Meeting_Types"
            "(mtg_type, mtg_type_desc) "
            "VALUES ({}, {})")
            try:
                query = query.format(mtg_type[0], 
                            "'{}'".format(mtg_type[1]))
                DB.c.execute(query)
            except:
                print("DIAGNOSTIC:", query)
                raise
                
        DB.conn.commit()        
            
    @classmethod
    def load_friend(cls, **search):
        query = ("SELECT * FROM Friends WHERE {} = {}".
                    format(*tuple(search.items())[0])) 
        DB.c.execute(query)
        row = DB.c.fetchone()
        if row:
            return model.Friend(*row)
        raise AttributeError("No Such Friend!")
        
    @classmethod
    def save_friend(cls, friend):
        query = ("INSERT INTO Friends"
        "(friend_id, friend_name, friend_phone, friend_twitter, friend_url) "
        "VALUES ({}, '{}', '{}', '{}', '{}')")
        DB.c.execute(query.format(friend.friend_id, friend.name, friend.phone,
                                  friend.twitter, friend.url))
        DB.conn.commit()

    @classmethod
    def load_group(cls, mtg_code, the_id):
        query = ("SELECT group_id, group_name, mtg_code, group_type from Groups "
                 "WHERE Groups.mtg_code = '{code}' AND "
                 "Groups.group_id = '{group_id}'".
                 format(code=mtg_code, group_id = the_id))
                 
        DB.c.execute(query)
        result = DB.c.fetchone()
        the_type = result[-1]
        output = None
        if the_type == "MEMBERS":
            output = model.Members(*result[:3])
        elif the_type == "ATTENDERS":
            output = model.Attenders(*result[:3])
        elif the_type == "STANDING":
            output = model.Attenders(*result[:3])
        elif the_type == "STUDY":
            output = model.Study_Group(*result[:3])
        elif the_type == "AD HOC":
            output = model.Ad_Hoc_Committee(*result[:3])
        elif the_type == "INTEREST":
            output = model.Interest_Group(*result[:3])
        elif the_type == "MAILING":
            output = model.Mailing(*result[:3])
        elif the_type == "MARRIAGE":
            output = model.Marriage(*result[:3])
        elif the_type == "HOUSEHOLD":
            output = model.Household(*result[:3])
        elif the_type == "POSITION":
            output = model.Position(*result[:3])
        return output
    
    @classmethod
    def save_group(cls, group):       
        if group.__class__.__name__ == "Members":
            the_type = "MEMBERS"
        elif group.__class__.__name__ == "Attenders":
            the_type = "ATTENDERS"
        elif group.__class__.__name__ == "Standing_Committee":
            the_type = "STANDING"
        elif group.__class__.__name__ == "Study_Group":
            the_type = "STUDY"
        elif group.__class__.__name__ == "Ad_Hoc_Committee":
            the_type = "AD HOC"
        elif group.__class__.__name__ == "Interest_Group":
            the_type = "INTEREST"
        elif group.__class__.__name__ == "Mailing":
            the_type = "MAILING"
        elif group.__class__.__name__ == "Marriage":
            the_type = "MARRIAGE"
        elif group.__class__.__name__ == "Household":
            the_type = "HOUSEHOLD"
        elif group.__class__.__name__ == "Position":
            the_type = "POSITION"
            
        query = ("INSERT INTO Groups"
        "(mtg_code, group_id, group_name, group_type) "
        "VALUES ('{}', '{}', '{}', '{}')")
        DB.c.execute(query.format(group.mtg_code, group.group_id, 
                                  group.name, the_type))
                                  
        if the_type == "HOUSEHOLD":
            DB.save_hh(group)
            
        DB.conn.commit()
        
    @classmethod
    def load_services(cls):
        query = ("SELECT * FROM Services")
        DB.c.execute(query)
        npym_chrono = model.Services()
        for row in DB.c.fetchall():
            Friend = DB.load_friend(friend_id = row[0])
            Group = DB.load_group(row[2], row[1])
            npym_chrono.add_service(Friend, Group, row[3], row[4], 
                                    row[5], row[6])
        return npym_chrono
        
    @classmethod
    def save_services(cls, services):
        query = ("INSERT INTO Services"
        "(friend_id, group_id, mtg_code,"
        " start_date, stop_date, role_name, user_initials, mod_date) "
        "VALUES ({}, {}, {}, {}, {}, {}, {}, {})")

        for srv in services.chronology:
            srv2 , srv3, srv4 = 'NULL', 'NULL', 'NULL'
            if isinstance(srv[2], datetime.date):
                srv2 = srv[2].toordinal()
                
            if isinstance(srv[3], datetime.date):
                srv3 = srv[3].toordinal()

            if srv[4] != None:  # a role pertains
                srv4 = "'{}'".format(srv[4])
                
            srv5 = "'{}'".format(srv[5])
                
            try:
                DB.c.execute(query.format(
                            srv[0].friend_id, 
                            "'{}'".format(srv[1].group_id), 
                            "'{}'".format(srv[1].mtg_code), 
                            srv2, srv3, srv4, 
                            srv5, srv[6]))
            except:
                print("DIAGNOSTIC")
                print(query)
                print(srv[0].friend_id, 
                            "'{}'".format(srv[1].group_id), 
                            "'{}'".format(srv[1].mtg_code), 
                            srv2, srv3, srv4, 
                            srv5, srv[6])
                raise
                              
        DB.conn.commit()

    @classmethod
    def join(cls, friend_id, group, period, role_name):
        friend = DB.load_friend(friend_id = friend_id)
        chrono.add_service(friend, group, 
                        period[0], period[1],
                        role_name, cls.user_initials, cls.mod_date())

    @classmethod
    def save_hh(cls, group):
        data = group.data
        mtg_code = group.mtg_code
        hh_id = group.group_id
        hh_name = group.name
        hh_street = data.get('hh_street', '')
        hh_apt = data.get('hh_street', '')
        hh_city = data.get('hh_city', '')
        hh_state = data.get('hh_state', '')
        hh_zip = data.get('hh_zip', '')
        hh_phone = data.get('hh_phone', '')
        hh_latlong = data.get('hh_latlong', '')
        DB.c.execute("""INSERT INTO Households(mtg_code, hh_id, hh_name,
        hh_street, hh_apt, hh_city, hh_state, hh_zip, hh_phone,
        hh_latlong) VALUES ('{}', '{}', '{}', '{}', '{}', 
                            '{}', '{}', '{}', '{}', '{}')""".format(
            mtg_code, hh_id, hh_name, hh_street, hh_apt, hh_city, 
            hh_state, hh_zip, hh_phone, hh_latlong))
                        
    @classmethod
    def auth_user(cls, user_id):
        cls.user_id = user_id

    @classmethod
    def dump_tables(cls):
        print("FRIENDS:")
        for row in DB.c.execute("SELECT * FROM friends"):
            print(row)
        print("MEETINGS:")    
        for row in DB.c.execute("SELECT * FROM meetings"):
            print(row)
        print("GROUPS:") 
        for row in DB.c.execute("SELECT * FROM groups"):
            print(row)
        print("SERVICES:")
        for row in DB.c.execute("SELECT * FROM services"):
            print(row)
        print("ROLES:")
        for row in DB.c.execute("SELECT * FROM roles"):
            print(row)
        print("MEETING_TYPES:")
        for row in DB.c.execute("SELECT * FROM meeting_types"):
            print(row)
        print("MEETING_TYPES:")
        for row in DB.c.execute("SELECT * FROM marriages"):
            print(row)
            
class DBcontext():

    def __enter__(self):
        DB.connect() 
        
    def __exit__(self, *stuff_happens):
        DB.disconnect()
        if stuff_happens[0]:
            print(stuff_happens)
            return False
        return True
        
def create_DB():

    DB.c.execute("""DROP TABLE IF EXISTS Meetings""")
    DB.c.execute("""CREATE TABLE Meetings
        (mtg_code text PRIMARY KEY,
         mtg_name text,
         mtg_quarter text,
         mtg_type int)""")

    DB.c.execute("""DROP TABLE IF EXISTS Groups""")
    DB.c.execute("""CREATE TABLE Groups
        (mtg_code text,
         group_id text,
         group_name text,
         group_type text)""")

    DB.c.execute("""DROP TABLE IF EXISTS Friends""")
    DB.c.execute("""CREATE TABLE Friends
        (friend_id int PRIMARY KEY,
         friend_name text,
         friend_phone text,
         friend_twitter text,
         friend_url text)""")

    DB.c.execute("""DROP TABLE IF EXISTS Households""")         
    DB.c.execute("""CREATE TABLE Households
        (mtg_code text,
         hh_id text,
         hh_name text,
         hh_street text,
         hh_apt text,
         hh_city text,
         hh_state text,
         hh_zip text,
         hh_phone text,
         hh_latlong text)""")

    DB.c.execute("""DROP TABLE IF EXISTS Roles""") 
    DB.c.execute("""CREATE TABLE Roles
        (role_name text)""")

    DB.c.execute("""DROP TABLE IF EXISTS Meeting_Types""") 
    DB.c.execute("""CREATE TABLE Meeting_Types
        (mtg_type int,
         mtg_type_desc text)""")
        
    DB.c.execute("""DROP TABLE IF EXISTS Services""") 
    DB.c.execute("""CREATE TABLE Services
        (friend_id int,
         group_id text,
         mtg_code text,
         start_date int,
         stop_date int,
         role_name text,
         user_initials text,
         mod_date int)""")
         
    DB.c.execute("""DROP TABLE IF EXISTS Users""") 
    DB.c.execute("""CREATE TABLE Users
        (user_initials text,
         user_timezone text,
         password_enc text)""")

    DB.c.execute("""DROP VIEW IF EXISTS member_attender""")         
    DB.c.execute("""CREATE VIEW 
    member_attender AS 
    SELECT fr.friend_name, fr.friend_id, mtg.mtg_code, mtg.mtg_name, 
        srv.start_date, srv.stop_date 
        FROM services srv, friends fr, groups gr, meetings mtg
        WHERE srv.friend_id = fr.friend_id
        AND (srv.mtg_code = mtg.mtg_code)
        AND (srv.group_id = gr.group_id AND srv.mtg_code = gr.mtg_code)
        AND (gr.group_type = "MEMBERS" OR gr.group_type = 'ATTENDERS')
        ORDER BY fr.friend_name""")

    DB.c.execute("""DROP VIEW IF EXISTS hhlds""")         
    DB.c.execute("""CREATE VIEW 
    hhlds AS
    SELECT mtg.mtg_code, gr.hh_id, gr.hh_name, gr.hh_street, gr.hh_city, gr.hh_state,
        gr.hh_zip, fr.friend_name, fr.friend_id,  
        srv.start_date, srv.stop_date 
        FROM services srv, friends fr, households gr, meetings mtg
        WHERE srv.friend_id = fr.friend_id
        AND (srv.mtg_code = mtg.mtg_code)
        AND (srv.group_id = gr.hh_id AND srv.mtg_code = gr.mtg_code)
        ORDER BY mtg.mtg_code, gr.hh_id, fr.friend_name""")

    DB.c.execute("""DROP VIEW IF EXISTS marriages""")         
    DB.c.execute("""CREATE VIEW 
    marriages AS
    SELECT mtg.mtg_code, gr.group_id, fr.friend_name, fr.friend_id,  
        srv.start_date, srv.stop_date 
        FROM services srv, friends fr, groups gr, meetings mtg
        WHERE srv.friend_id = fr.friend_id
        AND (srv.mtg_code = mtg.mtg_code)
        AND (srv.group_id = gr.group_id AND srv.mtg_code = gr.mtg_code)
        AND (gr.group_type = "MARRIAGE")
        ORDER BY mtg.mtg_code, gr.group_id, fr.friend_name""")
        
    DB.c.execute("""DROP VIEW IF EXISTS slates""")         
    DB.c.execute("""CREATE VIEW 
    slates AS        
    SELECT mtg.mtg_code, gr.group_name, srv.role_name, fr.friend_name, 
    srv.friend_id, srv.start_date, srv.stop_date  
        FROM services srv, friends fr, groups gr, meetings mtg
        WHERE srv.friend_id = fr.friend_id
        AND (srv.mtg_code = mtg.mtg_code)
        AND (srv.group_id = gr.group_id AND srv.mtg_code = gr.mtg_code)
        AND (gr.group_type = "STANDING" OR gr.group_type = "AD HOC" 
        OR gr.group_type = "POSITION")
        ORDER BY mtg.mtg_code, gr.group_name, srv.friend_id""")
    DB.conn.commit()
    
if __name__ == "__main__":
    
    with DBcontext() as ctx:
        
        create_DB()
        
        DB.import_meetings()  # raw data file
        
        mmm  = DB.load_meeting("mu")
        univ = DB.load_meeting("un")
        npym = DB.load_meeting("npym")
        hld  = DB.load_meeting("hld")
        boise = DB.load_meeting("bo")
        tacoma = DB.load_meeting("ta")
        sos = DB.load_meeting("sos") # south seattle
        corvallis = DB.load_meeting("co") # corvallis
        bridgecity = DB.load_meeting("br") # bridge city
        lopez = DB.load_meeting("lo") # lopez island       
        gfalls = DB.load_meeting("gre") # great falls
        missoula = DB.load_meeting("mio") # missoula
        sheridan = DB.load_meeting("shr") # sheridan
         
        mmm.add_group(model.Members('000', "Members"))   
        mmm.add_group(model.Attenders('555', "Attenders"))  
        
        the_data = dict(hh_street = '3745 SE Harrison St.',
            hh_city = 'Portland', hh_state = 'OR', hh_zip = '97214')
        mmm.add_group(model.Household('HH222', "Urner Residence", 
                                      code='mu', data=the_data))
                                      
        the_data = dict(hh_street = '1827 SE 38th St.',
            hh_city = 'Portland', hh_state = 'OR', hh_zip = '97214')
        mmm.add_group(model.Household('HH015', "Urner Residence", 
                                      code='mu', data=the_data)) 
                                      
        mmm.add_group(model.Marriage('M123', "Urner-Wicca", code="mu"))
        
        univ.add_group(model.Members('000', "Members"))   
        univ.add_group(model.Attenders('555', "Attenders"))  
 
        hld.add_group(model.Attenders('000', "Attenders"))    
        boise.add_group(model.Members('000', "Members"))
        tacoma.add_group(model.Members('000', "Members"))
        sos.add_group(model.Members('000', "Members"))
        corvallis.add_group(model.Members('000', "Members"))
        bridgecity.add_group(model.Members('000', "Members"))
        lopez.add_group(model.Members('000', "Members"))
        gfalls.add_group(model.Members('000', "Members")) 
        missoula.add_group(model.Members('000', "Members")) 
        sheridan.add_group(model.Members('000', "Attenders"))
        
        # Multnomah Positions
        for p_id, pos in (
            ('910', "Meeting Assistant Clerk"),
            ('911', "Meeting Clerk"),
            ('912', "Database Manager"),
            ('914', "AFSC Liaison"),
            ('915', "FCNL Liaison"),
            ('899', "Treasurer"),
            ('898', "Assistant Treasurer"),
            ('897', "Recording Clerk"),
            ('020', "Hearthkeeper"),
            ('021', "Newsletter Editor"),
            ('022', "Bulletin Editor"),
            ('023', "Web Keeper"),
            ('024', "Archivist")):
            mmm.add_group(model.Position(p_id, pos))

        # Multnomah Standing Committees
        for sc_id, sc in (
            ('001', "Property"),
            ('002', "M&O"),
            ('003', "W&M"),
            ('004', "Social"),
            ('005', "Communications"),
            ('006', "Program"),
            ('007', "Childrens Program"),
            ('008', "Nominating"),
            ('009', "PSCC"),
            ('010', "Library"),
            ('014', "Finance"),
            ('015', "Nursery"),
            ('016', "Middle School Advisors"),
            ('017', "Junior Friends Advisors"),
            ('018', "Youth Programming"),
            ('019', "Transportation Facilitator")):
            mmm.add_group(model.Standing_Committee(sc_id, sc))

        # Multnomah Ad Hoc Committees
        mmm.add_group(model.Ad_Hoc_Committee('107', "Sex & Gender"))
        mmm.add_group(model.Ad_Hoc_Committee('207', "Relocation"))

        # NPYM Positions
        for p_id, pos in (
            ('708', "Coord Comm Clerk"),
            ('709', "Coord Comm Associate Clerk"),
            ('710', "Treasurer"),
            ('711', "Presiding Clerk"),
            ('712', "Web Keeper"),
            ('713', "NPYM Secretary"),
            ('714', "Registrar"),
            ('715', "Annual Sess Recording Clerk")):
            npym.add_group(model.Position(p_id, pos))

        # NPYM Standing Committees
        for sc_id, sc in (
            ('111', "Information Technology"),
            ('112', "M&O"),
            ('113', "Nominating")):
            npym.add_group(model.Standing_Committee(sc_id, sc))
         
        for meeting in (mmm, univ, npym, sos, boise, corvallis, 
                        tacoma, bridgecity, hld, lopez, gfalls, missoula,
                        sheridan):
            DB.save_meeting(meeting)
           
        roles = model.Roles()
        for r in (
            "Committee Clerk", "Recording Clerk", "Committee Member",
            "Member ex officio", "Advisor", "Subscriber", "Resident",
            "Position holder", "Spouse"):
            roles.add_role(r)
        DB.save_roles(roles)
              
        types = model.Meeting_Types()
        for num, txt in (
            (5, "Yearly Meeting"),(1, "Monthly Meeting"),
            (4, "Quarterly Meeting"),(3, "Preparative Meeting"), 
            (2, "Worship Group"), (6, "Outside NPYM")):
            types.add_type(num, txt) 
        DB.save_mtg_types(types)
        
        DB.save_friend(model.Friend(808, "Urner, Kirby", '', 
        '@thekirbster',
        '4dsolutions.net'))
        DB.save_friend(model.Friend(192, "Abbot, Carl"))
        DB.save_friend(model.Friend(201, "Hollister, Diane"))
        DB.save_friend(model.Friend(339, "Seifert, Rick"))
        DB.save_friend(model.Friend(901, "Chandler, David"))
        
        DB.save_friend(model.Friend(818, "Goren, Mike"))
        DB.save_friend(model.Friend(775, "Gordon, Lyn"))
        DB.save_friend(model.Friend(211, "Dudley, Ann"))
        DB.save_friend(model.Friend(349, "Day, Camille"))
        DB.save_friend(model.Friend(911, "Carpentieri, Giovanna"))
     
        DB.save_friend(model.Friend(828, "Rhys, Marian"))
        DB.save_friend(model.Friend(785, "Schade, Curtis"))
        DB.save_friend(model.Friend(221, "Heidegger, Larry"))
        DB.save_friend(model.Friend(359, "Deibele, Theresa"))
        DB.save_friend(model.Friend(921, "Anderson, Beta"))
    
        DB.save_friend(model.Friend(838, "Ford, Peter"))
        DB.save_friend(model.Friend(795, "Mullen, Kathe"))
        DB.save_friend(model.Friend(231, "Ek, Dave"))
        DB.save_friend(model.Friend(369, "Monzon, Gary"))
        DB.save_friend(model.Friend(931, "Scholl, Lew"))
        
        DB.save_friend(model.Friend(848, "Pebly, Christine"))
        DB.save_friend(model.Friend(705, "Uhte, Carol"))
        DB.save_friend(model.Friend(241, "Allyn, Mark"))
        DB.save_friend(model.Friend(379, "Pinney, Sonya"))
        DB.save_friend(model.Friend(941, "Commor, Aimee Ford"))
    
        DB.save_friend(model.Friend(858, "MacDaniel, Pahtrisha"))
        DB.save_friend(model.Friend(715, "Eichenberger, Erin"))
        DB.save_friend(model.Friend(251, "Kenworthy, Betsey"))
        DB.save_friend(model.Friend(389, "Cross, Andy"))
        DB.save_friend(model.Friend(951, "Richard, Nancy"))
    
        DB.save_friend(model.Friend(868, "Houghton, Eric"))
        DB.save_friend(model.Friend(725, "Averill, Deborah"))
        DB.save_friend(model.Friend(261, "Marson, Ron"))
        DB.save_friend(model.Friend(399, "Crouch, Marty"))
        DB.save_friend(model.Friend(961, "Snook, Julie"))
    
        DB.save_friend(model.Friend(878, "Scholes, Rhys"))
        DB.save_friend(model.Friend(735, "Simpson, Ian"))
        DB.save_friend(model.Friend(271, "Riggs, Susan"))
        DB.save_friend(model.Friend(309, "von Kuster, Josh"))
        DB.save_friend(model.Friend(971, "Snyder, Joe"))
    
        DB.save_friend(model.Friend(898, "Bautista, Euclid"))
        DB.save_friend(model.Friend(745, "Urner, Carol"))
        DB.save_friend(model.Friend(281, "Hyzy, Kathy"))
        DB.save_friend(model.Friend(319, "Hickcox, Leslie"))
        DB.save_friend(model.Friend(981, "Bove, Renee"))
        
        DB.save_friend(model.Friend(222, "Crowne, Adrian Harris"))
        DB.save_friend(model.Friend(223, "Hill, Alberta"))
        DB.save_friend(model.Friend(226, "Weimseister, Clint"))
        DB.save_friend(model.Friend(229, "Kocourek, Linda"))
        DB.save_friend(model.Friend(224, "Yagoda, Lisa"))

        DB.save_friend(model.Friend(228, "Braithwaite, Ron"))
        DB.save_friend(model.Friend(390, "Crouch, Eddy"))
        DB.save_friend(model.Friend(391, "Hutchison, Perry"))
        DB.save_friend(model.Friend(392, "Ostrom, Warren"))    
        DB.save_friend(model.Friend(393, "Willard, Chris")) 

        DB.save_friend(model.Friend(394, "Kenny, Otis")) 
        DB.save_friend(model.Friend(395, "Brown, Jonathan"))
        DB.save_friend(model.Friend(396, "Williams, Kim"))
        DB.save_friend(model.Friend(397, "McLauchlan, Nancy"))
        DB.save_friend(model.Friend(398, "Foster, Georgia"))

        DB.save_friend(model.Friend(400, "Green, Dorsey"))
        DB.save_friend(model.Friend(401, "Zerwekh, Joyce"))
        DB.save_friend(model.Friend(402, "Graville, Jerry"))
        DB.save_friend(model.Friend(403, "Etter, Ted"))
        DB.save_friend(model.Friend(404, "Head, Tom"))

        DB.save_friend(model.Friend(405, "Fabik, Dave"))
        DB.save_friend(model.Friend(406, "Humphrey, Lucretia")) 
        DB.save_friend(model.Friend(407, "Hyzy, Kathy")) 
        DB.save_friend(model.Friend(408, "Willard, Kathryn")) 
        DB.save_friend(model.Friend(409, "Holden, Steve"))
        
        DB.save_friend(model.Friend(411, "Ewert, Jane"))
        DB.save_friend(model.Friend(410, "Urner, Tara"))
        DB.save_friend(model.Friend(412, "Alexander, Angie"))
        DB.save_friend(model.Friend(413, "Wicca, Dawn"))
        
        chrono = model.Services()

        per1213 = (datetime.date(2012, 6, 30), 
                   datetime.date(2013, 7, 1))
                   
        per1214 = (datetime.date(2012, 6, 30), 
                   datetime.date(2014, 7, 1))

        per1314 = (datetime.date(2013, 6, 30), 
                   datetime.date(2014, 7, 1))

        per1415 = (datetime.date(2012, 6, 30), 
                   datetime.date(2014, 7, 1))
                   
        per1416 = (datetime.date(2014, 6, 30), 
                   datetime.date(2016, 7, 1))
    
        per1417 = (datetime.date(2014, 6, 30), 
                   datetime.date(2016, 7, 1))
    
        per1316 = (datetime.date(2013, 6, 30), 
                   datetime.date(2016, 7, 1))

                                      
        unspec = (None, None)
    
        user_id = DB.auth_user(123)
     
        # Meeting Clerk
        with DB.load_group('mu', '911') as group:
            DB.join(389, group, per1416, "Position holder") # Andy
 
        # Treasurer
        with DB.load_group('mu', '899') as group:
            DB.join(828, group, per1416, "Position holder") # Marian
            
        # Assistant Treasurer
        with DB.load_group('mu', '898') as group:
            DB.join(911, group, per1416, "Position holder") # Giovanna
            
        # Recording Clerk
        with DB.load_group('mu', '897') as group:
            DB.join(391, group, per1416, "Position holder") # Perry
            
        # Archivist
        with DB.load_group('mu', '024') as group:
            DB.join(192, group, per1416, "Position holder") # Carl
            
        # PSCC   
        with DB.load_group('mu', '009') as group:  
            DB.join(725, group, per1416, "Committee Clerk")
            DB.join(261, group, per1416, "Committee Member")
            DB.join(399, group, per1416, "Committee Member")
            DB.join(745, group, per1416, "Committee Member")  
            DB.join(901, group, per1416, "Committee Member")        
            DB.join(961, group, per1416, "Committee Member")
            DB.join(878, group, per1416, "Committee Member")
            DB.join(319, group, per1416, "Member ex officio") # Leslie    
            DB.join(981, group, per1416, "Member ex officio") # Renee

        # FCNL Liaison
        with DB.load_group('mu', '915') as group:
            DB.join(319, group, per1316, "Position holder") # Leslie

        # AFSC Liaison
        with DB.load_group('mu', '914') as group:
            DB.join(390, group, per1213, "Position holder") # Eddy
            DB.join(808, group, per1314, "Position holder") # Kirby
            DB.join(981, group, per1416, "Position holder") # Renee
                            
        # Property                
        with DB.load_group('mu', '001') as group:
            DB.join(201, group, per1417, "Committee Clerk")
            DB.join(211, group, per1316, "Member ex officio")
            DB.join(231, group, per1316, "Committee Member")                    
            DB.join(369, group, per1417, "Committee Member")
            DB.join(931, group, per1417, "Committee Member")
                        
        # Communications  
        with DB.load_group('mu', '005') as group: 
            DB.join(339, group, per1316, "Committee Clerk")
            DB.join(901, group, per1417, "Committee Member")
            DB.join(222, group, per1417, "Committee Member")
            DB.join(818, group, per1417, "Committee Member")
            DB.join(775, group, per1417, "Member ex officio")        
            DB.join(211, group, per1417, "Member ex officio") 
            DB.join(349, group, per1417, "Tech Support")

        # Database Managers
        with DB.load_group('mu', '912') as group:
            DB.join(222, group, per1417, "Position holder")
            DB.join(818, group, per1417, "Position holder")
            
        # Web Keeper            
        with DB.load_group('mu', '023') as group:
            DB.join(901, group, per1417, "Position holder") # David C

        # Members Multnomah
        with DB.load_group('mu', '000') as group:
            DB.join(971, group, unspec, '')
            DB.join(339, group, unspec, '')
            DB.join(309, group, unspec, '')
            DB.join(261, group, unspec, '')
            DB.join(251, group, unspec, '')
            DB.join(201, group, unspec, '')
            DB.join(407, group, unspec, '')
            DB.join(401, group, unspec, '')
            
        # Attenders Multnomah
        with DB.load_group('mu', '555') as group: 
            DB.join(848, group, unspec, '')
            DB.join(808, group, unspec, '')

        # Households Multnomah
        with DB.load_group('mu', 'HH222') as group: 
            DB.join(745, group, (datetime.date(1995, 4, 10), None), 'Resident')
            DB.join(808, group, (datetime.date(1995, 4, 10), None), 'Resident')
            DB.join(410, group, (datetime.date(1995, 4, 10), None), 'Resident')
            DB.join(413, group, (datetime.date(1995, 4, 10), 
                                 datetime.date(2007, 3, 13)), 'Resident')
            
        # Households Multnomah        
        with DB.load_group('mu', 'HH015') as group: 
            DB.join(745, group, (datetime.date(1992, 12, 31),
                                 datetime.date(1995, 4, 9)), 'Resident')
            DB.join(808, group, (datetime.date(1992, 12, 31), 
                                 datetime.date(1995, 4, 9)), 'Resident')
            DB.join(410, group, (datetime.date(1994, 6, 7),
                                 datetime.date(1995, 4, 9)), 'Resident')
            DB.join(413, group, (datetime.date(1992, 12, 31),
                                 datetime.date(1995, 4, 9)), 'Resident')
                                 
        # Marriages Multnomah
        with DB.load_group('mu', 'M123') as group: 
            DB.join(808, group, (datetime.date(1993, 9, 11), 
                                 datetime.date(2007, 3, 13)), 'Spouse')
            DB.join(413, group, (datetime.date(1993, 9, 11),
                                 datetime.date(2007, 3, 13)), 'Spouse')
            
        # Members Boise
        with DB.load_group('bo', '000') as group:
            DB.join(394, group, unspec, '')

        # Members Tacoma
        with DB.load_group('ta', '000') as group:
            DB.join(393, group, unspec, '')
            DB.join(412, group, unspec, '')            
            DB.join(408, group, unspec, '')  
            
        # Members University
        with DB.load_group('un', '000') as group:
            DB.join(392, group, unspec, '')
            DB.join(400, group, unspec, '') 
            DB.join(229, group, unspec, '')
            
        # Members South Seattle
        with DB.load_group('sos', '000') as group:
            DB.join(395, group, unspec, '')

        # Members Corvallis
        with DB.load_group('co', '000') as group:
            DB.join(224, group, unspec, '')

        # Members Bridge City
        with DB.load_group('br', '000') as group:
            DB.join(411, group, unspec, '')
            DB.join(397, group, unspec, '')

        # Members Lopez Island
        with DB.load_group('lo', '000') as group:
            DB.join(402, group, unspec, '')

        # Members Great Falls
        with DB.load_group('gre', '000') as group:
            DB.join(406, group, unspec, '')

        # Members Missoula
        with DB.load_group('mio', '000') as group:
            DB.join(403 , group, unspec, '')
 
        # Attenders Sherican
        with DB.load_group('shr', '000') as group:           
            DB.join(398 , group, unspec, '')
            
        # Attenders Hillsdale
        with DB.load_group('hld', '000') as group:      
            DB.join(339, group, (datetime.date(2014,1,1), None), '') # Rick Seifert
            
        # Service Periods (terms) for NPYM srv records
        oct1214 = (datetime.date(2012, 10, 1), 
                   datetime.date(2014, 9, 30))

        oct1215 = (datetime.date(2012, 10, 1), 
                   datetime.date(2015, 9, 30))
                           
        oct1415 = (datetime.date(2014, 10, 1), 
                   datetime.date(2015, 9, 30))

        may1115 = (datetime.date(2011, 5, 1), 
                   datetime.date(2015, 9, 30))

        oct1216 = (datetime.date(2012, 10, 1), 
                   datetime.date(2016, 9, 30))
                   
        oct1316 = (datetime.date(2013, 10, 1), 
                   datetime.date(2016, 9, 30))

        oct1416 = (datetime.date(2014, 10, 1), 
                   datetime.date(2016, 9, 30))
                   
        oct1417 = (datetime.date(2014, 10, 1), 
                   datetime.date(2017, 9, 30))
                   
        oct1517 = (datetime.date(2015, 10, 1), 
                   datetime.date(2017, 9, 30))
                           
        # NPYM IT Committee
        with DB.load_group('npym', '111') as group:
            DB.join(226, group, oct1215, "Member ex officio") # Clint
            DB.join(224, group, oct1316, "Committee Member")  # Lisa
            DB.join(808, group, oct1417, "Committee Clerk")   # Kirby
            DB.join(223, group, oct1214, "Committee Member")  # Alberta
            DB.join(223, group, oct1415, "Committee Clerk")   # Alberta
            DB.join(228, group, may1115, "Committee Member")  # Ron
            DB.join(229, group, oct1316, "Member ex officio") # Linda

        # NPYM Oversight Committee
        with DB.load_group('npym', '112') as group:
            DB.join(397, group, oct1316, "Committee Clerk")  # Nancy
            DB.join(398, group, oct1316, "Committee Member") # Georgia
            DB.join(411, group, oct1316, "Committee Member") # Jane
            DB.join(251, group, oct1417, "Committee Member") # Betsey
            DB.join(400, group, oct1417, "Committee Member") # Dorsey

        # NPYM Nominating Committee
        with DB.load_group('npym', '113') as group:
            DB.join(402, group, oct1416, "Committee Member") # Jerry
            DB.join(403, group, oct1316, "Committee Member") # Etter
            DB.join(406, group, oct1517, "Committee Member") # Lucretia
            DB.join(407, group, oct1517, "Committee Member") # Hyzy
            DB.join(408, group, oct1517, "Committee Clerk") # Willard
            DB.join(401, group, oct1416, "Committee Member")  # Joyce
            
        # NPYM Secretary
        with DB.load_group('npym', '713') as group:
            DB.join(229, group, oct1416, "Position holder") # Linda

        # Registrar
        with DB.load_group('npym', '714') as group:
            DB.join(396, group, oct1416, "Position holder") # Kim
                        
        # Presiding Clerk
        with DB.load_group('npym', '711') as group:
            DB.join(392, group, oct1517, "Position holder") # Warren

        # Coordinating Committee Clerk
        with DB.load_group('npym', '708') as group:
            DB.join(394, group, oct1416, "Position holder") # Otis

        # Coordinating Committee Associate Clerk
        with DB.load_group('npym', '709') as group:
            DB.join(393, group, oct1216, "Position holder") # Chris

        # Annual Session Recording Clerk
        with DB.load_group('npym', '709') as group:
            DB.join(412, group, oct1416, "Position holder") # Angie
            
        # Treasurer
        with DB.load_group('npym', '710') as group:
            DB.join(395, group, oct1417, "Position holder") # Jonathan

        # Web Keeper
        with DB.load_group('npym', '712') as group:
            DB.join(389, group, oct1215, "Position holder") # Clint
                 
                                  
        DB.save_services(chrono)
        history = DB.load_services()
        # history.list_services()
        DB.dump_tables()

        
   
    