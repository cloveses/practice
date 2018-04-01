-module (event_app).
-behaviour (application).

-compile(export_all).

start(_Type,_StartArgs) ->
    case root_sup:start_link() of
        {ok,Pid} -> {ok,Pid};
        Other ->
            {error,Other}
    end.

stop(_State) -> ok.