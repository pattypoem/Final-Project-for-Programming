import datetime
import pickle
import argparse
from tabulate import tabulate
import uuid

class Task:
    """Representation of a task
    Attributes:
        - created - date (datetime module)
        - completed - date
        - name - string
        - unique id - number (UUID package)
        - priority - int value of 1, 2, or 3; 1 is default
        - due date - date, this is optional
    """
    def __init__(self, name, priority = 1):
        self.name = name
        self.priority = priority
        self.unique_id = uuid.uuid1()
        self.created = datetime.datetime.now()
        self.completed = None
        self.due_date = None

class Tasks:
    """A list of 'Task' objects."""
    def __init__(self, file):
        """Read pickled tasks file into a list"""
        
        # list of Task objects
        f = open(file, 'rb')
        try:
            self.tasks = pickle.load(f)
        except:
            self.tasks = []
        f.close()
        
    
    def pickle_tasks(self):
        """Pickle your task list to a file"""
        with open('.todo.pickle', 'wb') as f:
            pickle.dump(self.tasks, f)
    
    # Complete the rest of the methods, change the method definitions as needed
    def list(self):
        data = []
        data_with_duedate = []
        data_without_duedate = []
        for item in self.tasks:
            if item.completed == None:
                if item.due_date == '-':
                    data_without_duedate.append(item)
                else:
                    data_with_duedate.append(item)

        # sort the data with a due date
        def sort_date(item):
            duedate = datetime.datetime.strptime(item.due_date, '%m/%d/%Y')
            return duedate
        
        data_with_duedate.sort(key = sort_date)

        for item in data_with_duedate:
            time_difference = f"{(datetime.datetime.now() - item.created).days}d"
            data.append([item.unique_id, time_difference, item.due_date, item.priority, item.name, item.created, item.completed])


        # sort the data without a due date
        def sort_priority(item):
            return item.priority

        data_without_duedate.sort(key = sort_priority)

        for item in data_without_duedate:
            time_difference = f"{(datetime.datetime.now() - item.created).days}d"
            data.append([item.unique_id, time_difference, item.due_date, item.priority, item.name, item.created, item.completed])
            
        
        tasks_table = tabulate(data, headers = ['ID', 'Age', 'Due Date', 'Priority', 'Task'])
        print(tasks_table)
              

    def report(self):
        data = []
        data_with_duedate = []
        data_without_duedate = []
        for item in self.tasks:
            if item.due_date == '-':
                data_without_duedate.append(item)
            else:
                data_with_duedate.append(item)
        
        # sort the data with a due date
        def sort_date(item):
            duedate = datetime.datetime.strptime(item.due_date, '%m/%d/%Y')
            return duedate
        
        data_with_duedate.sort(key = sort_date)

        for item in data_with_duedate:
            time_difference = f"{(datetime.datetime.now() - item.created).days}d"
            data.append([item.unique_id, time_difference, item.due_date, item.priority, item.name, item.created, item.completed])


        # sort the data without a due date
        def sort_priority(item):
            return item.priority

        data_without_duedate.sort(key = sort_priority)

        for item in data_without_duedate:
            time_difference = f"{(datetime.datetime.now() - item.created).days}d"
            data.append([item.unique_id, time_difference, item.due_date, item.priority, item.name, item.created, item.completed])
            

        tasks_table = tabulate(data, headers = ['ID', 'Age', 'Due Date', 'Priority', 'Task', 'Created', 'Completed'])
        print(tasks_table)


    def done(self, id):
        for item in self.tasks:
            if item.unique_id == id:
                item.completed = datetime.datetime.now()
                break
        print(f"Completed task {id}")    

    def delete(self, id):
        for item in self.tasks:
            if item.unique_id == id:
                self.tasks.remove(item)
                break
        print(f"Deleted task {id}")


    def query(self, query_list):
        data = []
        for word in query_list:
            for item in self.tasks:
                if word in item.name:
                    time_difference = f"{(datetime.datetime.now() - item.created).days}d"
                    data_of_item = [item.unique_id, time_difference, item.due_date, item.priority, item.name]
                    if data_of_item not in data:
                        data.append(data_of_item)
        tasks_table = tabulate(data, headers = ['ID', 'Age', 'Due Date', 'Priority', 'Task'])
        print(tasks_table)


    def add(self, task_name, priority_number, due_date_item):
        new_item = Task(task_name)
        if priority_number:
            new_item.priority = priority_number
        if due_date_item:
            new_item.due_date = due_date_item
        else:
            new_item.due_date = '-'
        self.tasks.append(new_item)
        print(f"Created task {new_item.unique_id}")


def main():
    """ All the real work that drive the program"""
    parser = argparse.ArgumentParser(description='Update your ToDo list.')
    parser.add_argument('--add', type=str, required=False, help='a task string to add to your list')
    parser.add_argument('--priority',type=int, required=False, default=1, help='priority of task; default value is 1')
    parser.add_argument('--due', type=str, required=False, help='due date in dd/MM/YYYY format')
    parser.add_argument('--list', action='store_true', required=False, help='list all tasks that have not been completed')
    parser.add_argument('--query', type=str, required=False, nargs='+', help='search for tasks that match a search term')
    parser.add_argument('--done', type=int, required=False, help='complete the task')
    parser.add_argument('--delete', type=int, required=False, help='delete the task')
    parser.add_argument('--report', action='store_true', required=False, help='list all tasks')


    # Parse the argument
    args = parser.parse_args()

    # create instances of Tasks

    task_list = Tasks('.todo.pickle')

    # Read out arguments (note the types)
    if args.add:
        task_list.add(args.add, args.priority, args.due)
    elif args.list:
        task_list.list()
    elif args.report:
        task_list.report()
    elif args.query:
        task_list.query(args.query)
    elif args.done:
        task_list.done(args.done)
    elif args.delete:
        task_list.delete(args.delete)
    
    task_list.pickle_tasks()
    exit()


if __name__ == '__main__':
    main()