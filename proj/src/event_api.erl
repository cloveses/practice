-module (event_api).
-compile(export_all).

start_link() ->
    gen_event:start_link({local,?MODULE}).

add_handler(Handler,Args) ->
    gen_event:add_handler(?MODULE,Handler,Args).

delete_handler(Handler,Args) ->
    gen_event:delete_handler(?MODULE,Handler,Args).

issue(Val) ->
    gen_event:notify(?MODULE,{opt,Val}).