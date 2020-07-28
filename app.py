from flask import Flask, render_template, request, redirect, send_file, url_for
import mysql.connector
import json
import datetime

puples = ['Иванов', 'Петров', 'Сидоров']
count = 0
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd=password,
    database=database)
app = Flask(__name__)

login = 0
password = 0


@app.route('/', methods=['POST', 'GET'])
def index():
    global login
    global count
    global password
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM учителя')
        myresult = mycursor.fetchall()
        for row in myresult:
            if login == row[1] and password == row[2]:
                filename = 'opros.txt'
                f = open(filename, 'r')
                opr = []
                for line in f:
                    opr.append(line.rstrip("\n"))

                opr[1] = opr[1].split('#')
                filename = 'black_list.txt'
                black_list = []
                out = open(filename)
                for line in out:
                    black_list.append(line.rstrip('\n'))

                votes = {}
                filename = 'opros.txt'
                f = open(filename)
                a = 0
                for line in f:
                    a += 1
                    m = line.split('#')
                    if a == 2:
                        for i in range(len(m)):
                            if i != len(m) - 1:
                                votes[m[i]] = 0
                            else:
                                votes[m[i][0:-1]] = 0

                filename = 'data.txt'
                golosa = 0
                f = open(filename, 'r')
                for line in f:
                    vote = line.rstrip("\n")
                    votes[vote] += 1
                    golosa += 1

                return render_template('admin.html', count=count, golosa=golosa, votes=votes, opr=opr, login=login, black_list=black_list)
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM ученики')
        myresult = mycursor.fetchall()
        for row in myresult:
            if login == row[0] and password == row[1]:
                filename = 'opros.txt'
                f = open(filename, 'r')
                opr = []
                for line in f:
                    opr.append(line.rstrip("\n"))

                opr[1] = opr[1].split('#')
                filename = 'black_list.txt'
                black_list = []
                out = open(filename)
                for line in out:
                    black_list.append(line.rstrip('\n'))

                votes = {}
                filename = 'opros.txt'
                f = open(filename)
                a = 0
                for line in f:
                    a += 1
                    m = line.split('#')
                    if a == 2:
                        for i in range(len(m)):
                            if i != len(m) - 1:
                                votes[m[i]] = 0
                            else:
                                votes[m[i][0:-1]] = 0

                filename = 'data.txt'
                golosa = 0
                f = open(filename, 'r')
                for line in f:
                    vote = line.rstrip("\n")
                    votes[vote] += 1
                    golosa += 1
                return render_template('uchenik.html', golosa=golosa, votes=votes, opr=opr, login=login, black_list=black_list)
        return render_template('404error.html')
    else:
        return render_template('index.html')


@app.route('/opros_update', methods=['POST', 'GET'])
def update_opros():
    if request.method == 'POST':
        with open('opros.txt', 'wb'):
            pass
        with open('data.txt', 'wb'):
            pass
        with open('black_list.txt', 'wb'):
            pass
        var = request.form['var']
        vid = request.form['vid']
        title = request.form['title']

        f = open('opros.txt', 'w')
        f.write(title + '\n')
        f.write(var + '\n')
        f.write(vid + '\n')

        filename = 'opros.txt'
        f = open(filename, 'r')
        opr = []
        for line in f:
            opr.append(line.rstrip("\n"))

        opr[1] = opr[1].split()
        filename = 'black_list.txt'
        black_list = []
        out = open(filename)
        for line in out:
            black_list.append(line.rstrip('\n'))

        votes = {}
        filename = 'opros.txt'
        f = open(filename)
        a = 0
        for line in f:
            a += 1
            v = line.rstrip("\n")
            if a == 2:
                for i in line.split('#'):
                    votes[i] = 0

        filename = 'data.txt'
        golosa = 0
        f = open(filename, 'r')
        for line in f:
            vote = line.rstrip("\n")
            votes[vote] += 1
            golosa += 1

        return render_template('admin.html', golosa=golosa, votes=votes, login=login, opr=opr, black_list=black_list)
    else:
        opros = []
        f = open('opros.txt', 'r')
        for line in f:
            vote = line.rstrip("\n")
            opros.append(vote)
        return render_template('opros_update.html', opros=opros)

@app.route('/opros', methods=['GET'])
def opros():
    global count
    filename = 'data.txt'
    ans = request.args.get('field')

    out = open(filename, 'a')
    out.write(ans + '\n')
    out.close()

    filename = 'black_list.txt'
    out = open(filename, 'a')
    out.write(str(login) + '\n')
    out.close()

    filename = 'black_list.txt'
    black_list = []
    out = open(filename)
    for line in out:
        black_list.append(line.rstrip('\n'))

    votes = {}
    filename = 'opros.txt'
    f = open(filename)
    a = 0
    for line in f:
        a += 1
        v = line.rstrip("\n")
        m = line.split('#')
        if a == 2:
            for i in range(len(m)):
                if i != len(m) - 1:
                    votes[m[i]] = 0
                else:
                    votes[m[i][0:-1]] = 0
    print(votes)
    filename = 'data.txt'
    golosa = 0
    f = open(filename, 'r')
    for line in f:
        vote = line.rstrip("\n")
        votes[vote] += 1
        golosa += 1
    filename = 'opros.txt'
    f = open(filename, 'r')
    opr = []
    for line in f:
        opr.append(line.rstrip("\n"))
    opr[1] = opr[1].split('#')
    return render_template('admin.html',  golosa=golosa, opr=opr, votes=votes, black_list=black_list, login=login)


def proverka():
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM учителя')
    myresult = mycursor.fetchall()
    for row in myresult:
        if login == row[1] and password == row[2]:
            return True


@app.route('/jurnal', methods=['POST', 'GET'])
def jurnal():
    if proverka():
        if request.method == 'POST':
            lessons = ['алгебра', 'русский']
            puples = ['Иванов', 'Петров', 'Сидоров']
            vid = request.form['mark']
            if vid in lessons:
                dates = []
                mycursor = mydb.cursor()
                mycursor.execute('SELECT * FROM оценки')
                myresult = mycursor.fetchall()
                print(myresult)
                for row in myresult:
                    if int(row[1]) not in dates and row[0] == vid:
                        dates.append(int(row[1]))
                dates.sort()
                ocenki = {}
                itogs = []
                for name in puples:
                    ocenki[name] = {}
                    ocenki[name]['itog'] = 0
                    s = 0
                    for date in dates:
                        mycursor = mydb.cursor()
                        mycursor.execute("SELECT * FROM оценки")
                        myresult = mycursor.fetchall()
                        print(myresult)
                        for row in myresult:
                            if int(row[1]) == date and row[2] == name and row[0] == vid:
                                ocenki[name][date] = row[3]
                    print(ocenki)
                    a = 0
                    for row in ocenki[name]:
                        if row != 'itog' and 'н' not in ocenki[name][row] and 'б' not in ocenki[name][row]:
                            ocenki[name]['itog'] += int(ocenki[name][row])
                            a += 1
                    if a != 0:
                        ocenki[name]['itog'] = ocenki[name]['itog'] // a
                    itogs.append(ocenki[name]['itog'])
                    print(itogs)
                with open('static/graffik.json', 'w') as file:
                    json.dump(itogs, file, indent=2, ensure_ascii=False)
                return render_template('jurnal_table.html', dates=dates, puples=puples, ocenki=ocenki, login=vid)
            else:
                dates = []
                lessons = ['алгебра', 'русский']
                marks = {}
                itogs = []
                for lesson in lessons:
                    marks[lesson] = {}
                    marks[lesson]['itog'] = 0
                mycursor = mydb.cursor()
                mycursor.execute('SELECT * FROM оценки')
                myresult = mycursor.fetchall()
                for row in myresult:
                    if row[1] not in dates:
                        dates.append(row[1])
                dates.sort()
                mycursor = mydb.cursor()
                mycursor.execute('SELECT * FROM оценки')
                myresult = mycursor.fetchall()
                for lesson in lessons:
                    for date in dates:
                        for row in myresult:
                            if row[1] == date and row[0] == lesson and row[2] == vid:
                                marks[lesson][date] = row[3]
                    a = 0
                    for row in marks[lesson]:
                        if row != 'itog' and 'н' not in marks[lesson][row] and 'б' not in marks[lesson][row]:
                            marks[lesson]['itog'] += int(marks[lesson][row])
                            a += 1
                    if a != 0:
                        marks[lesson]['itog'] = marks[lesson]['itog'] // a
                    itogs.append(marks[lesson]['itog'])
                    print(itogs)

                with open('static/graffik.json', 'w') as file:
                    json.dump(itogs, file, indent=2, ensure_ascii=False)
                return render_template('table_marks_uchenik.html', login=vid, lessons=lessons, marks=marks,
                                       dates=dates)

        else:
            return render_template('jurnal.html', login=login)
    else:
        return render_template('404error.html')


@app.route('/mark', methods=['POST', 'GET'])
def mark():
    if proverka():
        if request.method == 'POST':
            date = request.form['date']
            family = request.form['family']
            mark = request.form['mark']
            mycursor = mydb.cursor()
            q = 'SELECT * FROM оценки'
            mycursor.execute(q)
            myr = mycursor.fetchall()
            print(myr)
            if len(myr) > 0:
                for row in range(len(myr)):
                    if myr[row][0] == login and myr[row][1] == date and myr[row][2] == family:
                        sql = "UPDATE оценки SET оценка=" + mark + " WHERE дата = '" + date + "' AND фамилия = '" + family + "' AND предмет = '" + login + "'"
                        # sql = "DELETE FROM оценки WHERE дата = 19"
                        mycursor.execute(sql)
                        mydb.commit()
                        break
                    else:
                        if row == len(myr) - 1:
                            mycursor = mydb.cursor()
                            vstavka = 'INSERT INTO оценки (предмет, дата, фамилия, оценка) VALUES (%s, %s, %s, %s)'
                            mycursor.execute(vstavka, (login, date, family, mark))
                            mydb.commit()
            else:
                mycursor = mydb.cursor()
                vstavka = 'INSERT INTO оценки (предмет, дата, фамилия, оценка) VALUES (%s, %s, %s, %s)'
                mycursor.execute(vstavka, (login, date, family, mark))
                mydb.commit()
            return redirect('jurnal_table')
        elif request.method == 'GET':
            return render_template('mark.html', data=datetime.datetime.now().date())
    else:
        return render_template('404error.html')


@app.route('/jurnal_table')
def open_jurnal():
    if proverka():
        dates = []
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM оценки')
        myresult = mycursor.fetchall()
        print(myresult)
        for row in myresult:
            if int(row[1]) not in dates and row[0] == login:
                dates.append(int(row[1]))
        dates.sort()
        ocenki = {}
        itogs = []
        for name in puples:
            ocenki[name] = {}
            ocenki[name]['itog'] = 0
            for date in dates:
                mycursor = mydb.cursor()
                mycursor.execute("SELECT * FROM оценки")
                myresult = mycursor.fetchall()
                print(myresult)
                for row in myresult:
                    if int(row[1]) == date and row[2] == name and row[0] == login:
                        ocenki[name][date] = row[3]
            print(ocenki)
            a = 0
            for row in ocenki[name]:
                if row != 'itog' and 'н' not in ocenki[name][row] and 'б' not in ocenki[name][row]:
                    ocenki[name]['itog'] += int(ocenki[name][row])
                    a += 1
            if a != 0:
                ocenki[name]['itog'] = ocenki[name]['itog'] // a
            itogs.append(ocenki[name]['itog'])
            print(itogs)
        with open('static/graffik.json', 'w') as file:
            json.dump(itogs, file, indent=2, ensure_ascii=False)
        return render_template('jurnal_table.html', dates=dates, puples=puples, ocenki=ocenki, login=login)
    else:
        return render_template('404error.html')


@app.route('/material')
def material():
    return render_template('material.html')


@app.route('/raspisanie', methods=['POST', 'GET'])
def raspisanie():
    if request.method == 'POST':
        d1l1 = request.form['1d-1l']
        d2l1 = request.form['2d-1l']
        d3l1 = request.form['3d-1l']
        d4l1 = request.form['4d-1l']
        d5l1 = request.form['5d-1l']
        d6l1 = request.form['6d-1l']

        d1l2 = request.form['1d-2l']
        d2l2 = request.form['2d-2l']
        d3l2 = request.form['3d-2l']
        d4l2 = request.form['4d-2l']
        d5l2 = request.form['5d-2l']
        d6l2 = request.form['6d-2l']

        d1l3 = request.form['1d-3l']
        d2l3 = request.form['2d-3l']
        d3l3 = request.form['3d-3l']
        d4l3 = request.form['4d-3l']
        d5l3 = request.form['5d-3l']
        d6l3 = request.form['6d-3l']

        d1l4 = request.form['1d-4l']
        d2l4 = request.form['2d-4l']
        d3l4 = request.form['3d-4l']
        d4l4 = request.form['4d-4l']
        d5l4 = request.form['5d-4l']
        d6l4 = request.form['6d-4l']

        d1l5 = request.form['1d-5l']
        d2l5 = request.form['2d-5l']
        d3l5 = request.form['3d-5l']
        d4l5 = request.form['4d-5l']
        d5l5 = request.form['5d-5l']
        d6l5 = request.form['6d-5l']

        d1l6 = request.form['1d-6l']
        d2l6 = request.form['2d-6l']
        d3l6 = request.form['3d-6l']
        d4l6 = request.form['4d-6l']
        d5l6 = request.form['5d-6l']
        d6l6 = request.form['6d-6l']
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM расписание')
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            sqlFormula = 'INSERT INTO расписание (понедельник, вторник, среда, четверг, пятница, суббота) VALUES (%s, %s, %s, %s, %s, %s)'
            mycursor.execute(sqlFormula, (d1l1, d2l1, d3l1, d4l1, d5l1, d6l1))
            mycursor.execute(sqlFormula, (d1l2, d2l2, d3l2, d4l2, d5l2, d6l2))
            mycursor.execute(sqlFormula, (d1l3, d2l3, d3l3, d4l3, d5l3, d6l3))
            mycursor.execute(sqlFormula, (d1l4, d2l4, d3l4, d4l4, d5l4, d6l4))
            mycursor.execute(sqlFormula, (d1l5, d2l5, d3l5, d4l5, d5l5, d6l5))
            mycursor.execute(sqlFormula, (d1l6, d2l6, d3l6, d4l6, d5l6, d6l6))
            mydb.commit()
            try:
                return redirect('/raspisanie')
            except:
                return 'Ошибка'
        else:
            mycursor.execute('DELETE FROM расписание WHERE id < 10000000000')
            sqlFormula = 'INSERT INTO расписание (понедельник, вторник, среда, четверг, пятница, суббота) VALUES (%s, %s, %s, %s, %s, %s)'
            mycursor.execute(sqlFormula, (d1l1, d2l1, d3l1, d4l1, d5l1, d6l1))
            mycursor.execute(sqlFormula, (d1l2, d2l2, d3l2, d4l2, d5l2, d6l2))
            mycursor.execute(sqlFormula, (d1l3, d2l3, d3l3, d4l3, d5l3, d6l3))
            mycursor.execute(sqlFormula, (d1l4, d2l4, d3l4, d4l4, d5l4, d6l4))
            mycursor.execute(sqlFormula, (d1l5, d2l5, d3l5, d4l5, d5l5, d6l5))
            mycursor.execute(sqlFormula, (d1l6, d2l6, d3l6, d4l6, d5l6, d6l6))
            mydb.commit()
            try:
                return redirect('/raspisanie')
            except:
                return 'Ошибка'


    else:
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM расписание')
        myresult = mycursor.fetchall()
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM темы')
        articles = mycursor.fetchall()
        articles1 = []
        for i in articles:
            if i[5] == login:
                articles1.append(i)
        return render_template('raspisanie.html', myresult=myresult, articles=articles1)


@app.route('/raspisanie_uchenik')
def raspisanie_uchenik():
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM расписание')
    myresult = mycursor.fetchall()
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM темы')
    myresult1 = mycursor.fetchall()
    return render_template('raspisanie_uchenik.html', myresult1=myresult1, myresult=myresult)


@app.route('/add_tema', methods=['POST', 'GET'])
def add_tema():
    if request.method == 'POST':
        data = request.form['data']
        title = request.form['title']
        classn = request.form['class']
        home = request.form['home']

        mycursor = mydb.cursor()
        sqlFormula = "INSERT INTO темы (дата, тема, классная, домашняя, предмет) VALUES (%s, %s, %s, %s, %s)"
        mycursor.execute(sqlFormula, (data, title, classn, home, login))
        mydb.commit()
        try:
            return redirect('/raspisanie')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('add_tema.html')


# @app.route('/all_raspisanie')
# def all_raspisanie():
#    mycursor = mydb.cursor()
#    mycursor.execute('SELECT * FROM темы')
#    articles = mycursor.fetchall()
#    articles1 = []
#    for i in articles:
#        if i[5] == login:
#            articles1.append(i)
#    return render_template('all_raspisanie.html', articles=articles1)


@app.route('/all_raspisanie/<int:id>/del')
def tema_delete(id):
    mycursor = mydb.cursor()
    sql = "DELETE FROM темы WHERE id=" + str(id)
    mycursor.execute(sql)
    mydb.commit()
    try:
        return redirect('/raspisanie')
    except:
        return 'При удалении статьи произошла ошибка'


@app.route('/all_raspisanie/<int:id>/update', methods=['POST', 'GET'])
def tema_update(id):
    if request.method == 'POST':
        mycuror = mydb.cursor()
        data = request.form['data']
        title = request.form['title']
        classn = request.form['class']
        home = request.form['home']
        sql = "UPDATE темы SET дата = '" + str(data) + "' WHERE id = " + str(id)
        sql1 = "UPDATE темы SET тема = '" + str(title) + "' WHERE id = " + str(id)
        sql2 = "UPDATE темы SET классная = '" + str(classn) + "' WHERE id = " + str(id)
        sql3 = "UPDATE темы SET домашняя = '" + str(home) + "' WHERE id = " + str(id)
        mycuror.execute(sql)
        mycuror.execute(sql1)
        mycuror.execute(sql2)
        mycuror.execute(sql3)
        mydb.commit()
        try:
            return redirect('/raspisanie')
        except:
            return 'При редактировании статьи произошла ошибка'
    else:
        sql = 'SELECT * FROM темы WHERE id=' + str(id)
        mycuror = mydb.cursor()
        mycuror.execute(sql)
        myresult = mycuror.fetchall()
        result = myresult[0]
        return render_template('update_tema.html', result=result)


@app.route('/raspol_uchenik', methods=['POST', 'GET'])
def raspol_uchenik():
    if request.method == 'POST':
        r1p1 = request.form['1r-1part']
        r2p1 = request.form['2r-1part']
        r3p1 = request.form['3r-1part']
        r1p2 = request.form['1r-2part']
        r2p2 = request.form['2r-2part']
        r3p2 = request.form['3r-2part']
        r1p3 = request.form['1r-3part']
        r2p3 = request.form['2r-3part']
        r3p3 = request.form['3r-3part']
        r1p4 = request.form['1r-4part']
        r2p4 = request.form['2r-4part']
        r3p4 = request.form['3r-4part']
        r1p5 = request.form['1r-5part']
        r2p5 = request.form['2r-5part']
        r3p5 = request.form['3r-5part']
        r1p6 = request.form['1r-6part']
        r2p6 = request.form['2r-6part']
        r3p6 = request.form['3r-6part']
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM рассадка')
        myresult = mycursor.fetchall()
        sqlFormula = 'INSERT INTO рассадка (1ряд, 2ряд, 3ряд) VALUES (%s, %s, %s)'
        mycursor.execute(sqlFormula, (r1p1, r2p1, r3p1))
        mycursor.execute(sqlFormula, (r1p2, r2p2, r3p2))
        mycursor.execute(sqlFormula, (r1p3, r2p3, r3p3))
        mycursor.execute(sqlFormula, (r1p4, r2p4, r3p4))
        mycursor.execute(sqlFormula, (r1p5, r2p5, r3p5))
        mycursor.execute(sqlFormula, (r1p6, r2p6, r3p6))
        mydb.commit()
        try:
            return redirect('/')
        except:
            return 'При добавлении расписания произошла ошибка!'

    else:
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM рассадка')
        myresult = mycursor.fetchall()
        if len(myresult) == 0 and login == 'классная' and password == '3':
            return render_template('raspol_uchenik.html')
        else:
            return render_template('raspol.html', myresult=myresult, login=login, password=password)


@app.route('/jurnal_uchenik', methods=['POST', 'GET'])
def jurnal_uchenika():
    dates = []
    lessons = ['алгебра', 'русский']
    marks = {}
    itogs = []
    for lesson in lessons:
        marks[lesson] = {}
        marks[lesson]['itog'] = 0
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM оценки')
    myresult = mycursor.fetchall()
    for row in myresult:
        if row[1] not in dates:
            dates.append(row[1])
    dates.sort()
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM оценки')
    myresult = mycursor.fetchall()
    for lesson in lessons:
        for date in dates:
            for row in myresult:
                if row[1] == date and row[0] == lesson and row[2] == login:
                    marks[lesson][date] = row[3]
        a = 0
        for row in marks[lesson]:
            if row != 'itog' and 'н' not in marks[lesson][row] and 'б' not in marks[lesson][row]:
                marks[lesson]['itog'] += int(marks[lesson][row])
                a += 1
        if a != 0:
            marks[lesson]['itog'] = marks[lesson]['itog'] // a
        itogs.append(marks[lesson]['itog'])
        print(itogs)


    with open('static/graffik.json', 'w') as file:
        json.dump(itogs, file, indent=2, ensure_ascii=False)
    return render_template('table_marks_uchenik.html', login=login, lessons=lessons, marks=marks, dates=dates)


@app.route('/update_raspol', methods=['POST', 'GET'])
def raspol_up():
    if request.method == 'POST':
        mycursor = mydb.cursor()
        sql = 'DELETE FROM рассадка WHERE id<1000000'
        mycursor.execute(sql)
        mydb.commit()
        r1p1 = request.form['1r-1part']
        r2p1 = request.form['2r-1part']
        r3p1 = request.form['3r-1part']
        r1p2 = request.form['1r-2part']
        r2p2 = request.form['2r-2part']
        r3p2 = request.form['3r-2part']
        r1p3 = request.form['1r-3part']
        r2p3 = request.form['2r-3part']
        r3p3 = request.form['3r-3part']
        r1p4 = request.form['1r-4part']
        r2p4 = request.form['2r-4part']
        r3p4 = request.form['3r-4part']
        r1p5 = request.form['1r-5part']
        r2p5 = request.form['2r-5part']
        r3p5 = request.form['3r-5part']
        r1p6 = request.form['1r-6part']
        r2p6 = request.form['2r-6part']
        r3p6 = request.form['3r-6part']
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM рассадка')
        myresult = mycursor.fetchall()
        sqlFormula = 'INSERT INTO рассадка (1ряд, 2ряд, 3ряд) VALUES (%s, %s, %s)'
        mycursor.execute(sqlFormula, (r1p1, r2p1, r3p1))
        mycursor.execute(sqlFormula, (r1p2, r2p2, r3p2))
        mycursor.execute(sqlFormula, (r1p3, r2p3, r3p3))
        mycursor.execute(sqlFormula, (r1p4, r2p4, r3p4))
        mycursor.execute(sqlFormula, (r1p5, r2p5, r3p5))
        mycursor.execute(sqlFormula, (r1p6, r2p6, r3p6))
        mydb.commit()
        try:
            return redirect('/raspol_uchenik')
        except:
            return 'При добавлении расписания произошла ошибка!'
    else:
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM рассадка')
        myresult = mycursor.fetchall()

        return render_template('update_raspol.html', mesta=myresult)


if __name__ == '__main__':
    app.run(debug=True)
