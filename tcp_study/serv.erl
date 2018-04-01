-module (serv).
-compile(export_all).

servtcp() ->
    {ok,Ls} = gen_tcp:listen(2356,[binary]),
    {ok,_Soc} = gen_tcp:accept(Ls),
    loop(Ls).

loop(Ls) ->
    receive
        {tcp_closed,_Soc} -> 
            io:format("Closed!~n"),gen_tcp:close(Ls);
        {tcp,_Soc,Bin} -> 
            io:format("Server receiveed:~p~n",[Bin]),loop(Ls)
    end.
