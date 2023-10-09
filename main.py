from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.toast import toast
from kivy.app import App
from kivymd.uix.button import MDIconButton,MDFlatButton,MDFloatingActionButton,MDTextButton
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen,NoTransition
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.image import Image
from datetime import date
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.textfield import MDTextFieldRect,MDTextField
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import TwoLineListItem,MDList
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.spinner import Spinner
import re,pickle,socket,json
from kivymd.uix.dialog import MDDialog
from kivy.uix.button import Button
from kivy.metrics import dp




Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"


with open("data.json") as jf:
    ip_file = json.load(jf)

IP = ip_file["IP"]
PORT = ip_file["PORT"]
HEADER = 4096







class data():
    def __init__(self,**kwargs):
        self.id = None
        self.name = None
        self.email =None
        self.design =None
        self.num = None
        self.DOB = None
        self.l_name=None
        self._nfc_num =None
        self._pass = None

    def set_data(self,_id,_name,_email,_num,_DOB,_design):
        self.id = _id
        self.name = _name
        self.email = _email        
        self.num = _num
        self.DOB = _DOB
        self.design =_design

# this method for update users class only in admin
    def set_data_for_users(self,f_name,l_name,_email,_num,_pass,_nfc_num):
        self.name = f_name
        self.l_name =l_name
        self.email = _email        
        self.num = _num
        self._pass = _pass
        self._nfc_num =_nfc_num

    def set_id(self,id):
        self.id = id

    def set_empty(self):
        self.id = ""
        self.name =""
        
        self.email = ""        
        self.num = ""
        self.DOB = ""
        self.design =""







Builder.load_file('login.kv')

################################################# 101 first _screen


class LoginScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

        self.img_box =BoxLayout(
            orientation= 'vertical',
            size_hint= (0.5,0.25),
            pos_hint={'center_x':0.5,'center_y':0.85},
            )
        self.logo =   Image(
                source=r"logo.png")
        self.img_box.add_widget(self.logo)

        self.box=BoxLayout(
            orientation= 'vertical',
            size_hint= (0.75,0.75),
            pos_hint={'center_x':0.6,'center_y':0.6},
            spacing = 10,
            # height=250,
            # width =200
            )
            
        self.email_field =MDTextField(
                hint_text="Email",
                multiline=False,
                font_size=30,
                # width=200,
                pos_hint={'center_x':0.5,'center_y':0.7},
                height=18,
                size_hint= (0.6,0.1))
                
        # self.email_field.bind(focus =self.on_focus)
        self.password_field =MDTextField(
                hint_text="password",
                multiline=False,
                font_size=30,
                password=True,
                pos_hint={'center_x':0.5,'center_y':0.6},
                size_hint= (0.6,0.1),
                # width=200,
                height=18)
        # self.password_field.bind(focus =self.on_focus)
        self.login_btn=  Button(
                text='Login',
                font_size='18sp',
                size_hint=(None,None),
                size=(200,50),
                # pos_hint={'center_x':0.5,'center_y':0.5},
                background_color=(0,0,1,1),
                on_release=self.connect)
        self.signUp_btn=  Button(
            text='SignUP',
            font_size='18sp',
            size_hint=(None,None),
            size=(200,50),
            # pos_hint={'center_x':0.5,'center_y':0.4},
            background_color=(0,0,1,1),
            on_release=self.sign_up)
        self.forgot_pass_btn =MDTextButton(
                text='forgot password',
                font_size='18sp',
                size_hint=(None,None),
                size=(200,50),
                italic=True,
                # pos_hint={'center_x':0.5,'center_y':0.3},
                underline=True,
                on_release=self.forgot_pass)
        self.add_widget(self.img_box)
        self.add_widget(self.email_field)
        self.add_widget(self.password_field)
        self.box.add_widget(self.login_btn)
        self.box.add_widget(self.signUp_btn)
        self.box.add_widget(self.forgot_pass_btn)

        
        self.add_widget(self.box)


    def on_focus(self,instance,value):
        if value:
            # When the TextInput gains focus, move the layout up
            self.size_hint_y = 0.6
            self.pos_hint={"center_x":0.5,"center_y":0.35}
        else:
            # When the TextInput loses focus, reset the layout position
            self.size_hint_y = 1
            self.pos_hint={"center_x":0.5,"center_y":0.5}



    
    def connect(self,event):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        
        email = self.email_field.text
        password = self.password_field.text
        
        


        if email=="" or password=="":
            toast("blank")
            return
        elif self.check_cred(email,password)==0:
            toast("Invalid email or password")
            return
        else:
            result = self.all_data(email,password)
            app._data.set_data(_id=result[0],
                               _name=result[1],
                               _email=result[2],
                               _num=result[3],
                               _DOB=result[4],
                               _design=result[5])
            if self.is_admin():
                self.email_field.set_text(None,"")
                self.password_field.set_text(None,"")

                currentScreen = app.screenManager.current_screen
                app.remove_scr(f"{currentScreen.name}")
                
                app.add_scr("Main_admin")
                app.screenManager.current = 'Main_admin'

            else:

                self.email_field.set_text(None,"")
                self.password_field.set_text(None,"")

                currentScreen = app.screenManager.current_screen
                app.remove_scr(f"{currentScreen.name}")

                app.add_scr("after_login")
                app.screenManager.current = 'after_login'
                
 
    
            
        
 
    def sign_up(self,event):
        app = App.get_running_app()
        currentScreen = app.screenManager.current_screen
        app.remove_scr(f"{currentScreen.name}")
        
        app.add_scr("sign_up")
        app.screenManager.current = 'sign_up'

 
 
 
 
    def forgot_pass(self,event):
        app = App.get_running_app()
        currentScreen = app.screenManager.current_screen
        app.remove_scr(f"{currentScreen.name}")
        
        app.add_scr("forgot_pass")
        app.screenManager.current = 'forgot_pass'




    
    def check_cred(self,_email,_pass):
        app = App.get_running_app()

        msg =pickle.dumps(["cred",_email,_pass])
        app.client.send(msg)
        data = app.client.recv(HEADER)
         
        return pickle.loads(data)





    def is_admin(self):
        app = App.get_running_app()
        if app._data.design == "admin":
            return True
        return False
    
 
 
 
    def all_data(self,_email,_pass):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return
            
        temp_list = ["all",_email,_pass]
        print(temp_list)
        msg =pickle.dumps(temp_list)
        app.client.send(msg)
        print("msg sent")
        data = app.client.recv(HEADER)
        
        return pickle.loads(data)
        


days ={
    1 :"MONDAY",
    2 :"TUESDAY",
    3 :"WEDNESDAY",
    4 :"THURSDAY",
    5 :"FRIDAY",
    6 :"SATURDAY",
    7 :"SUNDAY"
}



#################################################  101 sign_up
#################################################  







#################################################  101 user cmds
#################################################  






class user_cmds:

    
    def status(self):

        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("status")
        app.screenManager.current = "status"

       
    



    def check_hour(self):
        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("check_hours")
        app.screenManager.current = "check_hours" 
    


    def after_login(self):
        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("after_login")
        app.screenManager.current = "after_login"




    def logOut(self):
        app = App.get_running_app()
        app._data.set_empty()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("login")
        app.screenManager.current = "login"




############################################### 101userlogin
############################################### 




class user_login(user_cmds,Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

 
        app = App.get_running_app()
        box= MDBoxLayout(orientation= "vertical",spacing =30,
                          size_hint=(None,None),
                          pos_hint={'center_x':0.5,'center_y':0.3})

        name=Label(text=f"Name:{app._data.name}",color= (0,0,0,1)
        )
        email= Label(text=f"Email:{app._data.email}",color= (0,0,0,1))
        num = Label(text=f"Number:{app._data.num}",color= (0,0,0,1))
        birth = Label(text=f"DOB:{app._data.DOB}",color= (0,0,0,1))
        box.add_widget(name)
        box.add_widget(email)
        box.add_widget(num)
        box.add_widget(birth)
        self.ids.label_scr.add_widget(box)




    


#################################################### 101  check_hours


class check_hour(user_cmds,Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
 
        app = App.get_running_app()
        # screen =app.hr_scr.ids.table_box
        
        
        
        
        
        
         
        today_hr = self.tod_hr()[0]
        



        mon_hr = self.month_hr()[0]
        


        mon_hr_lab = Label(text=f"Month hours:{mon_hr}",color= (0,0,0,1))
        today_hr_obj = Label(text=f"Today's hour:{today_hr}",color= (0,0,0,1))
        layout = BoxLayout(orientation = "vertical",
                           size_hint =(None,None),
                           spacing=10,
                           pos_hint={'center_x':0.5,'center_y':0.8},)
        
        if mon_hr:
            layout.add_widget(mon_hr_lab)
        if today_hr:
            layout.add_widget(today_hr_obj)

        self.ids.table_box.add_widget(layout)

        
        result = self.month_data()
        
        table = MDDataTable(
            size_hint=(1, 0.75),
            background_color=(0,0,0,1),
            pos_hint={'center_x':0.5,'center_y':0.35},
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("Date", dp(18)),
                ("Time", dp(15)),
                ("Day", dp(16)),
                ("Status", dp(17)),
            ],
            row_data=result,
        )
        
     
        
        # screen.add_widget(table)
        self.ids.table_box.add_widget(table)






    def month_data(self):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        _year ,_mon =date.today().strftime('%Y-%m').split("-")
        msg =pickle.dumps(["mon_data",app._data.id,_mon])
        app.client.send(msg)
        data = app.client.recv(HEADER)

        return pickle.loads(data)
    






    def tod_hr(self):
        app = App.get_running_app()
        

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        Date = date.today().strftime('%Y-%m-%d')
        msg =pickle.dumps(["tod_hr",app._data.id,Date])
        app.client.send(msg)
        data = app.client.recv(HEADER)

        return pickle.loads(data)
    




    def month_hr(self):
        
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        _year ,_mon =date.today().strftime('%Y-%m').split("-")
        msg =pickle.dumps(["mon_hr",app._data.id,_mon])
        app.client.send(msg)
        data = app.client.recv(HEADER)

        return pickle.loads(data)

    




###########################################   101status
###########################################




class status(user_cmds,Screen):
    


    

    
        
    def checkIn(self):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return
        status = "Check In"



        msg = pickle.dumps([status,app._data.id,app._data.name])
        app.client.send(msg)
        data = app.client.recv(HEADER)
        info = pickle.loads(data)

        toast(info)
        return

       




    def checkOut(self):

        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return
        status = "Check Out"
        msg = pickle.dumps([status,app._data.id,app._data.name])
        app.client.send(msg)
        data = app.client.recv(HEADER)
        info = pickle.loads(data)
        toast(info)
        return

           
    
        



##################################################   101 forgot password
##################################################   




class forgot_pass(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.code = None
        self.sub_code_btn = None
        self.code_field = None
        self._pass =None
        self.cnf_pass = None
        self.set_pass_btn =None
        self.email_for_pass= None

        
        self.box = MDBoxLayout(
            orientation = "vertical",
            size_hint=(0.75,0.65),
            pos_hint={'center_x':0.5,'center_y':0.7},
            spacing=10,
            width=200
        )
        self.img = Image(source=r"logo.png")
        self.box.add_widget(self.img)

        self.email =MDTextField(
                hint_text="Email",
                multiline=False,
                font_size=30,
                height=30,
                size_hint= (1,None))
        
        self.submit_btn = MDFlatButton(text="Submit",
                                    size_hint= (None,None),
                                    on_release=self.submit_click,
                                    width = 200,
                                    md_bg_color = (0, 0, 1, 0.75),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1)
                                   
                                    )
        
        self.box.add_widget(self.email)
        self.box.add_widget(self.submit_btn)
        # self.scatter.add_widget(self.box)

        self.add_widget(self.box)

        

        self.login_box = MDBoxLayout(
            orientation = "vertical",
            size_hint=(None,None),
            pos_hint={'center_x':0.2,'center_y':0.95},
        )
        self.login_btn = MDFloatingActionButton(
                icon="login",
                type="standard",
                theme_icon_color="Custom",
                md_bg_color="#4075e6",
                icon_color="#211c29",
                on_release = self.login_func
            )
        self.login_box.add_widget(self.login_btn)


        
        self.add_widget(self.login_box)

    def login_func(self,event):
        app = App.get_running_app()
        currentScreen = app.screenManager.current_screen
        app.remove_scr(f"{currentScreen.name}")

        app.add_scr("login")
        app.screenManager.current = 'login'



    def check_email_in_data(self,_email):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        msg = pickle.dumps(["check_email_in_data",_email])
        app.client.send(msg)
        data = app.client.recv(HEADER)
        return pickle.loads(data)
        




    def submit_click(self,event):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return
        email = self.email.text

        if email=="":
            toast("please enter the email")
            return
        elif not self.check_email_in_data(email):
            toast('this Email is not exist in data')
            return
        

        temp_list= self.sent_mail(email)
        if temp_list[0]:
            self.code = temp_list[1]
            toast("Email has sent to you")
            self.email_for_pass = email
            self.create_code_field()

       
    def sent_mail(self,email):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        msg = pickle.dumps(["sent_mail",email])
        app.client.send(msg)
        data = app.client.recv(HEADER)
        return pickle.loads(data)
        
        
        
    def create_code_field(self):
        self.box.remove_widget(self.email)
        self.box.remove_widget(self.submit_btn)
        
        self.code_field=MDTextField(
                hint_text="Code",
                multiline=False,
                font_size=30,
                height=30,
                size_hint= (1,None))
        
        
        self.sub_code_btn  = MDFlatButton(text="Submit",
                                    size_hint= (None,None),
                                    on_release=self.sub_on_code,
                                    width = 200,
                                    md_bg_color = (0, 0, 1, 0.75),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1)
                                   
                                    )
        self.box.add_widget(self.code_field)
        self.box.add_widget(self.sub_code_btn)
        
    def sub_on_code(self,event):
        code = self.code_field.text

        if code =="":
            toast("please enter the code")
            return
        elif len(code)!=4:
            toast("code has 4 alpha digits")
            return
        elif code ==self.code:
            
            self.create_pass_field()
        else:
            toast('you entered wrong code ')
            return

    def create_pass_field(self):
        self.box.remove_widget(self.code_field)
        self.box.remove_widget(self.sub_code_btn)

        
        
        self._pass=MDTextField(
                hint_text="Password",
                multiline=False,
                font_size=30,
                width=200,
                height=30,
                password=True,
                size_hint= (1,None))
        
        self.cnf_pass=MDTextField(
                hint_text="Confirm Password",
                multiline=False,
                font_size=30,
                width=200,
                height=30,
                password=True,
                size_hint= (1,None))
        
        
        self.set_pass_btn  = MDFlatButton(text="Submit",
                                    size_hint= (None,None),
                                    on_release=self.sub_pass,
                                    width = 200,
                                    md_bg_color = (0, 0, 1, 0.75),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1)
                                   
                                    )
        self.box.add_widget(self._pass)
        self.box.add_widget(self.cnf_pass)
        self.box.add_widget(self.set_pass_btn)

            
    def sub_pass(self,event):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        _pass = self._pass.text
        cnf_pass = self.cnf_pass.text

        if _pass=="" or cnf_pass =="":
            toast("please! fill the both fields")
            return
        elif _pass!=cnf_pass:
            toast("please enter the same password")
            return
        elif len(_pass)<8:
            toast("please enter 8 characters")
            return
        else:
            msg = pickle.dumps(['set_pass',_pass,self.email_for_pass])
            app.client.send(msg)
            
            toast("Successfully Updated")
            self.login_func(event)





##################################################   101 admin cmds
##################################################   






class extra():


    def update_users(self,event):

        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("update_users")
        app.screenManager.current = "update_users"


    def logOut(self):
        app = App.get_running_app()
        app._data.set_empty()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("login")
        app.screenManager.current = "login"

    
    def AddNew(self):
        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("AddNew")
        app.screenManager.current = "AddNew"
        

    def Remove(self):
        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("Remove")
        app.screenManager.current = "Remove"

    def Users(self):
        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("Users")
        app.screenManager.current = "Users"

    def Mon_hr(self):
        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("Mon_hr")
        app.screenManager.current = "Mon_hr"

    # def daily_hr(self):
    #     app = App.get_running_app()
    #     current_screen = app.screenManager.current_screen
    #     app.remove_scr(f"{current_screen.name}")
    #     app.add_scr("daily_hr")
    #     app.screenManager.current = "daily_hr"

    def Balance_sheet(self):
        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("balance_sheet")
        app.screenManager.current = "balance_sheet"

    def Main(self):
        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("Main_admin")
        app.screenManager.current = "Main_admin"

    def user_manage(self):
        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("user_manage")
        app.screenManager.current = "user_manage"

    def time_manage(self):
        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("time_manage")
        app.screenManager.current = "time_manage"

    def company_manage(self):
        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("company_manage")
        app.screenManager.current = "company_manage"




######################################################  101 main Admin
######################################################  





class Main_admin(extra,Screen):
    

    def __init__(self, **kw):
        super().__init__(**kw)
        

        box = MDBoxLayout(
            orientation = "vertical",
            size_hint=(1,0.25),
            pos_hint={'center_x':0.5,'center_y':0.3},
            spacing =10
            
        )
        
        temp_list = self.starting_title()

        total_box = MDBoxLayout(orientation="vertical",size_hint=(0.75,1),pos_hint={"center_x":0.5})
        total_label = MDLabel(text=f"Total Emp:{temp_list[0]}",theme_text_color="Custom",halign="center",
                              text_color=(1,1,1,1),font_style="H6",size_hint=(0.75,1),pos_hint={"center_x":0.5}) 
        total_label.md_bg_color = (1,169/255,164/255,1)
        total_box.add_widget(total_label)
        total_box.md_bg_color=(0,0,1,0.75)
        total_box.radius=[20,20,20,20]

        pre_label_box = MDBoxLayout(orientation="vertical",size_hint=(0.75,1),pos_hint={"center_x":0.5})
        pre_label = MDLabel(text=f"Present Emp:{temp_list[1]}",theme_text_color="Custom",halign="center",
                              text_color=(1,1,1,1),font_style="H5",size_hint=(0.75,1),pos_hint={"center_x":0.5})
        pre_label.md_bg_color = (158/255, 231/255, 238/255, 1)# hue colour
        pre_label_box.add_widget(pre_label)
        pre_label_box.md_bg_color=(0,0,1,0.75)
        pre_label_box.radius=[20,20,20,20]


        abs_label_box = MDBoxLayout(orientation="vertical",size_hint=(0.75,1),pos_hint={"center_x":0.5})
        absent_label = MDLabel(text=f"Absent Emp:{temp_list[2]}",theme_text_color="Custom",halign="center",
                              text_color=(1,1,1,1),font_style="H5",size_hint=(0.75,1),pos_hint={"center_x":0.5})
        absent_label.md_bg_color = (0,178/255,1,1)#sky blue
        abs_label_box.add_widget(absent_label)
        abs_label_box.md_bg_color=(0,0,1,0.75)
        abs_label_box.radius=[20,20,20,20]

        cur_label_box = MDBoxLayout(orientation="vertical",size_hint=(0.75,1),pos_hint={"center_x":0.5})
        curr_bal = MDLabel(text=f"Balance:  {temp_list[3]}",theme_text_color="Custom",halign="center",
                              text_color=(1,1,1,1),font_style="H5",size_hint=(0.75,1),pos_hint={"center_x":0.5})
        curr_bal.md_bg_color = (0,1,0,0.8)#bright green
        cur_label_box.add_widget(curr_bal)
        cur_label_box.md_bg_color=(0,0,1,0.75)
        cur_label_box.radius=[20,20,20,20]

        box.add_widget(cur_label_box)
        box.add_widget(total_box)
        box.add_widget(pre_label_box)
        box.add_widget(abs_label_box)




        self.ids.main_admin_scr.add_widget(box)

    def starting_title(self):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        msg = pickle.dumps(['start_title'])
        app.client.send(msg)
        data = app.client.recv(HEADER)
        info = pickle.loads(data)
        return info

    
    
########################################################## 101 user management

class user_manage(extra,Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass


############################################################ 101 time_manage

class time_manage(extra,Screen):
    pass





#############################################################101 company_manage
class company_manage(extra,Screen):
    pass





#############################################################101 update_user_screen
class update_users(extra,Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.scrol_view = MDScrollView(size_hint=(1, 0.85),pos_hint={'center_x': 0.5,'center_y':0.5})

        self.md_list = MDList()
        temp_list = self.fetch_data()
        

        for i in temp_list:
            self.md_list.add_widget(
                TwoLineListItem(text=f"Name: {i[1]} {i[2]}",
                                secondary_text= f"Id:{i[0]}",
                                on_release =self.func,bg_color=(0,0.1,0.5,0.5))
            )

        self.scrol_view.add_widget(self.md_list)

        self.ids.update_users.add_widget(self.scrol_view)

    def fetch_data(self):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return
        # msg = pickle.dumps(["without_nfc_users"])
        # client.send(msg)
        # data = client.recv(HEADER)
        # return pickle.loads(data)
    
        msg = pickle.dumps(["users_data"])
        app.client.send(msg)
        data = app.client.recv(HEADER)

        return pickle.loads(data)
    

    def func(self,event):
        
        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("update_user_fields")
        app.screenManager.current = "update_user_fields"
        current_screen = app.screenManager.current_screen
        str1,id = event.secondary_text.split(':')
        app.update_user_fields.user_data.id=id
        app.update_user_fields.fetch_data()
        app.update_user_fields.cr_fields()








######################################################### 101 update_usr_field


class update_user_fields(extra,Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.user_data = data()
        
        self.f_name = None
        self.l_name = None
        self.email = None 
        self.cell_no = None
        self.password = None
        self.update_nfc_btn  = None
        


    def cr_fields(self):
        field_height = dp(40)
        font_size = 20
        # scatter = Scatter(do_rotation=False,size_hint=(1,1),pos_hint={"center_x":0.5,"center_y":0.5})
        image = Image(source ="logo.png")
        
        
        back_btn = MDIconButton(icon='arrow-left'
                                ,width = "50sp"
                                ,on_release = self.update_users
                                ,pos_hint ={"center_x":0.1,"center_y":0.9})
        self.add_widget(back_btn)


        box = MDBoxLayout(orientation="vertical",size_hint=(0.75,0.7)
                          ,pos_hint= {"center_x":0.5,"center_y":0.6},
                          spacing=10)
      
        self.f_name = MDTextFieldRect(multiline=False,size_hint= (1,None),text =self.user_data.name
                                        ,font_size= font_size,height=field_height,hint_text = "First Name")
        
        self.l_name = MDTextFieldRect(multiline =False,size_hint=(1,None),text =self.user_data.l_name
                                        ,font_size= font_size,height=field_height,hint_text = "Last Name")
     
        self.email = MDTextFieldRect(size_hint=(1,None),height=field_height,text =self.user_data.email
                                        ,font_size= font_size,multiline =False,hint_text = "Email")
       
        self.cell_no = MDTextFieldRect(size_hint=(1,None),height=field_height,text =self.user_data.num
                                        ,font_size= font_size,multiline =False,hint_text = "Cell No")
        
        self.password = MDTextFieldRect(size_hint=(1,None),height=field_height,text =self.user_data._pass
                                        ,font_size= font_size,multiline =False,hint_text = "Password")
        # nfc = Label(text=self.user_data._nfc_num)
        self.update_nfc_btn = MDFlatButton(text="Add Nfc",
                                            md_bg_color=(0,0,1,1),
                                            theme_text_color = "Custom",
                                            text_color=(1,1,1,1),
                                            size_hint=(0.5,None),
                                            on_release = self.add_nfc_call
                                            )
        box.add_widget(image)
        
        box.add_widget(self.f_name)
        
        box.add_widget(self.l_name)
    
        box.add_widget(self.email)
        
        box.add_widget(self.cell_no)
    
        box.add_widget(self.password)
        box.add_widget(self.update_nfc_btn)
        #adding box to the scatter
        # scatter.add_widget(box)
        # adding scatter to the screen
        self.add_widget(box)

        self.update_btn = MDFlatButton(text="Update",
                                        md_bg_color=(0,0,1,1),
                                        theme_text_color = "Custom",
                                        text_color=(1,1,1,1),
                                        size_hint=(0.5,None),
                                        pos_hint={"center_x":0.5,"center_y":0.15},
                                        on_release = self.update_call
                                        )
        self.add_widget(self.update_btn)

    def fetch_data(self):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        msg = pickle.dumps(["fetch_from_id",self.user_data.id])
        try:

            app.client.send(msg)
        except:
            toast('server offline')
            return
        
        data =app.client.recv(HEADER)
        temp_list = pickle.loads(data)
        print(temp_list)
        self.user_data.set_data_for_users(temp_list[0],temp_list[1],temp_list[2],temp_list[3],temp_list[4],temp_list[5])





    def update_call(self,event):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return
        f_name = self.f_name.text
        l_name =self.l_name.text
        email = self.email.text
        cell_no = self.cell_no.text
        password = self.password.text

        value_temp_list = list()
        var_temp_list = list()

        if f_name:
            value_temp_list.append(f_name.upper())
            var_temp_list.append("f_name")

        if l_name:
            value_temp_list.append(l_name.upper())
            var_temp_list.append("l_name")
            
        if email:
            value_temp_list.append(email)
            var_temp_list.append("email")

        if cell_no:
            try:
                cell= int(cell_no)
            except:
                toast("please fill the correct cell no")
                return
            var_temp_list.append(cell)
            var_temp_list.append("cell_no")

        if password:
            value_temp_list.append(password)
            var_temp_list.append("password")

        if not value_temp_list:
            toast("please fill any one for update")
            return
        print(var_temp_list,value_temp_list)
        
        msg = pickle.dumps(["update_fields",self.id,var_temp_list,value_temp_list])
        try:
            app.client.send(msg)
        except:
            toast("connection error!")
            return
        self.f_name.text=""
        self.l_name.text=""
        self.email.text=""
        self.cell_no.text=""
        self.password.text=""

        toast("updated successfully")



    def add_nfc_call(self,event):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        msg = pickle.dumps(["activate_nfc",self.user_data.id])
        app.client.send(msg)
        toast("request for NFC sent")
        data = app.client.recv(HEADER)
        check = pickle.loads(data)
        print(check)
        if check[0]:
            toast("nfc num updated successfully")
            return
        toast("some error during NFC UPDATION")










######################################################### 101 Add new






    
class Add_New(extra,Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.box = MDBoxLayout(
            
            orientation = "vertical",
            size_hint=(1,0.5),
            pos_hint={'center_x':0.5,'center_y':0.5},
            spacing=10,
            
        )
        
        # self.box.md_bg_color =(1,1,1,0.75)
       


        

        self.F_name_text = MDTextFieldRect(
                                    multiline=False,
                                    font_size=30,
                                    # width=200,
                                    height="40dp",
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "First Name",
                                    pos_hint={'center_x':0.5}
                                    )
        
        self.box.add_widget(self.F_name_text)

        self.L_name_text = MDTextFieldRect(
                                    multiline=False,
                                    font_size=30,
                                    # width=200,
                                    height="40dp",
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Last Name",
                                    pos_hint={'center_x':0.5}

                                    )
        
        self.box.add_widget(self.L_name_text)

        self.email_text = MDTextFieldRect(
                                    multiline=False,
                                    font_size=30,
                                    # width=200,
                                    height="40dp",
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Email",
                                    pos_hint={'center_x':0.5}
                                    )
        
        self.box.add_widget(self.email_text)


        self.Number_text = MDTextFieldRect(
                                    multiline=False,
                                    font_size=30,
                                    # width=200,
                                    height="40dp",
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Cell No",
                                    pos_hint={'center_x':0.5}
                                    )
        
        self.box.add_widget(self.Number_text)

        self.gender_text = Spinner(
            text='Gender',
            values=["MALE","FEMALE"],
            size_hint=(0.75,1),
            pos_hint={'center_x': 0.5,'center_y':0.5},
            sync_height = True,
            background_color=(0,178/255,1,1)
        )

        
        self.box.add_widget(self.gender_text)


        

        
        self.pass_text = MDTextFieldRect(
                                    multiline=False,
                                    font_size=30,
                                    # width=200,
                                    height="40dp",
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "password",
                                    password=True,
                                    pos_hint={'center_x':0.5}
                                    )
        
        self.box.add_widget(self.pass_text)

        self.cnf_pass_text = MDTextFieldRect(
                                    multiline=False,
                                    font_size=30,
                                    # width=200,
                                    height="40dp",
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "re_password",
                                    password=True,
                                    pos_hint={'center_x':0.5}
                                    )
        
        self.box.add_widget(self.cnf_pass_text)

        self.birth_date = MDTextFieldRect(
                                    multiline=False,
                                    font_size=30,
                                    # width=200,
                                    height="40dp",
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "yyy-mm-dd",
                                    pos_hint={'center_x':0.5}
                                    )
        
        self.box.add_widget(self.birth_date)

        

        
        self.submit_btn = MDFlatButton(text="submit",
                                    size_hint= (0.5,None),
                                    on_release =self.submit,
                                    md_bg_color = (0, 0, 1, 1),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1),
                                    pos_hint={'center_x':0.5,'center_y':0.1}
                                   
                                    )
        
        




        self.ids.add_new_scr.add_widget(self.box)
        self.ids.add_new_scr.add_widget(self.submit_btn)

    def show_date_picker(self,event):
    
        self.date_dialog.bind(on_save=self.on_save)
        
        
        self.date_dialog.open()
        

    def on_save(self,instance,value,date_range):
        

        self.birth_date._set_text(str(value))  
        


    
    
    def submit(self,event):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        f_name = self.F_name_text.text
        l_name = self.L_name_text.text 
        email =  self.email_text.text
        Number = self.Number_text.text
        gender = self.gender_text.text
        birth_date = self.birth_date.text
        _pass = self.pass_text.text
        cnf_pass = self.cnf_pass_text.text

        if f_name =="" or l_name =="" or email=="" or Number=="" or gender == "" or _pass=="" or cnf_pass=="" or birth_date =="":
            toast("Please fill all the fields")
        else:
            

            if self.check_email(email):
                toast("Invalid Email")
                return
            elif len(Number)>13 or len(Number)<11:
                toast("cell no must in 11-13  digits" )
                return
            elif _pass != cnf_pass:
                toast("please enter the same password")
                return
            
            elif len(_pass)>10:
                toast("please enter 10 or less than 10\n in password")
            else:
                try:
                    int(Number)
                except:
                    toast("Invalid Number!")
                    return
                
                msg = pickle.dumps(['add_new',f_name,l_name,email,Number,gender,birth_date,_pass])
                app.client.send(msg)
                data = app.client.recv(HEADER)
                info = pickle.loads(data)
                
                self.F_name_text.text = ""
                self.L_name_text.text = ""
                self.email_text.text = ""
                self.Number_text.text = ""
                self.gender_text.text = ""
                self.birth_date.text = ""
                self.pass_text.text = ""
                self.cnf_pass_text.text = ""

                toast(info)


                return
                



    def check_email(self,email):
 
        # pass the regular expression
        # and the string into the fullmatch() method
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        
        if(re.fullmatch(regex, email)):
            
            return False
    
        else:
            """INvalid mail"""
            return True




##################################################  101 sign_up
##################################################  


class sign_up(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.box = MDBoxLayout(
            
            orientation = "vertical",
            size_hint=(1,0.6),
            pos_hint={'center_x':0.5,'center_y':0.5},
            spacing=10,
            
        )
        font_size = 30
        field_height = 40
        
        # self.box.md_bg_color =(1,1,1,0.75)
       


        

        self.F_name_text = MDTextFieldRect(
                                    multiline=False,
                                    font_size=font_size,
                                    # width=200,
                                    height=field_height,
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "First Name",
                                    pos_hint={'center_x':0.5}
                                    )
        
        self.box.add_widget(self.F_name_text)

        self.L_name_text = MDTextFieldRect(
                                    multiline=False,
                                    font_size=font_size,
                                    # width=200,
                                    height=field_height,
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Last Name",
                                    pos_hint={'center_x':0.5}
                                    )
        
        self.box.add_widget(self.L_name_text)

        self.email_text = MDTextFieldRect(
                                    multiline=False,
                                    font_size=font_size,
                                    # width=200,
                                    height=field_height,
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Email",
                                    pos_hint={'center_x':0.5}
                                    )
        
        self.box.add_widget(self.email_text)


        self.Number_text = MDTextFieldRect(
                                    multiline=False,
                                    font_size=font_size,
                                    
                                    height=field_height,
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Cell No",
                                    pos_hint={'center_x':0.5}
                                    )
        
        self.box.add_widget(self.Number_text)

        self.gender_text = Spinner(
            text='Gender',
            values=["MALE","FEMALE"],
            size_hint=(0.75,1),
            pos_hint={'center_x': 0.5,'center_y':0.5},
            sync_height = True,
            background_color=(0,178/255,1,1)
        )

       
        
        
        self.box.add_widget(self.gender_text)


        



        
        self.pass_text = MDTextFieldRect(
                                    multiline=False,
                                    font_size=font_size,
                                    
                                    height=field_height,
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Password",
                                    password=True,
                                    pos_hint={'center_x':0.5}
                                    )
        
        self.box.add_widget(self.pass_text)

        self.cnf_pass_text = MDTextFieldRect(
                                    multiline=False,
                                    font_size=font_size,
                                
                                    height=field_height,
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Re Password",
                                    password=True,
                                    pos_hint={'center_x':0.5}
                                    )
        
        self.box.add_widget(self.cnf_pass_text)

        Date_box = MDBoxLayout(size_hint=(0.75,1),pos_hint={'center_x':0.5})


        self.birth_date = MDTextFieldRect(
                                    multiline=False,
                                    font_size=font_size,
                                    height=field_height,
                                    size_hint= (0.6,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Birth Date",
                                    disabled =True,
                                    pos_hint={'center_x':0.5}
                                    )
        
        Date_box.add_widget(self.birth_date)

        self.date_dialog = MDDatePicker(size_hint= (None,None),
                                        width=300,
                                        pos_hint={'center_x':0.5,'center_y':0.5},
                                        max_year =2005)


        self.dob_btn = MDFlatButton(text="click",
                                    size_hint= (0.1,None),
                                    on_release =self.show_date_picker,
                                    md_bg_color = (0, 0, 0, 0.5),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1)
                                   
                                    )
        
        Date_box.add_widget(self.dob_btn)

        self.box.add_widget(Date_box)


        self.box_btn = MDBoxLayout(orientation = "vertical",
                            size_hint=(1,None),
                            pos_hint={'center_x':0.5,'center_y':0.15},

        )

        self.submit_btn = MDFlatButton(text="submit",
                                    size_hint= (0.5,None),
                                    on_release =self.submit,
                                    md_bg_color = (0, 0, 1, 1),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1),
                                    pos_hint={'center_x':0.5}
                                   
                                    )
        
        self.box_btn.add_widget(self.submit_btn)


        self.box_log_btn = MDBoxLayout(orientation = "vertical",
                            size_hint=(None,None),
                            pos_hint={'center_x':0.8,'center_y':0.95},

        )
        self.login_btn = MDFlatButton(text="login",
                                    size_hint= (None,None),
                                    on_release = self.login_click,
                                    width = 200,
                                    md_bg_color = (0, 0, 1, 1),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1)
                                   
                                    )
        
        self.box_log_btn.add_widget(self.login_btn)

        self.img_box = MDBoxLayout(orientation = "vertical",
                            size_hint=(None,None),
                            pos_hint={'center_x':0.2,'center_y':0.9},

        )
        self.logo = Image(source=r"logo.png")
        
        self.img_box.add_widget(self.logo)


        self.add_widget(self.box_log_btn)
        self.add_widget(self.box)
        self.add_widget(self.box_btn)
        self.add_widget(self.img_box)

    def show_date_picker(self,event):
    
        self.date_dialog.bind(on_save=self.on_save)
        
        
        self.date_dialog.open()
        

    def on_save(self,instance,value,date_range):
        

        self.birth_date._set_text(str(value))  
        

    def login_click(self,event):
        app = App.get_running_app()
        currentScreen = app.screenManager.current_screen
        app.remove_scr(f"{currentScreen.name}")

        app.add_scr("login")
        app.screenManager.current = 'login'
    




    def submit(self,event):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        f_name = self.F_name_text.text
        l_name = self.L_name_text.text 
        email =  self.email_text.text
        Number = self.Number_text.text
        gender = self.gender_text.text
        birth_date = self.birth_date.text
        _pass = self.pass_text.text
        cnf_pass = self.cnf_pass_text.text

        if f_name =="" or l_name =="" or email=="" or Number=="" or gender == "" or _pass=="" or cnf_pass=="" or birth_date =="":
            toast("Please fill all the fields")
        else:
            

            if self.check_email(email):
                toast("Invalid Email")
                return
            elif len(Number)>13 or len(Number)<11:
                toast("cell no must in 11-13  digits" )
                return
            elif _pass != cnf_pass:
                toast("please enter the same password")
                return
            
            elif len(_pass)>10:
                toast("please enter 10 or less than 10\n in password")
            else:
                try:
                    int(Number)
                except:
                    toast("Invalid Number!")
                    return
                
                msg = pickle.dumps(['add_new',f_name,l_name,email,Number,gender,birth_date,_pass])
                app.client.send(msg)
                data = app.client.recv(HEADER)
                info = pickle.loads(data)
                
                self.F_name_text.text = ""
                self.L_name_text.text = ""
                self.email_text.text = ""
                self.Number_text.text = ""
                # self.gender_text.text = ""
                self.birth_date.text = ""
                self.pass_text.text = ""
                self.cnf_pass_text.text = ""

                toast(info)


                return
    
    


    
    

    def check_email(self,email):
 
        # pass the regular expression
        # and the string into the fullmatch() method
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        
        if(re.fullmatch(regex, email)):
            
            return False
    
        else:
            """INvalid mail"""
            return True
        



################################################101 remove_user
################################################




    
class Remove_scr(extra,Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.dialog =None

        self.box = MDBoxLayout(
            
            orientation = "vertical",
            size_hint=(None,None),
            pos_hint={'center_x':0.5,'center_y':0.4},
            spacing=20,
            height= 100,
            width =250
        )
        self.box.md_bg_color =(1,1,1,0.75)

        self.id_text = MDTextFieldRect(
                                    multiline=False,
                                    font_size=24,
                                    size_hint= (0.5,0.1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Enter Id",
                                    pos_hint={'center_x':0.5,'center_y':0.4}
                                    )
        
        self.ids.remove_scr.add_widget(self.id_text)

        self.remove_btn = MDFlatButton(text="Remove",
                                    size_hint= (0.5,None),
                                    on_release =self.show_alert_dialog,
                                    md_bg_color = (0, 0, 1, 1),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1),
                                    pos_hint={'center_x':0.5,'center_y':0.3}
                                   
                                    )
        

        self.ids.remove_scr.add_widget(self.remove_btn)
        # self.ids.remove_scr.add_widget(self.box)


    def rem_user(self,event):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        _id = self.id_text.text


        msg = pickle.dumps(["rem_usr",_id])
        app.client.send(msg)
        data = app.client.recv(HEADER)
        info = pickle.loads(data)

        
        self.cencel(event)
        self.id_text.text=""
        
        toast(info)
        
    
    def cencel(self,event):
        self.dialog.dismiss()

        # del self.dialog

    

        
    
    def show_alert_dialog(self,event):

        _id = self.id_text.text

        if _id=="":
            toast("please enter the Id:")
            return
        
        try:
            int(_id)
        except:
            toast('please enter the write Id')
            return

        
        self.dialog = MDDialog(
            text="Are You sure?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    md_bg_color = (0, 0, 1, 1),
                    theme_text_color= "Custom",
                    text_color=(1,1,1,1),
                    on_release=self.cencel
                ),
                MDFlatButton(
                    text="remove",
                    
                    md_bg_color = (0, 0, 1, 1),
                    theme_text_color= "Custom",
                    text_color=(1,1,1,1),
                    on_release = self.rem_user
                ),
            ],
        )
        self.dialog.open()
        
###################################################### 101 Users

class Users(extra,Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        
        
        
        
        
       
       
        emp = self.total_emp()
        
        

        total_lab = Label(text=f"Total Emp:{emp}",color= (0,0,0,1))
        
        layout = BoxLayout(orientation = "vertical",
                           size_hint =(None,None),
                           spacing=10,
                           pos_hint={'center_x':0.5,'center_y':0.85},)
        
        layout.add_widget(total_lab)
        
        self.ids.users_scr.add_widget(layout)

        temp_list = self.all_users()

        table = MDDataTable(
            size_hint=(1, 0.8),
            background_color=(0,0,0,1),
            pos_hint={'center_x':0.5,'center_y':0.4},
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("Id", dp(8)),
                ("Name", dp(16)),
                ("Email", dp(30)),
                ("Gender", dp(12)),
            ],
            row_data=temp_list,
        )
        # table.on_row_press= self.hassam
        # screen.add_widget(table)
        self.ids.users_scr.add_widget(table)

    
       

    def all_users(self):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        msg = pickle.dumps(["all_users"])
        app.client.send(msg)
        data = app.client.recv(HEADER)
        
        return pickle.loads(data)

    def total_emp(self):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return
            
        msg = pickle.dumps(["total_emp"])
        app.client.send(msg)
        data = app.client.recv(HEADER)

        return pickle.loads(data)
        




####################################################### 101 month_scr





class Month_scr(extra,Screen):
    
    def __init__(self, **kw):
        super().__init__(**kw)

        self.scrol_view = MDScrollView(size_hint=(1, 0.85),pos_hint={'center_x': 0.5,'center_y':0.5})

        self.md_list = MDList()
        temp_list = self.fetch_data()
        

        for i in temp_list:
            self.md_list.add_widget(
                TwoLineListItem(text=f"Name: {i[1]} {i[2]}",
                                secondary_text= f"Id:{i[0]}",
                                on_release =self.func)
            )

        self.scrol_view.add_widget(self.md_list)

        self.ids.month_scr.add_widget(self.scrol_view)

    def func(self,event):
        
        app = App.get_running_app()
        current_screen = app.screenManager.current_screen
        app.remove_scr(f"{current_screen.name}")
        app.add_scr("user_click")
        app.screenManager.current = "user_click"
        current_screen = app.screenManager.current_screen
        str1,id = event.secondary_text.split(':')
        app.admin_user_click.set_Id(int(id))
        app.admin_user_click.hassam()

    def fetch_data(self):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        msg = pickle.dumps(["users_data"])
        app.client.send(msg)
        data = app.client.recv(HEADER)

        return pickle.loads(data)
        



 
###################################################### 101 balance sheet


class Balance_sheet(extra,Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        
        
        self.table_expense = None
        self.table_income = None
        self.exp_table_box =None
        self.inc_table_box = None
        self.Date = None
        self.Desc = None
        self.Income = None
        self.expense = None
        self.add_btn = None
        self.two_btn_box = None
        self.curr_lab_box = None
        self.inc_field_box = None
        self.exp_field_box = None


        self.create_two_btn()
        self.curr_bal_lab()
        

    
    def curr_bal_lab(self):
        self.curr_lab_box= MDBoxLayout(orientation = "vertical",
                           size_hint =(1,0.1),
                           spacing=10,
                           pos_hint={'center_x':0.5,'center_y':0.8},)
        curr_bal = MDLabel(text=f"Balance:  {self.total_inc()-self.total_exp()}",theme_text_color="Custom",
                           text_color=(1,1,1,1),font_style="H4"
                            ,halign ="center")
        self.curr_lab_box.add_widget(curr_bal)

        self.curr_lab_box.md_bg_color=(0,1,0,0.8)
        self.curr_lab_box.radius = [25,25,25,25]
        
        self.ids.balance_scr.add_widget(self.curr_lab_box)

    def create_two_btn(self):
        self.two_btn_box =BoxLayout(orientation = "vertical",
                           size_hint =(1,0.5),
                           spacing= 20,
                           pos_hint={'center_x':0.5,'center_y':0.5},)
        

        expense_btn = MDFlatButton(text="Expense",
                                    size_hint= (0.5,None),
                                    on_release =self.create_table_expense,
                                    md_bg_color = (0, 0, 1, 1),
                                    theme_text_color= "Custom",
                                    pos_hint={'center_x':0.5,'center_y':0.45},
                                    text_color=(1,1,1,1)
                                   
                                    )
        
        income_btn = MDFlatButton(text="Income",
                                    size_hint= (0.5,None),
                                    on_release =self.create_table_income,
                                    md_bg_color = (0, 0, 1, 1),
                                    theme_text_color= "Custom",
                                    pos_hint={'center_x':0.5,'center_y':0.35},
                                    text_color=(1,1,1,1)
                                   
                                    )
        
        self.two_btn_box.add_widget(expense_btn)
        self.two_btn_box.add_widget(income_btn)

        self.ids.balance_scr.add_widget(self.two_btn_box)
        


    def create_table_expense(self,event):

        if self.two_btn_box:
            self.ids.balance_scr.remove_widget(self.two_btn_box)
        
        temp_list= self.expense_func()
        
        self.exp_table_box = MDBoxLayout(orientation = "vertical",
                           size_hint =(1,0.62),
                           spacing= 0,
                           pos_hint={'center_x':0.5,'center_y':0.59},)

        self.exp_table_box.line_color=(0,0,1,1)
        self.exp_table_box.md_bg_color = (1,1,1,0.75)

        self.table_expense = MDDataTable(
            size_hint=(1, 1),
            background_color=(0,0,0,1),
            pos_hint={'center_x':0.5,'center_y':0.1},
            use_pagination=True,
            rows_num = 7,
            column_data=[
                ("Date", dp(18)),
                ("Description", dp(30)),
                ("Expense", dp(16)),
            ],
            row_data=temp_list,
        )
        
        self.exp_table_box.add_widget(self.table_expense)

        box = BoxLayout(size_hint=(1,None)
                        ,pos_hint={"center_x":0.5})
        
        
        label = MDLabel(text=f"Total: {self.total_exp()}",color=(0,0,0,1),font_style = "H5"
                         ,halign ="left"
                         ,size_hint=(0.75,None))
        box.add_widget(label)


        

        removebtn= MDFlatButton(text="Remove",
                                    size_hint= (0.25,None),
                                    on_release =self.remove_exp,
                                    md_bg_color = (0, 0, 1, 1),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1)
                                   
                                    )
        
        box.add_widget(removebtn)
        self.exp_table_box.add_widget(box)
        
        # table.on_row_press= self.hassam
        # screen.add_widget(table)
        # self.ids.balance_scr.add_widget(box)
        self.ids.balance_scr.add_widget(self.exp_table_box)

        self.create_exp_fields()

    def total_exp(self):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        msg = pickle.dumps(["total_exp"])
        app.client.send(msg)
        data=app.client.recv(HEADER)
        return pickle.loads(data)

        
    def total_inc(self):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return
        msg = pickle.dumps(["total_inc"])
        app.client.send(msg)
        data=app.client.recv(HEADER)
        return pickle.loads(data)

    def create_table_income(self,event):
        if self.two_btn_box:
            self.ids.balance_scr.remove_widget(self.two_btn_box)
        temp_list= self.income_func()

        self.inc_table_box = MDBoxLayout(orientation = "vertical",
                           size_hint =(1,0.62),
                           spacing= 0,
                           pos_hint={'center_x':0.5,'center_y':0.59},)
        
        self.inc_table_box.line_color=(0,0,1,1)
        self.inc_table_box.md_bg_color = (1,1,1,0.75)
        
        self.table_income = MDDataTable(
            size_hint=(1, 1),
            background_color=(0,0,0,1),
            pos_hint={'center_x':0.5,'center_y':0.1},
            use_pagination=True,
            rows_num =7,
            column_data=[
                ("Date", dp(18)),
                ("Description", dp(30)),
                ("Income", dp(16)),
            ],
            row_data=temp_list,
        )
        
        self.inc_table_box.add_widget(self.table_income)

        box = BoxLayout(size_hint=(1,None)
                        ,pos_hint={"center_x":0.5})
        
        
        label = MDLabel(text=f"Total: {self.total_inc()}",color=(0,0,0,1),font_style = "H5"
                         ,halign ="left"
                         ,size_hint=(0.75,None))
        box.add_widget(label)


        

        removebtn= MDFlatButton(text="Remove",
                                    size_hint= (0.25,None),
                                    on_release =self.remove_inc,
                                    md_bg_color = (0, 0, 1, 1),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1)
                                   
                                    )
        
        box.add_widget(removebtn)
        self.inc_table_box.add_widget(box)
        # table.on_row_press= self.hassam
        # screen.add_widget(table)
        # self.ids.balance_scr.add_widget(box)
        self.ids.balance_scr.add_widget(self.inc_table_box)

        self.create_inc_fields()

    
    def create_inc_fields(self):

        self.inc_field_box = MDBoxLayout(orientation = "vertical",
                           size_hint =(1,0.22),
                           spacing=5,
                           pos_hint={'center_y':0.11}
                           )
        # self.inc_field_box.line_color=(0,0,1,1)
        
       
        
        
        date_box = MDBoxLayout(size_hint= (1,1))
        
        self.Date = MDTextField(
                                    multiline=False,
                                    font_size=30,
                                    width=200,
                                    
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Date",
                                    disabled = True,
                                    # validator = "date",
                                    mode = "rectangle"
                                    )
        # self.Date.font_size=self.Date.height
        print(self.Date.height)
        self.date_dialog = MDDatePicker(size_hint= (None,None),
                                        width=300,
                                        pos_hint={'center_x':0.5,'center_y':0.5},
                                        max_year =2005)


        self.dob_btn = MDFlatButton(text="Date",
                                    size_hint= (0.25,None),
                                    on_release =self.show_date_picker,
                                    width = 100,
                                    md_bg_color = (0, 0, 0, 0.25),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1),
                                    
                                   
                                    )

        date_box.add_widget(self.Date)
        date_box.add_widget(self.dob_btn)

        self.Desc = MDTextField(
                                    multiline=False,
                                    font_size=30,
                                    # width=200,
                                    # height="38dp",
                                    size_hint= (1,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Desc",
                                    mode = "rectangle"
                                    )
        

       
        

        self.Income = MDTextField(
                                    multiline=False,
                                    font_size=30,
                                    # width=200,
                                    # height="38dp",
                                    size_hint= (1,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Income",
                                    mode = "rectangle"
                                    )

        

        self.add_btn = MDFlatButton(text="Add",
                                    size_hint= (None,None),
                                    on_release =self.add_income,
                                    width = 200,
                                    md_bg_color = (0, 0, 1, 1),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1),
                    
                                   
                                    )


        self.inc_field_box.add_widget(date_box)
        self.inc_field_box.add_widget(self.Desc)
        self.inc_field_box.add_widget(self.Income)
        self.inc_field_box.add_widget(self.add_btn)

        self.ids.balance_scr.add_widget(self.inc_field_box)

        

    def create_exp_fields(self):

        self.exp_field_box = MDBoxLayout(orientation = "vertical",
                           size_hint =(1,0.22),
                           spacing=5,
                           pos_hint={'center_y':0.11}
                           )
        
        # self.exp_field_box.line_color=(0,0,1,1)
        
        
        date_box = MDBoxLayout(size_hint= (1,1))
        
        self.Date = MDTextField(
                                    multiline=False,
                                    font_size=30,
                                    width=200,
                                    height="38dp",
                                    size_hint= (0.75,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Date",
                                    disabled = True,
                                    mode = "rectangle"
                                    )
        # self.Date.font_size=self.Date.height
        print(self.Date.height)
        self.date_dialog = MDDatePicker(size_hint= (None,None),
                                        width=300,
                                        pos_hint={'center_x':0.5,'center_y':0.5},
                                        max_year =2005)


        self.dob_btn = MDFlatButton(text="Date",
                                    size_hint= (0.25,None),
                                    on_release =self.show_date_picker,
                                    width = 100,
                                    md_bg_color = (0, 0, 0, 0.25),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1),
                                    
                                   
                                    )

        date_box.add_widget(self.Date)
        date_box.add_widget(self.dob_btn)

        self.Desc = MDTextField(
                                    multiline=False,
                                    font_size=30,
                                    width=200,
                                    height="38dp",
                                    size_hint= (1,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Desc",
                                    mode = "rectangle"
                                    )
        

       
        

        self.Income = MDTextField(
                                    multiline=False,
                                    font_size=30,
                                    width=200,
                                    height="38dp",
                                    size_hint= (1,1),
                                    background_color=(0,0,0,0),
                                    hint_text = "Expense",
                                    mode = "rectangle"
                                    )

        

        self.add_btn = MDFlatButton(text="Add",
                                    size_hint= (None,None),
                                    on_release =self.add_income,
                                    width = 200,
                                    md_bg_color = (0, 0, 1, 1),
                                    theme_text_color= "Custom",
                                    text_color=(1,1,1,1)
                                   
                                    )


        self.exp_field_box.add_widget(date_box)
        self.exp_field_box.add_widget(self.Desc)
        self.exp_field_box.add_widget(self.Income)
        self.exp_field_box.add_widget(self.add_btn)

        self.ids.balance_scr.add_widget(self.exp_field_box)

    def show_date_picker(self,event):
    
        self.date_dialog.bind(on_save=self.on_save)
        
        
        self.date_dialog.open()
        

    def on_save(self,instance,value,date_range):
        

        self.Date._set_text(str(value))  
        


    def add(self,event):
        print("added")


    def remove_exp(self,event):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return
        msg = pickle.dumps(["remove_exp"])
        app.client.send(msg)


        if self.exp_table_box:
            self.ids.balance_scr.remove_widget(self.exp_table_box)
            del self.exp_table_box

        self.create_table_expense(event)
        toast("removed")


    def remove_inc(self,event):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        msg = pickle.dumps(["remove_inc"])
        app.client.send(msg)
        

        

        if self.inc_table_box:
            self.ids.balance_scr.remove_widget(self.inc_table_box)
            del self.inc_table_box

        self.create_table_income(event)
        toast("removed")
                
        

    def income_func(self):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        msg = pickle.dumps(["income_data"])
        app.client.send(msg)
        data= app.client.recv(HEADER)
        return pickle.loads(data)

        



    def expense_func(self):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return
        msg = pickle.dumps(["expense_data"])
        app.client.send(msg)
        data= app.client.recv(HEADER)
        return pickle.loads(data)

        




    
        
    
    def add_income(self,event):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return
        _date = self.Date.text
        _desc = self.Desc.text
        _income = self.Income.text

        if _date =="" or _desc =="" or _income =="":
            toast("plase fill the all fields:")
            return
        try:
            msg = pickle.dumps(["add_income",_date,_desc,_income])
            app.client.send(msg)     
            
        except:
            toast("internal Error occur")
            return
        
        if self.inc_table_box:
            self.ids.balance_scr.remove_widget(self.inc_table_box)
            self.ids.balance_scr.remove_widget(self.inc_field_box)
            
            del self.inc_field_box
            del self.inc_table_box

            self.create_table_income(event)

    def add_expense(self,event):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        _date = self.Date.text
        _desc = self.Desc.text
        _expense = self.expense.text

        if _date =="" or _desc =="" or _expense =="":
            toast("plase fill the all fields:")
            return
        try:
            msg = pickle.dumps(["add_expense",_date,_desc,_expense])
            app.client.send(msg)
            
        except:
            toast("internal Error occur")
            return
        if self.exp_table_box:
            self.ids.balance_scr.remove_widget(self.exp_table_box)
            self.ids.balance_scr.remove_widget(self.exp_field_box)
            del self.exp_field_box
            del self.exp_table_box

            self.create_table_expense(event)

        





#################################################  101 user_click()
#################################################





class user_click(extra,Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.Uid =None
        layout = BoxLayout( orientation = "vertical",
            size_hint=(1,0.2),
            pos_hint={'center_x':0.5,'center_y':0.8},
            spacing=10,

            )
        
        self.dic_for_month ={
        "Jan":'01',
        "Feb":'02',
        "Mar":'03',
        "Apr":'04',
        "May":'05',
        'Jun':'06',
        "Jul":'07',
        "Aug":'08',
        "Sep":'09',
        "Oct":'10',
        "Nov":'11',
        "Dec":'12'
        }
        month_list=[
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        'Jun',
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
        ]
       

      
        

        self.Month = Spinner(
            text='Months',
            values=month_list,
            size_hint=(1,1),
            pos_hint={'center_x': 0.5,'center_y':0.5},
            sync_height = True,
            # dropdown_cls=scatter,
            
        )
    

        
        self.Years = Spinner(
            text='Years',
            values=self.fetch_year(),
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5,'center_y':0.5},
            sync_height = True
        )
        

        self.btn = MDFlatButton(text="select",size_hint =(None,None)
                                ,on_release=self.on_select,
                                pos_hint={'center_x': 0.5,'center_y':0.5},
                                md_bg_color=(0,0,1,1),
                                theme_text_color = "Custom",
                                text_color=(1,1,1,1)
                                )


        layout.add_widget(self.Month)
        layout.add_widget(self.Years)
        layout.add_widget(self.btn)
        self.ids.detail_scr.add_widget(layout)

        return


    def on_select(self, instance):
        _month=self.Month.text
        _years =self.Years.text

        if _month=="Months" or _years=="Years":
            toast("please select the values")
            return
        
        temp_list =self.fetch_month_data(self.dic_for_month[_month],_years)
        
        table = MDDataTable(
            size_hint=(1, 0.65),
            background_color=(0,0,0,1),
            pos_hint={'center_x':0.5,'center_y':0.35},
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("Date", dp(18)),
                ("Time", dp(16)),
                ("Day", dp(18)),
                ("Status", dp(16)),
                
            ],
            row_data=temp_list
        )


        self.ids.detail_scr.add_widget(table)

        
        
    def fetch_year(self):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return

        msg = pickle.dumps(["fetch_year"])
        app.client.send(msg)
        data = app.client.recv(HEADER)
        return pickle.loads(data)       

        
    
    def fetch_month_data(self,_mon,_year):
        app = App.get_running_app()

        if not app.is_server_connected():
            if not app.connect_to_server():
                return
        
        msg = pickle.dumps(['fetch_mon_data',self.Uid,_mon,_year])
        app.client.send(msg)
        data = app.client.recv(HEADER)
        return pickle.loads(data)
        
    
    def hassam(self):
        pass

    def set_Id(self,_id):
        self.Uid = _id



##################################################   101 build class
##################################################   101 build class




class LoginApp(MDApp):

    def build(self):
        Window.size = (360, 640)
        
            
        self.screenManager = ScreenManager(transition=NoTransition())
        
        self._data = data()

        self._login1 =LoginScreen(name="login")
        self.screenManager.add_widget(self._login1)
        
        self.client  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect_to_server()

        self.us_scr =None
        self.status = None
        self.hr_scr = None
        self.sign_up = None
        self.forgot_pass= None

        self.m_admin = None
        self.admin_AddNew = None
        self.admin_remove = None
        self.admin_users = None
        self.admin_monthly_hr = None
        self.admin_daily_hr =None
        self.admin_bln_sheet = None
        self.admin_user_click = None
        self.user_manage = None
        self.company_manage = None
        self.time_manage = None
        self.update_users = None
        self.update_user_fields= None
              

        return self.screenManager
       
    def remove_scr(self,str):
        if str=="Main_admin":
            self.screenManager.remove_widget(self.m_admin)
            del self.m_admin
            
        elif str=="AddNew":
            self.screenManager.remove_widget(self.admin_AddNew)
            del self.admin_AddNew

        elif str=="Remove":
            self.screenManager.remove_widget(self.admin_remove)
            del self.admin_remove

        elif str=="Users":
            self.screenManager.remove_widget(self.admin_users)
            del self.admin_users
            
        elif str=="Mon_hr":
            self.screenManager.remove_widget(self.admin_monthly_hr)
            del self.admin_monthly_hr

        elif str=="daily_hr":
            self.screenManager.remove_widget(self.admin_daily_hr)
            del self.admin_daily_hr

        elif str=="balance_sheet":
            self.screenManager.remove_widget(self.admin_bln_sheet)
            del self.admin_bln_sheet

        elif str=="after_login":
            self.screenManager.remove_widget(self.us_scr)
            del self.us_scr
        
        elif str=="status":
            self.screenManager.remove_widget(self.status)
            del self.status

        elif str=="check_hours":
            self.screenManager.remove_widget(self.hr_scr)
            del self.hr_scr
        
        elif str=="login":
            self.screenManager.remove_widget(self._login1)
            del self._login1

        elif str=="user_click":
            self.screenManager.remove_widget(self.admin_user_click)
            del self.admin_user_click

        elif str=="sign_up":
            self.screenManager.remove_widget(self.sign_up)
            del self.sign_up
        elif str=="forgot_pass":
            self.screenManager.remove_widget(self.forgot_pass)
            del self.forgot_pass
        elif str=="user_manage":
            self.screenManager.remove_widget(self.user_manage)
            del self.user_manage
        elif str=="time_manage":
            self.screenManager.remove_widget(self.time_manage)
            del self.time_manage
        elif str=="company_manage":
            self.screenManager.remove_widget(self.company_manage)
            del self.company_manage
        elif str=="update_users":
            self.screenManager.remove_widget(self.update_users)
            del self.update_users
        elif str=="update_user_fields":
            self.screenManager.remove_widget(self.update_user_fields)
            del self.update_user_fields


    def add_scr(self,str):
        if str=="Main_admin":
            self.m_admin = Main_admin(name="Main_admin")
            self.screenManager.add_widget(self.m_admin)

        elif str=="AddNew":
            self.admin_AddNew = Add_New(name="AddNew")
            self.screenManager.add_widget(self.admin_AddNew)

        elif str=="Remove":
            self.admin_remove = Remove_scr(name="Remove")
            self.screenManager.add_widget(self.admin_remove)
        
        elif str=="Users":
            self.admin_users = Users(name="Users")
            self.screenManager.add_widget(self.admin_users)

        elif str=="Mon_hr":
            self.admin_monthly_hr = Month_scr(name="Mon_hr")
            self.screenManager.add_widget(self.admin_monthly_hr)

        
        elif str=="balance_sheet":
            self.admin_bln_sheet = Balance_sheet(name="balance_sheet")
            self.screenManager.add_widget(self.admin_bln_sheet)

        elif str=="after_login":
            self.us_scr=user_login(name="after_login")
            self.screenManager.add_widget(self.us_scr)
        
        elif str=="status":
            self.status =status(name="status")
            self.screenManager.add_widget(self.status)

        elif str=="check_hours":
            self.hr_scr =check_hour(name="check_hours")
            self.screenManager.add_widget(self.hr_scr)

        elif str=="login":
            self._login1 =LoginScreen(name="login")
            self.screenManager.add_widget(self._login1)

        elif str=="user_click":
            self.admin_user_click = user_click(name="user_click")
            self.screenManager.add_widget(self.admin_user_click)

        elif str=="sign_up":
            self.sign_up = sign_up(name="sign_up")
            self.screenManager.add_widget(self.sign_up)

        elif str=="forgot_pass":
            self.forgot_pass = forgot_pass(name="forgot_pass")
            self.screenManager.add_widget(self.forgot_pass)

        elif str=="user_manage":
            self.user_manage = user_manage(name="user_manage")
            self.screenManager.add_widget(self.user_manage)

        elif str=="time_manage":
            self.time_manage = time_manage(name="time_manage")
            self.screenManager.add_widget(self.time_manage)
        
        elif str=="company_manage":
            self.company_manage = company_manage(name="company_manage")
            self.screenManager.add_widget(self.company_manage)

        elif str=="update_users":
            self.update_users = update_users(name="update_users")
            self.screenManager.add_widget(self.update_users)

        elif str=="update_user_fields":
            self.update_user_fields = update_user_fields(name="update_user_fields")
            self.screenManager.add_widget(self.update_user_fields)
 
    def connect_to_server(self):
        try:
            self.client.connect((IP,PORT))
            return True
            
        except:
            toast("Sorry\nServer is Offline...")
            self.screenManager.current = "login"
            return False
    
    def is_server_connected(self):

        try:
            peer = self.client.getpeername()
            return True
        except:
            return False
    
    
    def update_background_pos_size(self, instance, value):
        # Calculate the position and size of the background rectangle
        rect_width = instance.width  # Set the desired width of the rectangle (e.g., 50% of the window width)
        rect_height = instance.height  # Set the desired height of the rectangle (e.g., 50% of the window height)
        rect_pos_x = (instance.width - rect_width) * 0.5  # Calculate the x-coordinate for the rectangle to center it horizontally
        rect_pos_y = (instance.height - rect_height) * 0.5  # Calculate the y-coordinate for the rectangle to center it vertically
    

        
        
       
        self.background_rect.pos = (rect_pos_x, rect_pos_y)
        self.background_rect.size = (rect_width, rect_height)

   

    
LoginApp().run()