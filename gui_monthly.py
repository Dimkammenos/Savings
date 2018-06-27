from tkinter import *

root = Tk()
app = Frame(root)
app.grid()
root.title('Διαχείρηση χρημάτων')
root.geometry('600x450')
root.maxsize(680,300)
root.minsize(680,300)

def submit():
    years = ['Ιανουάριος', 'Φεβρουάριος', 'Μάρτιος', 'Απρίλιος',
     'Μάϊος', 'Ιούνιος', 'Ιούλιος', 'Αύγουστος',
      'Σεπτέβριος', 'Οκτώβριος', 'Νοέμβριος', 'Δεκέμβριος']
    global year, month, salary, spare, electricity, water, rent
    while True:
        y = year.get()
        m = month.get()
        s = salary.get()
        sp = spare.get()
        el = electricity.get()
        w = water.get()
        r = rent.get()
        try:
            y = int (y)
            m = int(m)
            s = float(s)
            sp = float(sp)
            el = float(el)
            w = float(w)
            r = float(r)

            bills = el + w
            if s < bills:
                food = 0
                forfun = 0
                education = 0
                save = -el -w - r +sp + s
            else:
                food = (s * 0.5) - r - ((el + w) / 2)
                education = s * 0.1
                forfun = (s * 0.1) - ((el + w) / 2)
                save = (s * 0.3) + sp

            a = Toplevel(app)
            a.title(years[m - 1])
            Label(a,text = '    \tΜπορείς να χρησιμοποιήσεις για:\n').grid(row = 1, column = 3)
            Label(a,text = 'Φαγητό:').grid(row = 2, column = 3)
            Label(a,text = food, justify = 'left').grid(row = 2, column = 4)
            Label(a,text = 'Διασκέδαση:').grid(row = 3, column = 3)
            Label(a,text = forfun, justify = 'left').grid(row = 3, column = 4)
            Label(a,text = 'Εκπαίδευση:').grid(row = 4, column = 3)
            Label(a,text = education, justify = 'left').grid(row = 4, column = 4)
            Label(a,text = 'Αποταμίευση:').grid(row = 5, column = 3)
            Label(a,text = save, justify = 'left').grid(row = 5, column = 4)
            def quit():
                a.destroy()
            def saving():
                import xml.etree.ElementTree as ET
                import sqlite3
                import sys
                year = str(y)
                conn = sqlite3.connect('monthly'+year+'.db')
                cur = conn.cursor()

                cur.execute('''CREATE TABLE if NOT EXISTS `year_income` (
                	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                	`month`	INTEGER NOT NULL,
                	`income`	INTEGER NOT NULL,
                	`rent`	INTEGER NOT NULL,
                	`electricity`	INTEGER NOT NULL,
                	`water`	INTEGER NOT NULL,
                	`Savings`	INTEGER NOT NULL,
                	`Spare`	INTEGER NOT NULL
                );
                ''')
                try:
                    cur.execute('''SELECT id from year_income group by id having month = ?''', (m ,))
                    second =cur.fetchall()
                    if not second:
                        cur.execute('''SELECT id from year_income group by id ''')
                        mon =cur.fetchall()
                        mont = list()
                        for m1 in mon:
                            mont += m1
                            id= max(mont)
                    else:
                        s1 = list()
                        for x in second:
                            s1 += x
                            id = max(s1)
                    cur.execute('''SELECT savings FROM year_income where id = ?''', (id ,))
                    old_sav =  float(cur.fetchone()[0])
                    new_sav = old_sav + save

                    cur.execute("""INSERT INTO year_income(month, income, rent, electricity, water,
                        savings,spare)
                         VALUES (?,?,?,?,?,?,?)""", (m, s, r, el, w, new_sav, sp ))

                except:
                    cur.execute("""INSERT INTO year_income(month, income, rent, electricity, water,
                        savings,spare)
                         VALUES (?,?,?,?,?,?,?)""", (m, s, r, el, w, save ,sp ))

                conn.commit()
                cur.close()
                a.destroy()

            Button(a, text = 'Αποθήκευση', command = saving, width = 15, height = 1).grid(row = 7, column = 3)
            Button(a, text = 'Επανάληψη', command = quit, width = 15, height = 1).grid(row = 7, column = 4)

            Label(a, text= '\t').grid(row = 6, column = 1)
            a.maxsize(480,200)
            a.minsize(480,200)
            break

        except:
            a = Toplevel(app)
            a.title('Πρόβλημα')
            a.geometry('320x150')
            Label(a,text = '\n Λάθος στοιχεία!!\t\n').grid(row = 1, column = 1)
            Label(a, text = '  Παρακαλώ ελέγξτε εκ νέου τα στοιχεία').grid(row = 2, column = 1)
            Label(a, text = 'που δώσατε. Χρησιμοποιείστε μόνο αριθμούς!!').grid(row = 3, column = 1)
            def quit():
                a.destroy()
            Button(a, text = 'Εντάξει', command = quit, width = 15, height = 1).grid(row = 5, column = 1)
            Label(a, text= '\t').grid(row = 4, column = 0)
            a.maxsize(370,175)
            a.minsize(370,175)
            break
#Buttons
Button(app, text = 'Υπολογισμός', width = 25, height = 2, bg = 'yellow', command = submit).grid(row = 10, column = 4)


#Labels
Label(app,text = '\tΈτος  ').grid(row = 2, column = 2)
Label(app,text = '\tΜήνας  ').grid(row = 2, column = 4)
Label(app,text = '\tΥπόλοιπο  ').grid(row = 4, column = 2)
Label(app,text = '\tΜισθός  ').grid(row = 4, column = 4)
Label(app,text = '\tΕνοίκιο  ').grid(row = 6, column = 2)
Label(app,text = '\tΛογ. Ρεύματος  ').grid(row = 6, column = 4)
Label(app,text = '\tΛογ. Νερού  ').grid(row = 8, column = 2)
Label(app,text = '').grid(row = 1, column = 1)
Label(app,text = '').grid(row = 3, column = 1)
Label(app,text = '').grid(row = 5, column = 1)
Label(app,text = '').grid(row = 7, column = 1)
Label(app,text = '').grid(row = 9, column = 1)
#Label(app,text = '\n\n').grid(row=13, column = 1)
#Label(app,text = 'Copywrite Dimitris Kammenos').grid(row=14,column =4)

#Entry
year = Entry(app)
year.grid(row = 2,column = 3)
month = Entry(app)
month.grid(row = 2,column = 5)
spare = Entry(app)
spare.grid(row = 4,column = 3)
salary = Entry(app)
salary.grid(row = 4,column = 5)
rent = Entry(app)
rent.grid(row = 6,column = 3)
electricity = Entry(app)
electricity.grid(row = 6,column = 5)
water = Entry(app)
water.grid(row = 8,column = 3)
#end of program
root.mainloop()
