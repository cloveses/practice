-module (mypra).
-compile(export_all).

% No. 2
nth_list(N,Mlst) when N > 0, N =< length(Mlst) ->
    nth_list(N,Mlst,1);
nth_list(_,_) ->
    "The number is not in [0,len]!".

nth_list(N,[H|_],N) ->
    H;
nth_list(N,[_|T],M) ->
    nth_list(N,T,M + 1).

% No. 3
filter_list(Mlst) -> filter_list(Mlst,[],1).

filter_list([],Clst,_) -> lists:reverse(Clst);

filter_list([H|T],Clst,N) when N rem 2 == 1 ->
    filter_list(T,[H|Clst],N + 1);

filter_list([_|T],Clst,N) ->
    filter_list(T,Clst,N + 1).

% No. 4
filter_list2(Mlst) ->
    lists:filter(fun(X) -> X rem 2 == 1 end,Mlst).

% No. 5
mysum(Mlst,N,M) when N =< M -> mysum(Mlst,N,M,[],1);
mysum(_,_,_) -> "Error:N > M.".

mysum([],_,_,_,_) -> 0;

mysum(_,_,M,Res,Seq) when Seq > M -> lists:sum(Res);

mysum([_|T],N,M,Res,Seq) when Seq < N -> 
    mysum(T,N,M,Res,Seq + 1);

mysum([H|T],N,M,Res,Seq) when Seq >= N ->
    mysum(T,N,M,[H|Res],Seq +1).

% No. 6
pre_sub([],[]) -> 'Yes';
pre_sub([],_) -> 'Yes';
pre_sub(_,[]) -> 'No';
pre_sub([H|Ta],[H|Tb]) ->
    pre_sub(Ta,Tb);
pre_sub([_|_],[_|_]) -> 'No'.

% No. 7
myreverse([]) -> [];
myreverse(Mlst) -> myreverse(Mlst,[]).

myreverse([],Res) -> Res;
myreverse([H|Mlst],Res) -> myreverse(Mlst,[H|Res]).

% 1、将列表中的integer,float,atom转成字符串并合并成一个字个字符串：[1,a,4.9,"sdfds"] 结果："1a4.9sdfds"（禁用++ -- append concat实现）
% 2、得到列表或无组中的指定位的元素   {a,g,c,e} 第1位a      [a,g,c,e] 第1位a（禁用erlang lists API实现）
% 3、根据偶数奇数过淲列表或元组中的元素（禁用API实现）
% 4、便用匿名函数对列表奇数或偶数过淲
% 5、计算数字列表[1,2,3,4,5,6,7,8,9]索引N到M的和
% 6、查询List1是为List2的前缀（禁用string API实现）
% 7、逆转列表或元组（禁用lists API实现）
% 8、对列表进行排序
% 9、对数字列表进行求和再除以指定的参数，得到商余
% 10、获得当前的堆栈
% 11、获得列表或元组中的最大最小值（禁用API实现）
% 12、查找元素在元组或列表中的位置
% 14、判断A列表（[3,5,7,3]）是否在B列表（[8,3,5,3,5,7,3,9,3,5,6,3]）中出现，出现则输出在B列表第几位开始
% 15、{8,5,2,9,6,4,3,7,1} 将此元组中的奇数进行求和后除3的商（得值A），并将偶数求和后剩3（得值B），然后求A+B结果
% 16、在shell中将unicode码显示为中文
% 17、传入列表L1=[K|_]、L2=[V|_]、L3=[{K,V}|_]，L1和L2一一对应，L1为键列表，L2为值列表，L3存在重复键，把L3对应键的值加到L2
% 18、删除或查询元组中第N个位置的值等于Key的tuple（禁用lists API实现）
% 19、对一个字符串按指定符字劈分（禁用string API实现）
% 20、合并多个列表或元组
% 21、{5,1,8,7,3,9,2,6,4} 将偶数剩以它在此元组中的偶数位数， 比如，8所在此元组中的偶数位数为1，2所在此元组中的偶数位数为2
% 22、排序[{"a",5},{"b",1},{"c",8},{"d",7},{"e",3},{"f",9},{"g",2},{"h",6},{"i",4}],  以元组的值进行降序 优先用API
% 23、{8,5,2,9,6,4,3,7,1} 将此元组中的奇数进行求和
% 24、传入任意I1、I2、D、Tuple四个参数，检查元组Tuple在索引I1、I2位置的值V1、V2,如果V1等于V2则删除V1，把D插入V2前面，返回新元组,
%     如果V1不等于V2则把V2替换为V1，返回新元组
%     注意不能报异常，不能用try，不满足条件的，返回字符串提示
% 25、删除列表或元组中全部符合指定键的元素
% 26、替换列表或元组中第一个符合指定键的元素
% 27、将指定的元素插入到列表中指定的位置，列表中后面的元素依次向后挪动
% 28、对[6,4,5,7,1,8,2,3,9]进行排序（降序--冒泡排序）或API排序
% 29、将字符串"goods,143:6|money:15|rmb:100|money:100|goods,142:5"解析成[{money,115},{rmb,100},{goods,[{143,6},{142,5}]}]可以代码写定KEY进行匹配归类处理
% 30、移除元组或列表中指定位置的元素