-module (mybin).
-compile(export_all).

to_binary(Term) when is_atom(Term) ->
    atom_to_binary(Term,utf8);
to_binary(Term) when is_integer(Term) ->
    integer_to_binary(Term);
to_binary(Term) when is_list(Term) ->
    list_to_binary(Term);
to_binary(Term) when is_float(Term) ->
    float_to_binary(Term).

get_binary(List) -> get_binary(List,<<>>).

get_binary([],Ret) -> Ret;
get_binary([H|T],Ret) ->
    Bin = to_binary(H),
    get_binary(T,<<Ret/binary,Bin/binary>>).

to_list(List) ->
    binary_to_list(get_binary(List)).

