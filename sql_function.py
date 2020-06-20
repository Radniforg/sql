import psycopg2 as pg

def create_test_db(conn):
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")
    cur.execute("INSERT INTO test (num, data) VALUES (100, 'bdd')")
    cur.execute("SELECT * FROM test;")
    print(cur.fetchone())


def create_db(conn): # создает таблицы
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS student (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gpa NUMERIC(10,2),
    birth TIMESTAMP WITH TIME ZONE
    )''');
    cur.execute('''CREATE TABLE IF NOT EXISTS course (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
    )''');
    cur.execute('''CREATE TABLE IF NOT EXISTS student_course (
    student_id INTEGER REFERENCES student(id),
    course_id INTEGER REFERENCES course(id),
    CONSTRAINT student_course_pk PRIMARY KEY(student_id, course_id)
    )''');
    print('Tables created')


def get_students(course_id, conn): # возвращает студентов определенного курса
    cur = conn.cursor()
    cur.execute("""select s.id, s.name, c.name from student_course sc
    join student s on s.id = sc.student_id
    join course c on c.id = sc.course_id
    """)
    fetch = cur.fetchall()
    current_course = []
    for student in fetch:
        if student[0] == int(course_id):
            current_course.append(student)
    return current_course

def add_student(student, conn): # просто создает студента
    cur = conn.cursor()
    cur.execute("INSERT INTO student (name, gpa, birth) VALUES (%s, %s, %s)",
                (student['name'], student['gpa'], student['birth']))

def add_students(course_id, students, conn): # создает студентов и записывает их на курс
    cur = conn.cursor()
    count_check = 0
    cur.execute("SELECT * FROM course;")
    course_time = cur.fetchall()
    try:
        for course in course_time:
            if int(course[0]) == int(course_id):
                count_check = 1
                print('check')
        if count_check == 0:
            cur.execute("INSERT INTO course (id, name) VALUES (%s, %s)",
                        (course_id, 'temp_name'))
    except IndexError:
        cur.execute("INSERT INTO course (id, name) VALUES (%s, %s)",
                    (course_id, 'temp_name'))
    for student in students:
        cur.execute("INSERT INTO student (name, gpa, birth) VALUES (%s, %s, %s)",
                (student['name'], student['gpa'], student['birth']))
        cur.execute('SELECT LASTVAL()')
        temp_id = cur.fetchone()[0]
        cur.execute("INSERT INTO student_course (student_id, course_id) VALUES (%s, %s)",
                    (temp_id, course_id))


def get_student(student_id, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM student;")
    for student in cur.fetchall():
        if student[0] == int(student_id):
            return student
    return 'Student not found'


def restart(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE student_course")
    cur.execute("DROP TABLE student")
    cur.execute("DROP TABLE course")


with pg.connect(database = 'test', user = 'test', password = '1234') as connection:
    #restart(connection)
    create_db(connection)
    students = [{'name': 'Train', 'gpa': '3.6', 'birth': '1998-05-31 09:26:56.66 +02:00'},
                {'name': 'Max', 'gpa': '4.3', 'birth': '1996-03-14 09:26:56.66 +02:00'}]
    add_students(1, students, connection)
    print(get_students(1, connection))
    # add_student(students[0], connection)
    # print(get_student('1', connection))