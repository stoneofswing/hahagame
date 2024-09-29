from operator import *

def make_converter(c, f):
    u, v, w, x, y = [make_connector() for _ in range(5)] # return 5 initialized connectors via 'make_connector'
    multiplier(c, w, u) # first call 'multiplier',input 3 connectors,
    multiplier(v, x, u)
    adder(v, y, f)
    constant(w, 9)
    constant(x, 5)
    constant(y, 32)


def adder(a, b, c):
    return make_ternary_constraint(a, b, c, add, sub, sub) 

def multiplier(a, b, c):
    return make_ternary_constraint(a, b, c, mul, truediv, truediv) # call 'make_ternary_constraint',input 3 dictionaries and 3 functions

def constant(connector, value):
    constraint = {}
    connector['set_val'](constraint, value)
    return constraint

def make_ternary_constraint(a, b, c, ab, ca, cb):

    def new_value():
        av, bv, cv = [connector['has_val']() for connector in (a, b, c)]
        if av and bv:
            c['set_val'](constraint, ab(a['val'], b['val']))
        elif av and cv:
            b['set_val'](constraint, ca(a['val'], c['val']))
        elif bv and cv:
            a['set_val'](constraint, cb(b['val'], c['val']))

    def forget_value():
        for connector in (a, b, c):     
            connector['forget'](constraint)

    constraint = {'new_value': new_value, 'forget': forget_value}
    for connector in (a, b, c):
        connector['connect'](constraint)

    return constraint


def make_connector(name=None):
    informant  = None
    constraints = []
    def set_value(source, value):
        nonlocal informant
        val = connector['val']
        if val is None:
            informant, connector['val'] = source, value
            if name is not None:
                print(name, '=', value)
            inform_all_except(source, 'new_value', constraints)
        else:
            if val != value:
                print('contradiction detected', val, 'vs', value)

    def forget_value(source):
        nonlocal informant
        if informant == source:
            informant, connector['val'] = None, None
            if name is not None:
                print(name, 'is forgotten')
            inform_all_except(source, 'forget', constraints)
        
    connector = {'val': None, 
                 'set_val': set_value,
                 'forget': forget_value,
                 'has_val': lambda: connector['val'] is not None,
                 'connect': lambda source: constraints.append(source)}

    return connector # return a dictionary

def inform_all_except(source, message, constraints):
    '''frame = inspect.currentframe()
    op(frame, honor_existing=False, depth=1)'''
    for c in constraints:
        if c != source:
            c[message]()
        else:
            print('skip', source)
    

celsius = make_connector('celsius') # not only a dictionary,but also a connector or a frame of 'make_connector'
fahrenheit = make_connector('fahrenheit') # same

make_converter(celsius, fahrenheit) # input two connector as arguement
celsius['set_val']('user', 25)
