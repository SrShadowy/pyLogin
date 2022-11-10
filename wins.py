from tkinter import Entry, Tk, Button, Label, NSEW, Frame, FALSE, END
import tkinter as tk
import hashlib
from db import load_data_base

class login_page():

    #----colorações----
    __blue_one    = '#648da9' #azul-cinza
    __blue_two    = '#61ede4' #azul mar
    __blue_three  = '#2a79a1' #azul agua escura
    __white       = '#ffffff' #branco
    __gray        = '#a7acb6' #cinza
    __gray_one    = '#333333' #cinza denovo
    __gray_two    = '#222222' #mais um cinza
    __black_one   = '#181717' #preto azulado
    #----------Animação do gif--------#
    _gif_framelist = [];      
    _gif_frame_index = 0; 
    _gif_count = 0;
    _gif_anim = str();
    _gif_list_gif_frames =[];
    #----posição do mouse-------
    __cur_x = 0
    __cur_y = 0
    #---------resolução--------
    __width = 500
    __height = 600
    _page = 0; #0 == login | 1 == register ...

    def __init__(self):
        # a data base
        self.db = load_data_base();

        # a janela
        self.__win_main = Tk();
        self.__win_main.geometry(str(self.__width)+'x'+str(self.__height));
        self.__win_main.resizable(width=FALSE, height=FALSE);

        #Objetos
        self.__main_frame = Frame(self.__win_main, width=self.__width, height=self.__height, bg=self.__gray);
        self.__main_frame.grid(padx=0,pady=0,row=0,column=0,sticky=NSEW)
        self.__painel = Frame(self.__win_main, bg=self.__black_one)
        self.__painel.grid(sticky=NSEW,row=0, pady=100, padx=100);
        self.__btn_login = Button(self.__painel, height=2, width=25, text='LOGIN', command=self.login);
        self.__btn_login.place(x=5, y=5);
        self.__btn_login['border'] = 0
        self.__btn_register = Button(self.__painel, height=2, width=25, text='REGISTER', command=self.register);
        self.__btn_register.place(x=192, y=5);
        self.__btn_register['border'] = 0
        self.__btn_login.config(fg=self.__blue_three, bg=self.__gray_two)
        self.__btn_register.config(fg=self.__white, bg=self.__gray_one)
        self._lbl_welcome = Label(self.__painel, text='Bem-vindo!', font=('Arial 19'), fg=self.__white, bg=self.__black_one);
        self._edt_user = Entry(self.__painel, width=25, justify='left', font=("", 18), highlightthickness=0, relief='solid', bg=self.__gray_one, fg=self.__white );
        self._lbl_user = Label(self.__painel, text='Nome de usuário*', bg=self.__gray_one, fg=self.__gray);
        self._edt_email = Entry(self.__painel, width=25, justify='left', font=("", 18), highlightthickness=0, relief='solid', bg=self.__gray_one, fg=self.__white );
        self._lbl_email = Label(self.__painel, text='E-mail*', bg=self.__gray_one, fg=self.__gray);
        self._edt_password = Entry(self.__painel,  show="*",  width=25, justify='left', font=("", 18), highlightthickness=0, relief='solid', bg=self.__gray_one, fg=self.__white );
        self._lbl_password = Label(self.__painel, text='Senha*', bg=self.__gray_one, fg=self.__gray);
        self._edt_confirm_password = Entry(self.__painel, show="*",  width=25, justify='left', font=("", 18), highlightthickness=0, relief='solid', bg=self.__gray_one, fg=self.__white );
        self._lbl_confirm_password = Label(self.__painel, text='Confirmar senha*', bg=self.__gray_one, fg=self.__gray);

        self._lbl_go_reset = Label(self.__painel, text='Esqueci minha senha *', fg=self.__blue_two, bg= self.__black_one)
        self._lbl_go_reset.bind('<Button-1>', func=self._call_lost_pass)
        self._btn_action = Button(self.__painel, height= 3, width=45, text='Entrar *')
        self._btn_action.config(command= self._action);
        self._btn_action['border'] = '0'
        self._btn_action.config(bg=self.__gray_one, fg=self.__blue_two)

        self.lbl_gif = Label(self.__painel, bg=self.__black_one, image="")
        self.lbl_gif.place_forget();


        #Ações dos objectos
        self._edt_confirm_password.bind('<FocusIn>', func= lambda event, a=self._lbl_confirm_password: self.anim_move_down(a))
        self._edt_confirm_password.bind('<FocusOut>', func= lambda event, a=self._lbl_confirm_password, b=self._edt_confirm_password: self.anim_move_up(a, b))
        self._edt_confirm_password.bind('<KeyRelease>', func=self.compare_password )
        self._edt_email.bind('<FocusIn>', func= lambda event, a=self._lbl_email: self.anim_move_down(a))
        self._edt_email.bind('<FocusOut>', func= lambda event, a=self._lbl_email, b=self._edt_email: self.anim_move_up(a, b))
        self._edt_password.bind('<FocusIn>', func= lambda event, a=self._lbl_password: self.anim_move_down(a))
        self._edt_password.bind('<FocusOut>', func= lambda event, a=self._lbl_password, b=self._edt_password: self.anim_move_up(a, b))
        self._edt_user.bind('<FocusIn>', func= lambda event, a=self._lbl_user: self.anim_move_down(a))
        self._edt_user.bind('<FocusOut>', func= lambda event, a=self._lbl_user, b=self._edt_user: self.anim_move_up(a, b))
        
        self.load_gif('loading.gif');
        self.hide_widgt();
        self.login();
        #self.register();
        

        
        
    def compare_password(self, event):
        pass_1 = self._edt_password.get();
        pass_2 = self._edt_confirm_password.get();
        if len(pass_1) <= 0 or len(pass_2) <= 0:
            return;
            
        if pass_1 == pass_2:
            self._edt_confirm_password.config(highlightthickness=5, highlightcolor="green");
        else:
            self._edt_confirm_password.config(highlightthickness=5, highlightcolor="red");

           
    def _action(self):
        if(self._page == 0): #LOGIN
            user = self._edt_email.get();
            password = hashlib.md5( self._edt_password.get().encode() ).hexdigest();
            status = self.db.compare_data(user, password);
            if(status != 0):
                self._lbl_welcome.config(text="Login e senha incorretos ou não encontrados", font='Arial 13')
                self._lbl_welcome.place(x=20);
                return 1;

            self.hide_widgt();
            self.welcome();
            return status;

        if(self._page == 1): #Create account
            user_name   = self._edt_user.get();
            email       = self._edt_email.get();
            password    = self._edt_password.get();
            hash_pass   = hashlib.md5(password.encode());
            confirm_    = hashlib.md5(self._edt_confirm_password.get().encode());
            if(hash_pass.hexdigest() != confirm_.hexdigest()):
                print('hash error')
                print(hash_pass.hexdigest())
                print(confirm_.hexdigest())
                return;
           
            data = {"User" : user_name,
            "Email" : email,
            "Password" : hash_pass.hexdigest(),
            "Backup_senha" : password
            };


            status = self.db.write_json(data);
            if(status == 1):
                self._lbl_user.config(fg="red", text="Nome de usuário já está em uso");
            if(status == 2):
                self._lbl_email.config(fg="red", text="O E-mail em questão já está em uso");

            if(status == 0):
                self._page = 0
                self._action();

        if(self._page == 3): #resetar senha

            user = self._edt_user.get();
            email = self._edt_email.get();

            self.ret_ = self.db.change_pass(0, user=user, email=email);
            #print(self.ret_)
            if(self.ret_ != 0):
                self._page = 4;
                self.hide_widgt();
                self.lose_my_pass();
            else:
                self._lbl_welcome.config(text='Email e usuário não conhecidem ou não existem', font='Arial 12');
                self._lbl_welcome.place(x=5)

            
            return;
        if(self._page == 4): #resetar senha etapa 2
            ps = hashlib.md5( self._edt_password.get().encode() ).hexdigest();
            self.ret_ = self.db.change_pass(1, new_pass=ps, backup=self._edt_confirm_password.get());
            self.login();
            return; 


        if(self._page == 5): # NADA >\\<
            return; 
        
        self.hide_widgt();
        return;

    def _call_lost_pass(self, event):
        self._page = 3;
        self.hide_widgt();
        self.lose_my_pass();

    def anim_move_down(self, elemnt):
        if not hasattr(elemnt, 'move_down'):
            elemnt.move_down = False;
        if( elemnt.move_down == False):
            elemnt.move_down = True;
            y = elemnt.winfo_y();
            y += 30;
            elemnt.config(bg=self.__black_one)
            elemnt.place(y=y);

    def anim_move_up(self, elemnt, main):
        letter = main.get();
        if len(letter) == 0:
            y = elemnt.winfo_y();
            y -= 30;
            elemnt.config(bg=self.__gray_one)
            elemnt.place(y=y);
            elemnt.move_down = False;



    def load_gif(self, gif):
        while True:
            try:
                part = 'gif -index {}'.format(self._gif_frame_index);
                frame = tk.PhotoImage(file=gif, format=part);
            except:
                self._gif_last_frame = self._gif_frame_index - 1;
                print('gif loaded')
                break;
            self._gif_framelist.append(frame);
            self._gif_frame_index += 1;

    def animate_gif(self,elemnt, count):
        elemnt.config(image = self._gif_framelist[count])
        count +=1
        if count > self._gif_last_frame:
            count = 0  
        self._gif_anim = self.__painel.after(22, lambda : self.animate_gif(elemnt,count))        
          
    def stop_gif(self):
        self.lbl_gif.place_forget();
        self.__painel.after_cancel(self._gif_anim);


    def loading(self, fnc):
        self.hide_widgt();
        self.lbl_gif.pack();
        self.lbl_gif.place(x=50, y=100)
        self.animate_gif(self.lbl_gif, 0)
        self.__painel.after(500, fnc);
        self.__painel.after(800, self.stop_gif);

      
    def login(self):
        self.__btn_login.focus_set();
        self.hide_widgt();
        self.define_title('LogIn')
        self._lbl_email.config(text='Usuário ou E-mail*');
        self._lbl_welcome.config(text='Bem-vindo');
        self.__btn_login.config(bg=self.__gray_two, fg=self.__blue_two)
        self.__btn_register.config(fg=self.__white, bg=self.__gray_one)
        self.__painel.grid(pady=100, padx=61);
        self._lbl_go_reset.place(x= 23, y=320)
        self._btn_action.place(x=23, y=250)
        self._lbl_email.place(x=30, y=133);
        self._lbl_password.place(x=30, y=193);
        self._edt_email.place(x=23, y=130);
        self._lbl_welcome.place(x=120,y=80)
        self._edt_password.place(x=23, y=190);
        self._btn_action.config(text='Entrar')
        if self._page != 0:
            self._page = 0;
            self.hide_widgt();
            self.loading(self.login);
        
    def register(self):
        self.__painel.focus();
        self.hide_widgt();
        self.define_title('SingIn')
        self.__btn_register.config(bg=self.__gray_two, fg=self.__blue_two)
        self.__btn_login.config(fg=self.__white, bg=self.__gray_one)
        self.__painel.grid(pady=50, padx=61);
        self._lbl_user.place(x=30, y=83);
        self._edt_user.place(x=23,y=80)
        self._edt_email.place(x=23, y=150);
        self._lbl_email.place(x=30, y=153);
        self._lbl_password.place(x=30, y=223);
        self._edt_password.place(x=23, y=220);
        self._edt_confirm_password.place(x=23, y=290);
        self._lbl_confirm_password.place(x=30, y= 293);

        self._btn_action.config(text='Cadastrar')
        self._btn_action.place(x=23, y=400)
        if self._page != 1:
            self._page = 1;
            self.hide_widgt();
            self.loading(self.register);


    def welcome(self):
        self.hide_widgt();
        if(self._page != 5):
            self._page = 5;
            self.loading(self.welcome);
            self.__btn_login.place_forget();
            self.__btn_register.place_forget();

        self.define_title('Welcome has ' + self.db.user['User'])
        self._lbl_welcome.config(text='Seja bem vindo(a): ' + self.db.user['User']);
        self._lbl_welcome.place(x=10, y=50);
        return;

    def lose_my_pass(self):
        self.hide_widgt();
        self.define_title('Recovery password')
        if(self._page == 3):
            self.__btn_register.config(bg=self.__gray_one, fg=self.__white)
            self.__btn_login.config(fg=self.__white, bg=self.__gray_one)
            self.__painel.grid(pady=100, padx=61);
            self._lbl_welcome.place(x=50, y=60);
            self._lbl_welcome.config(text='Recompere sua senha');
            self._lbl_email.place(x=23, y=113);
            self._edt_email.place(x=20, y=110);
            self._lbl_user.place(x=23, y=203);
            self._edt_user.place(x=20, y=200);
            self._btn_action.config(text='Próxima etapa');
            self._btn_action.place(x=23, y=300);
        elif (self._page == 4):
            self._lbl_welcome.config(text='Introduza uma nova senha');
            self._lbl_welcome.place(x=30, y=60);
            self._edt_password.place(x=20, y=110);
            self._lbl_password.place(x=23, y=113);
            self._edt_confirm_password.place(x=20, y=200);
            self._lbl_confirm_password.place(x=23, y=203);
            self._btn_action.config(text='Alterar senha');
            self._btn_action.place(x=23, y=300);
        return;

    def clear_text_edit(self):
        self._edt_password.delete(0, END);
        self._edt_email.delete(0, END);
        self._edt_confirm_password.delete(0, END);
        self._edt_user.delete(0, END);

    def execute_binds_text(self):
        a=self._lbl_user
        b=self._edt_user;
        self.anim_move_up(a, b)
        a=self._lbl_confirm_password
        self.anim_move_up(a, b)
        a=self._lbl_email
        self.anim_move_up(a, b)
        a=self._lbl_password
        self.anim_move_up(a, b)

    def restore(self):
        self._lbl_welcome.config(text='Bem-vindo!', font=('Arial 19'), fg=self.__white, bg=self.__black_one);
        self._lbl_user.config(text='Nome de usuário*', bg=self.__gray_one, fg=self.__gray);
        self._lbl_email.config(text='E-mail*', bg=self.__gray_one, fg=self.__gray);
        self._lbl_password.config(text='Senha*', bg=self.__gray_one, fg=self.__gray);
        self._lbl_confirm_password.config(text='Confirmar senha*', bg=self.__gray_one, fg=self.__gray);

    def hide_widgt(self):
        self.clear_text_edit();
        self.execute_binds_text();
        self.restore();
        self.__painel.focus_set();
        self._lbl_email.place_forget();
        self._btn_action.place_forget();
        self._lbl_welcome.place_forget();
        self._edt_password.place_forget();
        self._lbl_password.place_forget();
        self._edt_email.place_forget();
        self._lbl_confirm_password.place_forget();
        self._lbl_go_reset.place_forget();
        self._lbl_user.place_forget()
        self._edt_user.place_forget()
        self._edt_confirm_password.place_forget()

    def define_title(self, title):
        self.__win_main.title(title);
    def run(self):
        self.__win_main.mainloop();