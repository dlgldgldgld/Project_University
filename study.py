filter [Function, List] ==> Function = condition  => filter( lambda x: x<2, [0,1,2,3,4]) => [0,1]
reduce [Function, List] ==> if reduce( lambda x,y: x+y, [0,1,2,3,4]) ==> ((0+1) + 2)+3 .... == 10
map [Function, List]
"""
a = map( lambda x,y: x+y, [0,1,2,3,4],[3,5,1,2,8])

print a