-module (root_sup).
-behaviour (supervisor).
-compile(export_all).

start_link() ->
    supervisor:start_link({local,?MODULE},?MODULE,[]).

init([]) ->
    Event = {event_mod,{event_mod,start_link,[]},
        permanent,2000,worker,[event_mod]},
    Myserv = {myserv,{myserv,start_link,[]},
        permanent,2000,worker,[myserv]},
    Children = [Event,Myserv],
    RestartStrategy = {one_for_one,0,1},
    {ok,{RestartStrategy,Children}}.