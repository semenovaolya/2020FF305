from flask import (
    Flask,
    render_template,
    request,
    redirect,
)
import lab

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def select():
    button = request.form.get('button')
    if button == 'Date':
        return redirect('/date')
    if button == 'Type':
        return redirect('/type')


@app.route('/date')
def date():
    return render_template('date.html')


@app.route('/date', methods=['POST'])
def date1():
    start_date = request.form.get('sdate')
    end_date = request.form.get('edate')
    result = lab.date_search('dism.log', start_date, end_date)
    return render_template('date.html', result=result)


@app.route('/type')
def type_():
    return render_template('type.html')


@app.route('/type', methods=['POST'])
def type_1():
    count_log = request.form.get('count')
    type_log = request.form.get('type')
    if not count_log:
        count_log = 10
    try:
        count_log = int(count_log)
    except ValueError:
        count_log = 0
    result = lab.count_search('dism.log', count_log, type_log=type_log)
    print(result)
    return render_template('type.html', result=result)


if __name__ == '__main__':
    app.run(debug=True, port='5000')