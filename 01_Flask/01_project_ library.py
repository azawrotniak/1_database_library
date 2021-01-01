from flask import Flask, request, render_template
from psycopg2 import connect, OperationalError
from psycopg2._psycopg import ProgrammingError
import datetime

app = Flask(__name__)

username = "postgres"
password = "coderslab"
hostname = "localhost"
database = "library_db"


def execute_sql(sql_code, parametr=None):
    try:
        conn = connect(
            user=username, password=password, host=hostname, database=database
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql_code, (parametr,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
    except OperationalError as err:
        print('err')
    except ProgrammingError as err:
        print('err')
    return results


def search_id_client(sql_code, first_name, last_name):
    try:
        conn = connect(
            user=username, password=password, host=hostname, database=database
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql_code, (first_name, last_name))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
    except OperationalError as err:
        print('err')
    except ProgrammingError as err:
        print('err')
    return results


def delete_item(sql_code, id):
    try:
        conn = connect(
            user=username, password=password, host=hostname, database=database
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql_code, (id,))
        cursor.close()
        conn.close()
    except OperationalError as err:
        print('err')
    except ProgrammingError:
        print('No results')


def add_book(sql_code, ISBN, name, description):
    try:
        conn = connect(
            user=username, password=password, host=hostname, database=database
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql_code, (ISBN, name, description))
        cursor.close()
        conn.close()
    except OperationalError as err:
        print(err)
    except ProgrammingError:
        print('No results')


def add_client(sql_code, first_name, last_name):
    try:
        conn = connect(
            user=username, password=password, host=hostname, database=database
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql_code, (first_name, last_name))
        cursor.close()
        conn.close()
    except OperationalError as err:
        print(err)
    except ProgrammingError:
        print('No results')


def add_author(sql_code, name):
    try:
        conn = connect(
            user=username, password=password, host=hostname, database=database
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql_code, (name,))
        cursor.close()
        conn.close()
    except OperationalError as err:
        print(err)
    except ProgrammingError:
        print('No results')


def add_category(sql_code, name):
    try:
        conn = connect(
            user=username, password=password, host=hostname, database=database
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql_code, (name,))
        cursor.close()
        conn.close()
    except OperationalError as err:
        print(err)
    except ProgrammingError:
        print('No results')


def loan_book(sql_code, id_book, id_client, loan_date):
    try:
        conn = connect(
            user=username, password=password, host=hostname, database=database
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql_code, (id_book, id_client, loan_date))
        cursor.close()
        conn.close()
    except OperationalError as err:
        print(err)
    except ProgrammingError:
        print('No results')


def return_book(sql_code, return_date, id):
    try:
        conn = connect(
            user=username, password=password, host=hostname, database=database
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql_code, (return_date, id))
        cursor.close()
        conn.close()
    except OperationalError as err:
        print(err)
    except ProgrammingError:
        print('No results')


def update_book_loan(sql_code, id_client, id_book):
    try:
        conn = connect(
            user=username, password=password, host=hostname, database=database
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql_code, (id_client, id_book))
        cursor.close()
        conn.close()
    except OperationalError as err:
        print(err)
    except ProgrammingError:
        print('No results')


@app.route('/', methods=['GET'])
def display_main():
    return render_template('main.html')


@app.route('/books', methods=['GET'])
def display_books():
    sql_code = """select b.id, b.name as Tytuł, b.description as Opis, a.name as author, c.name as Kategoria from book b 
        left join author a on a.id=b.id_author 
        left join book_category bc ON bc.id_book =b.id
        left join category c on bc.id_category = c.id
        order by b.id;"""
    book_list = execute_sql(sql_code)
    return render_template('books.html', books=book_list)


@app.route('/clients', methods=['GET'])
def display_clients():
    sql_code = 'select * from client;'
    client_list = execute_sql(sql_code)
    print(client_list)
    return render_template('clients.html', clients=client_list)


@app.route('/authors', methods=['GET'])
def display_authors():
    sql_code = 'select * from author;'
    author_list = execute_sql(sql_code)
    return render_template('authors.html', authors=author_list)


@app.route('/delete_book/<id>', methods=['GET'])
def delete_book(id):
    sql_code = f'delete from book where id={id};'
    delete_item(sql_code, id)
    return render_template('main.html')


@app.route('/delete_client/<id>', methods=['GET'])
def delete_client(id):
    sql_code = f'delete from client where id={id};'
    delete_item(sql_code, id)
    return render_template('main.html')


@app.route('/add_book', methods=['GET', 'POST'])
def new_book():
    if request.method == 'GET':
        add = True
        return render_template('form_add_book.html', add=add)
    else:
        sql_code = 'Insert into book (ISBN,name,description) values(%s,%s,%s);'
        ISBN = request.form.get('ISBN')
        name = request.form.get('name')
        description = request.form.get('description')
        add_book(sql_code, ISBN, name, description)
        return render_template('main.html')


@app.route('/add_client', methods=['GET', 'POST'])
def new_client():
    if request.method == 'GET':
        added = True
        return render_template('form_add_client.html', added=added)
    else:
        sql_code = 'Insert into client (first_name,last_name) values(%s,%s);'
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        added = add_client(sql_code, first_name, last_name)
        return render_template('main.html', added=added)


@app.route('/add_author', methods=['GET', 'POST'])
def new_author():
    if request.method == 'GET':
        return render_template('form_add_author.html')
    else:
        sql_code = 'Insert into author (name) values(%s);'
        name = request.form.get('name')
        add_author(sql_code, name)
        return render_template('main.html')


@app.route('/add_category', methods=['GET', 'POST'])
def new_category():
    if request.method == 'GET':
        return render_template('form_add_category.html')
    else:
        sql_code = 'Insert into category (name) values(%s);'
        name = request.form.get('name')
        add_author(sql_code, name)
        return render_template('main.html')


@app.route('/book_details/<id>', methods=['GET'])
def details_book(id):
    if request.method == 'GET':
        sql_code = f'select * from book where id=%s;'
        details_list = execute_sql(sql_code, id)
        details = details_list[0]
        return render_template('form_add_book.html', details=details)


@app.route('/authors/display_book/<id>', methods=['GET'])
def authors_book(id):
    if request.method == 'GET':
        sql_code = f"""select b.id, b.name as Tytuł, b.description as Opis, a.name as author, c.name as Kategoria from book b 
            left join author a on a.id=b.id_author 
            left join book_category bc ON bc.id_book =b.id
            left join category c on bc.id_category = c.id
            where a.id = %s
            order by b.id;"""
        book_list = execute_sql(sql_code, id)
        return render_template('books.html', books=book_list)


@app.route('/category', methods=['GET'])
def category():
    if request.method == 'GET':
        sql_code = f'select * from category;'
        category_list = execute_sql(sql_code)
        return render_template('category.html', categories=category_list)


@app.route('/category/display_book/<id>', methods=['GET'])
def category_book(id):
    if request.method == 'GET':
        sql_code = f"""select b.id, b.name as Tytuł, b.description as Opis, a.name as author, c.name as Kategoria from book b 
            left join author a on a.id=b.id_author 
            left join book_category bc ON bc.id_book =b.id
            left join category c on bc.id_category = c.id
            where c.id = %s
            order by b.id;"""
        book_list = execute_sql(sql_code, id)
        return render_template('books.html', books=book_list)


@app.route('/category/delete_category/<id>', methods=['GET'])
def delete_category(id):
    sql_code = f'delete from category where id={id};'
    delete_item(sql_code, id)
    return render_template('main.html')


@app.route('/delete_authors/<id>', methods=['GET'])
def delete_author(id):
    sql_code = f'delete from author where id={id};'
    delete_item(sql_code, id)
    return render_template('main.html')


@app.route('/details_client/<id>', methods=['GET'])
def details_client(id):
    if request.method == 'GET':
        sql_code = f"""select c.id, c.first_name, c.last_name, b2.id as book_id, b2.name, b2.description, a2.name as author, c2.name as category, bc2.loan_date, bc2.id as id_loan from client c
            left join book_clients bc2 on bc2.id_client = c.id 
            left join book b2 on b2.id =bc2.id_book 
            left join author a2 on a2.id= b2.id_author
            left join book_category bc ON bc.id_book =b2.id
            left join category c2 on bc.id_category = c2.id
            where c.id=%s and bc2.return_date is null;
            """
        details_list = execute_sql(sql_code, id)
        sql_code = "select * from client where id=%s;"
        details = execute_sql(sql_code, id)
        details = details[0]

        return render_template('form_add_client.html', details=details, details_list=details_list)


@app.route('/loan_book', methods=['GET', 'POST'])
def new_loan():
    if request.method == 'GET':
        return render_template('form_loan_book.html')
    else:
        sql_code = 'select id from book where name=%s;'
        name = request.form.get('title_book')
        id_book = execute_sql(sql_code, (name,))
        if id_book == []:
            massage = 'Brak ksiązki o takim tytule'
            return render_template('main.html', massage=massage)
        id_book = id_book[0][0]

        sql_code = 'select id from client where first_name=%s and last_name=%s;'
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        id_client = search_id_client(sql_code, first_name, last_name)
        if id_client == []:
            massage = 'Brak takiego użytkownika'
            return render_template('main.html', massage=massage)
        id_client = id_client[0][0]

        loan_date = str(datetime.datetime.today())
        sql_code = 'Insert into book_clients (id_book, id_client, loan_date) values(%s,%s,%s);'
        loan_book(sql_code, id_book, id_client, loan_date)
        return render_template('form_loan_book.html')


@app.route('/return_book/<id>', methods=['GET'])
def new_return(id):
    if request.method == 'GET':
        return_date = str(datetime.datetime.today())
        sql_code = f"update book_clients set return_date=%s where id=%s;"
        return_book(sql_code, return_date, id)
        return render_template('main.html')


@app.route('/list_loan_book', methods=['GET'])
def list_loan_book():
    if request.method == 'GET':
        sql_code = f"""select c.id, c.first_name, c.last_name, b2.id as book_id, b2.name, b2.description, a2.name as author, c2.name as category, bc2.loan_date, bc2.id as id_loan from client c
            left join book_clients bc2 on bc2.id_client = c.id 
            left join book b2 on b2.id =bc2.id_book 
            left join author a2 on a2.id= b2.id_author
            left join book_category bc ON bc.id_book =b2.id
            left join category c2 on bc.id_category = c2.id
            where bc2.return_date is null;
            """
        details_list = execute_sql(sql_code, id)
        return render_template('loaned_books.html', details_list=details_list)


app.run()
