import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import time
from celery import Celery
from celery.result import AsyncResult

# Initialize the Dash app and Celery
app = dash.Dash(__name__)
celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def long_running_task():
    time.sleep(30)
    return "Task Completed"

app.layout = html.Div([
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),
    html.Button('Start Task', id='start-button', n_clicks=0),
    html.Div(id='task-output'),
    html.Div(id='task-status')
])

@app.callback(
    Output('task-output', 'children'),
    Input('start-button', 'n_clicks'),
    State('task-output', 'children'),
    prevent_initial_call=True
)
def start_task(n_clicks, task_id):
    task = long_running_task.delay()
    return task.id

@app.callback(
    Output('task-status', 'children'),
    Input('interval-component', 'n_intervals'),
    State('task-output', 'children')
)
def update_status(n, task_id):
    if not task_id:
        return "No Task Started"
    task_result = AsyncResult(task_id)
    if task_result.ready():
        return task_result.result
    else:
        return "Task in Progress"

if __name__ == '__main__':
    app.run_server(debug=True)
