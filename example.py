from flask import Flask, make_response, render_template, request


# Это callable WSGI-приложение
app = Flask(__name__)

# @app.before_request
# def log_path():
#    print(f"Request path: {request.path}")
#    print("1. After middleware")

@app.before_request
def check_id():
    if request.endpoint == "resource":
        id = request.args.get("id")
        if not id:
            # в случае запроса на /resouce сработает условие мидлвары
            return 'Bad Request: Missing "id" parameter', 400
    return None # иначе возвращаем None, чтобы продолжить цепочку

@app.after_request
def add_custom_header(response):
    response.headers["X-Custom-Header"] = "value"
    print("3. After middleware")
    return response

# @app.route('/')
# def home():
#     print("2. After middleware")
#     return "Hello from middleware!"

# @app.before_request
# def log_path():
#     print(f"Request path: {request.path}")


@app.route("/")
def home():
    return "Hello from Hexlet"


@app.route("/resource")
def resource():
    id = request.args.get("id")
    return f"Resource with id: {id}"

# @app.after_request
# def log_response(response):
#    print("Response has been sent")
#    return response



# @app.route('/users', methods=['GET', 'POST'])
# def users():
#     if request.method == 'POST':
#         return 'Hello from POST /users'
#     return 'Hello from GET /users'


# @app.get('/users')
# def users_get():
#     return 'GET /users'


# @app.post('/users')
# def users():
#     return 'Users', 302


@app.errorhandler(404)
def not_found(error):
    return 'Oops!', 404


@app.route('/hello')
def hello():
    # создаем объект response
    response = make_response('Hello, World!')
    # Устанавливаем заголовок
    response.headers['X-MyHeader'] = 'Thats my header!'
    # Меняем тип ответа
    response.mimetype = 'text/plain'
    # Задаем статус
    response.status_code = 201
    # Устанавливаем cookie
    response.set_cookie('super-cookie', '42')
    return response


# @app.route('/users/')
# def get_users():
#     print(request.args)  # => {'page': 12, 'per': 5}
#     page = request.args.get('page', 1)
#     per = request.args.get('per', 10, type=int)
#     # Обработка
#     prev_page = (page - 1) * per
#     current_page = page * per
#     users_at_page = users[prev_page:current_page]
#     return users_at_page


@app.route('/courses/<id>')
def courses_show(id):
    return f'Course id: {id}'


@app.route('/courses/<course_id>/lessons/<lesson_id>')
def lessons_show(course_id, lesson_id):
    return f'Course id: {course_id}, Lesson id: {lesson_id}'


# @app.route('/users/<id>')
# def users_show(id):
#     return render_template(
#         'index.html',
#         name=id,
#     )


@app.route('/courses/')
def courses_index():
    courses = get_courses(courses_dict) # Возвращает список курсов, которые представлены словарем

    return render_template(
        'courses/layout.html',
        courses=courses
    )
def filter_q():
    return '12'

# @app.route('/courses/')
# def courses_index():
#     query = request.args.get('query')
#     filtered_courses = filter_q()

#     return render_template(
#         'courses/layout.html',
#         courses=filtered_courses,
#         search=query,
#     )

@app.route('/users/<id>')
def users_show(id):
    return render_template(
        'users/show.html',
        name=id,
    )
    
courses_dict = {
    'math': 1,
    'english': 2,
}

def get_courses(courses_dict):
    name = list(courses_dict.keys())
    id = list(courses_dict.values())
    return name, id

users = [
    {'id': 1, 'name': 'mike'},
    {'id': 2, 'name': 'mishel'},
    {'id': 3, 'name': 'adel'},
    {'id': 4, 'name': 'keks'},
    {'id': 5, 'name': 'kamila'}
]

def filtred(query, name_list):
    # filtred_list = ['make' 'peter']
    filtred_list = []
    for dict in name_list:
        name = dict['name']
        if query in name:
            filtred_list.append(name)
    return filtred_list

@app.route('/users/')
def users_index():
    query = request.args.get('query')
    filtered_name = filtred(query, users)
    # filtered_name = ['make', 'peter']
    return render_template(
        'users/index.html',
        names=filtered_name,
        search=query,
    )
    

