def create():
    '''Create a task'''


def delete():
    '''Delete the task'''


def edit():
    '''Edit the task'''


def show():
    '''Show all tasks'''


def quite():
    '''Finish work with programm'''



menu = dict(zip(['c', 'd', 'e', 'sh', 'q'],
[{
'name' : 'create task',
'func' : create},
{'name' : 'delete task',
'func' : delete},
{'name' : 'edit task',
'func' : edit},
{'name' : 'show tasks',
'func' : show},
{'name' : 'quite',
'func' : quite}]))


def show_menu():
    '''Keep menu visible'''

    while 1:
        try:
            print('Choose a liter, what you wanna do!')
            for k in sorted(list(menu.items())):
                print('{} \t---\t print "{}"'.format(str(k[1]['name']), k[0]))
            i = input()
            menu[i]['func']

        except:
            print('There is no such instruction, try again!')

        else:
            if i == 'q': break

    print('Bye')
