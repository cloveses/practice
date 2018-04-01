-module (event_mod).
-compile(export_all).
-behaviour (gen_event).

start_link() ->
    gen_event:start_link({local,?MODULE}).

init([]) -> {ok,[]}.

add_handler() ->
    gen_event:add_handler(?MODULE,?MODULE,[]).

delete_handler() ->
    gen_event:delete_handler(?MODULE,?MODULE,[]).

log_test() ->
    gen_event:notify(?MODULE,test).

handle_event(test,State) ->
    error_logger:info_msg("Test send up.~n"),
    {ok,File} = file:open("aqw.txt",write),
    io:format(File,"aqwkdkkdkd~n",[]),
    file:close(File),
    {ok,State};
handle_event(_Msg,State) ->
    {ok,State}.