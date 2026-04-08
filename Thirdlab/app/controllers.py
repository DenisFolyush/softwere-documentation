import configparser
from flask import Flask, render_template, request, redirect, url_for

from app.business_logic.ticket_logic import TicketBusinessLogic
from app.data_access.sql_data_access import SQLDataAccess
from pathlib import Path

app = Flask(__name__)
logic = TicketBusinessLogic(SQLDataAccess())

LAB4_ROOT = Path(__file__).resolve().parents[2] / '4lab'
LAB4_CONFIG = LAB4_ROOT / 'config.ini'


def read_lab4_config():
    parser = configparser.ConfigParser()
    parser.read(LAB4_CONFIG, encoding='utf-8')
    return {
        'strategy': parser.get('output', 'strategy', fallback='console'),
        'file_path': parser.get('output', 'file_path', fallback='output_records.json'),
        'redis_url': parser.get('redis', 'url', fallback='redis://redis:6379'),
        'redis_key': parser.get('redis', 'key', fallback='parking_records'),
        'kafka_bootstrap_servers': parser.get('kafka', 'bootstrap_servers', fallback='kafka:9092'),
        'kafka_topic': parser.get('kafka', 'topic', fallback='parking_violations'),
    }


def read_lab4_output_preview(config):
    preview = None
    output_path = config.get('file_path', 'output_records.json')
    output_file = Path(output_path)
    if not output_file.is_absolute():
        output_file = LAB4_ROOT / output_file

    if output_file.exists() and output_file.is_file():
        try:
            import json
            with open(output_file, 'r', encoding='utf-8') as stream:
                data = json.load(stream)
            preview = {
                'path': str(output_file),
                'exists': True,
                'sample': data[:10] if isinstance(data, list) else data,
                'count': len(data) if isinstance(data, list) else None,
            }
        except Exception as exc:
            preview = {
                'path': str(output_file),
                'exists': True,
                'error': str(exc),
            }
    else:
        preview = {
            'path': str(output_file),
            'exists': False,
        }

    return preview


def write_lab4_config(config):
    parser = configparser.ConfigParser()
    parser['output'] = {
        'strategy': config.get('strategy', 'console'),
        'file_path': config.get('file_path', 'output_records.json'),
    }
    parser['redis'] = {
        'url': config.get('redis_url', 'redis://redis:6379'),
        'key': config.get('redis_key', 'parking_records'),
    }
    parser['kafka'] = {
        'bootstrap_servers': config.get('kafka_bootstrap_servers', 'kafka:9092'),
        'topic': config.get('kafka_topic', 'parking_violations'),
    }
    with open(LAB4_CONFIG, 'w', encoding='utf-8') as stream:
        parser.write(stream)


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


@app.route('/lab4-strategy', methods=['GET', 'POST'])
def lab4_strategy():
    if request.method == 'POST':
        write_lab4_config({
            'strategy': request.form.get('strategy', 'console'),
            'file_path': request.form.get('file_path', 'output_records.json'),
            'redis_url': request.form.get('redis_url', 'redis://redis:6379'),
            'redis_key': request.form.get('redis_key', 'parking_records'),
            'kafka_bootstrap_servers': request.form.get('kafka_bootstrap_servers', 'kafka:9092'),
            'kafka_topic': request.form.get('kafka_topic', 'parking_violations'),
        })
        return redirect(url_for('lab4_strategy'))

    config = read_lab4_config()
    preview = read_lab4_output_preview(config)
    return render_template('lab4_strategy.html', config=config, preview=preview)


if __name__ == '__main__':
    app.run(debug=True)
