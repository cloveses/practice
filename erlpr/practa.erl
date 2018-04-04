-module (practa).
-compile(export_all).


% 对数字列表中指定位置前后元素分别求和，并计算他们的商和余数
cacl(_N,L) when not is_tuple(L);not is_list(L) -> "Error!";

cacl(N,L) when is_tuple(L) -> cacl2(N,tuple_to_list(L));

cacl(N,L) ->cacl2(N,L).

cacl2(N,L) when N < 1;N > length(L) ->
    "Error!";

cacl2(N,L) ->
    {L1,L2} = lists:split(N,L),
    L1sum = lists:sum(L1),
    L2sum = lists:sum(L2),
    {L1sum div L2sum,L1sum rem L2sum}.

% # 元组列表的格式化
% [{money,200},{goods,1001,1},{goods,71143,9},{money,150},{rmb,600},{goods,71143,1},{goods,1001,1},{card,3001,281479271678954},{card,4001,281479271678955}]
% [{money,350},{goods,[{1001,2},{71143,10}]},{rmb,600},{card,[{3001,281479271678953},{4001,281479271678955}]}]

% 列表全部转为元组便于操作
combine(L) -> 
    combine(lists:map(fun(X) -> tuple_to_list(X) end,L),[]).


combine([],Res) -> Res;
% 从列表中取出一项，进行匹配操作（求和或合并）
combine([H|T],Res) -> combine(T,comba(H,Res,[])).

% 无匹配，则直接加入
comba(H,[],Rem) -> [H|Rem];

%匹配，且可求和
comba([K|T1],[[K|T2]|Rt],Rem) when length(T1) == 1,length(T2) ==1 ->
    [[K,lists:nth(1,T1)+lists:nth(1,T2)]|Rt] ++ Rem;
%匹配，加入列表
comba([K|T1],[[K|T2]|Rt],Rem) ->
    [[K,[list_to_tuple(T1),list_to_tuple(T2)]] | Rt++Rem];
%无匹配，继续取下一项匹配
comba(H,[Rh|Rt],Rem) -> comba(H,Rt,[Rh|Rem]).

%主调用函数
format(L) -> lists:map(fun(X) -> list_to_tuple(X) end,combine(L)).



format2([]) -> [];
format2(L) -> format2(L,[]).

format2([],Lb) -> Lb;
format2([H|T],Lb) -> 
    case lists:keyfind(element(1,H),1,Lb) of
        false -> format2(T,[H|Lb]);
        Res ->format2(T,combb(H,Res,Lb))
    end.

combb(H,Res,Lb) when length(H) == 2,length(Res) == 2 ->
    lists:keyreplace(element(1,Res),Lb,{element(1,Res),element(2,Res) + element(2,H)});

combb(H,Res,Lb) when is_tuple(Res)->
    {_,Ht} = lists:split(1,tuple_to_list(H)),
    {[K|_],Rt} = lists:split(1,tuple_to_list(Res)),
    lists:keyreplace(K,Lb,{K,[list_to_tuple(Ht),list_to_tuple(Rt)]});

combb(H,[K,Rt],Lb) ->
    {_,Ht} = lists:split(1,tuple_to_list(H)),
    lists:keyreplace(K,Lb,{K,[list_to_tuple(Ht)|Rt]}).
