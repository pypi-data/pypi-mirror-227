#includes
import os


def perimeter(a, b = "pass"): #perimeter периметр
    if b != "pass":
        try:
            return (a+b)*2
        except:
            return "FATAL ERROR"
    else:
        try:
            return a*4
        except:
            return "FATAL ERROR"

def square(a, b = "pass"): #square площадь
    if b != "pass":
        try:
            return a*b
        except:
            return "FATAL ERROR"
    else:
        try:
            return a*a
        except:
            return "FATAL ERROR"
        

def ifse(condition, action, elaction = 'False', elifcondition = 'False', elifaction = 'False'): #if else elif action - дейтвие, condition - условие
    try:
        if eval(str(condition)):
            return eval(str(action))
        elif eval(str(elifcondition)):
            return eval(str(elifaction))
        else:
            return eval(str(elaction))
    except:
        return "FATAL ERROR if construction or library construction"
def whil(condition, action): #while action - дейтвие, condition - условие
    try:
        while eval(str(condition)):
            return eval(str(action))
    except:
        return "FATAL ERROR while construction or library construction"
def forin(condition, action, rangee): #for action - дейтвие, condition - условие
    try:
        #return "for"
        for condition in eval(str(rangee)): #eval(str(condition)):
            return eval(str(action))
    except:
        return "FATAL ERROR for construction or library construction"
#@
#r
#@
#r
#@
#r
#@
#r
#@
#r
#@