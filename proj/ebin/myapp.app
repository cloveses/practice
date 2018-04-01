{application, myapp,
[{description,"a simple logger."},
{vsn,"1.0"},
{modules,[event_api,root_sup,event_app]},
{registered,[root_sup]},
{applications,[kernel,stdlib]},
{mod,{event_app,[]}}]}.