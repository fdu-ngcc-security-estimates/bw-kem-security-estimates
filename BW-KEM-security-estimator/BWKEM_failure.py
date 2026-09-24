from scipy.stats import chi2
from math import exp, sqrt, log, ceil
import math
import numpy as np
from scipy.optimize import minimize_scalar
from proba_util import*

def logsum(a, b):

    if a > b:
        return a + math.log1p(math.exp(b - a))
    else:
        return b + math.log1p(math.exp(a - b))


def Chernoff_Bound(F, theta, ps):

    epsilon = var_of_law(build_mod_switching_error_law(ps.q, ps.rqc))

    sigma2_s = var_of_law(build_centered_binomial_law(ps.ks))
    sigma2_e = var_of_law(build_centered_binomial_law(ps.ke))
    sigma2_c = var_of_law(build_centered_binomial_law(ps.ke_ct))

    s_square = ps.N * ps.l * sigma2_s * (sigma2_e + sigma2_c +  epsilon)

    m_theta_log = -math.inf
    for x, fx in F.items():
        if fx <= 0:
            continue
        val = math.log(fx) + theta * (x * x) / (1 - 2 * theta * s_square)
        m_theta_log = logsum(m_theta_log, val)
    m_theta_log = m_theta_log - (1 / 2) * log(1 - 2 * theta * s_square)

    dis = ps.q * sqrt(2 * ps.n) / (2**(ps.tau + 2)) - sqrt(ps.n / 4) * (ps.q*1. / (2**(ceil(log(ps.q,2)))) + 1 )
    r_square = (dis)**2

    delta1_log = -theta * r_square + ps.n * m_theta_log
    delta_log = (delta1_log + log(ps.N / ps.n)) / log(2)

    return delta_log

def ErrorRate_BWKEM_Chernoff(ps):

    e_ct = build_centered_binomial_law(ps.ke_ct)
    ct_v = build_mod_switching_error_law(ps.q, ps.rq2)  

    e2_v = law_convolution(ct_v, e_ct)

    epsilon = var_of_law(build_mod_switching_error_law(ps.q, ps.rqc))

    sigma2_s = var_of_law(build_centered_binomial_law(ps.ks))
    sigma2_e = var_of_law(build_centered_binomial_law(ps.ke))
    sigma2_c = var_of_law(build_centered_binomial_law(ps.ke_ct))

    s_square = ps.N * ps.l * sigma2_s * (sigma2_e + sigma2_c +  epsilon)

    def objective(theta):
        if theta < 0 or theta >= 1 / (2 * s_square):
            return np.inf
        return Chernoff_Bound(e2_v, theta, ps)

    res = minimize_scalar(objective, bounds=(0, 1 / (2 * s_square)), method='bounded')
    theta_opt = res.x
    delta_log = Chernoff_Bound(e2_v, theta_opt, ps)
    print("failure probability <= 2^%.2f (theta=%.8f)" % (delta_log, theta_opt))
