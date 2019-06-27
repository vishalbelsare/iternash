#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x336a5d9f

# Compiled with Coconut version 1.4.0-post_dev40 [Ernest Scribbler]

# Coconut Header: -------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.dirname(_coconut_os_path.abspath(__file__)))
_coconut_cached_module = _coconut_sys.modules.get(str("__coconut__"))
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules[str("__coconut__")]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import *
from __coconut__ import _coconut, _coconut_MatchError, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_forward_dubstar_compose, _coconut_back_dubstar_compose, _coconut_pipe, _coconut_back_pipe, _coconut_star_pipe, _coconut_back_star_pipe, _coconut_dubstar_pipe, _coconut_back_dubstar_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_get_function_match_error, _coconut_base_pattern_func, _coconut_addpattern, _coconut_sentinel, _coconut_assert
if _coconut_sys.version_info >= (3,):
    _coconut_sys.path.pop(0)

# Compiled Coconut: -----------------------------------------------------------

from scipy.special import comb
from mpmath import hyp2f1

from iternash import Game
from iternash import agent
from iternash import expr_agent
from iternash import bbopt_agent
from iternash import debug_agent


common_params = dict(m=100, eps=0.01, p_mod=0.9, r_n=0, r_m=1, r_f=0)


# conservative estimate of required training episodes
conservative_n_agent = expr_agent(name="n", expr="m/p_mod * (1-eps)/eps", default=common_params["m"])


# black-box-optimized n agent that attempts to set PC to eps
bbopt_n_agent = bbopt_agent(name="n", tunable_actor=lambda bb, env: int(conservative_n_agent(env) * bb.loguniform("n/n_c", 0.001, 1000)), util_func=expr_agent(None, "-abs(math.log(PC) - math.log(eps))"), file=__file__, default=common_params["m"])


# optimal defection probability in the sequential defection game
#  (note that this formula is recursive and requires iteration to solve)
seq_d_p_agent = expr_agent(name="p", expr="""(
    (n * p_mod - (d-1)/(1-p))
    / (n * p_mod + m - (d-1)/(1-p))
    * (r_m - r_n)/(r_m - r_f)
)^(1/(m-d))""", default=0.9)


# probability of catastrophe in the sequential defection game
seq_d_PC_agent = expr_agent(name="PC", expr="(1-p)^(d-1) * (1 - p^(m-d+1))", default=0.1)


# optimal defection probability in the non-sequential two defection game
nonseq_2d_p_agent = expr_agent(name="p", expr="""(
    (n * p_mod)
    / (n * p_mod + m*(m-1))
    * (r_m - r_n)/(r_m - r_f)
)^(1/(m-1))""", default=0.9)


# probability of catastrophe in the non-sequential two defection game
nonseq_2d_PC_agent = expr_agent(name="PC", expr="1 - p^m - m*(1-p)*p^(m-1)", default=0.1)


# black-box-optimized p agent that attempts to find the optimal p
#  in the non-sequential defection game
def _coconut_lambda_0(env):
    p = env["p"]
    p_mod = env["p_mod"]
    n = env["n"]
    PC = env["PC"]
    return (p + (1 - p) * (1 - p_mod))**n * PC
nonseq_d_bbopt_p_agent = bbopt_agent(name="p", tunable_actor=lambda bb, env: 1 - bb.loguniform("p", 0.000001, 1), util_func=(_coconut_lambda_0), file=__file__, default=0.9)


# probability of catastrophe in the non-sequential defection game
@agent(name="PC", default=0.1)
def nonseq_d_PC_agent(env):
    m = env["m"]
    d = env["d"]
    p = env["p"]


# agent that prints n, p, PC every 100 steps
    return comb(m, d) * p**(m - d) * (1 - p)**d * (_coconut_forward_compose(hyp2f1, float))(1, d - m, d + 1, (p - 1) / p)
printing_debugger = debug_agent("n = {n}; p = {p}; PC = {PC}", period=100)


# absent-minded driver game where catastrophe occurs if there are
#  ever d sequential defections during deployment
seq_d_game = Game("seq_d_game", conservative_n_agent, seq_d_PC_agent, seq_d_p_agent, printing_debugger, d=2, **common_params)


# absent-minded driver game where catastrophe occurs upon the
#  second defection during deployment
nonseq_2d_game = Game("nonseq_2d_game", bbopt_n_agent, nonseq_2d_p_agent, nonseq_2d_PC_agent, printing_debugger, **common_params)


# absent-minded driver game where catastrophe occurs upon the
#  dth defection during deployment
nonseq_d_game = Game("nonseq_d_game", nonseq_d_bbopt_p_agent, bbopt_n_agent, nonseq_d_PC_agent, printing_debugger, d=2, **common_params)


if __name__ == "__main__":
    print("Running sequential defection game...")
    (print)(seq_d_game.run(500))

    print("Running non-sequential two defection game...")
    (print)(nonseq_2d_game.run(500))

    print("Running non-sequential defection game...")
    (print)(nonseq_d_game.run(500))
