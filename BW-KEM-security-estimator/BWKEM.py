from math import log, ceil
from BWKEM_failure import *
from MLWE_security import MLWE_summarize_attacks, MLWEParameterSet
from proba_util import build_mod_switching_error_law

class BWKEM_ParameterSet:
    def __init__(self, N, l, q, ks, ke, rqc, rq2, n, tau, ke_ct=None):
        if ke_ct is None:
            ke_ct = ke
        self.N = N
        self.l = l
        self.q = q
        self.ks = ks          # binomial distribution B_{ks} for the secret key
        self.ke = ke          # binomial distribution B_{ke} for the public key errors
        self.ke_ct = ke_ct    # binomial distribution B_{ke_ct} for the ciphertext errors
        self.rqc = rqc        # 2^(bits in the first ciphertext)
        self.rq2 = rq2        # 2^(bits in the second ciphertext)
        
        # parameters of C_{n,\tau}(\lambda)
        self.n = n
        self.tau = tau


def BWKEM_to_MLWE(ps):
    if ps.ks != ps.ke:
        raise "The security script does not handle different error parameter in secrets and errors (ks != ke) "

    # Check whether ciphertext error variance after rounding is larger than secret key error variance
    Rc = build_mod_switching_error_law(ps.q, ps.rqc)
    var_rounding = sum([i*i*Rc[i] for i in Rc.keys()])

    if ps.ke_ct/2. + var_rounding < ps.ke/2.:
        raise "The security of the ciphertext MLWE may not be stronger than the one of the public key MLWE"    

    return MLWEParameterSet(ps.N, ps.l, ps.l + 1, ps.ks, ps.q)


def keySize(ps):
    mu = ps.tau * ps.n - ps.n * (log(ps.n,2) - 1) / 4.
    Kmax = (ps.N / ps.n)  * mu / 8.
    # print('|K_max| = %d\n'%(Kmax))
    return Kmax


def communication_costs(ps):
    """ Compute the communication cost of a parameter set
    :param ps: Parameter set (ParameterSet)
    :returns: (|pk|, |ct|) (in Bytes)
    """
    seedLen = keySize(ps)
    pk = seedLen + ps.l * ceil( ps.N * ceil(log(ps.q,2))/8)
    ct = ps.l * ceil(ps.N * ceil(log(ps.rqc,2))/8) + ceil(ps.N * ceil(log(ps.rq2,2))/8)
    print('|K| = %d, |pk| = %d, |ct| = %d'%(seedLen, pk, ct))
    return (pk, ct)

def summarize(ps):
    print ("params: ", ps.__dict__)
    print ("security:")
    MLWE_summarize_attacks(BWKEM_to_MLWE(ps))
    print ("com costs: ", communication_costs(ps))
    ErrorRate_BWKEM_Chernoff(ps)


if __name__ == "__main__":

    # BWKEM_ParameterSet(N, l, q, eta_s, eta_e, 2**du, 2**dv, n, tau,
    #                    ke_ct=eta_ct)

    # Recommended parameter sets from Table 2
    BW_KEM_c128 = BWKEM_ParameterSet(
        256, 2, 3329, 6, 6, 2**10, 2**4, 8, 1, ke_ct=5
    )
    BW_KEM_c256 = BWKEM_ParameterSet(
        256, 4, 3329, 3, 3, 2**10, 2**5, 32, 2, ke_ct=3
    )
    BW_KEM_c384 = BWKEM_ParameterSet(
        512, 3, 3329, 2, 2, 2**10, 2**4, 32, 2, ke_ct=2
    )
    BW_KEM_c512 = BWKEM_ParameterSet(
        512, 4, 3329, 2, 2, 2**10, 2**6, 32, 2, ke_ct=2
    )

    # Strengthened parameter sets from Table 2
    BW_KEM_c128_s = BWKEM_ParameterSet(
        256, 2, 3329, 6, 6, 2**11, 2**5, 8, 1, ke_ct=5
    )
    BW_KEM_c256_s = BWKEM_ParameterSet(
        256, 4, 3329, 3, 3, 2**11, 2**6, 32, 2, ke_ct=3
    )
    BW_KEM_c384_s = BWKEM_ParameterSet(
        512, 3, 3329, 2, 2, 2**11, 2**5, 32, 2, ke_ct=2
    )
    BW_KEM_c512_s = BWKEM_ParameterSet(
        512, 4, 3329, 2, 2, 2**11, 2**7, 32, 2, ke_ct=2
    )

    parameter_sets = (
        ("BW-KEM-c128", BW_KEM_c128),
        ("BW-KEM-c256", BW_KEM_c256),
        ("BW-KEM-c384", BW_KEM_c384),
        ("BW-KEM-c512", BW_KEM_c512),
        ("BW-KEM-c128-s", BW_KEM_c128_s),
        ("BW-KEM-c256-s", BW_KEM_c256_s),
        ("BW-KEM-c384-s", BW_KEM_c384_s),
        ("BW-KEM-c512-s", BW_KEM_c512_s),
    )

    for name, parameter_set in parameter_sets:
        print(f"{name}:")
        print("--------------------")
        summarize(parameter_set)
        print()
