import flask
import os
import random

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "nadoeli_zadachi"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/<pagename>")
@app.route("/index/<pagename>")
def index(pagename):
    return flask.render_template("base.htm", title=pagename)


@app.route("/list_prof/<list_type>")
def list_prof(list_type):
    jobs = ("инженер-исследователь",
            "пилот",
            "строитель",
            "экзобиолог",
            "врач",
            "инженер по терраформированию",
            "климатолог",
            "специалист по радиационной защите",
            "астрогеолог", "гляциолог",
            "инженер жизнеобеспечения",
            "метеоролог",
            "оператор марсохода",
            "киберинженер",
            "штурман",
            "пилот дронов")
    return flask.render_template("list_prof.htm", list_type=list_type, jobs=jobs)


@app.route("/gallery", methods=("GET", "POST"))
def gallery():
    gallery_path = "static/img/gallery"
    if flask.request.method == "GET":
        slides = map(lambda filname: os.path.join(
            gallery_path, filname), os.listdir(gallery_path))
        return flask.render_template("gallery.htm", slide_paths=slides)
    elif flask.request.method == "POST":
        print("post")
        if 'file' not in flask.request.files:
            print("err1")
            flask.flash('Ошибка загрузки', "error")
            return flask.redirect(flask.request.url)
        f = flask.request.files["file"]
        if not f.filename:
            print("err2")
            flask.flash("Файл не выбран", "error")
            return flask.redirect(flask.request.url)
        if f and allowed_file(f.filename):
            print("here")
            last_slide = max(map(int, map(lambda fname: fname.rsplit(".")[
                             0][5:], os.listdir(gallery_path))))
            new_name = f"slide{last_slide + 1}.{f.filename.rsplit('.')[1]}"
            print(new_name)
            f.save(os.path.join(gallery_path, new_name))
            flask.flash("Картинка загружена", "info")
            return flask.redirect(flask.request.url)


@app.route("/answer")
@app.route("/auto_answer")
def auto_answer():
    data = {
        "title": "И на Марсе будут яблони цвести!",
        "surname": "Watny",
        "name": "Mark",
        "education": "выше среднего",
        "profession": "штурман марсохода",
        "sex": "мужской",
        "motivation": "Всегда мечтал застрять на Марсе",
        "ready": True
    }
    return flask.render_template("auto_answer.htm", **data)


@app.route("/distribution")
def distribution():
    members = (
        "Ридли Скотт",
        "Энди Уир",
        "Марк Уотни"
    )
    return flask.render_template("distribution.htm", members=members)


@app.route("/table/<gender>/<int:age>")
def table(gender, age: int):
    fem_colors = ("#ffa500", "#ff4500")
    male_colors = ("#00ffff", "#87cefa")
    color = random.choice({"male": male_colors, "female": fem_colors}[gender])
    is_adult = age > 21
    return flask.render_template("table.htm", wall_color=color, is_adult=is_adult)


if __name__ == "__main__":
    app.run(host="::1", port=8080, debug=True)
