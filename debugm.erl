-module (debugm).
-export([start/0,send/1,loop/0]).

start() -> spawn_link(debugm,loop,[]).

send(Pid) ->
    Pid ! {self(),ping},
    receive pong -> pong end.

loop() ->
    receive
        {Pid,ping} ->
            spawn(crash,do_not_exist,[]),
            Pid ! pong,
            loop()
        end.