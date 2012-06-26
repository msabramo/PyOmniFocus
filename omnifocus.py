import os

from sqlalchemy import Column, Integer, Text, String, Boolean, \
     ForeignKey, DateTime, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, aliased
from sqlalchemy.ext.declarative import declarative_base

sqlite_db_filename = os.path.expanduser('~/Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2')
engine = create_engine('sqlite:///' + sqlite_db_filename, echo=False)

Base = declarative_base()
Session = sessionmaker()
session = Session(bind=engine)
db_prefix = ''


class ProjectInfo(Base):
    """CREATE TABLE ProjectInfo (
            pk                              text NOT NULL PRIMARY KEY,
            containsSingletonActions        integer NOT NULL,
            folder                          text,
            folderEffectiveActive           integer NOT NULL,
            lastReviewDate                  timestamp,
            minimumDueDate                  timestamp,
            nextReviewDate                  timestamp,
            nextTask                        text,
            numberOfAvailableTasks          integer NOT NULL,
            numberOfDueSoonTasks            integer NOT NULL,
            numberOfOverdueTasks            integer NOT NULL,
            numberOfRemainingTasks          integer NOT NULL,
            reviewRepetitionString          text,
            status                          text NOT NULL,
            task                            text,
            taskBlocked                     integer NOT NULL,
            taskBlockedByFutureStartDate    integer NOT NULL,
            taskDateToStart                 timestamp
        );

    """

    __tablename__ = db_prefix + 'ProjectInfo'

    pk = Column(Text, primary_key=True)
    task = Column(Text)


class Context(Base):
    __tablename__ = db_prefix + 'Context'

    persistentIdentifier = Column(Text, primary_key=True)
    name = Column(Text)
    tasks = relationship('Task')

    @classmethod
    def get(cls, context_name):
        return session.query(cls).filter(cls.name == context_name).one()


class Task(Base):
    """CREATE TABLE Task (
            persistentIdentifier                    text NOT NULL PRIMARY KEY,
            blocked                                 integer NOT NULL,
            blockedByFutureStartDate                integer NOT NULL,
            childrenCount                           integer NOT NULL,
            childrenCountAvailable                  integer NOT NULL,
            childrenCountCompleted                  integer NOT NULL,
            completeWhenChildrenComplete            integer NOT NULL,
            containingProjectContainsSingletons     integer NOT NULL,
            containingProjectInfo                   text,
            containsNextTask                        integer NOT NULL,
            context                                 text,
            creationOrdinal                         integer,
            dateAdded                               timestamp NOT NULL,
            dateCompleted                           timestamp,
            dateDue                                 timestamp,
            dateModified                            timestamp NOT NULL,
            dateToStart                             timestamp,
            effectiveContainingProjectInfoActive    integer NOT NULL,
            effectiveContainingProjectInfoRemaining integer NOT NULL,
            effectiveDateDue                        timestamp,
            effectiveDateToStart                    timestamp,
            effectiveFlagged                        integer NOT NULL,
            effectiveInInbox                        integer NOT NULL,
            estimatedMinutes                        integer,
            flagged                                 integer NOT NULL,
            hasCompletedDescendant                  integer NOT NULL,
            hasFlaggedTaskInTree                    integer NOT NULL,
            hasUnestimatedLeafTaskInTree            integer NOT NULL,
            inInbox                                 integer NOT NULL,
            isDueSoon                               integer NOT NULL,
            isOverdue                               integer NOT NULL,
            maximumEstimateInTree                   integer,
            minimumEstimateInTree                   integer,
            name                                    text,
            nextTaskOfProjectInfo                   text,
            noteXMLData                             blob,
            parent                                  text,
            projectInfo                             text,
            rank                                    integer NOT NULL,
            repetitionMethodString                  text,
            repetitionRuleString                    text,
            sequential                              integer NOT NULL
        );

    """

    __tablename__ = db_prefix + 'Task'

    persistentIdentifier = Column(Text, primary_key=True)
    blocked = Column(Integer)
    blockedByFutureStartDate = Column(Integer)
    childrenCount = Column(Integer)
    childrenCountAvailable = Column(Integer)
    childrenCountCompleted = Column(Integer)
    completeWhenChildrenComplete = Column(Integer)
    containingProjectContainsSingletons = Column(Integer)
    containingProjectInfo = Column(Text)
    containsNextTask = Column(Integer)
    name = Column(Text)
    context_id = Column('context', Text, ForeignKey('Context.persistentIdentifier'))
    context = relationship('Context', backref=backref('Task'))
    projectInfo = Column(Text)
    parent_id = Column('parent', Text, ForeignKey('Task.persistentIdentifier'))

    children = relationship('Task', primaryjoin='Task.persistentIdentifier == Task.parent_id')

    def __repr__(self):
        return self.name

    def context_name(self):
        return task.context.name if self.context else 'None'


class Database(object):
    @classmethod
    def get_projects(cls):
        return session.query(Task).filter(Task.projectInfo != None)

    @classmethod
    def get_project(cls, project_name):
        return cls.get_projects().filter(Task.name == project_name).one()

    @classmethod
    def get_contexts(cls):
        return session.query(Context)

    @classmethod
    def get_context(cls, context_name):
        return Context.get(context_name)


if __name__ == '__main__':
    tasks = Context.get('Costco').tasks

    for task in tasks:
        print('%-80s %-30s %d' % (task, task.context_name(), task.blocked))

    for project in Database.get_projects():
        print(project.name)

    for context in Database.get_contexts():
        print('Context: %r' % context.name)
