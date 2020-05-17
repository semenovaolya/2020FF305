from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from forms import DateFilterForm
from forms import FilterForm
from log_reader import count_filter_logs
from log_reader import date_filter_logs
from log_reader import log_delete
import jinja2
import os

UPLOAD_FOLDER = r'.\files'
ALLOWED_EXTENSIONS = {'.log', '.txt'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a really really really long secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_files_with_extension(path, extension):
    """Возвращает имена файлов c расширениями extension
    из директории path

    Parameters
    -------------
    path
        путь директории
    extension
        список разрешенных расширений
    """
    path = os.path.abspath(path)
    list_file = os.listdir(path)
    list_log = []
    for file in list_file:
        file_name, file_extension = os.path.splitext(file)
        if file_extension in extension:
            list_log.append(file)
    return list_log


@app.route('/', methods=['GET', 'POST'])
def index():
    files = get_files_with_extension(UPLOAD_FOLDER, ALLOWED_EXTENSIONS)
    template_context = dict(files=files)

    # обрабатываем форму выбора лог-файла
    if request.method == 'POST':
        index.test = request.form.get('test')
        return redirect(url_for('filter_file'))

    return render_template('index.html', **template_context)


@app.route('/filter/', methods=['GET', 'POST'])
def filter_file():
    try:
        file = index.test
        if file is None:
            raise AttributeError
    except AttributeError:
        return redirect(url_for('index'))

    form = FilterForm()
    date_form = DateFilterForm()
    template_context = dict(form=form,
                            date_form=date_form,
                            current_file=file)

    # обрабатываем форму FilterForm
    if form.validate_on_submit() and form.count.data is not None:
        count = int(form.count.data)
        mes_type = str(date_form.mes_type.data)
        filter_file.file = file
        file = os.path.join(UPLOAD_FOLDER, file)
        filter_file.logs = count_filter_logs(file, count,
                                             message_type=mes_type)
        return redirect(url_for('result'))

    # обрабатываем форму DateFilterForm
    if date_form.validate_on_submit() and (
            date_form.date_start.data is not None or
            date_form.date_end.data is not None):
        date_start = str(date_form.date_start.data)
        date_end = str(date_form.date_end.data)
        mes_type = str(date_form.mes_type.data)
        filter_file.file = file
        file = os.path.join(UPLOAD_FOLDER, file)
        filter_file.logs = date_filter_logs(file,
                                            date_start=date_start,
                                            date_end=date_end,
                                            message_type=mes_type)
        return redirect(url_for('result'))

    return render_template('filter.html', **template_context)


@app.route('/result/', methods=['GET', 'POST'])
def result():
    try:
        logs = filter_file.logs
        file = filter_file.file
    except AttributeError:
        return redirect(url_for('filter_file'))

    len_logs = len(logs)

    # обрабатываем запрос на удаление логов
    if request.method == 'POST':
        file = os.path.join(UPLOAD_FOLDER, file)
        del_log = request.form.getlist('del')
        log_delete(file, del_log)
        return redirect(url_for('filter_file'))

    return render_template('result.html', logs=logs,
                           current_file=file, len_logs=len_logs)


if __name__ == '__main__':
    app.run(debug=True)
