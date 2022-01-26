# TODO >> STEP1 -> implement test cases for semantic analysis
# TODO >> STEP2 -> improve struct definition handling, problem with strings (e.g. char point2[24] in STRUC FDAT)
# TODO >> STEP3 -> check what should be accomplished during semantic analysis phase and add objectives
# TODO >> STEP4 -> implement each visitor method for interpration phase


# QUESTIONS >> Where references to modules/subroutines and functions should be stored? In parse try probably,
# check if it's already implemented

#Semantic analyser goes through dat files, collecting and inserting symtables into parse tree of subroutine

#ParseTree needs symtable and symtable (for example routines symbols) need reference to part of parse trees

#During interpretation phase:
#1. going through lines, it can be variable assignment, output setting, if, switch case, subroutine call, sruct var def)
#2. it all needs reference to the symbols, to find type and to find value OR call other function/subroutine
#3. does each subroutine call need semantic analysis at the beginning?


#Some of the visitors in Semantic Analysis rely on the order of processing files (first .dat and then .src)