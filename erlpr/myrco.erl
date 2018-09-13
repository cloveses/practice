-module (myrco).
-compile(export_all).

-include ("rec.hrl").

test(#person{age=Age} = P) ->
    P#person{age = Age + 1}.

showPerson(#person{age=Age,name=Name} = _) ->
    io:format("name:~p age:~p~n",[Name,Age]).
