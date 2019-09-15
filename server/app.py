from flask import Flask, request, render_template, abort
from server.database import init_db, db_session
import traceback
from server.models import Workflows, WorkflowMessages
from server.schema_forms import SnakemakeUpdateForm
import json
import uuid

app = Flask(__name__, template_folder="templates")
init_db()


@app.route('/')
def index():

    return f"<html> \
             <h1>Welcome to the development server of vzflow. </h1> <br> \
             If you can see this message then your DB is set properly <br> \
             DB info: {Workflows.query.all()}. <br> \
             To check the status of the workflow go to the following route: <a href=\"/workflow_status\">/workflow_status</a> <br> \
             </html>"

@app.route('/workflows')
def index2():
    workflows = Workflows.query.all()
    return render_template('workflows.html', workflows=workflows)


@app.route('/workflow_status/<id>', methods=['GET'])
def get_status(id):
    try:
        workflow = Workflows.query.filter(Workflows.id == id).first()
        w_msg = WorkflowMessages.query.filter(WorkflowMessages.wf_id == id).all()
        l = []
        for i in w_msg:
            msg = eval(i.msg)
            if "level" in msg.keys():
                if msg["level"] == 'progress':
                    l.append({'level': msg["level"],
                              'done': msg["done"],
                              'total': msg["total"]})

        if workflow:
            return render_template('workflow_status.html', workflow=workflow, w_msg=l)
        else:
            return f"<html>No workflow currently running with id= {id}!!!</html>"

    except:
        traceback.print_exc()
        return f"<html>No workflow currently running with id= {id}!!!</html>"\



@app.route('/create_workflow', methods=['GET'])
def create_workflow():
    try:
        w = Workflows(str(uuid.uuid4()), "Initialized")
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
    # business requirements aren't necessarily satisfied (length, time bounds, etc)

    message = eval(r['msg'])
    w = WorkflowMessages(msg=r["msg"], wf_id=r["id"])
    db_session.add(w)
    db_session.commit()

    print('New update from snakemake {}'.format(id))

    return "ok"


if __name__ == '__main__':
    app.run()
