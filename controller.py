"""
Route management.

This provides all of the websites routes and handles what happens each
time a browser hits each of the paths. This serves as the interaction
between the browser and the database while rendering the HTML templates
to be displayed.

You will have to make
"""

# Importing the required packages
from flask import *
import model
from time import sleep
from datetime import datetime, timezone
import sqlite3
import werkzeug

# import database

# Initialise the application
app = Flask(__name__)
app.secret_key = """U29tZWJvZHkgb25jZSB0b2xkIG1lIFRoZSB3b3JsZCBpcyBnb25uYSBy
b2xsIG1lIEkgYWluJ3QgdGhlIHNoYXJwZXN0IHRvb2wgaW4gdGhlIHNoZWQgU2hlIHdhcyBsb29r
aW5nIGtpbmRhIGR1bWIgV2l0aCBoZXIgZmluZ2VyIGFuZCBoZXIgdGh1bWIK"""


#####################################################
#   INDEX
#####################################################


@app.route('/')
def introduction_page():
    """ Here is the route for introduction page """
    return render_template('landingPage.html')
    # page['title'] = 'User MainPage'
    #return "introduction page

@app.route('/coachApplication', methods = ["GET", "POST"])
def coachApplication():
    return render_template('coachApplication.html')

@app.route('/login', methods = ["GET","POST"])
def login_page():
    encode_user_id = request.cookies.get("user_id")
    is_login = model.decode_auth_token(encode_user_id, app)
    if is_login[0]:
        identity = model.get_identify(is_login[1])
        if identity == "Leader":
            resp = make_response(redirect(url_for('main_page')))
            return resp
        elif identity == "Coach":
            resp = make_response(redirect(url_for('coachMainPage')))
            return resp

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        result = model.login_check(username, password)
        if result:
            if result[1] == "Leader":
                resp = make_response(redirect(url_for('main_page')))
                encode_cookie = model.encode_auth_token(result[0], app)
                resp.set_cookie('user_id', encode_cookie)
                return resp
            elif result[1] == "Coach":
                resp = make_response(redirect(url_for('coachMainPage')))
                encode_cookie = model.encode_auth_token(result[0], app)
                print(type(encode_cookie))
                # encode_cookie = encode_cookie.encode('utf')
                resp.set_cookie('user_id', encode_cookie)
                return resp
            elif result[1] == "Admin":
                resp = make_response(redirect(url_for('admin')))
                encode_cookie = model.encode_auth_token(result[0], app)
                resp.set_cookie('user_id', encode_cookie)
                return resp
        else:
            flash("Incorrect username/password, please try again")
            return redirect(url_for('login_page'))
        # Remember to give a token for identification here
    else:
        return render_template('login.html')

@app.route('/forgotpassword', methods = ["GET", "POST"])
def forgotPassword_page():
    if request.method == "POST":
        username = request.form["username"]
        fname = request.form["firstname"]
        lname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["newPassword"]
        check = model.reset_check(username, email, fname, lname)
        if check:
            result = model.forgotPassword(username, password)
            return redirect(url_for('login_page'))
        else:
            flash("Account does not exists")
            return render_template("ForgotPassword.html")
    else:
        return render_template('ForgotPassword.html')

@app.route('/register', methods = ["GET","POST"])
def register_page():
    if request.method == "POST":
        fname = request.form["firstname"]
        lname = request.form["lastname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        gender = request.form["gender"]
        result = model.register_check(fname, lname, email, username, password, gender)
        if result:
            return redirect(url_for('login_page'))
        else:
            flash("The username already exists, please log in")
            return render_template('Register.html')
    else:
        return render_template('Register.html')

@app.route('/main')
@app.route('/main/<section>', methods = ['GET', 'POST'])
def main_page(section = None):
    encode_user_id = request.cookies.get("user_id")
    is_login = model.decode_auth_token(encode_user_id, app)
    identity = model.get_identify(is_login[1])

    if is_login[0] and identity == "Leader":
        user_id = is_login[1]
        username = model.get_username(user_id)
        if request.method == "POST":
            if request.form["form-name"] == "progress":
                goal_id = request.form["made-progress-button"]
                model.make_progress(user_id, goal_id)

            elif request.form["form-name"] == "new_goal":
                new_goal_content = request.form["new-goal-input"]
                new_goal_times = request.form["new-times-input"]
                model.add_new_goal(user_id, new_goal_content, new_goal_times)

        goal_results = model.get_goals(user_id)
        goal_num = goal_results[0]
        goals = goal_results[1]
        total_times = goal_results[2]
        progress = goal_results[3]
        ids= goal_results[4]
        maxgoals = 3

        session_results = model.mainPage_leader_schedule(user_id)
        return render_template('newhome.html',
                                username=username,
                                maxgoals=maxgoals,
                                goals=goals,
                                total_times=total_times,
                                goal_num=goal_num,
                                progress=progress,
                                ids=ids,
                                sessions = session_results)
    else:
        return redirect("/login")


@app.route('/findCoach')
def findCoachPage():
    return render_template('findCoachPage.html',
                            username = "xxx")

@app.route('/matching')
def matchingPage():
    return render_template('matching.html')


@app.route('/coachMain')
@app.route('/coachMain/<section>', methods = ['GET', 'POST'])
def coachMainPage(section=None):
    encode_user_id = request.cookies.get("user_id")
    is_login = model.decode_auth_token(encode_user_id, app)
    identity = model.get_identify(is_login[1])
    if is_login[0] and identity == "Coach":
        user_id = is_login[1]
        username = model.get_username(user_id)
        leaders_list = model.get_leaders_list(user_id)
        if request.method == "POST":
            if request.form["form-name"] == "leader_choice":
                leader_id = request.form["choosed_leader"]
                leader_goal_result = model.get_goals(leader_id)
                leader_goal_result_num = leader_goal_result[0]
                leader_goal_result_goals = leader_goal_result[1]
                leader_goal_result_total_times = leader_goal_result[2]
                leader_goal_result_progresses = leader_goal_result[3]

                leader_sessions_result = model.mainPage_leader_schedule(leader_id)
                next_session = ["No Appointment Yet", ""]
                if leader_sessions_result:
                    next_session = leader_sessions_result[0]


                sender = user_id
                result =  model.get_chat_history(sender,leader_id)
                hassent = 0

                return render_template("coachMain.html",
                                        username=username,
                                        leaders=leaders_list,
                                        goal_num = leader_goal_result_num,
                                        goal_names = leader_goal_result_goals,
                                        goal_total_times = leader_goal_result_total_times,
                                        goal_progresses = leader_goal_result_progresses,
                                        next_session = next_session,
                                        result=result,
                                        allmsg=len(result),
                                        hassent=hassent,
                                        choosed_leader_id = leader_id,
                                        board_display = True)
            # to check if msg --------------------------------
            elif request.form["form-name"] == "message":
                 # same as above ----------------------------
                leader_id = request.form["leader_id_msg"]
                leader_goal_result = model.get_goals(leader_id)
                leader_goal_result_num = leader_goal_result[0]
                leader_goal_result_goals = leader_goal_result[1]
                leader_goal_result_total_times = leader_goal_result[2]
                leader_goal_result_progresses = leader_goal_result[3]

                leader_sessions_result = model.mainPage_leader_schedule(leader_id)
                next_session = ["No Appointment Yet", ""]
                if leader_sessions_result:
                    next_session = leader_sessions_result[0]
                # ----------------------------------------------

                # print(sender)
                sender = user_id

                text = request.form['message']
                hassent = 1
                model.chat_fromcoach(leader_id, text, sender)
                result =  model.get_chat_history(sender,leader_id)



                return render_template("coachMain.html",
                                        username=username,
                                        leaders=leaders_list,
                                        goal_num = leader_goal_result_num,
                                        goal_names = leader_goal_result_goals,
                                        goal_total_times = leader_goal_result_total_times,
                                        goal_progresses = leader_goal_result_progresses,
                                        next_session = next_session,
                                        result=result,
                                        allmsg=len(result),
                                        hassent=hassent,
                                        choosed_leader_id = leader_id,
                                        board_display = True)

            elif request.form["form-name"] == "add_time":
                          start = request.form["start"]
                          end = request.form["end"]
                          date = request.form["addbutton"]
                          event = request.form["event"]
                          weekday = int(request.form["weekday"])
                          if weekday == 0:
                              weekday = 7
                          numdays = int(request.form["numdays"])
                          check1 = False
                          check2 = False
                          try:
                              a = request.form["check1"]
                              check1 = True
                          except werkzeug.exceptions.BadRequestKeyError as e:
                              pass
                          try:
                              a = request.form["check2"]
                              check2 = True
                          except werkzeug.exceptions.BadRequestKeyError as e:
                              pass
                          sh = int(start[0:-3])
                          eh = int(end[0:-3])

                          if eh > sh :
                              if check1:
                                  j = weekday+1
                                  while j < 8:
                                      diff = j-weekday
                                      daylist = date.split("-")
                                      daylist[0] = int(daylist[0])
                                      daylist[1] = int(daylist[1])
                                      daylist[2] = int(daylist[2])
                                      newday = daylist[2]+diff
                                      newyear = daylist[0]
                                      newmonth = daylist[1]
                                      if daylist[2]+diff > numdays:
                                          newday -= numdays
                                          newmonth = daylist[1]+1
                                          if daylist[1]+1 >12:
                                              newmonth -= 12
                                              newyear += 1
                                      newdate = "-".join([str(newyear),str(newmonth),str(newday)])
                                      i=0
                                      while i < eh-sh:
                                          try:
                                              newsta=str(sh+i)+":00"
                                              newend=str(sh+i+1)+":00"
                                              model.add_time(user_id,newsta,newend,newdate,event)
                                          except sqlite3.IntegrityError as e:
                                              pass
                                          i+=1
                                      j+=1
                              if check2:
                                  j = int(date.split("-")[2])+7
                                  while j <= numdays:
                                      newdate = "-".join(date.split("-")[0:2]+[str(j)])
                                      i=0
                                      while i < eh-sh:
                                          try:
                                              newsta=str(sh+i)+":00"
                                              newend=str(sh+i+1)+":00"
                                              model.add_time(user_id,newsta,newend,newdate,event)
                                          except sqlite3.IntegrityError as e:
                                              pass
                                          i+=1
                                      j+=7
                              i=0
                              while i < eh-sh:
                                  try:
                                      newsta=str(sh+i)+":00"
                                      newend=str(sh+i+1)+":00"
                                      model.add_time(user_id,newsta,newend,date,event)
                                  except sqlite3.IntegrityError as e:
                                      pass
                                  i+=1
                          coach_time = model.get_coach_time(user_id)

                          sender = user_id
                          receiver = model.get_userid_for_msg(user_id)
                          result =  model.get_chat_history(sender,receiver)
                          hassent = 0
                          print(date)
                          return render_template("coachMain.html",
                                                  username=username,
                                                  leaders=leaders_list,
                                                  goal_num = 0,
                                                  next_session = ["", ""],
                                                  result=result,
                                                  allmsg=len(result),
                                                  hassent=hassent,
                                                  choosed_leader_id = None,
                                                  board_display = False,
                                                  coach_time = coach_time,
                                                  date=date)

        else:
            # encode_user_id = request.cookies.get("user_id")
            # user_id = model.decode_auth_token(encode_user_id, app)
            # username = model.get_username(user_id)

            sender = user_id
            receiver = model.get_userid_for_msg(user_id)
            result =  model.get_chat_history(sender,receiver)
            hassent = 0
            coach_time = model.get_coach_time(user_id)

            return render_template("coachMain.html",
                                    username=username,
                                    leaders=leaders_list,
                                    goal_num = 0,
                                    next_session = ["", ""],
                                    result=result,
                                    allmsg=len(result),
                                    hassent=hassent,
                                    choosed_leader_id = None,
                                    board_display = False,
                                    coach_time = coach_time,
                                    date = " ")
    else:
        return redirect("/login")


@app.route('/profile')
def profilepage():
    encode_user_id = request.cookies.get("user_id")
    is_login = model.decode_auth_token(encode_user_id, app)
    identity = model.get_identify(is_login[1])
    if is_login[0]:
        user_id = is_login[1]
        profile = model.get_profile(user_id,identity)
        if identity == "Leader":
            return render_template('profile.html', profile = profile)
        elif identity == "Coach":
            return render_template('coachprofile.html', profile = profile)
    else:
        return redirect("/login")

@app.route('/editprofile', methods = ['GET','POST'])
def editprofile():
    encode_user_id = request.cookies.get("user_id")
    is_login = model.decode_auth_token(encode_user_id, app)
    identity = model.get_identify(is_login[1])
    if is_login[0]:
        user_id = is_login[1]
        if request.method == 'GET':
            profile = model.get_profile(user_id,identity)
            if identity == "Leader":
                return render_template('editprofile.html', profile = profile)
            elif identity == "Coach":
                goallist = model.get_all_goals()
                industrylist = model.get_all_industries()
                return render_template('EditCoachProfile.html', profile = profile,goallist=goallist,industrylist=industrylist)
        elif request.method == 'POST':
            username = request.form["username"]
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            age = request.form["age"]
            gender = request.form["gender"]
            email = request.form["email"]
            mobile = request.form["mobile"]
            if identity == "Leader":
                birthday = request.form["birthday"]
                location = request.form["location"]
                business = request.form["business"]
                company_name = request.form["company_name"]
                company_size = request.form["company_size"]
                jwt_key = request.form["jwt_key"]
                jwt_sec = request.form["jwt_sec"]
                model.editprofile(username,firstname,lastname,age,gender,birthday,email,location,mobile,business,company_name,company_size,user_id)
                profile = model.get_profile(user_id, identity)
                return render_template('editprofile.html', profile = profile, user_id = user_id)
            elif identity == "Coach":
                experience = request.form["experience"]
                industry = request.form["industry"]
                goal1 = request.form["goal1"]
                goal2 = request.form["goal2"]
                goal3 = request.form["goal3"]
                model.EditCoachProfile(username,firstname,lastname,age,gender,email,mobile,experience,industry,goal1,goal2,goal3,user_id)
                profile = model.get_profile(user_id,identity)
                goallist = model.get_all_goals()
                industrylist = model.get_all_industries()
                return render_template('EditCoachProfile.html', profile = profile,goallist=goallist,industrylist=industrylist)



@app.route('/evidencebasedcoach')
def evidencbasedcoach():
    return render_template('evidencebasedcoach.html')
@app.route('/feedback')
def feedback():
    encode_user_id = request.cookies.get("user_id")
    is_login = model.decode_auth_token(encode_user_id, app)
    identity = model.get_identify(is_login[1])
    user_id = is_login[1]


    if is_login[0] and identity == "Leader":
        return render_template('feedback.html')
    elif is_login[0] and identity == "Coach":
        leaders = model.get_leaders_list(user_id)
        leader_len = len(leaders)
        # feedback from leaders
        # feedback = ...a list... and put in render

        return render_template('feedback_coach.html',leaders=leaders, leader_len=leader_len)

@app.route('/assessment')
def assessment():
    return render_template('assessment.html', leaders=leaders)


#chat
@app.route('/yourcoach', methods = ["GET","POST"])
def chat():
    encode_user_id = request.cookies.get("user_id")
    decode_result = model.decode_auth_token(encode_user_id, app)
    identity = model.get_identify(decode_result[1])
    if decode_result[0] and identity == "Leader":
        user_id = decode_result[1]
        username = model.get_username(user_id)
        if request.method == 'GET':
            sender = user_id
            receiver = model.get_coachid(user_id)

            coach_time = model.get_coach_time(model.get_coachid(user_id))
            result =  model.get_chat_history(sender,receiver)
            date=' '
            hassent = 0
            return render_template('your_coach.html',result=result,allmsg=len(result),hassent=hassent,coach_time=coach_time,date=date)
        if request.method == 'POST':
            if request.form["form-name"] == "message":
                sender = user_id
                receiver = model.get_coachid(user_id)
                text = request.form['message']
                date = ' '
                coach_time = model.get_coach_time(model.get_coachid(user_id))
                # text = request.values()
                # print(text);
                # print("-----************")

                hassent =1
                model.chat_fromuser(receiver, text, sender)
                result =  model.get_chat_history(sender,receiver)
                return render_template('your_coach.html',result=result,allmsg=len(result),coach_time=coach_time,hassent=hassent,date=date)

            elif request.form["form-name"] == "pick_time":
                time = request.form['pick_button'].split(", ")
                start = time[0][1:-1]
                end = time[1][1:-1]
                date = time[2][1:-1]
                model.pick_time(user_id,start,end,date)
                coach_time = model.get_coach_time(model.get_coachid(user_id))

                sender = user_id
                receiver = model.get_coachid(user_id)
                result =  model.get_chat_history(sender,receiver)
                hassent = 0
                '''
                generate link
                '''
                coach_id = model.get_coachid(user_id)
                zoom_info = model.get_zoom_key_sec(coach_id)
                zoom_key = zoom_info[0]
                zoom_sec = zoom_info[1]
                print("zoom_key:",zoom_key)
                print("zoom_sec:",zoom_sec)
                gen=model.generateToken(zoom_key,zoom_sec)
                zoom_user_id = model.getUser_id(gen)
                meeting_detail = model.meeting_json(start,end,date,zoom_user_id)
                meeting_link = model.create_meeting(gen,meeting_detail)
                print(meeting_link)
                model.update_link(meeting_link,coach_id,start,end,date)
                return render_template('your_coach.html',result=result,allmsg=len(result),coach_time=coach_time,hassent=hassent,date=date)
    else:
        return redirect("/login")

@app.route('/logout', methods = ["GET","POST"])
def logout():
    encode_user_id = request.cookies.get("user_id")
    decode_result = model.decode_auth_token(encode_user_id, app)
    if decode_result[0]:
        model.add_blacklist_token(encode_user_id)
        return redirect("/")
    else:
        return redirect("/login")


@app.route('/admin')
@app.route('/admin/<section>', methods=['GET','POST'])
def admin(section = None):
    coachInfo = model.coachName()
    clientInfo = model.clientName()
    if request.method == 'POST':
        username = request.form["choosed_user"]
        result = model.deleteUser(username)
        if result:
            return redirect(url_for("admin"))

    return render_template('admin.html', coachInfo = coachInfo, clientInfo = clientInfo)

@app.route('/admin/addNewCoach', methods=['GET', 'POST'])
def adminAddCoach():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        age = request.form["age"]
        result = model.addCoach(firstname, lastname, email, username, password, age, "Coach")
        if result:
            return redirect(url_for("admin"))
        else:
            flash("The username already exists")
            return render_template('admin.html')
    return render_template('admin.html')

@app.route('/admin/addNewClient', methods=['GET', 'POST'])
def adminAddClient():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        result = model.addClient(firstname, lastname, email, username, password, "Leader")
        if result:
            return redirect(url_for("admin"))
        else:
            flash("The username already exists")
            return render_template('admin.html')
    return render_template('admin.html')
