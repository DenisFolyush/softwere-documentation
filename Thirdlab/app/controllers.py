from flask import Flask, render_template, request, redirect, url_for

from app.business_logic.ticket_logic import TicketBusinessLogic
from app.data_access.sql_data_access import SQLDataAccess

app = Flask(__name__)
logic = TicketBusinessLogic(SQLDataAccess())

@app.route('/')
def index():
    tickets = logic.get_all()
    return render_template('list.html', tickets=tickets)

@app.route('/ticket/<int:tid>')
def detail(tid):
    ticket = logic.get_by_id(tid)
    if not ticket:
        return "Not found", 404
    return render_template('detail.html', ticket=ticket)

@app.route('/ticket/new', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        logic.add(request.form.to_dict())
        return redirect(url_for('index'))
    return render_template('form.html', ticket=None)

@app.route('/ticket/<int:tid>/edit', methods=['GET','POST'])
def edit(tid):
    ticket = logic.get_by_id(tid)
    if request.method == 'POST':
        logic.update(tid, request.form.to_dict())
        return redirect(url_for('index'))
    return render_template('form.html', ticket=ticket)

@app.route('/ticket/<int:tid>/delete', methods=['POST'])
def delete(tid):
    logic.delete(tid)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
