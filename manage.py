from flask_script import Manager
from classbase import app, db, Professor, Class

manager = Manager(app)

@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    johnson = Professor(name='Johnson', about='Johnson teaches MISY225.')
    russ = Professor(name='Russ', about='Russ teaches HIST200.')
    class1 = Class(name='MISY225', about='Java Programming', professor=johnson)
    class2 = Class(name='HIST200', about='History of Delaware', professor=russ)
    db.session.add(johnson)
    db.session.add(russ)
    db.session.add(class1)
    db.session.add(class2)
    db.session.commit()

if __nmame__ == "__main__":
    manager.run()
