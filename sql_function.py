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
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
    )''');

def get_students(course_id, conn): # возвращает студентов определенного курса
    pass

def add_students(course_id, students, conn): # создает студентов и
                                       # записывает их на курс
    pass


def add_student(student, conn): # просто создает студента
    for
    cur = conn.cursor()
    cur.execute("INSERT INTO student (name, gpa, birth) VALUES (student['name'], "
                "student['gpa'], student['birth'])");

def get_student(student_id, conn):
    pass


with pg.connect(database = 'test', user = 'test', password = '1234') as connection:
    create_db(connection)