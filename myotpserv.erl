-module(myotpserv).
-compile(export_all).
-behaviour (gen_server).
% -export ([add/4]).

add_msg(_,_,[],Newlst) -> Newlst;
add_msg(User,Msg,[{User,Msgs}|T],Newlst) ->
    [{User,[Msg|Msgs]}|T] ++ Newlst;
add_msg(User,Msg,[H|T],Newlst) ->
    add_msg(User,Msg,T,[H|Newlst]).

start_link() -> start_link([]).

start_link(DataLst) ->
    gen_server:start_link({local,?MODULE},?MODULE,DataLst,[]).

init(DataLst) -> {ok,DataLst}.

reg_user(User) ->
    gen_server:cast(?MODULE,{reg,User}).

send_msg(Msg) ->
    gen_server:cast(?MODULE,{send,Msg}).

get_statu() ->
    gen_server:call(?MODULE,statu).

handle_call(statu,_From,DataLst) ->
    {reply,DataLst,DataLst}.

handle_cast({reg,User},DataLst) ->
    {noreply,[{User,[]}|DataLst]};
handle_cast({send,{User,Msg}},DataLst) ->
    Newlst = add_msg(User,Msg,DataLst,[]),
    {noreply,Newlst}.

terminate(_,_) -> ok.