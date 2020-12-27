from flask import Flask, request, render_template
from psycopg2 import connect, OperationalError
from psycopg2._psycopg import ProgrammingError

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
        return render_template('form_add_client.html')
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
        print(sql_code)
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
        sql_code = f'select * from client where id=%s;'
        print(sql_code)
        details_list = execute_sql(sql_code, id)
        details = details_list[0]
        return render_template('form_add_client.html', details=details)


app.run()
