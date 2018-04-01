-module(root_sup).
-compile(export_all).

-behaviour(supervisor).

start_link() ->
    supervisor:start_link({local,?MODULE},?MODULE,[]).

init([]) ->
    RootMgr = {event_api, {event_api, start_link,[]},
            permanent,2000,worker,[event_api]},
    Children =[RootMgr],
    RestartStrategy = {one_for_one,4,3600},
    {ok, {RestartStrategy,Children}}.