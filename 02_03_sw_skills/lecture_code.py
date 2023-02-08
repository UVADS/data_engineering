






#% 5 OPEN CLOSED 

if workobj == type1:
    print("execute code for type 1")

elif workobj == type2:
    print("execute code for type 2")
else:
    print("execute code for all other types")



#### What happens if I add a new type, and/or I end up having 10 types?
# better:
class DefaultType:
    ...
    def do_work(self):
        print("execute code for all types")

class Type1(DefaultType):
    def do_work(self):
        print("execute for type 1")

class Type2(DefaultType):
    def do_work(self):
        print("execute for type 2")


class Type3

concrete_type = TypeX()

concrete_type.do_work()

# NOTE: especially bad when you have multiple if/else ladders!




#% 6 Liskov Substitution (Ducks)

class Special:
    def do_special_things():
        print("doing special things")

def do_even_more_special_things():
        print("doing even more special things")


def function_to_trigger_special(special):
    # code does stuff


class Ordinary:  # NB: does NOT inherit from Special
    def do_special_things():
        with open('somefile.txt', 'w') as target:
            target.write('writing ordinary things to a file')
        

    def do_even_more_special_things():
        with open('somefile.txt', 'w') as target:
            target.write('writing more ordinary things to a file')

extra = Special()
function_to_trigger_special(extra)

norm = Ordinary()
function_to_trigger_special(norm)

## Note that we don't have to know how the function works, as long as we know how to
## "quack like a duck"



#% 7 Dependency Inversion

cont = Controller()

data = Data()

report = Reportmaker()

# Controler uses data and Reportmaker

# so easy to see Reportmaker should have no knowledge of how data and controller work

# BUT Controller should also NOT know how Reportmaker works
# for example

report = ReportPrinter(parameters)

if isinstance(report, pdfwriter):
    # call it's pdf writer
else isinstance(report, textwriter):
    # write it ourselves


# Better:
report = ReportPrinter()

report.write()  # have subclasses handle the details, that way Data Nor Controller need to know.




















