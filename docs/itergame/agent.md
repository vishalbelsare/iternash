Module itergame.agent
=====================

Functions
---------

    
`agent(name_or_agent_func=None, **kwargs)`
:   Decorator for easily constructing agents.
    
    If a string is passed to the decorator it will use that as the name,
    otherwise the name is inferred from the name of the function.
    
    Examples:
    
        @agent()  # or just @agent
        def x(env) =
            ...
    
        @agent("x")
        def x_agent(env) =
            ...
    
        @agent(name="x", default=...)
        def x_agent(env) =
            ...

    
`bbopt_agent(name, tunable_actor, util_func, file, alg=None, extra_copy_funcs=None, print_chosen_alg=False, **kwargs)`
:   Construct an agent that selects its action using a black box optimizer.
    
    Parameters:
    - _name_ is the name the agent's action will be assigned in the environment.
    - _tunable_actor_ is a function from (bb, env) to an action (see the BBopt docs
        for how to use the bb object to define tunable parameters).
    - _util_func_ is the a function from the env resulting from the agent's action
        to the utility it should get for that action (or just a variable name).
    - _file_ should be set to __file__.
    - _alg_ determines the black box optimization algorithm to use (the default
        is tree_structured_parzen_estimator).
    - _kwargs_ are passed to `Agent`.

    
`debug_agent(debug_str, name=None, **kwargs)`
:   Construct an agent that prints a formatted debug string.
    
    Example:
        debug_agent("x = {x}")
            is roughly equivalent to
        Agent(None, env -> print("x = {x}".format(**env)))

    
`debug_all_agent(pretty=True, **kwargs)`
:   Construct an agent that prints the entire env, prettily if _pretty_.

    
`expr_agent(name, expr, globs=None, aliases=None, eval=<built-in function eval>, **kwargs)`
:   Construct an agent that computes its action by evaluating an expression.
    
    Parameters:
    - _name_ is the name the agent's action will be assigned in the environment.
    - _expr_ is an expression to be evaluated in the environment to determine the
        agent's action.
    - _globs_ are the globals to be used for evaluating the agent's action.
    - _aliases_ are simple replacements to be made to the expr before evaluating it
        (the default is {"\n": ""}).
    - _eval_ is the eval function to use (defaults to Python eval, but can be set to
        coconut.convenience.coconut_eval instead to use Coconut eval).
    - _kwargs_ are passed to `Agent`.

    
`hist_agent(name, record_var, maxhist=None, record_var_copy_func=<object object>, initializer=(), **kwargs)`
:   Construct an agent that records a history.
    
    Parameters:
    - _name_ is the name of this agent.
    - _record_var_ is the name of the agent to record or a function of env to get the value to record.
    - _maxhist_ is the maximum history to store.
    - _initializer_ is an iterable to fill the initial history with.
    - _kwargs_ are passed to Agent.

    
`human_agent(name, pprint=True, globs=None, aliases=None, eval=<built-in function eval>, **kwargs)`
:   Construct an agent that prompts a human for an expression as in expr_agent.
    
    Parameters are as per expr_agent plus _pprint_ which determines whether to
    pretty print the environment for the human.

    
`init_agent(name, constant)`
:   Construct an agent that just initializes name to the given constant.

    
`iterator_agent(name, iterable, extra_defaults=None, extra_copy_funcs=None, **kwargs)`
:   Construct an agent that successively produces values from the given
    iterable. Extra arguments are passed to Agent.

Classes
-------

`Agent(name, actor, default=<object object>, period=1, extra_defaults={}, copy_func=<function deepcopy>, extra_copy_funcs=None, debug=False)`
:   Agent class.
    
    Parameters:
    - _name_ is the key to assign this agent's action in the environment, or None
        for no name.
    - _actor_ is a function from the environment to the agent's action.
    - _default_ is the agent's initial action.
    - _period_ is the period at which to call the agent (default is 1).
    - _extra_defaults_ are extra variables that need to be given defaults.
    - _copy_func_ determines the function used to copy the agent's action (default is deepcopy).
    - _extra_copy_funcs_ are extra copiers for other env vars put there by this agent.
    - _debug_ controls whether the agent should print what it's doing.

    ### Class variables

    `NO_DEFAULT`
    :

    ### Instance variables

    `copy_func`
    :

    `extra_copy_funcs`
    :

    ### Methods

    `clone(self, name=None, actor=None, default=<object object>, period=None, extra_defaults=None, copy_func=<object object>, extra_copy_funcs=None, debug=None)`
    :   Create a copy of the agent (optionally) with new parameters.

    `get_defaults(self)`
    :   Get a dictionary of all default values to assign.