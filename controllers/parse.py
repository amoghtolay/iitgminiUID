###############################################################
# Amogh's code for
# This is the page having only one text box and will get the
# query and proceed appropriately
##############################################################
import json
from types import *
def generateQuery():
    filterNum = (len(request.vars)) /2;
    index = 0;
    queries = []
    queries.append ( dbUid.allResidents.id > 0 )
    while index < filterNum:
        for table in dbUid:
            for field in table:
                if ( index < filterNum ):
                    key = request.vars['where'+str(index)].strip('\r\n')
                    value = request.vars['input'+str(index)].strip('\n\r')
                    if ( key == str ( field ) ):
                        queries.append( field.contains( value ) )
                        index+=1
    queryAnd = reduce ( lambda a,b: ( a&b ), queries )
    rows = dbUid( queryAnd ).select()
#################################################################
# Singleton query append. Useful for query generation of one and
# appending to prev one
###############################################################
def genAndAppend( oldQuery, singleQuery, operator, isFirst ):
    if type( singleQuery[0] ) is ListType:
        print "Is list"
        pass
    # call itself function over here to ensure nesting is taken care of
    else:
        for table in dbUid:
            for field in table:
                if singleQuery[0] == str(field):
                    if singleQuery[2] == "contains":
                        newQuery = field.contains( singleQuery[1] )
                    if singleQuery[2] == "==":
                        newQuery = ( field == singleQuery[1] )
                    if singleQuery[2] == ">":
                        newQuery = ( field > singleQuery[1] )
                    if singleQuery[2] == "<":
                        newQuery = ( field > singleQuery[1] )
                    if singleQuery[2] == ">=":
                        newQuery = ( field >= singleQuery[1] )
                    if singleQuery[2] == "<=":
                        newQuery = ( field <= singleQuery[1] )
                    if singleQuery[2] == "like":
                        newQuery = ( field.like( singleQuery[1] ) )
                    if singleQuery[2] == "startswith":
                        newQuery = ( field.startswith( singleQuery[1] ) )
        if isFirst:
            return newQuery
        if operator == "AND":
            return ( oldQuery & newQuery )
        if operator == "OR":
            return ( oldQuery | newQuery )

def parseAndQueryGenerate():
    rawStringTemp = """
                    [
                        (
                            "allResidents.name",
                            "Amogh",
                            "contains",
                        ),
                        (
                            "allResidents.uid",
                            "0",
                            ">",
                        ),
                        [
                            (
                                "allResidents.fbLink",
                                "facebook",
                                "contains",
                            ),
                            (
                                "allResidents.type",
                                "Student",
                                "==",
                            )
                        ]
                    ]
                    """
    rawStringTempSimple = """
                    [
                        [
                            "allResidents.name",
                            "Amogh",
                            "contains",
                            "AND"
                        ],
                        [
                            "allResidents.uid",
                            "0",
                            ">",
                            "OR"
                        ],
                        [
                            "allResidents.fbLink",
                            "amogh",
                            "contains",
                            "X"
                        ]
                    ]
                    """
    rawQuery = json.loads ( rawStringTempSimple )
# Now, got the rawQuery in RAM in the form of dicts of dicts
# now, generate the query
# Now, queryList contains all independent queries
# Now, get the operator precedence and other stuff from rawQuery
    for i in range( len( rawQuery ) ):
        if i is 0:
            queryCreate = genAndAppend ( None, rawQuery[i], "X", True )
        if type( rawQuery[i-1][0] ) is not ListType:
            if rawQuery[i-1][3] == "AND":
                queryCreate = genAndAppend ( queryCreate, rawQuery[i], "AND", False )
            if rawQuery[i-1][3] == "OR":
                queryCreate = genAndAppend ( queryCreate, rawQuery[i], "OR", False )
        if type( rawQuery[i-1][0] ) is ListType:
            pass

    print queryCreate
    rows = dbUid( queryCreate ).select()
    tempOut = ""
    for row in rows:
        tempOut += str(row.id) + ", "
    return tempOut
