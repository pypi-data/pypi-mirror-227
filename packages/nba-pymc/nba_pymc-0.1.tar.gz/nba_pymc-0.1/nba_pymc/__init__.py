from pymc.util import UNSET
from pymc import *
from nbag import construct
import pymc


def aR(rho, *args, name=None, steps=None, constant=False, ar_order=None, **kwargs):
    return construct(pymc.AR, name, rho, *args, steps=steps, constant=constant, ar_order=ar_order, **kwargs)

def asymmetricLaplace(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.AsymmetricLaplace, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def bernoulli(*args, name=None, **kwargs):
    return construct(pymc.Bernoulli, name, *args, **kwargs)

def beta(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Beta, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def betaBinomial(*args, name=None, **kwargs):
    return construct(pymc.BetaBinomial, name, *args, **kwargs)

def binomial(*args, name=None, **kwargs):
    return construct(pymc.Binomial, name, *args, **kwargs)

def bound(dist, lower=None, upper=None, size=None, shape=None, initval=None, dims=None, name=None, **kwargs):
    return construct(pymc.Bound, name, dist, lower, upper, size, shape, initval, dims, **kwargs)

def cAR(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.CAR, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def categorical(*args, name=None, **kwargs):
    return construct(pymc.Categorical, name, *args, **kwargs)

def cauchy(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Cauchy, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def censored(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Censored, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def chiSquared(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.ChiSquared, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def constantData(value, name=None, *, dims=None, coords=None, export_index_as_coords=False, infer_dims_and_coords=False, **kwargs):
    return construct(pymc.ConstantData, name, value, dims=dims, coords=coords, export_index_as_coords=export_index_as_coords, infer_dims_and_coords=infer_dims_and_coords, **kwargs)

def continuous(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Continuous, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def customDist(*dist_params, name=None, dist=None, random=None, logp=None, logcdf=None, moment=None, ndim_supp=0, ndims_params=None, dtype='floatX', **kwargs):
    return construct(pymc.CustomDist, name, *dist_params, dist=dist, random=random, logp=logp, logcdf=logcdf, moment=moment, ndim_supp=ndim_supp, ndims_params=ndims_params, dtype=dtype, **kwargs)

def data(value, name=None, *, dims=None, coords=None, export_index_as_coords=False, infer_dims_and_coords=False, mutable=None, **kwargs):
    return construct(pymc.Data, name, value, dims=dims, coords=coords, export_index_as_coords=export_index_as_coords, infer_dims_and_coords=infer_dims_and_coords, mutable=mutable, **kwargs)

def customDist(*dist_params, name=None, dist=None, random=None, logp=None, logcdf=None, moment=None, ndim_supp=0, ndims_params=None, dtype='floatX', **kwargs):
    return construct(pymc.CustomDist, name, *dist_params, dist=dist, random=random, logp=logp, logcdf=logcdf, moment=moment, ndim_supp=ndim_supp, ndims_params=ndims_params, dtype=dtype, **kwargs)

def deterministic(var, model=None, dims=None, name=None):
    return construct(pymc.Deterministic, name, var, model, dims)

def diracDelta(*args, name=None, **kwargs):
    return construct(pymc.DiracDelta, name, *args, **kwargs)

def dirichlet(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Dirichlet, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def dirichletMultinomial(*args, name=None, **kwargs):
    return construct(pymc.DirichletMultinomial, name, *args, **kwargs)

def discrete(*args, name=None, **kwargs):
    return construct(pymc.Discrete, name, *args, **kwargs)

def discreteUniform(*args, name=None, **kwargs):
    return construct(pymc.DiscreteUniform, name, *args, **kwargs)

def discreteWeibull(*args, name=None, **kwargs):
    return construct(pymc.DiscreteWeibull, name, *args, **kwargs)

def distribution(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Distribution, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def eulerMaruyama(dt, sde_fn, *args, name=None, steps=None, **kwargs):
    return construct(pymc.EulerMaruyama, name, dt, sde_fn, *args, steps=steps, **kwargs)

def exGaussian(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.ExGaussian, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def exponential(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Exponential, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def gamma(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Gamma, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def gaussianRandomWalk(*args, name=None, **kwargs):
    return construct(pymc.GaussianRandomWalk, name, *args, **kwargs)

def geometric(*args, name=None, **kwargs):
    return construct(pymc.Geometric, name, *args, **kwargs)

def gumbel(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Gumbel, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def halfCauchy(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.HalfCauchy, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def halfNormal(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.HalfNormal, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def halfStudentT(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.HalfStudentT, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def hurdleGamma(psi, alpha=None, beta=None, mu=None, sigma=None, name=None, **kwargs):
    return construct(pymc.HurdleGamma, name, psi, alpha, beta, mu, sigma, **kwargs)

def hurdleLogNormal(psi, mu=0, sigma=None, tau=None, name=None, **kwargs):
    return construct(pymc.HurdleLogNormal, name, psi, mu, sigma, tau, **kwargs)

def hurdleNegativeBinomial(psi, mu=None, alpha=None, p=None, n=None, name=None, **kwargs):
    return construct(pymc.HurdleNegativeBinomial, name, psi, mu, alpha, p, n, **kwargs)

def hurdlePoisson(psi, mu, name=None, **kwargs):
    return construct(pymc.HurdlePoisson, name, psi, mu, **kwargs)

def hyperGeometric(*args, name=None, **kwargs):
    return construct(pymc.HyperGeometric, name, *args, **kwargs)

def interpolated(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Interpolated, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def inverseGamma(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.InverseGamma, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def kroneckerNormal(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.KroneckerNormal, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def kumaraswamy(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Kumaraswamy, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def lKJCholeskyCov(eta, n, sd_dist, name=None, *, compute_corr=True, store_in_trace=True, **kwargs):
    return construct(pymc.LKJCholeskyCov, name, eta, n, sd_dist, compute_corr=compute_corr, store_in_trace=store_in_trace, **kwargs)

def lKJCorr(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.LKJCorr, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def laplace(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Laplace, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def logNormal(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.LogNormal, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def logistic(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Logistic, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def logitNormal(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.LogitNormal, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def logNormal(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.LogNormal, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def matrixNormal(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.MatrixNormal, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def mixture(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Mixture, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def moyal(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Moyal, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def multinomial(*args, name=None, **kwargs):
    return construct(pymc.Multinomial, name, *args, **kwargs)

def mutableData(value, name=None, *, dims=None, coords=None, export_index_as_coords=False, infer_dims_and_coords=False, **kwargs):
    return construct(pymc.MutableData, name, value, dims=dims, coords=coords, export_index_as_coords=export_index_as_coords, infer_dims_and_coords=infer_dims_and_coords, **kwargs)

def mvGaussianRandomWalk(*args, name=None, **kwargs):
    return construct(pymc.MvGaussianRandomWalk, name, *args, **kwargs)

def mvNormal(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.MvNormal, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def mvStudentT(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.MvStudentT, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def mvStudentTRandomWalk(*args, name=None, **kwargs):
    return construct(pymc.MvStudentTRandomWalk, name, *args, **kwargs)

def negativeBinomial(*args, name=None, **kwargs):
    return construct(pymc.NegativeBinomial, name, *args, **kwargs)

def normal(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Normal, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def normalMixture(w, mu, sigma=None, tau=None, comp_shape=(), name=None, **kwargs):
    return construct(pymc.NormalMixture, name, w, mu, sigma, tau, comp_shape, **kwargs)

def orderedLogistic(*args, name=None, compute_p=True, **kwargs):
    return construct(pymc.OrderedLogistic, name, *args, compute_p=compute_p, **kwargs)

def orderedMultinomial(*args, name=None, compute_p=True, **kwargs):
    return construct(pymc.OrderedMultinomial, name, *args, compute_p=compute_p, **kwargs)

def orderedProbit(*args, name=None, compute_p=True, **kwargs):
    return construct(pymc.OrderedProbit, name, *args, compute_p=compute_p, **kwargs)

def pareto(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Pareto, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def poisson(*args, name=None, **kwargs):
    return construct(pymc.Poisson, name, *args, **kwargs)

def polyaGamma(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.PolyaGamma, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def potential(var, model=None, dims=None, name=None):
    return construct(pymc.Potential, name, var, model, dims)

def rice(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Rice, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def simulator(*args, name=None, **kwargs):
    return construct(pymc.Simulator, name, *args, **kwargs)

def skewNormal(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.SkewNormal, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def stickBreakingWeights(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.StickBreakingWeights, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def studentT(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.StudentT, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def triangular(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Triangular, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def truncated(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Truncated, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def truncatedNormal(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.TruncatedNormal, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def uniform(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Uniform, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def vonMises(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.VonMises, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def wald(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Wald, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def weibull(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Weibull, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def wishart(*args, name=None, rng=None, dims=None, initval=None, observed=None, total_size=None, transform=UNSET, **kwargs):
    return construct(pymc.Wishart, name, *args, rng=rng, dims=dims, initval=initval, observed=observed, total_size=total_size, transform=transform, **kwargs)

def wishartBartlett(S, nu, is_cholesky=False, return_cholesky=False, initval=None, name=None):
    return construct(pymc.WishartBartlett, name, S, nu, is_cholesky, return_cholesky, initval)

def zeroInflatedBinomial(psi, n, p, name=None, **kwargs):
    return construct(pymc.ZeroInflatedBinomial, name, psi, n, p, **kwargs)

def zeroInflatedNegativeBinomial(psi, mu=None, alpha=None, p=None, n=None, name=None, **kwargs):
    return construct(pymc.ZeroInflatedNegativeBinomial, name, psi, mu, alpha, p, n, **kwargs)

def zeroInflatedPoisson(psi, mu, name=None, **kwargs):
    return construct(pymc.ZeroInflatedPoisson, name, psi, mu, **kwargs)

