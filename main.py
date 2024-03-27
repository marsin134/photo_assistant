from flask import Flask, render_template, request, redirect
from data.python import delete_fon, db_session, effects
from data.python.users import User, LoginForm, RegisterForm
from flask_login import LoginManager, login_user

UPLOAD_FOLDER = 'static/image'
URL = '127.0.0.1'

app = Flask(__name__, template_folder="data/html")

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '1'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route('/index')
def index():
    return render_template('test.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            # login_user(user, remember=form.remember_me.data)
            login_user(user)
            return redirect("/")
        return render_template('login_form.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login_form.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register_form.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first() or \
                db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register_form.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        else:
            user = User(
                login=form.login.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
    return render_template('register_form.html', title='Регистрация', form=form)


@app.route('/delete_fon', methods=['POST', 'GET'])
def delete_fons():
    if request.method == 'GET':
        return render_template('forma_delete_fon.html')
    elif request.method == 'POST':
        filename, rembg_img_name = delete_fon.delete(UPLOAD_FOLDER)
        if filename and rembg_img_name:
            return render_template('forma_delete_fon.html', filename=filename, rembg_img=rembg_img_name)
        return render_template('forma_delete_fon.html', message='Произошла ошибка, возможно вы не указали файл')


@app.route('/choice_effects')
def choice_effects():
    return render_template('forma_choice_effect.html', effects=effects.effects)


@app.route('/make_eff/<effect>', methods=['POST', 'GET'])
def make_effects(effect):
    if request.method == 'GET':
        return render_template('forma_make_effect.html', effect=effect)
    elif request.method == 'POST':
        filename, rembg_img_name = effects.make_effect(effect, UPLOAD_FOLDER + '/effect_im')
        if filename and rembg_img_name:
            return render_template('forma_make_effect.html', filename='/' + filename, rembg_img='/' + rembg_img_name,
                                   effect=effect)
        return render_template('forma_make_effect.html', message='Произошла ошибка, возможно вы не указали файл',
                               effect=effect)


if __name__ == '__main__':
    db_session.global_init("db/photo_assistant.db")
    app.run(port=8080, host=URL, debug=True)
