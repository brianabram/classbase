from flask_script import Manager
from coursebase import app, db, Professor, course

manager = Manager(app)

@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    johnson = Professor(name='Johnson', about='Johnson teaches MISY225.')
    russ = Professor(name='Russ', about='Russ teaches HIST200.')
    course1 = course(name='MISY225', about='Java Programming', professor=johnson)
    course2 = course(name='HIST200', about='History of Delaware', professor=russ)
    db.session.add(johnson)
    db.session.add(russ)
    db.session.add(course1)
    db.session.add(course2)
    db.session.commit()

if __nmame__ == "__main__":
    manager.run()
