import mysql.connector
from tkinter import *
import hashlib
import re

ws = Tk()

ws.title("Car wash Booking")
ws.geometry("1080x1080")
ws['bg'] = '#012'

username_l = StringVar()
password_l = StringVar()
username_s = StringVar()
password_s = StringVar()


# img = PhotoImage(file="a40012e.png")
# label = Label(
#     ws,
#     image=img
# )
# label.place(x=0, y=0)


def user_home():
    ui = Tk()
    ui.title("Car wash Booking")
    ui.geometry("1080x1080")
    ui['bg'] = '#012'
    tb = Text(ui, font=('Arial 12'), width=50, height=2, background="#fff")
    tb.place(x=300, y=650)
    select_city = StringVar(ui)
    select_city.set("Select an Option")

    select_locations = StringVar(ui)
    select_locations.set("Select an Option")

    select_shops = StringVar(ui)
    select_shops.set("Select an Option")

    service = StringVar(ui)
    service.set("Select an Option")

    phoneno = StringVar(ui)
    rcnum = StringVar(ui)
    mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
    db = mydb.cursor()
    sql = "SELECT DISTINCT cities FROM bodyshops"
    db.execute(sql)
    list_cities = [i[0] for i in db]
    sql = "SELECT DISTINCT servicetype FROM services"
    db.execute(sql)
    services_list = [i[0] for i in db]
    mydb.commit()
    mydb.close()

    data_loc = {"Select an Option": ["Select city"]}
    data_shops = {("Select an Option", "Select an Option"): ["Select location"]}
    mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
    db = mydb.cursor()
    sql = "SELECT DISTINCT cities FROM bodyshops"
    db.execute(sql)
    for i in [i[0] for i in db]:
        sql = "SELECT DISTINCT locations FROM bodyshops WHERE cities=%s"
        db.execute(sql, [i])
        data_loc[i] = [q[0] for q in db]
        for j in data_loc[i]:
            sql = "SELECT DISTINCT bodyshopname FROM bodyshops WHERE cities=%s AND locations=%s "
            db.execute(sql, [i, j])
            data_shops[tuple([i, j])] = [_q[0] for _q in db]
    mydb.close()

    def ins():
        mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
        db = mydb.cursor()
        if (all([select_city.get(), select_locations.get(), select_shops.get(), phoneno.get(), rcnum.get(),
                 service.get()])):
            sql = "SELECT COUNT(*) FROM accrejdb where cities=%s AND locations=%s AND bodyshopname=%s"
            db.execute(sql, [select_city.get(), select_locations.get(), select_shops.get()])
            if (list(db)[0][0] > 5):
                data_shops[tuple([select_city.get(), select_locations.get()])].remove(select_shops.get())
                tb.insert(INSERT, "Five Bookings Exceeded RESELECT OPTIONS\n")
            else:
                sql = "SELECT cities,locations,bodyshopname,servicetype,userid FROM bookings"
                db.execute(sql)
                if (tuple([select_city.get(), select_locations.get(), select_shops.get(), service.get(),
                           username_l.get()]) in [i for i in db]):
                    tb.insert(INSERT, "Already Requested For Service\n")
                else:
                    sql = "SELECT * FROM bodyshops"
                    db.execute(sql)
                    if (tuple([select_city.get(), select_locations.get(), select_shops.get()]) in [i for i in db]):
                        sql = "INSERT INTO bookings VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        db.execute(sql, [select_city.get(), select_locations.get(), select_shops.get(), phoneno.get(),
                                         rcnum.get(), service.get(), username_l.get()])
                        mydb.commit()
                        tb.insert(INSERT, "Booking Successful\n")
                    else:
                        tb.insert(INSERT, "Bodyshop Doesn't Exist RESELECT OPTIONS\n")

        else:
            tb.insert(INSERT, "Booking Failed\n")

        mydb.close()

    def run2(self):
        self = select_locations.get()
        Label(ui, text="Select Shop", font=('Arial', 16), width=15).place(x=signup_x, y=signup_y + 100)
        OptionMenu(ui, select_shops, *data_shops[tuple([select_city.get(), select_locations.get()])]).place(
            x=signup_x + 200, y=signup_y + 100)

    def run(self):
        self = select_city.get()
        Label(ui, text="Select Locations", font=('Arial', 16), width=15).place(x=signup_x, y=signup_y + 50)
        OptionMenu(ui, select_locations, *data_loc[select_city.get()], command=run2).place(x=signup_x + 200,
                                                                                           y=signup_y + 50)

    noti = Text(ui, font=('Arial 12'), width=45, height=15, background="#fff")

    def show():
        noti.place(x=650, y=80)
        btnn.configure(command=hide)
        noti.delete('1.0', END)
        mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
        db = mydb.cursor()
        sql = "SELECT cities,locations,bodyshopname,servicetype,status FROM accrejdb WHERE userid=%s"
        db.execute(sql, [username_l.get()])
        for i in db:
            noti.insert(INSERT, ' '.join(i) + '\n')
        sql = "SELECT cities,locations,bodyshopname,servicetype FROM bookings WHERE userid=%s"
        db.execute(sql, [username_l.get()])
        for i in db:
            noti.insert(INSERT, ' '.join(i) + " pending" + '\n')
        mydb.commit()
        mydb.close()

    def hide():
        noti.place_forget()
        btnn.configure(command=show)

    btnn = Button(ui, text="Notifications ", font=('Arial 10'), command=show, width=10, height=1)
    btnn.place(x=800, y=50)
    Button(ui, text="Logout", font=('Arial 10'), command=ui.destroy, width=10, height=1).place(x=900, y=50)
    Label(ui, text='Car Wash Booking', font=('Arial', 30)).place(x=300, y=50)
    signup_x = 300
    signup_y = 270

    Label(ui, text="Select city", font=('Arial', 16), width=15).place(x=signup_x, y=signup_y)
    OptionMenu(ui, select_city, *list_cities, command=run).place(x=signup_x + 200, y=signup_y)

    Label(ui, text="Select Locations", font=('Arial', 16), width=15).place(x=signup_x, y=signup_y + 50)
    OptionMenu(ui, select_locations, *data_loc[select_city.get()], command=run2).place(x=signup_x + 200,
                                                                                       y=signup_y + 50)

    Label(ui, text="Select Shop", font=('Arial', 16), width=15).place(x=signup_x, y=signup_y + 100)
    OptionMenu(ui, select_shops, *data_shops[tuple([select_city.get(), select_locations.get()])]).place(
        x=signup_x + 200, y=signup_y + 100)

    Label(ui, text="Select service", font=('Arial', 16), width=15).place(x=signup_x, y=signup_y + 150)
    OptionMenu(ui, service, *services_list).place(x=signup_x + 200, y=signup_y + 150)

    Label(ui, text="PhoneNo", font=('Arial', 16), width=15).place(x=signup_x, y=signup_y + 200)
    Entry(ui, width=25, font=('Arial 16'), textvariable=phoneno).place(x=signup_x + 200, y=signup_y + 200)
    Label(ui, text="RC.NO", font=('Arial', 16), width=15).place(x=signup_x, y=signup_y + 250)
    Entry(ui, width=25, font=('Arial 16'), textvariable=rcnum).place(x=signup_x + 200, y=signup_y + 250)

    Button(ui, text="Confirm Booking", font=('Arial 10'), command=ins, width=10, height=2).place(x=signup_x + 250,
                                                                                                 y=signup_y + 300)

    ui.mainloop()


def admin_home():
    ah = Tk()
    ah.title("Admin side")
    ah.geometry("1080x1080")
    ah['bg'] = '#012'
    city = StringVar(ah)
    loc = StringVar(ah)
    shop = StringVar(ah)
    tb = Text(ah, font=('Arial 12'), width=30, height=2, background="#fff")
    tb.place(x=450, y=500)

    def ins():
        mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
        db = mydb.cursor()
        try:
            if all([city.get(), loc.get(), shop.get()]):
                sql = "SELECT * from bodyshops"
                db.execute(sql)
                if (city.get().lower(), loc.get().lower(), shop.get().lower()) in [tuple([i.lower() for i in j]) for j
                                                                                   in db]:
                    tb.insert(INSERT, "Body Shop Already Taken\n")
                else:
                    sql = "INSERT INTO bodyshops (cities,locations,bodyshopname) VALUES (%s,%s,%s)"
                    db.execute(sql, [city.get(), loc.get(), shop.get()])
                    tb.insert(INSERT, "Added Successful\n")
                    mydb.commit()
            else:
                tb.insert(INSERT, "Empty Fields Detected\n")
        except:
            tb.insert(INSERT, "Process Failed\n")

        mydb.close()

    def display():
        tb = Text(ah, font=('Arial 12'), width=30, height=10, background="#fff")
        tb.place(x=800, y=600)
        mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
        db = mydb.cursor()

        sql = "SELECT * FROM bodyshops"
        db.execute(sql)
        for i in db:
            for j in i:
                tb.insert(INSERT, str(j) + "  ")
            tb.insert(INSERT, "\n")
        mydb.commit()
        mydb.close()
        tb.after(3000, tb.destroy)

    def display2():
        tb = Text(ah, font=('Arial 12'), width=50, height=10, background="#fff")
        tb.place(x=100, y=600)
        mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
        db = mydb.cursor()

        sql = "SELECT * FROM bookings"
        db.execute(sql)
        for i in db:
            for j in i:
                tb.insert(INSERT, str(j) + "  ")
            tb.insert(INSERT, "\n")
        mydb.commit()
        mydb.close()
        tb.after(3000, tb.destroy)

    def AddServices():
        AS = Tk()
        AS.title("Admin side")
        AS.geometry("1080x1080")
        AS['bg'] = '#012'
        services = StringVar(AS)
        price = IntVar(AS)
        tb = Text(AS, font=('Arial 12'), width=30, height=2, background="#fff")
        tb.place(x=450, y=500)

        def ins():
            mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
            db = mydb.cursor()
            try:
                sql = "INSERT INTO services VALUES (%s,%s)"
                db.execute(sql, [services.get(), price.get()])
                tb.insert(INSERT, "Added Successful\n")
                mydb.commit()
            except:
                tb.insert(INSERT, "Process Failed\n")

            mydb.close()

        def display():
            tb = Text(AS, font=('Arial 12'), width=30, height=10, background="#fff")
            tb.place(x=100, y=500)
            mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
            db = mydb.cursor()

            sql = "SELECT * FROM services"
            db.execute(sql)
            for i in db:
                for j in i:
                    tb.insert(INSERT, str(j) + "  ")
                tb.insert(INSERT, "\n")
            mydb.commit()
            mydb.close()
            tb.after(3000, tb.destroy)

        Button(AS, text="Exit", font=('Arial 10'), command=AS.destroy, width=10, height=1).place(x=900, y=20)
        Button(AS, text="Show services", font=('Arial 10'), command=display, width=10, height=1).place(x=800, y=20)
        Label(AS, text='ADD Services', font=('Arial', 30)).place(x=400, y=170)
        signup_x = 300
        signup_y = 270

        Label(AS, text="Service", font=('Arial', 16), width=12).place(x=signup_x, y=signup_y)
        Entry(AS, width=25, font=('Arial 16'), textvariable=services).place(x=signup_x + 180, y=signup_y)

        Label(AS, text="price", font=('Arial', 16), width=12).place(x=signup_x, y=signup_y + 50)
        Entry(AS, width=25, font=('Arial 16'), textvariable=price).place(x=signup_x + 180, y=signup_y + 50)
        Button(AS, text="submit", font=('Arial 12'), command=ins, width=10, height=2).place(x=signup_x + 200,
                                                                                            y=signup_y + 100)
        AS.mainloop()

    def Bookings():
        BK = Tk()
        BK.title("Admin side")
        BK.geometry("1080x1080")
        BK['bg'] = '#012'
        filter = StringVar(BK)
        filter.set("No filter")

        def labes(sn, yco):
            def accept_bk():
                mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
                db = mydb.cursor()
                sql = "SELECT COUNT(*) FROM accrejdb where cities=%s AND locations=%s AND bodyshopname=%s"
                db.execute(sql, sn[:3])
                if (list(db)[0][0] > 5):
                    mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
                    db = mydb.cursor()
                    sn.append('Reject')
                    sql = "INSERT INTO accrejdb VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                    db.execute(sql, sn)
                    sql = "DELETE FROM bookings WHERE cities=%s AND locations=%s AND bodyshopname=%s AND Phoneno=%s AND model=%s AND servicetype=%s AND userid=%s"
                    sn.pop()
                    db.execute(sql, sn)
                    accbtn.destroy()
                    rejbtn.destroy()
                    Label(BK, text='Rejected Because of Booking Limit', font=('Arial', 10)).place(x=800, y=yco)
                    mydb.commit()
                    mydb.close()
                else:
                    sn.append('Accept')
                    sql = "INSERT INTO accrejdb VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                    db.execute(sql, sn)
                    sql = "DELETE FROM bookings WHERE cities=%s AND locations=%s AND bodyshopname=%s AND Phoneno=%s AND model=%s AND servicetype=%s AND userid=%s"
                    sn.pop()
                    db.execute(sql, sn)
                    accbtn.destroy()
                    rejbtn.destroy()
                    Label(BK, text='Accept', font=('Arial', 10)).place(x=800, y=yco)
                    mydb.commit()
                    mydb.close()

            def reject_bk():
                mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
                db = mydb.cursor()
                sn.append('Reject')
                sql = "INSERT INTO accrejdb VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                db.execute(sql, sn)
                sql = "DELETE FROM bookings WHERE cities=%s AND locations=%s AND bodyshopname=%s AND Phoneno=%s AND model=%s AND servicetype=%s AND userid=%s"
                sn.pop()
                db.execute(sql, sn)
                accbtn.destroy()
                rejbtn.destroy()
                Label(BK, text='Reject', font=('Arial', 10)).place(x=800, y=yco)
                mydb.commit()
                mydb.close()

            li = Label(BK, font=('Arial', 12))
            li.place(x=100, y=yco)
            li.configure(text='-'.join(sn))
            if (sn != "No New Bookings"):
                accbtn = Button(BK, text="Accept", font=('Arial 10'), command=accept_bk, width=10, height=1)
                accbtn.place(x=800, y=yco)
                rejbtn = Button(BK, text="Reject", font=('Arial 10'), command=reject_bk, width=10, height=1)
                rejbtn.place(x=900, y=yco)

        # def filtered():
        #     Bookings()
        #     if (filter.get() != "No filter"):
        #         sql = "SELECT * FROM Bookings where cities=%s"
        #         db.execute(sql, [filter.get()])
        #         _lst = [i for i in db]
        #         print(_lst)
        #         if (_lst):
        #             for i, j in zip(_lst, range(150, 1000, 50)):
        #                 s = []
        #                 for q in i:
        #                     s.append(q)
        #                 labes(s, j)
        #         else:
        #             labes("No New Bookings", 150)
        #         mydb.commit()
        #         mydb.close()
        #     else:
        #         sql = "SELECT * FROM Bookings"
        #         db.execute(sql)
        #         _lst = [i for i in db]
        #         if (_lst):
        #             for i, j in zip(_lst, range(150, 1000, 50)):
        #                 s = []
        #                 for q in i:
        #                     s.append(q)
        #                 labes(s, j)
        #         else:
        #             labes("No New Bookings", 150)
        #         mydb.commit()
        #         mydb.close()

        mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
        db = mydb.cursor()
        sql = "SELECT DISTINCT cities FROM bodyshops"
        db.execute(sql)
        cities = [i[0] for i in db]
        cities.append("No filter")
        mydb.commit()
        mydb.close()
        # OptionMenu(BK, filter, *cities,command=filtered).place(x=800, y=20)
        Button(BK, text="Exit", font=('Arial 10'), command=BK.destroy, width=10, height=1).place(x=900, y=20)
        Label(BK, text='Bookings', font=('Arial', 30)).place(x=100, y=50)
        mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
        db = mydb.cursor()

        sql = "SELECT * FROM Bookings"
        db.execute(sql)
        _lst = [i for i in db]
        if (_lst):
            for i, j in zip(_lst, range(150, 1000, 50)):
                s = []
                for q in i:
                    s.append(q)
                labes(s, j)
        else:
            labes("No New Bookings", 150)
        mydb.commit()
        mydb.close()
        BK.mainloop()

    Button(ah, text="Logout", font=('Arial 10'), command=ah.destroy, width=10, height=1).place(x=900, y=20)
    Button(ah, text="Show Places", font=('Arial 10'), command=display, width=10, height=1).place(x=800, y=20)
    Button(ah, text="Show Bookings", font=('Arial 10'), command=display2, width=10, height=1).place(x=700, y=20)
    Button(ah, text="Bookings", font=('Arial 10'), command=Bookings, width=10, height=1).place(x=600, y=20)
    Button(ah, text="Add Services", font=('Arial 10'), command=AddServices, width=10, height=1).place(x=500, y=20)
    Label(ah, text='ADD Body Shops', font=('Arial', 30)).place(x=400, y=170)
    signup_x = 300
    signup_y = 270

    Label(ah, text="Add city", font=('Arial', 16), width=12).place(x=signup_x, y=signup_y)
    Entry(ah, width=25, font=('Arial 16'), textvariable=city).place(x=signup_x + 180, y=signup_y)

    Label(ah, text="Add Locations", font=('Arial', 16), width=12).place(x=signup_x, y=signup_y + 50)
    Entry(ah, width=25, font=('Arial 16'), textvariable=loc).place(x=signup_x + 180, y=signup_y + 50)

    Label(ah, text="Add Shop", font=('Arial', 16), width=12).place(x=signup_x, y=signup_y + 100)
    Entry(ah, width=25, font=('Arial 16'), textvariable=shop).place(x=signup_x + 180, y=signup_y + 100)

    Button(ah, text="submit", font=('Arial 12'), command=ins, width=10, height=2).place(x=signup_x + 200,
                                                                                        y=signup_y + 150)

    ah.mainloop()


def registration():
    mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
    db = mydb.cursor()
    try:
        sql = "SELECT username FROM users"
        db.execute(sql)
        if str(hashlib.md5(username_s.get().encode()).hexdigest()) in [i[0] for i in db]:
            errmsg=Label(ws, text="*Username Taken", font=('Arial', 12), fg='#ff0000', bg='#012', width=20)
            errmsg.place(x=700, y=350)
            ws.after(3000, errmsg.destroy)
        else:
            sql = "INSERT INTO users VALUES(MD5(%s),MD5(%s))"
            val = (username_s.get(), password_s.get())
            if re.search('[A-Z]', val[1]) and re.search('[a-z]', val[1]) and re.search('[0-9]', val[1]) and re.search(
                    '[@_!#$%^&*()<>?/\|}{~:]', val[1]) and len(val[1]) >= 8:
                db.execute(sql, val)
                errmsg=Label(ws, text="*Registration Successful", font=('Arial', 12), fg='#00ff00', bg='#012', width=30)
                errmsg.place(x=700, y=350)
                ws.after(3000, errmsg.destroy)

            else:
                errmsg=Label(ws, text="*Weak Password Try Again", font=('Arial', 12), fg='#ff0000', bg='#012', width=30)
                errmsg.place(x=700, y=350)
                ws.after(3000, errmsg.destroy)

    except Exception as e:
        errmsg=Label(ws, text="*Registration Failed, Error Occured", font=('Arial', 12), fg='#ff0000', bg='#012', width=30)
        errmsg.place(x=700, y=430)
        ws.after(3000, errmsg.destroy)

    mydb.commit()
    mydb.close()


def validate():
    mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
    db = mydb.cursor()
    try:
        sql = "SELECT * FROM users"
        db.execute(sql)
        list_db = {}
        for i in db:
            list_db[i[0]] = i[1]
        if list_db.get(hashlib.md5(username_l.get().encode()).hexdigest(), '') == hashlib.md5(
                password_l.get().encode()).hexdigest():
            if hashlib.md5(username_l.get().encode()).hexdigest() == "9a7174d1cf08b61c7bf9cafe287f4dce" and hashlib.md5(
                    password_l.get().encode()).hexdigest() == "b7a84f4452aa9d48aa8c0f43073bbd8d":
                admin_home()
            else:
                user_home()
        else:
            errmsg=Label(ws, text="*Incorrect Username or Password", font=('Arial', 12), fg='#ff0000', bg='#012', width=30)
            errmsg.place(x=200, y=350)
            ws.after(3000, errmsg.destroy)
    except Exception as e:
        errmsg=Label(ws, text="*Error Encountered", font=('Arial', 12), fg='#ff0000', bg='#012', width=30)
        errmsg.place(x=350, y=450)
        ws.after(3000, errmsg.destroy)
    mydb.commit()
    mydb.close()


login_x = 80
login_y = 270
Label(ws, text='Car Wash Booking', font=('Arial', 30)).place(x=400, y=100)
# LOGIN
Label(ws, text='Login', width=15, font=('Arial', 18)).place(x=login_x + 150, y=200)

Label(ws, text="Username", font=('Arial', 16), width=10).place(x=login_x, y=login_y)
Entry(ws, width=25, font=('Arial 16'), textvariable=username_l).place(x=login_x + 150, y=login_y)
Label(ws, text="Password", font=('Arial', 16), width=10).place(x=login_x, y=login_y + 50)
Entry(ws, width=25, font=('Arial 16'), textvariable=password_l).place(x=login_x + 150, y=login_y + 50)
Button(ws, text="Login", font=('Arial 12'), command=validate, width=10, height=1).place(x=login_x + 200,
                                                                                        y=login_y + 130)
# SIGNUP
signup_x = 600
signup_y = 270
Label(ws, text='SignUp', width=15, font=('Arial', 18)).place(x=signup_x + 150, y=200)

Label(ws, text="Username", font=('Arial', 16), width=10).place(x=signup_x, y=signup_y)
Entry(ws, width=25, font=('Arial 16'), textvariable=username_s).place(x=signup_x + 150, y=signup_y)
Label(ws, text="Password", font=('Arial', 16), width=10).place(x=signup_x, y=signup_y + 50)
Entry(ws, width=25, font=('Arial 16'), textvariable=password_s).place(x=signup_x + 150, y=signup_y + 50)
Button(ws, text="SignUp", font=('Arial 12'), command=registration, width=10, height=1).place(x=signup_x + 200,
                                                                                             y=signup_y + 130)

ws.mainloop()
