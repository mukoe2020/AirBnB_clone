#!/usr/bin/python3

import cmd

class MyCLI(cmd.Cmd):
    def do_hello(self, person):
        """Greeting a person"""
        if person:
            print("hello there!", person)
        else:
            print("hi you!")

    def do_EOF(self, arg):
        """Exiting the program with ctrl D"""
        return True
    
    def do_exit(self, arg):
        """Exiting the console with exit or ctrl C"""
        return True
    
if __name__ == "__main__":
    MyCLI().cmdloop()