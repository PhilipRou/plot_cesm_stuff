import numpy as np
import xarray as xr
from cartopy.util import add_cyclic_point



def make_cyclic(da):
    values_cyc, lon_cyc = add_cyclic_point(da, da.lon)
    da_cyclic = xr.DataArray(values_cyc, coords={'lat': da.lat, 'lon':lon_cyc})
    return da_cyclic



def moderation_exacerbation_metric(data_ref_mean, data_SAI_mean, data_noSAI_mean):
    '''
    Determines whether SAI leads to moderation compared to no-SAI (negative result)
    or exacerbation (positive result).
    '''
    return np.abs(data_SAI_mean - data_ref_mean) - np.abs(data_noSAI_mean - data_ref_mean)



def significant_moderation_exacerbation(data_ref_mean, data_SAI_eoc, data_noSAI_eoc, n_boot=1000, seed=0):
    '''
    Bootstrap of moderation_exacerbation_metric to determine its uncertainty.
    '''
    D_mean = moderation_exacerbation_metric(data_ref_mean, data_SAI_eoc.mean(dim="year"), data_noSAI_eoc.mean(dim="year"))
    n = data_SAI_eoc.sizes["year"]
    # assert data_noSAI_eoc.sizes["year"] == n

    rng = np.random.default_rng(seed)
    counts = rng.multinomial(n, np.full(n, 1 / n), size=n_boot)   # (n_boot, n): draws per year
    weights = xr.DataArray(counts / n, dims=("boot", "year"))

    D_boot = moderation_exacerbation_metric(
        data_ref_mean,
        xr.dot(weights, data_SAI_eoc, dim="year"),
        xr.dot(weights, data_noSAI_eoc, dim="year")
    )
    sigma = D_boot.std("boot")

    return D_mean, sigma



def get_moderation_exacerbation_masks(D_mean, sigma, k=2.0):
    # mask_significant = (k * sigma < np.abs(D_mean))
    mask_moderate    = (D_mean + k * sigma < 0).fillna(False)# .where(mask_significant).fillna(False)
    mask_exacerbate  = (D_mean - k * sigma > 0).fillna(False)# .where(mask_significant).fillna(False)
    mask_insignificant = k * sigma > np.abs(D_mean)

    mask_moderate = make_cyclic(mask_moderate)
    mask_exacerbate = make_cyclic(mask_exacerbate)
    mask_insignificant = make_cyclic(mask_insignificant)

    return mask_moderate, mask_exacerbate, mask_insignificant



def moderation_metric_substantial(data_ref_mean, data_SAI_mean, data_noSAI_mean, alpha):
    '''
    Checks whether a substantial moderation takes place when SAI is used (compared to no-SAI).
    Substantial means: the SAI-value is lower than the no-SAI-value by more than a factor of (1+alpha),
    where alpha is 0 <= alpha <= 1.
    In this case, a NEGATIVE value of the below expression is returned.
    '''
    return np.abs(data_SAI_mean - data_ref_mean) - ( 1 -alpha) * np.abs(data_noSAI_mean - data_ref_mean)



def exacerbation_metric_substantial(data_ref_mean, data_SAI_mean, data_noSAI_mean, alpha):
    '''
    Checks whether a substantial exacerbation takes place when SAI is used (compared to no-SAI).
    Substantial means: the SAI-value exceeds the no-SAI-value by more than a factor of (1+alpha),
    where alpha is 0 <= alpha <= 1.
    In this case, a POSITIVE value of the below expression is returned.
    '''
    return np.abs(data_SAI_mean - data_ref_mean) - ( 1 +alpha) * np.abs(data_noSAI_mean - data_ref_mean)



def significant_substantial_moderation(data_ref_mean, data_SAI_eoc, data_noSAI_eoc, alpha, n_boot=1000, seed=0):
    '''
    Bootstrap of moderation_metric_substantial to determine its uncertainties.
    '''
    D_mean = moderation_metric_substantial(data_ref_mean, data_SAI_eoc.mean(dim="year"), data_noSAI_eoc.mean(dim="year"), alpha)
    n = data_SAI_eoc.sizes["year"]

    rng = np.random.default_rng(seed)
    counts = rng.multinomial(n, np.full(n, 1 / n), size=n_boot)   # (n_boot, n): draws per year
    weights = xr.DataArray(counts / n, dims=("boot", "year"))

    D_boot = moderation_metric_substantial(
        data_ref_mean,
        xr.dot(weights, data_SAI_eoc, dim="year"),
        xr.dot(weights, data_noSAI_eoc, dim="year"),
        alpha
    )
    sigma = D_boot.std("boot")

    return D_mean, sigma



def significant_substantial_exacerbation(data_ref_mean, data_SAI_eoc, data_noSAI_eoc, alpha, n_boot=1000, seed=0):
    '''
    Bootstrap of either exacerbation_metric_substantial to determine its uncertainties.
    '''
    D_mean = exacerbation_metric_substantial(data_ref_mean, data_SAI_eoc.mean(dim="year"), data_noSAI_eoc.mean(dim="year"), alpha)
    n = data_SAI_eoc.sizes["year"]

    rng = np.random.default_rng(seed)
    counts = rng.multinomial(n, np.full(n, 1 / n), size=n_boot)   # (n_boot, n): draws per year
    weights = xr.DataArray(counts / n, dims=("boot", "year"))

    D_boot = exacerbation_metric_substantial(
        data_ref_mean,
        xr.dot(weights, data_SAI_eoc, dim="year"),
        xr.dot(weights, data_noSAI_eoc, dim="year"),
        alpha
    )
    sigma = D_boot.std("boot")

    return D_mean, sigma



def get_sig_sub_mod_ex_masks(D_mod, sigma_mod, D_ex, sigma_ex, k=2.0):
    # mask_significant_necessary_mod = k * sigma_mod < np.abs(D_mod)
    # mask_significant_necessary_ex  = k * sigma_ex < np.abs(D_ex)
    mask_mod = (D_mod + k * sigma_mod < 0).fillna(False)# .where(mask_significant_necessary_mod).fillna(False)
    mask_ex  = (D_ex  - k * sigma_ex  > 0).fillna(False)# .where(mask_significant_necessary_ex).fillna(False)
    mask_insignificant = ~(mask_mod | mask_ex)

    mask_mod = make_cyclic(mask_mod)
    mask_ex  = make_cyclic(mask_ex)
    mask_insignificant = make_cyclic(mask_insignificant)

    return mask_mod, mask_ex, mask_insignificant



def compute_substantial_masks(data_ref_mean, data_SAI_eoc_mean, data_noSAI_eoc_mean, k= 1 /3):
    D_SAI   = data_SAI_eoc_mean - data_ref_mean
    D_noSAI = data_noSAI_eoc_mean - data_ref_mean

    mask_subst_incr = (D_noSAI < 0) & (D_SAI > ( 1 -k) * D_noSAI)  |  (D_noSAI > 0) & (D_SAI > ( 1 +k) * D_noSAI)
    mask_subst_decr = (D_noSAI < 0) & (D_SAI < ( 1 +k) * D_noSAI)  |  (D_noSAI > 0) & (D_SAI < ( 1 -k) * D_noSAI)

    mask_no_subst_change = ~(mask_subst_incr | mask_subst_decr)

    mask_subst_decr = make_cyclic(mask_subst_decr)
    mask_subst_incr = make_cyclic(mask_subst_incr)
    mask_no_subst_change = make_cyclic(mask_no_subst_change)

    return mask_subst_decr, mask_subst_incr, mask_no_subst_change