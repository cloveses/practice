-module (myserv).
-behaviour (gen_server).
-compile(export_all).

start_link() ->
    gen_server:start_link({local,?MODULE},?MODULE,[],[]).

init([]) ->{ok,[]}.

add_hdl() ->
    gen_server:cast(?MODULE,addhdl).
del_hdl() ->
    gen_server:cast(?MODULE,delhdl).

log_test() ->
    event_mod:log_test().

handle_cast(addhdl,State) ->
    event_mod:add_handler(),
    {noreply,State};
handle_cast(delhdl,State) ->
    event_mod:del_handler(),
    {noreply,State}.

handle_call(_,_,State) -> {reply,{ok,ok},State}.
handle_info(_,State) -> {noreply,State}.
code_change(_OldVsn,State,_Extra) -> {ok,State}.
terminate(_,_) -> ok.