#!/usr/bin/env python

"""OmniFocus CLI

Usage:
  omnifocus-cli.py project list
  omnifocus-cli.py context list
  omnifocus-cli.py project <project_name> list-tasks
  omnifocus-cli.py context <context_name> list-tasks
  omnifocus-cli.py -h | --help
  omnifocus-cli.py --version

"""

from docopt import docopt
from omnifocus import Database


def main():
    arguments = docopt(__doc__)
    # print(arguments)

    if arguments['project'] and arguments['list']:
        for project in Database.get_projects():
            print(project.name.encode('utf-8'))

    if arguments['context'] and arguments['list']:
        for context in Database.get_contexts():
            print(context.name.encode('utf-8'))

    if arguments['project'] and arguments['list-tasks']:
        project = Database.get_project(arguments['<project_name>'])
        for task in project.children:
            print('%-20s %-60s' % (task.context.name.encode('utf-8'), task.name.encode('utf-8')))

    if arguments['context'] and arguments['list-tasks']:
        context = Database.get_context(arguments['<context_name>'])
        for task in context.tasks:
            print(task.name.encode('utf-8'))


if __name__ == '__main__':
    main()
