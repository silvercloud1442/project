import flask
from flask import jsonify, request
from requests import post, delete, get
from data.db_session import create_session
from data.jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    session = create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('job', 'team_leader', 'work_size', "collaborators", "is_finished"))
                 for item in jobs]

        }
    )



@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    session = create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    session.delete(jobs)
    session.commit()
    return jsonify({'success': 'OK'})

print(get('http://localhost:5000/api/jobs').json())

job_id = int(input('Job id:'))

print(delete('http://localhost:5000/api/jobs/{}'.format(job_id)).json())

print(delete('http://localhost:5000/api/jobs/999').json())

print(get('http://localhost:5000/api/jobs').json())
