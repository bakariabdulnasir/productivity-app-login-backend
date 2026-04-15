from app import create_app, db
from app.models.user import User
from app.models.task import Task

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(username="testuser")
    user1.set_password("1234")

    db.session.add(user1)
    db.session.commit()

    task1 = Task(title="Learn Flask", description="Build API", user_id=user1.id)
    task2 = Task(title="Build Project", description="Finish lab", user_id=user1.id)

    db.session.add_all([task1, task2])
    db.session.commit()

    print("Database seeded!")