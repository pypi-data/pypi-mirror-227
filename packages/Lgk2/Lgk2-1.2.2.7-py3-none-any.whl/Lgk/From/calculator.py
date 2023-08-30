import math

def calculator(args):
    args = "".join(args)
    args = eval(args)
    return args

def calculate(args):
    args = args.replace("x", "*").replace("×", "*").replace("^", "**").replace("÷", "/")