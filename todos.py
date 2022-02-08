
# TODO >> STEP1 -> implement test cases for semantic analysis
# TODO >> STEP2 -> improve struct definition handling, problem with strings (e.g. char point2[24] in STRUC FDAT)
# TODO >> STEP3 -> check what should be accomplished during semantic analysis phase and add objectives
# TODO >> STEP4 -> implement each visitor method for interpration phase



#Semantic analyser goes through dat files, collecting and inserting symtables into parse tree of subroutine

#ParseTree needs symtable and symtable (for example routines symbols) need reference to part of parse trees

#During interpretation phase:
#1. going through lines, it can be variable assignment, output setting, if, switch case, subroutine call, sruct var def)
#2. it all needs reference to the symbols, to find type and to find value OR call other function/subroutine
#3. does each subroutine call need semantic analysis at the beginning?


#Some of the visitors in Semantic Analysis rely on the order of processing files (first .dat and then .src)


#SCOPE SYMBOL TABLES HIERARCHY, CREATE AND PROCESS; WHAT WITH MODULE.DAT Symbol which need to be accessed from inside functions?
#1. GLOBAL SYMTABLE

#2. Goto MODULE.DAT, create module.dat SYMTABLE, push to the scopestack
# enc_scope = GLOBAL;
# stores variable symbols from .dat file; and MAYBE symbol of .dat file, which has ref to ctx? causes problem with invoking it, it will be available one scope higher and can be only found by TYPE, name is unknown, when calling function from outside
# stored only as reference in child scope; it will be used when searching up tree when looking for symbol

#3. Add all variable symbols to the module.dat symtable


#4. Goto MODULE.SRC, create module.src SYMTABLE, push to the scopestack, create module procedure symbol and store it in global symtable, should have ref to routinebody
# enc_scope = MODULE.DAT
# stores runtime variable symbols and formal parameters (probably)
# stored in RoutineBody ctx

### MAYBE ###
#5. Add formal parameters and declared variables on the beginning of function/procedure
###

#6. Store module.src symtable in routine body, same as other routines/functions

#7. Pop of the scopestack

#8. Go to next function definition