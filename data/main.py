import os
from sqlalchemy import or_
from pathlib import Path
from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_restful import Api
from flask_ngrok import run_with_ngrok
from werkzeug.utils import redirect, secure_filename
from data.MessagesForm import MessagesForm
from data.db_session import global_init, create_session
from data.jobs import Jobs
from data.message import Message
from data.projectform import ProjectForm
from data.users import User
from data.RegisterForm import RegisterForm
from data.LoginForm import LoginForm
from data.JobsForm import JobsForm
from data.projects import Projects

app = Flask(__name__)

api = Api(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)
# run_with_ngrok(app)
global_init('db/dbase.sqlite')


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    session = create_session()
    category = request.args.get('cat')
    if category == None:
        jobs_list = []
        for jobs in session.query(Jobs).all():
            jobs_list.append(jobs)
        return render_template('index.html', jobs=jobs_list)
    else:
        jobs_list = []
        for jobs in session.query(Jobs).filter(or_(Jobs.category == category, Jobs.category_2 == category)).all():
            jobs_list.append(jobs)
        return render_template('index.html', jobs=jobs_list)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            description=form.description.data,
            email=form.email.data,
            worker=form.worker.data
        )
        pas = form.password.data
        user.hassed_password = User.set_password(pas)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs', methods=['GET', 'POST'])
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        session = create_session()
        job = Jobs()
        job.customer = current_user.id
        job.title = form.title.data
        job.cost = form.cost.data
        job.description = form.description.data
        job.brief = ''.join(form.description.data[:30] + '...')
        job.category = form.category.data
        job.category_2 = form.category_2.data
        UPLOAD_DIR: Path = Path(__file__).parent / 'static/jobs_img'
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        for upload in request.files.getlist('images'):
            filename = secure_filename(upload.filename)
            if filename != '':
                save_path = str(UPLOAD_DIR / filename)
                upload.save(save_path)
                job.img = '\\static' + save_path.split("\\static")[1]
        session.add(job)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('job_add.html', title='Adding a job',
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        session = create_session()
        if current_user.id == 1:
            job = session.query(Jobs).filter(Jobs.id == id).first()
        else:
            job = session.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
        if job:
            form.title.data = job.title
            form.cost.data = job.cost
            form.description.data = job.description
            form.category.data = job.category
            form.category_2.data = job.category_2
    if form.validate_on_submit():
        session = create_session()
        if current_user.id == 1:
            job = session.query(Jobs).filter(Jobs.id == id).first()
        else:
            job = session.query(Jobs).filter(Jobs.id == id,
                                             Jobs.user == current_user).first()
        if job:
            job.customer = current_user.id
            job.title = form.title.data
            job.cost = form.cost.data
            job.description = form.description.data
            job.category = form.category.data
            job.category_2 = form.category_2.data
            UPLOAD_DIR: Path = Path(__file__).parent / 'static/jobs_img'
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            for upload in request.files.getlist('images'):
                filename = secure_filename(upload.filename)
                if filename != '':
                    save_path = str(UPLOAD_DIR / filename)
                    upload.save(save_path)
                    job.img = '\\static' + save_path.split("\\static")[1]
            session.add(job)
            session.commit()
            return redirect('/')
    return render_template('job_add.html', title='Editing', form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
def jobs_delete(id):
    session = create_session()
    if current_user.id == 1:
        job = session.query(Jobs).filter(Jobs.id == id).first()
    else:
        job = session.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
    if job:
        session.delete(job)
        session.commit()
    return redirect('/')

@app.route('/jobs_delete2/<int:id>', methods=['GET', 'POST'])
def jobs_delete2(id):
    session = create_session()
    if current_user.id == 1:
        job = session.query(Jobs).filter(Jobs.id == id).first()
    else:
        job = session.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
    if job:
        session.delete(job)
        session.commit()
    return redirect('/jobs_list/{}'.format(current_user.id))


@app.route('/profile/<int:id>', methods=['GET'])
def profile(id):
    session = create_session()
    user = session.query(User).filter(User.id == id).first()
    projects = session.query(Projects).filter(user.id == Projects.author).all()
    return render_template('profile.html', user=user, projects=projects)


@app.route('/project/<int:id>', methods=["GET", 'POST'])
def project(id):
    form = ProjectForm()
    if form.validate_on_submit():
        session = create_session()
        project = Projects()
        project.title = form.title.data
        project.author = id
        project.description = form.description.data
        UPLOAD_DIR: Path = Path(__file__).parent / 'static/projects_img'
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        for upload in request.files.getlist('images'):
            filename = secure_filename(upload.filename)
            if filename != '':
                save_path = str(UPLOAD_DIR / filename)
                upload.save(save_path)
                project.img = '\\static' + save_path.split("\\static")[1]
        session.add(project)
        session.merge(current_user)
        session.commit()
        return redirect('/profile/{}'.format(id))
    return render_template('project_add.html',
                           form=form)


@app.route('/job_info/<int:id>', methods=['GET'])
def job_info(id):
    session = create_session()
    job = session.query(Jobs).filter(Jobs.id == id).first()
    user = session.query(User).filter(job.customer == User.id).first()
    return render_template('job_info.html', job=job, user=user)


@app.route('/project_edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    form = ProjectForm()
    if request.method == "GET":
        session = create_session()
        project = session.query(Projects).filter(Projects.id == id, Projects.author == current_user.id).first()
        if project:
            form.title.data = project.title
            form.img.data = project.img
            form.description.data = project.description
    if form.validate_on_submit():
        session = create_session()
        project = session.query(Projects).filter(Projects.id == id,
                                                Projects.author == current_user.id).first()
        if project:
            project.title = form.title.data
            UPLOAD_DIR: Path = Path(__file__).parent / 'static/projects_img'
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            for upload in request.files.getlist('images'):
                filename = secure_filename(upload.filename)
                if filename != '':
                    save_path = str(UPLOAD_DIR / filename)
                    upload.save(save_path)
                    project.img = '\\static' + save_path.split("\\static")[1]
            project.description = form.description.data
            session.add(project)
            session.commit()
            return redirect('/profile/{}'.format(current_user.id))
    return render_template('project_add.html', title='Editing', form=form)


@app.route('/project_delete/<int:id>', methods=['GET', 'POST'])
def project_delete(id):
    session = create_session()
    project = session.query(Projects).filter(Projects.id == id, Projects.author == current_user.id).first()
    if project:
        session.delete(project)
        session.commit()
    return redirect('/profile/{}'.format(current_user.id))


@app.route('/jobs_list/<int:id>', methods=['GET'])
def jobs_list(id):
    session = create_session()
    jobs = session.query(Jobs).filter(Jobs.customer == id).all()
    user = session.query(User).filter(User.id == id).first()
    return render_template('jobs_list.html', jobs=jobs, user=user)


@app.route('/messages/', methods=['GET', 'POST'])
def messages():
    form = MessagesForm()
    session = create_session()
    from_id = int(request.args.get('from_id'))
    to_id = int(request.args.get('to_id'))
    if current_user.id == from_id:
        if form.validate_on_submit():
            message = Message()
            message.text = form.text.data
            message.from_id = from_id
            message.to_id = to_id
            session.add(message)
            session.commit()
            return redirect('/messages/?from_id={}&to_id={}'.format(from_id, to_id))
        f1 = (Message.from_id == from_id and Message.to_id == to_id)
        f2 = (Message.to_id == from_id and Message.from_id == to_id)
        messages = session.query(Message).filter(or_(f1, f2)).all()
        messages2 = []
        for message in messages:
            if message.from_id == from_id and message.to_id == to_id:
                messages2.append(message)
            if message.to_id == from_id and message.from_id == to_id:
                messages2.append(message)
        return render_template('messages.html', messages=messages2, from_id=from_id, to_id=to_id, form=form)
    else:
        return render_template('error.html')

@app.route('/chats/', methods=["GET"])
def chats():
    id = int(request.args.get('user_id'))
    session = create_session()
    msg = session.query(Message).filter(or_(Message.from_id == id, Message.to_id == id)).all()
    messages = []
    users = []
    for message in msg:
        if message.from_id not in users and message.from_id != id:
            msg2 = session.query(Message).filter(Message.from_id == message.from_id).first()
            us = session.query(User).filter(User.id == msg2.from_id).first()
            user = us.name + ' ' + us.surname
            users.append(message.from_id)
            messages.append([user, msg2.text, msg2.from_id, True])
        if message.to_id not in users and message.to_id != id:
            msg2 = session.query(Message).filter(Message.to_id == message.to_id).first()
            us = session.query(User).filter(User.id == msg2.to_id).first()
            user = us.name + ' ' + us.surname
            users.append(message.to_id)
            messages.append([user, msg2.text, msg2.to_id, False])
    return render_template('chats.html', messages=messages)


@app.route("/workers/", methods=['GET'])
def workers():
    session = create_session()
    users = session.query(User).filter(User.worker == True).all()
    return render_template('workers.html', users=users)

if __name__ == '__main__':
    app.run()
