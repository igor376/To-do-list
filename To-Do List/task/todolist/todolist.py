from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta, datetime

engine = create_engine("sqlite+pysqlite:///todo.db?check_same_thread=False")
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, nullable=False)
    task = Column(String)
    deadline = Column(Date, nullable=False)

    def __repr__(self):
        return f'{self.id}. {self.task}'


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def all_task():
    print("All tasks:")
    rows = session.query(Task).order_by(Task.deadline).all()
    print_rows(rows, show_date=True)


def add_task():
    session.add(Task(task=input("Enter task\n"), deadline=datetime.strptime(input("Enter deadline\n"), "%Y-%m-%d")))
    session.commit()
    print("The task has been added!\n")


def week_task():
    for day in [date.today() + timedelta(i) for i in range(7)]:
        print(f'{date.strftime(day, "%A %d %b")}:')
        rows = session.query(Task).filter(Task.deadline == day).order_by(Task.deadline).all()
        if len(rows) == 0:
            print("Nothing to do!\n")
            continue
        else:
            for i, value in enumerate(rows):
                print(f'{i + 1}. {value.task}')
            print()


def today_task():
    print(f'Today {date.strftime(date.today(), "%d %b")}:')
    rows = session.query(Task).filter(Task.deadline == date.today()).all()
    print_rows(rows)


def print_rows(rows, show_date=False):
    if len(rows) == 0:
        print('Nothing to do!')
        return
    for row in rows:
        if show_date:
            print(f'{row}. {date.strftime(row.deadline, "%d %b")}')
        else:
            print(row)
    print()


def missed_task():
    rows = session.query(Task).filter(Task.deadline < date.today()).all()
    if len(rows) == 0:
        print("Nothing is missed!")
    else:
        print("Missed tasks:")
        print_rows(rows, show_date=True)
        print()


def delete_task():
    print("Choose the number of the task you want to delete:")
    rows = session.query(Task).order_by(Task.deadline).all()
    print_rows(rows, show_date=True)
    id_for_delete = int(input())
    session.query(Task).filter(Task.id == id_for_delete).delete()
    rows = session.query(Task).filter(Task.id > id_for_delete).all()
    for row in rows:
        session.query(Task).filter(Task.id == row.id).update({"id": row.id - 1})
    session.commit()


while True:
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    user_chose = input()
    if user_chose == "1":
        today_task()
    elif user_chose == "2":
        week_task()
    elif user_chose == "3":
        all_task()
    elif user_chose == "4":
        missed_task()
    elif user_chose == "5":
        add_task()
    elif user_chose == "6":
        delete_task()
    else:
        print("Buy!")
        exit()
