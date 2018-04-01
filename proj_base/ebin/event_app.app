{application, event_app,
[{description,"a simple logger."},
{vsn,"1.0"},
{modules,[event_mod,root_sup,event_app,myserv]},
{registered,[event_mod,root_sup,myserv]},
{applications,[kernel,stdlib]},
{mod,{event_app,[]}}]}.