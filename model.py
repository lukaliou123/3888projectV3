#import database here
import sql
from datetime import *
from flask import *
import jwt
from time import time
import requests
import json


now = datetime.now()


    #------------------------------------------------------------

""" Check if the login inforamtion is correct"""
def login_check(username, password):
    dbConnect = sql.SQLDatabase()
    result = dbConnect.login_credential_check(username, password)

    if result == None:
        return False
    else:
        return result

    #------------------------------------------------------------


""" Register new account and Check if the account registered available(if username already used) """
def register_check(fname, lname, email, username, password, gender):
    dbConnect = sql.SQLDatabase()
    if gender == "None":
        gender_res = None
    result = dbConnect.registration_check(fname, lname, email, username, password, gender_res)
    if result:
        return True
    else:
        return False


    #------------------------------------------------------------

""" Get the information about schedule of the leader """
def mainPage_leader_schedule(user_id):
    dbConnect = sql.SQLDatabase()
    result = sorted(dbConnect.get_schedule_event(user_id),key = lambda x: x[0])

    if len(result) == 0:
        return None
    else:
        selected_result = []

        #check if the schedule is expire, and sperate y/m/d with h:m
        i = 0
        while i<len(result):
            time = result[i][0]
            if time > str(now):
                daytime = result[i][0]
                event = result[i][1]
                day = daytime.split(" ")[0].replace("-","/")
                time = daytime.split(" ")[1]
                daytime_event_list = (day, time, event)
                selected_result.append(daytime_event_list)
            i+=1

        return selected_result


    #------------------------------------------------------------


def get_profile(user_id,identity):
    db = sql.SQLDatabase()
    result = db.getprofile(user_id,identity)

    return result

def editprofile(username,firstname,lastname,age,gender,birthday,email,location,mobile,business,company_name,company_size,user_id):
    db = sql.SQLDatabase()
    db.editprofile(username,firstname,lastname,age,gender,birthday,email,location,mobile,business,company_name,company_size,user_id)

#------------------------------------------------------------
"""Things for goals in learders' main page"""

"""Get all goals with all imformation splitted"""
def get_goals(user_id):
    db = sql.SQLDatabase()
    result = db.get_goals(user_id)
    goal_num = len(result)
    goals = []
    total_times = []
    progress = []
    ids = []
    for goal in result:
        goals.append(goal[0])
        total_times.append(goal[1])
        progress.append(goal[2])
        ids.append(goal[3])
    return goal_num, goals, total_times, progress, ids

def make_progress(user_id, goal_id):
    db = sql.SQLDatabase()
    result = db.make_progress(user_id, goal_id)

def add_new_goal(user_id, new_goal, new_times):
    db = sql.SQLDatabase()
    result = db.add_new_goal(user_id, new_goal, new_times)


#------------------------------------------------------------


def forgotPassword(username, password):
    dbConnect = sql.SQLDatabase()
    result = dbConnect.forgotPassword_handler(username, password)
    return result

def reset_check(username, email, fname, lname):
    dbConnect = sql.SQLDatabase()
    result = dbConnect.resetPassword_check(username, email, fname, lname)
    return result

#------------------------------------------------------------
def get_coachid(user_id):

    db = sql.SQLDatabase()
    return db.get_coachid(user_id)[0]
def get_userid_for_msg(leader_id):

    db = sql.SQLDatabase()
    return db.get_userid_for_msg(leader_id)[0]
# chat history
def get_chat_history(sender_id,receiver_id):
    db = sql.SQLDatabase()

    if receiver_id == sender_id:
        return "wrong chat ! cannot chat to yourself !"

    return db.get_chat_history(sender_id, receiver_id)

# chat from user side
def chat_fromuser(receiver_id, text, sender_id):

    db = sql.SQLDatabase()
    if sender_id != receiver_id:
        return db.send_message_user(receiver_id, sender_id, text)

    else:
        return "failed sending msg"
# chat from coach side
def chat_fromcoach(receiver_id, text, sender_id):

    db = sql.SQLDatabase()
    if sender_id != receiver_id:
        return db.send_message_coach(receiver_id, sender_id, text) #TODO *********

    else:
        return "failed sending msg"

#------------------------------------------------------------
""" Get the leaders' list for a coach """

def get_leaders_list(user_id):
    db = sql.SQLDatabase()
    result = db.get_leaders_list(user_id)
    return result

#------------------------------------------------------------

def get_coach_time(coach_id):
    db = sql.SQLDatabase()
    return db.get_coach_time(coach_id)

def pick_time(leader_id,start,end,date):

    coach_id = get_coachid(leader_id)
    db = sql.SQLDatabase()
    return db.pick_time(leader_id,coach_id,start,end,date)

#------------------------------------------------------------
"""
get username using user_id
"""
def get_username(user_id):
    db = sql.SQLDatabase()
    return db.get_username(user_id)[0]

#------------------------------------------------------------
"""
add token into blacklist
"""
def add_blacklist_token(token):
    db = sql.SQLDatabase()
    db.add_black_token(token)

#------------------------------------------------------------
"""
check if the token is not in the blacklist
True means the token is not in the blacklist
"""
def check_token(token):
    db = sql.SQLDatabase()
    result = db.check_token(token)
    return result

#------------------------------------------------------------
"""
Check the identity of given user_id
"""
def get_identify(user_id):
    db = sql.SQLDatabase()
    result = db.get_identify(user_id)
    if result == None:
        return None
    else:
        return result[0]

#------------------------------------------------------------
"""
JWT Auth_use: encode the user_id
Generates the Auth Token
return: string
"""
def encode_auth_token(user_id, app):
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=7, seconds=0),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256',
        )
    except Exception as e:
        return e
#------------------------------------------------------------
"""
Decodes the auth token
param: auth_token:
return: integer|string
"""

def decode_auth_token(auth_token, app):
    db = sql.SQLDatabase()
    black_list_check = db.check_token(auth_token)
    if not black_list_check:
        return False, "Please log in first."
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return True, payload['sub']
    except jwt.ExpiredSignatureError:
        return False, 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return False, 'Invalid token. Please log in again.'

#------------------------------------------------------------
"""
Functions about zoom link
"""

def get_zoom_key_sec(coach_id):

    db = sql.SQLDatabase()
    return db.get_zoom_key_sec(coach_id)

def generateToken(zoom_key,zoom_secert):
    token = jwt.encode({'iss': zoom_key, 'exp': time() + 5000},zoom_secert,algorithm='HS256')
    token1 = token.decode()#.lstrip("b")
    # print("gen1:",token1)
    return token1

#generateToken = generateToken(zoom_key,zoom_secert)

def getUser_id(generateToken):
    headers = {'authorization': 'Bearer %s' % generateToken,'content-type': 'application/json'}
    r = requests.get('https://api.zoom.us/v2/users/', headers=headers)
    users = json.loads(r.text)["users"]
    id_json = json.dumps(users[0])
    id = json.loads(id_json)["id"]
    return id

#zoom_user_id = getUsers_id(zoom_key,zoom_secert)


def meeting_json(start,end,date,zoom_user_id):
    start_time = date+" "+start+":00"
    end_time = date+" "+end+":00"
    start_time1 = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time1 = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    seconds_diff = (end_time1-start_time1).seconds
    duration = int(seconds_diff /60)
    print("duration: ",duration)
    start_date = date+"T"+start+":00"
    print("start_date: ",start_date)
    meetingdetails = {"topic": "The title",
                      "type": 2,
                      "start_time": start_date+"Z",
                      "duration": duration,
                      "schedule_for":zoom_user_id,
                      "timezone": "Australia/Sydney",
                      "agenda": "test",
                      "settings": {"host_video":False,
                                   "participant_video": True,
                                   "cn_meeting":True,
                                   "join_before_host": True,
                                   "jbh_time": 5,
                                   "mute_upon_entry": False,
                                   "watermark": True,
                                   "audio": "voip",
                                   "auto_recording": "cloud"
                                   }
                  }
    return meetingdetails

def create_meeting(gen,meetingdetails):
    headers = {'authorization': 'Bearer %s' % gen,'content-type': 'application/json'}
    r = requests.post(f'https://api.zoom.us/v2/users/me/meetings', headers=headers, data=json.dumps(meetingdetails))
    join_url = json.loads(r.text)["join_url"]

    return join_url
    # return (join_url)

def update_link(link,coach_id,start,end,date):
        db = sql.SQLDatabase()
        db.update_zoom_link(link,coach_id,start,end,date)
#------------------------------------------------------------
def add_time(user_id,start,end,date,event):

    db = sql.SQLDatabase()
    db.add_time(user_id,start,end,date,event)

def coachName():
    db = sql.SQLDatabase()
    result = db.info_coach()
    return result

def clientName():
    db = sql.SQLDatabase()
    result = db.info_client()
    return result

def deleteUser(username):
    db = sql.SQLDatabase()
    result = db.delete_user(username)
    return result

def addCoach(firstname, lastname, email, username, password, age, identity):
    db = sql.SQLDatabase()
    result = db.add_Coach(firstname, lastname, email, username, password, age, identity)
    if result:
        return result
    else:
        return False

def addClient(firstname, lastname, email, username, password, identity):
    db = sql.SQLDatabase()
    result = db.add_Client(firstname, lastname, email, username, password, identity)
    if result:
        return result
    else:
        return False

def get_all_goals():
    db = sql.SQLDatabase()
    result = db.get_all_goals()
    if result:
        return result
    else:
        return False

def get_all_industries():
    db = sql.SQLDatabase()
    result = db.get_all_industries()
    if result:
        return result
    else:
        return False

def EditCoachProfile(username,firstname,lastname,age,gender,email,mobile,experience,industry,goal1,goal2,goal3,user_id):
    db = sql.SQLDatabase()
    db.EditCoachProfile(username,firstname,lastname,age,gender,email,mobile,experience,industry,goal1,goal2,goal3,user_id)
