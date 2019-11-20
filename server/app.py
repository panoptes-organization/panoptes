import uuid
import traceback

from server.server_utilities.db_queries import maintain_jobs, get_db_workflows_by_id
from server.database import init_db, db_session
from server.models import Workflows, WorkflowMessages
from server.schema_forms import SnakemakeUpdateForm
from server.routes import *
from flask import Flask, request, render_template, abort, send_from_directory

app = Flask(__name__, template_folder="static/src/")
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.register_blueprint(routes)
app.jinja_env.globals.update(get_jobs=get_jobs)
app.jinja_env.globals.update(get_job=get_job)

init_db()


@app.route('/')
def index():
    wf = [w.get_workflow() for w in get_db_workflows()]
    info = {
        'workflows': len(wf),
        'completed': sum([1 if w['status']=='Done' else 0 for w in wf]),
        'jobs_done': sum([w['jobs_done'] for w in wf]),
        'jobs_total': sum([w['jobs_total']for w in wf]),
    }
    return render_template("index.html", info=info)


@app.route('/workflows/')
def workflows_page():
    workflows = [w.get_workflow() for w in get_db_workflows()]
    return render_template('workflows.html', workflows=workflows)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contribute')
def contribute():
    return render_template('contribute.html')


@app.route('/workflow/<id>', methods=['GET'])
def get_status(id):
    try:
        workflow = get_db_workflows_by_id(id).get_workflow()
        
        if workflow:
            return render_template('workflow.html', workflow=workflow)
        else:
            return f"<html>No workflow currently running with id= {id}!!!</html>"

    except:
        traceback.print_exc()
        return f"<html>No workflow currently running with id= {id}!!!</html>"


@app.route('/workflow/<wf_id>/job/<job_id>', methods=['GET'])
def get_job_status(wf_id, job_id):
    return render_template('job.html', job=get_job(wf_id, job_id))


@app.route('/create_workflow', methods=['GET'])
def create_workflow():
    try:
        w = Workflows(str(uuid.uuid4()), "Running")
        db_session.add(w)
        db_session.commit()

        return w.get_workflow()
    except:
        traceback.print_exc()
        return f"<html>No workflow currently running with id= {id}!!!</html>"


@app.route('/update_workflow_status', methods=['POST'])
def update_status():
    update_form = SnakemakeUpdateForm()
    errors = update_form.validate(request.form)

    if errors:
        abort(404, str(errors))
    else:
        r = update_form.load(request.form)
    # now all required fields exist and are the right type
    maintain_jobs(msg=r["msg"], wf_id=r["id"])
    return "ok"


@app.route('/vendor/<path:path>')
def send_vendor(path):
    return send_from_directory('static/vendor', path)


@app.route('/node_modules/<path:path>')
def send_node_modules_charts(path):
    return send_from_directory('static/node_modules', path)


@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('static/src', path)


if __name__ == '__main__':
    app.run()
