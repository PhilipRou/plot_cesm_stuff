import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import cmocean



def plot_2D_resolcomp(
    data_highres,
    data_lowres,
    data_difference,
    title,
    minval_forcolorbar,
    maxval_forcolorbar,
    absmaxval_forcolorbar,
    lon_west,
    lon_east,
    lat_south,
    lat_north,
):
    fig = plt.figure(figsize=(15, 5))

    proj = ccrs.Robinson(central_longitude=(lon_west + lon_east) / 2)
    tran = ccrs.PlateCarree()
    ax1 = fig.add_subplot(1, 3, 1, projection=proj)
    ax2 = fig.add_subplot(1, 3, 2, projection=proj)
    ax3 = fig.add_subplot(1, 3, 3, projection=proj)

    for ax in [ax1, ax2, ax3]:
        # ax.gridlines()
        ax.coastlines(resolution='110m', color='black')
        ax.set_extent((lon_west, lon_east, lat_south, lat_north))
        # if isinstance(proj, ccrs.Robinson):
        #     ax.set_facecolor("white")

    p1 = data_highres.plot(
        ax=ax1,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.deep,
        vmin=minval_forcolorbar,
        vmax=maxval_forcolorbar,
        add_colorbar=False
    )
    p2 = data_lowres.plot(
        ax=ax2,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.deep,
        vmin=minval_forcolorbar,
        vmax=maxval_forcolorbar,
        add_colorbar=False
    )
    p3 = data_difference.plot(
        ax=ax3,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.balance,
        vmin=-absmaxval_forcolorbar,
        vmax=absmaxval_forcolorbar,
        add_colorbar=False
    )

    ax1.set_title("high res")
    ax2.set_title(title + "\n\nlow res")
    ax3.set_title("difference")

    cbar1 = fig.colorbar(
        p1,
        ax=[ax1, ax2],
        location="left",
        orientation="vertical",
        fraction=0.05,
        pad=0.08,
        shrink=0.6
    )
    cbar2 = fig.colorbar(
        p3,
        ax=ax3,
        location="right",
        orientation="vertical",
        fraction=0.05,
        pad=0.08,
        shrink=0.6
    )

    return fig



def plot_2D_SAIcomp(
    data_SAI,
    data_noSAI,
    data_difference,
    title,
    minval_forcolorbar,
    maxval_forcolorbar,
    absmaxval_forcolorbar,
    lon_west,
    lon_east,
    lat_south,
    lat_north,
):
    fig = plt.figure(figsize=(5, 15))

    proj = ccrs.Robinson(central_longitude=(lon_west + lon_east)/2)
    tran = ccrs.PlateCarree()
    ax1 = fig.add_subplot(3, 1, 1, projection=proj)
    ax2 = fig.add_subplot(3, 1, 2, projection=proj)
    ax3 = fig.add_subplot(3, 1, 3, projection=proj)

    for ax in [ax1, ax2, ax3]:
        # ax.gridlines()
        ax.coastlines(resolution='110m', color='black')
        ax.set_extent((lon_west, lon_east, lat_south, lat_north))
        # if isinstance(proj, ccrs.Robinson):
            # ax.set_facecolor("white")

    p1 = data_SAI.plot(
        ax=ax1,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.deep,
        vmin=minval_forcolorbar,
        vmax=maxval_forcolorbar,
        add_colorbar=False
    )
    p2 = data_noSAI.plot(
        ax=ax2,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.deep,
        vmin=minval_forcolorbar,
        vmax=maxval_forcolorbar,
        add_colorbar=False
    )
    p3 = data_difference.plot(
        ax=ax3,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.balance,
        vmin=-absmaxval_forcolorbar,
        vmax=absmaxval_forcolorbar,
        add_colorbar=False
    )

    ax1.set_title(title, fontsize = 14)
    fig.text(0.04, 0.75, "SAI", rotation=90,
         va='center', ha='center', fontsize=16)
    fig.text(0.04, 0.50, "no SAI", rotation=90,
         va='center', ha='center', fontsize=16)
    fig.text(0.04, 0.2, "difference", rotation=90,
         va='center', ha='center', fontsize=16)

    cbar1 = fig.colorbar(
        p1,
        ax=[ax1, ax2],
        # location="left",
        orientation="horizontal",
        fraction=0.05,
        pad=0.08,
        # shrink=0.6
    )
    cbar2 = fig.colorbar(
        p3,
        ax=ax3,
        # location="right",
        orientation="horizontal",
        fraction=0.05,
        pad=0.08,
        # shrink=0.6
    )

    return fig



def plot_2D_anomaly(
        var,
        module,
        data_reference,
        data_SAI_endofcent,
        data_noSAI_endofcent,
        data_SAI,
        data_noSAI,
        title,
        minval_forcolorbar_ref,
        maxval_forcolorbar_ref,
        minval_forcolorbar_endofcent,
        maxval_forcolorbar_endofcent,
        absmaxval_forcolorbar_diff,
        lon_west,
        lon_east,
        lat_south,
        lat_north,
):
    if var == "HMXL":
        cmap_for_refs = cmocean.cm.deep
    elif var == "TREFHT":
        cmap_for_refs = cmocean.cm.balance
    elif var == "PRECIP":
        cmap_for_refs = cmocean.cm.rain

    cbar_pad = 0.02
    cbar_shrink = 1.00
    cbar_orientation = "horizontal"
    cbar_extend = "neither"

    data_difference_SAI_noSAI = data_SAI - data_noSAI
    data_difference_noSAI_ref = data_noSAI - data_reference
    data_difference_SAI_ref = data_SAI - data_reference

    if module == "ocn":
        data_difference_SAI_noSAI = data_difference_SAI_noSAI.assign_coords(TLONG=data_SAI.TLONG)
        data_difference_SAI_noSAI = data_difference_SAI_noSAI.assign_coords(TLAT=data_SAI.TLAT)
        data_difference_noSAI_ref = data_difference_noSAI_ref.assign_coords(TLONG=data_noSAI.TLONG)
        data_difference_noSAI_ref = data_difference_noSAI_ref.assign_coords(TLAT=data_noSAI.TLAT)
        data_difference_SAI_ref = data_difference_SAI_ref.assign_coords(TLONG=data_SAI.TLONG)
        data_difference_SAI_ref = data_difference_SAI_ref.assign_coords(TLAT=data_SAI.TLAT)
        x_forplots = "TLONG"
        y_forplots = "TLAT"
    else:
        data_difference_SAI_noSAI = data_difference_SAI_noSAI.assign_coords(lon=data_SAI.lon)
        data_difference_SAI_noSAI = data_difference_SAI_noSAI.assign_coords(lat=data_SAI.lat)
        data_difference_noSAI_ref = data_difference_noSAI_ref.assign_coords(lon=data_noSAI.lon)
        data_difference_noSAI_ref = data_difference_noSAI_ref.assign_coords(lat=data_noSAI.lat)
        data_difference_SAI_ref = data_difference_SAI_ref.assign_coords(lon=data_SAI.lon)
        data_difference_SAI_ref = data_difference_SAI_ref.assign_coords(lat=data_SAI.lat)
        x_forplots = "lon"
        y_forplots = "lat"

    fig = plt.figure(figsize=(10, 12), constrained_layout=True)

    proj = ccrs.Robinson(central_longitude=(lon_west + lon_east) / 2)
    tran = ccrs.PlateCarree()
    ax11 = fig.add_subplot(3, 2, 1, projection=proj)
    ax12 = fig.add_subplot(3, 2, 2, projection=proj)
    ax21 = fig.add_subplot(3, 2, 3, projection=proj)
    ax22 = fig.add_subplot(3, 2, 4, projection=proj)
    ax31 = fig.add_subplot(3, 2, 5, projection=proj)
    ax32 = fig.add_subplot(3, 2, 6, projection=proj)

    for ax in [ax11, ax12, ax21, ax22, ax31, ax32]:
        ax.coastlines(resolution='110m', color='black')
        ax.set_extent((lon_west, lon_east, lat_south, lat_north), crs=tran)
        ax.tick_params(axis='both', labelsize=16)

    p11 = data_reference.plot(
        ax=ax11,
        x=x_forplots,
        y=y_forplots,
        transform=tran,
        cmap=cmap_for_refs,
        vmin=minval_forcolorbar_ref,
        vmax=maxval_forcolorbar_ref,
        cbar_kwargs={
            "orientation": cbar_orientation,
            "pad": cbar_pad,  # space between plot and colorbar
            "shrink": cbar_shrink,  # fraction of axes width
            "label": "",
            "extend": cbar_extend,
        }
    )
    p21 = data_noSAI_endofcent.plot(
        ax=ax21,
        x=x_forplots,
        y=y_forplots,
        transform=tran,
        cmap=cmap_for_refs,
        vmin=minval_forcolorbar_endofcent,
        vmax=maxval_forcolorbar_endofcent,
        cbar_kwargs={
            "orientation": cbar_orientation,
            "pad": cbar_pad,
            "shrink": cbar_shrink,
            "label": "",
            "extend": cbar_extend,
        }
    )
    p31 = data_SAI_endofcent.plot(
        ax=ax31,
        x=x_forplots,
        y=y_forplots,
        transform=tran,
        cmap=cmap_for_refs,
        vmin=minval_forcolorbar_endofcent,
        vmax=maxval_forcolorbar_endofcent,
        cbar_kwargs={
            "orientation": cbar_orientation,
            "pad": cbar_pad,
            "shrink": cbar_shrink,
            "label": "",
            "extend": cbar_extend,
        }
    )
    p12 = data_difference_SAI_noSAI.plot(
        ax=ax12,
        x=x_forplots,
        y=y_forplots,
        transform=tran,
        cmap=cmocean.cm.balance,
        vmin=-absmaxval_forcolorbar_diff,
        vmax=absmaxval_forcolorbar_diff,
        cbar_kwargs={
            "orientation": cbar_orientation,
            "pad": cbar_pad,
            "shrink": cbar_shrink,
            "label": "",
            "extend": cbar_extend,
        }
    )
    p22 = data_difference_noSAI_ref.plot(
        ax=ax22,
        x=x_forplots,
        y=y_forplots,
        transform=tran,
        cmap=cmocean.cm.balance,
        vmin=-absmaxval_forcolorbar_diff,
        vmax=absmaxval_forcolorbar_diff,
        cbar_kwargs={
            "orientation": cbar_orientation,
            "pad": cbar_pad,
            "shrink": cbar_shrink,
            "label": "",
            "extend": cbar_extend,
        }
    )
    p32 = data_difference_SAI_ref.plot(
        ax=ax32,
        x=x_forplots,
        y=y_forplots,
        transform=tran,
        cmap=cmocean.cm.balance,
        vmin=-absmaxval_forcolorbar_diff,
        vmax=absmaxval_forcolorbar_diff,
        cbar_kwargs={
            "orientation": cbar_orientation,
            "pad": cbar_pad,
            "shrink": cbar_shrink,
            "label": "",
            "extend": cbar_extend,
        }
    )

    ax11.set_title("Ref (no SAI 2000-2009)", fontsize=16)
    ax21.set_title("no SAI 2090-2098", fontsize=16)
    ax31.set_title("SAI 2090-2098", fontsize=16)
    ax12.set_title("SAI - no SAI", fontsize=16)
    ax22.set_title("no SAI - Ref", fontsize=16)
    ax32.set_title("SAI - Ref", fontsize=16)
    fig.suptitle(title, fontsize=18)

    for p in [p11, p21, p31, p12, p22, p32]:
        p.colorbar.ax.tick_params(labelsize=16)

    # fig.subplots_adjust(
    #     wspace=0.05,    # space between columns
    #     hspace=0.05,    # space between rows
    #     top=0.92        # leaves room for suptitle; lower = title closer to plots
    # )

    return fig



def plot_2D_resolandSAIcomp_3x3(
    data_highres_SAI,
    data_lowres_SAI,
    data_highres_noSAI,
    data_lowres_noSAI,
    data_difference_SAI,
    data_difference_noSAI,
    data_difference_highres,
    data_difference_lowres,
    title,
    minval_forcolorbar,
    maxval_forcolorbar,
    absmaxval_forcolorbar,
    lon_west,
    lon_east,
    lat_south,
    lat_north,
):
    """
    The suffixes of data_difference_ indicate which was left constant when determining the difference,
    e.g. data_difference_SAI = data_highres_SAI - data_lowres_SAI.
    """

    fig = plt.figure(figsize=(15, 12))

    fig.subplots_adjust(
        hspace=-0.5,
        wspace=0.05,
        bottom=0.12,    # space at bottom for the colorbars
    )

    proj = ccrs.Robinson(central_longitude=(lon_west + lon_east)/2)
    tran = ccrs.PlateCarree()
    ax11 = fig.add_subplot(3, 3, 1, projection=proj)
    ax12 = fig.add_subplot(3, 3, 2, projection=proj)
    ax13 = fig.add_subplot(3, 3, 3, projection=proj)
    ax21 = fig.add_subplot(3, 3, 4, projection=proj)
    ax22 = fig.add_subplot(3, 3, 5, projection=proj)
    ax23 = fig.add_subplot(3, 3, 6, projection=proj)
    ax31 = fig.add_subplot(3, 3, 7, projection=proj)
    ax32 = fig.add_subplot(3, 3, 8, projection=proj)

    for ax in [ax11, ax12, ax13, ax21, ax22, ax23, ax31, ax32]:
        # ax.gridlines()
        ax.coastlines(resolution='110m', color='black')
        ax.set_extent((lon_west, lon_east, lat_south, lat_north))
        # if isinstance(proj, ccrs.Robinson):
        #     ax.set_facecolor("white")

    p11 = data_highres_SAI.plot(
        ax=ax11,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.deep,
        vmin=minval_forcolorbar,
        vmax=maxval_forcolorbar,
        add_colorbar=False
    )
    p12 = data_lowres_SAI.plot(
        ax=ax12,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.deep,
        vmin=minval_forcolorbar,
        vmax=maxval_forcolorbar,
        add_colorbar=False
    )
    p13 = data_difference_SAI.plot(
        ax=ax13,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.balance,
        vmin=-absmaxval_forcolorbar,
        vmax=absmaxval_forcolorbar,
        add_colorbar=False
    )
    p21 = data_highres_noSAI.plot(
        ax=ax21,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.deep,
        vmin=minval_forcolorbar,
        vmax=maxval_forcolorbar,
        add_colorbar=False,
    )
    p22 = data_lowres_noSAI.plot(
        ax=ax22,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.deep,
        vmin=minval_forcolorbar,
        vmax=maxval_forcolorbar,
        add_colorbar=False,
    )
    p23 = data_difference_noSAI.plot(
        ax=ax23,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.balance,
        vmin=-absmaxval_forcolorbar,
        vmax=absmaxval_forcolorbar,
        add_colorbar=False,
    )
    p31 = data_difference_highres.plot(
        ax=ax31,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.balance,
        vmin=-absmaxval_forcolorbar,
        vmax=absmaxval_forcolorbar,
        add_colorbar=False,
    )
    p32 = data_difference_lowres.plot(
        ax=ax32,
        x="TLONG",
        y="TLAT",
        transform=tran,
        cmap=cmocean.cm.balance,
        vmin=-absmaxval_forcolorbar,
        vmax=absmaxval_forcolorbar,
        add_colorbar=False,
    )

    fig.suptitle(title, fontsize=18)
    ax11.set_title("high res", fontsize=16)
    ax12.set_title("low res", fontsize=16)
    ax13.set_title("difference", fontsize=16)
    fig.text(0.04, 0.75, "SAI", rotation=90,
         va='center', ha='center', fontsize=16)
    fig.text(0.04, 0.50, "no SAI", rotation=90,
         va='center', ha='center', fontsize=16)
    fig.text(0.04, 0.25, "difference", rotation=90,
         va='center', ha='center', fontsize=16)
    for ax in [ax21, ax22, ax23, ax31, ax32]:
        ax.set_title("")

    # Upper colorbar for the data values
    cax1 = fig.add_axes([0.125, 0.1, 0.775, 0.02])
    cbar1 = fig.colorbar(p13, cax=cax1, orientation="horizontal")
    # cbar1.set_label("blabla", fontsize=12)
    cbar1.ax.tick_params(labelsize=10)

    # Lower cbar for the differences
    cax2 = fig.add_axes([0.125, 0.05, 0.775, 0.02])
    cbar2 = fig.colorbar(p11, cax=cax2, orientation="horizontal")
    cbar2.ax.tick_params(labelsize=10)

    return fig



def D_from_means(data_ref_mean, data_SAI_mean, data_noSAI_mean):
    return np.abs(data_SAI_mean - data_ref_mean) - np.abs(data_noSAI_mean - data_ref_mean)



def significance(data_ref_mean, data_SAI_eof, data_noSAI_eof, n_boot=1000, seed=0):
    D_mean = D_from_means(data_ref_mean, data_SAI_eof.mean(dim="year"), data_noSAI_eof.mean(dim="year"))
    n = data_SAI_eof.sizes["year"]
    # assert data_noSAI_eof.sizes["year"] == n

    rng = np.random.default_rng(seed)
    counts = rng.multinomial(n, np.full(n, 1 / n), size=n_boot)   # (n_boot, n): draws per year
    weights = xr.DataArray(counts / n, dims=("boot", "year"))

    D_boot = D_from_means(
        data_ref_mean,
        xr.dot(weights, data_SAI_eof, dim="year"),
        xr.dot(weights, data_noSAI_eof, dim="year")
    )
    sigma = D_boot.std("boot")

    return D_mean, sigma



def get_significance_masks(D_mean, sigma, k=1.0):
    mask_significant = (k * sigma < np.abs(D_mean))
    mask_moderate    = ((D_mean + k * sigma) < 0).where(mask_significant).fillna(False)
    mask_exacerbate  = ((D_mean - k * sigma) > 0).where(mask_significant).fillna(False)
    mask_insignificant = np.logical_not(mask_significant)

    return mask_moderate, mask_exacerbate, mask_insignificant



def plot_TREFHT_significance(
    data_reference,
    data_SAI,
    data_noSAI,
    mask_moderate,
    mask_exacerbate,
    mask_insignificant,
    title,
    rasterized,
    n_level_cmap_ref,
    n_level_cmap_diff,
    cbar_ticks_ref,
    cbar_ticks_diff,
    minval_forcolorbar_ref,#=data2D_min,
    maxval_forcolorbar_ref,#=data2D_max,
    absmaxval_forcolorbar_diff,#=diff_max,
    lon_west,#=TLONG_min,
    lon_east,#=TLONG_max,
    lat_south,#=TLAT_min,
    lat_north,#=TLAT_max,
):

    cbar_pad         = 0.05  # space between plot and colorbar, def: 0.15 horizontal, 0.05 vertical
    cbar_shrink_ref  = 1.00  # fraction of axes width, def: 1.0
    cbar_shrink_diff = 1.00  # fraction of axes width, def: 1.0
    cbar_frac        = 0.15  # fraction of original Axes to use for colorbar, def: 0.15
    cbar_extend_ref  = "neither"
    cbar_extend_diff = "neither"
    cbar_orientation = "horizontal"
    cbar_ticks_ref   = cbar_ticks_ref
    cbar_ticks_diff  = cbar_ticks_diff
    cmap_ref  = cmocean.cm.thermal
    cmap_diff = cmocean.cm.balance
    proj = ccrs.Robinson(central_longitude=(lon_west + lon_east)/2)
    tran = ccrs.PlateCarree()
    plt.rcParams["hatch.linewidth"] = 1.5
    plt.rcParams["hatch.color"] = "olivedrab"

    levels_ref  = np.linspace(minval_forcolorbar_ref, maxval_forcolorbar_ref, n_level_cmap_ref + 1)
    levels_diff = np.linspace(-absmaxval_forcolorbar_diff, absmaxval_forcolorbar_diff, n_level_cmap_diff + 1)

    data_difference_noSAI_ref = data_noSAI - data_reference
    data_difference_noSAI_ref = data_difference_noSAI_ref.assign_coords(lon=data_noSAI.lon)
    data_difference_noSAI_ref = data_difference_noSAI_ref.assign_coords(lat=data_noSAI.lat)

    data_difference_SAI_ref = data_SAI - data_reference
    data_difference_SAI_ref = data_difference_SAI_ref.assign_coords(lon=data_SAI.lon)
    data_difference_SAI_ref = data_difference_SAI_ref.assign_coords(lat=data_SAI.lat)

    fig = plt.figure(figsize=(12, 6.5)) #, constrained_layout=True)
    gs  = GridSpec(nrows=2, ncols=3, figure=fig)
    ax_ref            = fig.add_subplot(gs[0,0],  projection=proj)
    ax_diff_noSAI_ref = fig.add_subplot(gs[1,0],  projection=proj)
    ax_diff_SAI_ref   = fig.add_subplot(gs[:,1:], projection=proj)

    for ax in [ax_ref, ax_diff_noSAI_ref, ax_diff_SAI_ref]:
        ax.coastlines(resolution='110m', color='black')
        ax.set_extent((lon_west, lon_east, lat_south, lat_north), crs=tran)
        ax.tick_params(axis='both', labelsize=16)

    p_ref = data_reference.plot(
        ax=ax_ref,
        x="lon",
        y="lat",
        transform=tran,
        cmap=cmap_ref,
        levels=levels_ref,
        rasterized=rasterized,
        cbar_kwargs={
            "orientation": cbar_orientation,
            "pad": cbar_pad,
            "shrink": cbar_shrink_ref,
            "label": "",
            "extend": cbar_extend_ref,
            "fraction": cbar_frac,
            "ticks": cbar_ticks_ref,
        }
    )
    p_diff_noSAI_ref = data_difference_noSAI_ref.plot(
        ax=ax_diff_noSAI_ref,
        x="lon",
        y="lat",
        transform=tran,
        cmap=cmap_diff,
        levels=levels_diff,
        rasterized=rasterized,
        cbar_kwargs={
            "orientation": cbar_orientation,
            "pad": cbar_pad,
            "shrink": cbar_shrink_diff,
            "label": "",
            "extend": cbar_extend_diff,
            "fraction": cbar_frac,
            "ticks": cbar_ticks_diff,
        }
    )
    p_diff_SAI_ref = data_difference_SAI_ref.plot(
        ax=ax_diff_SAI_ref,
        x="lon",
        y="lat",
        transform=tran,
        cmap=cmap_diff,
        levels=levels_diff,
        rasterized=rasterized,
        cbar_kwargs={
            "orientation": cbar_orientation,
            "pad": cbar_pad,
            "shrink": cbar_shrink_diff,
            "label": "",
            "extend": cbar_extend_diff,
            "fraction": cbar_frac,
            "ticks": cbar_ticks_diff,
            "aspect": 40, # only for this plot because it's bigger
        }
    )
    for mask, ls in [(mask_moderate, "solid"), (mask_exacerbate, "dashed")]:
            ax_diff_SAI_ref.contour(
            data_SAI.lon,
            data_SAI.lat,
            mask.astype(float),
            levels=[0.5],
            colors="olivedrab",
            linestyles=ls,
            linewidths=1.5,
            transform=tran,
        )

    ax_diff_SAI_ref.contourf(
        data_SAI.lon,
        data_SAI.lat,
        mask_insignificant.astype(float),
        levels=[0.5, 1.5],
        hatches=["///"],
        colors="none",
        transform=tran,
    )

    ax_ref.text(-0.06, 0.5, "Reference", transform=ax_ref.transAxes,
                rotation=90, va="center", ha="center", fontsize=17)
    ax_diff_noSAI_ref.text(-0.06, 0.5, "no SAI - Ref", transform=ax_diff_noSAI_ref.transAxes,
                           rotation=90, va="center", ha="center", fontsize=17)
    ax_diff_SAI_ref.text(-0.025, 0.5, "SAI - Ref", transform=ax_diff_SAI_ref.transAxes,
                         rotation=90, va="center", ha="center", fontsize=17)
    # ax_diff_SAI_ref.set_title("Ref - SAI", fontsize=16)
    fig.suptitle(title, fontsize=18)

    for p in (p_ref, p_diff_noSAI_ref, p_diff_SAI_ref):
        p.colorbar.ax.tick_params(labelsize=14)
        # p.colorbar.set_label("TREFHT [°C]", fontsize=14)

    fig.subplots_adjust(
        wspace=0.15,    # space between columns
        hspace=0.01,    # space between rows
        top=0.97,       # leaves room for suptitle; higher -> plots closer to title
        left=0.05,      # space to the left
        right=0.98      # space to the right
    )

    ax_diff_SAI_ref.set_anchor('S')

    return fig



def plot_precip_significance(
    data_reference,
    data_SAI,
    data_noSAI,
    mask_moderate,
    mask_exacerbate,
    mask_insignificant,
    title,
    rasterized,
    n_level_cmap_ref,
    n_level_cmap_diff,
    cbar_ticks_ref,
    cbar_ticks_diff,
    minval_forcolorbar_ref,
    maxval_forcolorbar_ref,
    absmaxval_forcolorbar_diff,
    lon_west,
    lon_east,
    lat_south,
    lat_north,
):

    cbar_pad         = 0.05  # space between plot and colorbar, def: 0.15 horizontal, 0.05 vertical
    cbar_shrink_ref  = 1.00  # fraction of axes width, def: 1.0
    cbar_shrink_diff = 1.00  # fraction of axes width, def: 1.0
    cbar_frac        = 0.15  # fraction of original Axes to use for colorbar, def: 0.15
    cbar_extend_ref  = "neither"
    cbar_extend_diff = "neither"
    cbar_orientation = "horizontal"
    cbar_ticks_ref   = cbar_ticks_ref
    cbar_ticks_diff  = cbar_ticks_diff
    cmap_ref  = cmocean.cm.rain
    cmap_diff = cmocean.cm.balance
    proj = ccrs.Robinson(central_longitude=(lon_west + lon_east)/2)
    tran = ccrs.PlateCarree()
    plt.rcParams["hatch.linewidth"] = 0.5
    plt.rcParams["hatch.color"] = "dimgrey"
    mask_linewidth = 1.0

    levels_ref  = np.linspace(minval_forcolorbar_ref, maxval_forcolorbar_ref, n_level_cmap_ref + 1)
    levels_diff = np.linspace(-absmaxval_forcolorbar_diff, absmaxval_forcolorbar_diff, n_level_cmap_diff + 1)

    data_difference_noSAI_ref = data_noSAI - data_reference
    data_difference_noSAI_ref = data_difference_noSAI_ref.assign_coords(lon=data_noSAI.lon)
    data_difference_noSAI_ref = data_difference_noSAI_ref.assign_coords(lat=data_noSAI.lat)

    data_difference_SAI_ref = data_SAI - data_reference
    data_difference_SAI_ref = data_difference_SAI_ref.assign_coords(lon=data_SAI.lon)
    data_difference_SAI_ref = data_difference_SAI_ref.assign_coords(lat=data_SAI.lat)

    fig = plt.figure(figsize=(12, 6.5)) #, constrained_layout=True)
    gs  = GridSpec(nrows=2, ncols=3, figure=fig)
    ax_ref            = fig.add_subplot(gs[0,0],  projection=proj)
    ax_diff_noSAI_ref = fig.add_subplot(gs[1,0],  projection=proj)
    ax_diff_SAI_ref   = fig.add_subplot(gs[:,1:], projection=proj)

    for ax in [ax_ref, ax_diff_noSAI_ref, ax_diff_SAI_ref]:
        ax.coastlines(resolution='110m', color='black', lw=1.5)
        ax.set_extent((lon_west, lon_east, lat_south, lat_north), crs=tran)
        ax.tick_params(axis='both', labelsize=16)

    p_ref = data_reference.plot(
        ax=ax_ref,
        x="lon",
        y="lat",
        transform=tran,
        cmap=cmap_ref,
        levels=levels_ref,
        rasterized=rasterized,
        cbar_kwargs={
            "orientation": cbar_orientation,
            "pad": cbar_pad,
            "shrink": cbar_shrink_ref,
            "label": "",
            "extend": cbar_extend_ref,
            "fraction": cbar_frac,
            "ticks": cbar_ticks_ref,
        }
    )
    p_diff_noSAI_ref = data_difference_noSAI_ref.plot(
        ax=ax_diff_noSAI_ref,
        x="lon",
        y="lat",
        transform=tran,
        cmap=cmap_diff,
        levels=levels_diff,
        rasterized=rasterized,
        cbar_kwargs={
            "orientation": cbar_orientation,
            "pad": cbar_pad,
            "shrink": cbar_shrink_diff,
            "label": "",
            "extend": cbar_extend_diff,
            "fraction": cbar_frac,
            "ticks": cbar_ticks_diff,
        }
    )
    p_diff_SAI_ref = data_difference_SAI_ref.plot(
        ax=ax_diff_SAI_ref,
        x="lon",
        y="lat",
        transform=tran,
        cmap=cmap_diff,
        levels=levels_diff,
        rasterized=rasterized,
        cbar_kwargs={
            "orientation": cbar_orientation,
            "pad": cbar_pad,
            "shrink": cbar_shrink_diff,
            "label": "",
            "extend": cbar_extend_diff,
            "fraction": cbar_frac,
            "ticks": cbar_ticks_diff,
            "aspect": 40, # only for this plot because it's bigger
        }
    )
    for mask, ls in [(mask_moderate, "solid"), (mask_exacerbate, "dashed")]:
        ax_diff_SAI_ref.contour(
            data_SAI.lon,
            data_SAI.lat,
            mask.astype(float),
            levels=[0.5],
            colors="dimgrey",
            linestyles=ls,
            linewidths=mask_linewidth,
            transform=tran,
        )

    ax_diff_SAI_ref.contourf(
        data_SAI.lon,
        data_SAI.lat,
        mask_insignificant.astype(float),
        levels=[0.5, 1.5],
        hatches=["...."],
        colors="none",
        transform=tran,
    )

    ax_ref.text(-0.06, 0.5, "Reference", transform=ax_ref.transAxes,
                rotation=90, va="center", ha="center", fontsize=17)
    ax_diff_noSAI_ref.text(-0.06, 0.5, "no SAI - Ref", transform=ax_diff_noSAI_ref.transAxes,
                           rotation=90, va="center", ha="center", fontsize=17)
    ax_diff_SAI_ref.text(-0.025, 0.5, "SAI - Ref", transform=ax_diff_SAI_ref.transAxes,
                         rotation=90, va="center", ha="center", fontsize=17)
    # ax_diff_SAI_ref.set_title("Ref - SAI", fontsize=16)
    fig.suptitle(title, fontsize=18)

    for p in (p_ref, p_diff_noSAI_ref, p_diff_SAI_ref):
        p.colorbar.ax.tick_params(labelsize=14)
        # p.colorbar.set_label("TREFHT [°C]", fontsize=14)

    fig.subplots_adjust(
        wspace=0.15,    # space between columns
        hspace=0.01,    # space between rows
        top=0.97,       # leaves room for suptitle; higher -> plots closer to title
        left=0.05,      # space to the left
        right=0.98      # space to the right
    )

    ax_diff_SAI_ref.set_anchor('S')

    return fig