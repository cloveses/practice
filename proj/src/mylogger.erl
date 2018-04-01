-module (mylogger).
-behaviour (gen_event).
-compile(export_all).

add_handler() ->
    event_api:add_handler(?MODULE,[]).

delete_handler() ->
    event_api:delete_handler(?MODULE,[]).

handle_event({opt,_},State) ->
    error_logger:info_msg("abcccc opt."),
    {ok,State};
handle_event(_Msg,State) ->
    {ok,State}.
