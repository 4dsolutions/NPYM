# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:09:13 2015

@author: kurner
(copyleft) MIT License, 2015

Initial stages of middle-ware ORM for moving table data to/from instances of classes.

Main idea:

Friends join Groups (of several subtype) for finite duration periods,
though None may apply to start and/or end datetime.  One may join in
a role (e.g. clerk, recording clerk, member).  Slate positions within
a Monthly Meeting (MM) e.g. Archivist, are not roles, but Groups of 
one individual.

Meetings of different type (Monthly, Yearly, Worship Group, Preparative), host 
myriad groups.  Each household is a group (HouseHold is a subclass of Group, 
as is a Marriage, as is a magazine subscription -- leaving it up to each 
Meeting what it considers its business to record / track.

More information:
http://www.quakerquaker.org/profiles/blogs/group-theory

"""
import datetime
import time

class Meeting:
    
    def __init__(self, mtg_code, mtg_name, mtg_quarter, mtg_type):
        self.mtg_code = mtg_code
        self.mtg_quarter = mtg_quarter
        self.mtg_name = mtg_name
        self.mtg_type = mtg_type
        self.the_groups = set()
        
    def add_group(self, the_group):
        the_group.mtg_code = self.mtg_code
        self.the_groups.add(the_group)
        
    def __call__(self, group_id):
        for group in self.the_groups:
            if group_id == group.group_id:
                return group
    
    def __repr__(self):
        return "Meeting: {}".format(self.code)
        
class Friend:
    def __init__(self, friend_id, name, phone="", twitter="", url=""):
        self.friend_id = friend_id
        self.name = name
        self.phone = phone
        self.twitter = twitter
        self.url = url

class Group:
    
    def __init__(self, group_id, name, code=None, data={}):
        self.mtg_code = code
        self.group_id = group_id
        self.name = name
        self.data = data
        
    def __enter__(self):
        return self
        
    def __exit__(self, *stuff):
        if not stuff:
            return True
        else:
            return False
        
    def __repr__(self):
        return "{}: {} {}".format(self.mtg_code, self.group_id, self.name)

class Members(Group): pass
class Attenders(Group): pass
class Interest_Group(Group): pass
class Study_Group(Group): pass
class Marriage(Group): pass
class Household(Group): pass 
class Mailing(Group): pass    
class Committee(Group): pass
class Position(Group): pass
class Standing_Committee(Committee): 
    def __repr__(self):
        return "{} {} (Standing)".format(self.group_id, self.name)

class Ad_Hoc_Committee(Committee):
    def __repr__(self):
        return "{} {} (Ad Hoc)".format(self.group_id, self.name)
        
class Subcommittee(Committee): pass

class Roles:
    def __init__(self):
        self.the_roles = set()
    def add_role(self, the_role):
        self.the_roles.add(the_role)

class Meeting_Types:
    def __init__(self):
        self.the_types = set()
    def add_type(self, *the_type):
        self.the_types.add(the_type) # set of (int, text) tuples
        
class DB:
    user_id = 808
    user_initials = "NPYM IT"
    
    @classmethod
    def mod_date(cls):
        return time.mktime(time.gmtime())

class Services:
    
    def __init__(self):
        self.chronology = list()
        
    def add_service(self, friend_id, group, start, stop, role_name, 
                    user_initials = DB.user_initials, mod_date = DB.mod_date()):                       
        self.chronology.append((friend_id, group, start, stop, 
                                role_name, user_initials, mod_date)) 
        
    def list_services(self):
        print("CHRONOLOGY OF SERVICE: NPYM\n===========================\n")
        for srv in self.chronology:
            print(
            "{group}:\n"
            "{name} ({friend_id})\n"
            "From: {start}  To: {stop}\n" 
            "As: {role}\n"
            "Entered by: {user} on: {mod_date} GMT\n".format(
            group = srv[1],
            name = srv[0].name, 
            friend_id = srv[0].friend_id,
            start = datetime.date.fromordinal(srv[2]) \
                if isinstance(srv[2], int) \
                else srv[2],
            stop  = datetime.date.fromordinal(srv[3]) \
                if isinstance(srv[3], int) \
                else srv[3],
            role  = srv[4], user = srv[5], \
            mod_date = datetime.datetime.fromtimestamp(srv[6])))

if __name__ == "__main__":

    PDX = Meeting("mu", "wqm", "Multnomah Meeting", 1)
    SEA = Meeting("un", "pnqm", "University Meeting", 1)
    NPYM = Meeting("npym", "", "NPYM", 5)

    PDX.add_group(Members('000', "Members"))    # another kind of group
    PDX.add_group(Attenders('555', "Attenders"))  # another kind of group
    SEA.add_group(Members('000', "Members"))   
    SEA.add_group(Attenders('555', "Attenders"))  
    
    PDX.add_group(Standing_Committee('001', "Property"))
    SEA.add_group(Standing_Committee('001', "Supervisory"))
    NPYM.add_group(Standing_Committee('111', "Information Technology"))

    PDX.add_group(Ad_Hoc_Committee('005', "Personnel"))
    PDX.add_group(Ad_Hoc_Committee('007', "Relocation"))

    roles = Roles()
    roles.add_role("Committee Clerk")
    roles.add_role("Recording Clerk")
    roles.add_role("Committee Member")
    roles.add_role("Database Manager")
    roles.add_role("Editor")  
    roles.add_role("Web Keeper")
    roles.add_role("Member ex officio")
    roles.add_role("Advisor")
    roles.add_role("Subscriber")
    roles.add_role("Resident")
    roles.add_role("Spouse")
    
    types = Meeting_Types()
    types.add_type(5, "Yearly Meeting")
    types.add_type(4, "Quarterly Meeting")
    types.add_type(1, "Monthly Meeting")
    types.add_type(3, "Preparative Meeting")
    types.add_type(2, "Worship Group") 
    types.add_type(6, "Outside NPYM")  
    
    npym_chrono = Services()
    user_id = 123
    
    npym_chrono.add_service(
        Friend(765, "Meyer, Lilly"), PDX('001'),
        datetime.date(2015,10,10), datetime.date(2016,10,10),
        "Committee Clerk")
    
    npym_chrono.add_service(    
        Friend(201, "Heigdegger, Larry"), PDX('007'), 
        datetime.date(2015,10,10), datetime.date(2016,10,10),
        "Recording Clerk")
    
    npym_chrono.add_service(
        Friend(339, "Mitchell, Sandy"), SEA('001'),  
        datetime.date(2015,10,10), datetime.date(2016,10,10),
        "Committee Clerk")   
        
    npym_chrono.add_service(
        Friend(901, "Davis, Chris"), SEA('001'), 
        datetime.date(2015,10,10), datetime.date(2016,10,10),
        "Recording Clerk") 
        
    npym_chrono.add_service(
        Friend(339, "Mitchell, Sandy"), SEA('000'), 
        datetime.date(2000,1,1), None, None) 
        
    npym_chrono.add_service(
        Friend(201, "Heigdegger, Larry"), SEA('555'),
        datetime.date(2000,1,1), None, None) 

    npym_chrono.add_service(
        Friend(808, "Urner, Kirby"), NPYM('111'),
        datetime.date(2014,10,1), datetime.datetime(2017,9,30),
        "Committee Clerk") 
        
    npym_chrono.list_services()
