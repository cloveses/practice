-module (otpserv).
-behaviour (gen_server).
-compile(export_all).

start_link() ->
    gen_server:start_link({local,?MODULE},?MODULE,[],[]).

init([]) ->{ok,[]}.

%用户接口
add_hdl() ->
    gen_server:cast(?MODULE,addhdl).
del_hdl() ->
    gen_server:cast(?MODULE,delhdl).
sync_hdl() ->
    gen_server:call(?MODULE,sync_hdl).
stop() ->
    gen_server:cast(?MODULE,stop).

%异步回调接口
handle_cast(addhdl,State) ->
    io:format("Action: addhdl,Success!~n"),
    {noreply,State};
handle_cast(delhdl,State) ->
    io:format("Action: delhdl,Success!~n"),
    {noreply,State};
handle_cast(stop,State) ->
    {stop,normal,State}.

%同步回调接口
handle_call(sync_hdl,_,State) -> 
    io:format("Sync Action: sync_hdl,Success!~n"),
    {reply,{ok,'sync_hdl'},State}.

%带外消息回调接口,如果不接收带外消息,则不定义此函数,会忽略到达的消息.
handle_info(_,State) -> {noreply,State}.
% code_change(_OldVsn,State,_Extra) -> {ok,State}.
terminate(_,_) -> 
    io:format("Normal Exit!"),
    ok.