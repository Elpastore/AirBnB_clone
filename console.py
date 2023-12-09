#!/usr/bin/python3
import sys
import cmd
import shlex
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
            }

    def emptyline(self):
        #print('emptyline()')
        #return cmd.Cmd.emptyline(self)
        pass
    
    def precmd(self, line):
        if "." in line:
            match_1 = re.match(r'(\w+)\.show\("([^"]+)"\)', line)
            match_2 = re.match(r'(\w+)\.destroy\("([^"]+)"\)', line)
            if match_1:
                class_name = match_1.group(1)
                instance_id = match_1.group(2)
                #print(f"Class Name: {class_name}")
                #print(f"Instance ID: {instance_id}")
                line = line.replace(".", " ").replace("(","").replace(")", "")
                line  = line.split(" ")
                line = f"{line[1]} {line[0]}"
                #print(line)
                lines = line.split("\"")
                new = f'{lines[0]} {class_name} {instance_id}'
                #print(new)
                return cmd.Cmd.precmd(self, new)
            elif match_2:
                class_name = match_2.group(1)
                instance_id = match_2.group(2)
                #print(f"Class Name: {class_name}")
                #print(f"Instance ID: {instance_id}")
                line = line.replace(".", " ").replace("(","").replace(")", "")
                line  = line.split(" ")
                line = f"{line[1]} {line[0]}"
                #print(line)
                lines = line.split("\"")
                new = f'{lines[0]} {class_name} {instance_id}'
                #print(new)
                return cmd.Cmd.precmd(self, new)
  
            line = line.replace(".", " ").replace("(","").replace(")", "")
            line  = line.split(" ")
            line = f"{line[1]} {line[0]}"
            #print(line)
        return cmd.Cmd.precmd(self, line)
 
    def do_create(self, line):
        if not line:
            print("** class name missing **")
            return
        try:
            create = eval(line)()
            create.save()
            print(create.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        arguments = shlex.split(line)   #this split the line if there is spacce or quote

        if not arguments or len(arguments) < 1:
            print("** class name missing **")

        elif arguments[0] not in HBNBCommand.classes:
            print("** class doesn't exist**")

        elif len(arguments) == 1 and arguments[0] in HBNBCommand.classes:
             print("** instance id missing **")
        else:
            dictionary = storage.all()
            key = "{}.{}".format(arguments[0], arguments[1])
            if key not in dictionary:
                print("** no instance found **")
            else:
                print(dictionary[key])
        return

    def do_destroy(self, line):
        arguments = shlex.split(line)   #this split the line if there is spacce or quote
        if not arguments or len(arguments) < 1:
            print("** class name missing **")

        elif arguments[0] not in HBNBCommand.classes:
            print("** class doesn't exist**")

        elif len(arguments) == 1 and arguments[0] in HBNBCommand.classes:
             print("** instance id missing **")
        else:
            new_dict = storage.all()
            key = "{}.{}".format(arguments[0], arguments[1])
            if key not in new_dict:
                print("** no instance found **")
            else:
                del new_dict[key]
                storage.save()
        
    def do_all(self, line):
        arguments = shlex.split(line)

        string = []
        dictionary = storage.all()
        if not line:
            for key, value in dictionary.items():
                string.append(str(value))
            print(string)
        
        else:
            if arguments[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for key, value in dictionary.items():
                if key.split('.')[0] == arguments[0]:
                    string.append(str(value))
            print(string)

    def do_update(self, line):
        arguments = shlex.split(line)
        if not arguments or len(arguments) < 1:
            print("** class name missing **")
            return

        elif arguments[0] not in HBNBCommand.classes:
            print("** class doesn't exist**")
            return
        elif arguments[0] in HBNBCommand.classes and len(arguments) == 1:
            print("** instance id missing **")
            return
        elif arguments[0] in HBNBCommand.classes and len(arguments) == 2:
            print("** attribute name missing **")
            return
        elif arguments[0] in HBNBCommand.classes and len(arguments) == 3:
            print("** value missing **")
            return
        else:
            dictionary = storage.all()
            key = "{}.{}".format(arguments[0], arguments[1])
            if key not in dictionary:
                print("** no instance found **")
                return

            #update BaseModel id attr_name value
            #setattr(obj, attribute_name, value
            #ex:    obj = BaseModel()
            #       obj.name = "Betty"
            #===>   setattr(obj, name, value)
            instance = dictionary[key]
            attribute_name = arguments[2]
            if attribute_name not in ["id", "created_at", "updated_at"]:
                #if not arguments[3]:
                #    print("** value missing **")
                value = arguments[3]
                try:

                    value = type(getattr(instance, attribute_name))(value)
                except AttributeError:
                    pass
                setattr(instance, attribute_name, value)
                instance.save()
    
    def do_count(self, line):
        # count BaseModel
        arguments = shlex.split(line)
        class_name = arguments[0]
       #let's load the dictionnay containing all instances have been created
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        else:
            dictionnary = storage.all()
            count = 0
            for key in dictionnary:
                if key.split(".")[0] == class_name:
                    count += 1
            print(count)

    def do_EOF(self, line):
        print()
        return True
    
    def do_quit(self, line):
        """Quit command to exit the program

        """
        return True

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Non-interactive mode, process command-line arguments
        commands = ' '.join(sys.argv[1:])
        HBNBCommand().onecmd(commands)
    else:
        # Interactive mode
        HBNBCommand().cmdloop()
