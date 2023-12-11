from sqlalchemy import select
import typer


from .database import Model, engine, Session
from .models import User, Task, TaskList


def add_demo_data():
    """Ajout de données de démo à la base."""
    with Session() as session:
        with session.begin():
            thierry = User(username="tchappui", fullname="Thierry Chappuis")
            session.add(thierry)
            course = TaskList(name="cours à créer", owner=thierry)
            session.add(course)
            tasks = [
                Task(
                    list=course,
                    description="Trouver un bon titre",
                    owner=thierry,
                ),
                Task(list=course, description="Créer un plan", owner=thierry),
                Task(
                    list=course,
                    description="Enregistrer la vidéo d'introduction",
                    owner=thierry,
                ),
            ]
            session.add_all(tasks)
            course.tasks.extend(tasks)


def request_demo_data():
    """Recherche des données de démo dans la base."""
    with Session() as session:
        with session.begin():
            query = (
                select(Task)
                .join(Task.owner)
                .where(User.username == "tchappui")
            )
            for task in session.scalars(query):
                print(f"- {task}")


def main():
    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)

    # Enregistrons quelques données dans notre base
    add_demo_data()

    # Request demo data
    request_demo_data()


if __name__ == "__main__":
    typer.run(main)
