import numpy as np

def compute_pressure(
    diameter_km            : float,
    x_vals_km              : float,
    y_vals_km              : float,
    v_proj_km_s            : float = 10,
    rho_proj_kg_m3         : float = 2900,
    rho_crust_kg_m3        : float = 2900,
    transition_diameter_km : float = 7,
    compressibility        : float = 1.5,
    bulk_sound_speed_km_s  : float = 3.5,
    pressure_decay_const   : float = 1.87,
    return_params          : bool  = False,
):
    """
    `transition_diameter_km` is transition diameter from simple to complex crater.
    """

    ## Convert inputs to SI and shorthands
    D_o       = diameter_km * 1e3
    x_1d      = x_vals_km * 1e3
    y_1d      = y_vals_km * 1e3
    v_proj    = v_proj_km_s * 1e3
    rho_proj  = rho_proj_kg_m3
    rho_crust = rho_crust_kg_m3
    D_star    = transition_diameter_km * 1e3
    C         = bulk_sound_speed_km_s * 1e3
    S         = compressibility
    n         = pressure_decay_const
    g         = 3.72076
    ## EVERYTHING FROM HERE FORWARD IS SI

    D_tr = 0.7576 * D_o**0.921 * D_star**0.079

    E_proj = ((1/0.2212) * D_tr * v_proj**0.09 * g**0.22)**(1/0.26)
    r_proj = ((3 * E_proj) / (2 * np.pi * rho_proj * v_proj**2))**(1/3)

    R_ic = r_proj * 0.7
    u_ic = 0.5 * v_proj
    tau_rise = r_proj / v_proj

    x_2d, y_2d = np.meshgrid(x_1d, y_1d)  ## X and Y are each 2D arrays, now calculations can be better broadcasted/vectorized

    R_dir = np.sqrt(x_2d**2 + (y_2d - R_ic)**2)
    R_ref = np.sqrt(x_2d**2 + (y_2d + R_ic)**2)
    delta_t = (R_ref - R_dir) / C

    def calc_u_p(r):
        return np.where(
            r <= R_ic,
            u_ic,
            u_ic*(r/R_ic)**(-n)
        )

    def calc_P_direct(r):
        u_p = calc_u_p(r)
        return rho_crust * u_p * (C + S*u_p)

    P_direct    = calc_P_direct(R_dir)
    P_reflected = calc_P_direct(R_ref)

    P_eff = np.where(
        delta_t >= tau_rise,
        P_direct,
        P_direct - P_reflected*(1 - delta_t/tau_rise)
    )

    P_eff = P_eff * 1e-9

    if return_params:
        return(
            P_eff,
            {
                'v_proj_km_s'            : v_proj_km_s,
                'rho_proj_kg_m3'         : rho_proj_kg_m3,
                'rho_crust_kg_m3'        : rho_crust_kg_m3,
                'transition_diameter_km' : transition_diameter_km,
                'compressibility'        : compressibility,
                'bulk_sound_speed_km_s'  : bulk_sound_speed_km_s,
                'pressure_decay_const'   : pressure_decay_const,
                'transient_diameter_km'  : D_tr * 1e-3,
                'E_proj_J'               : E_proj,
                'proj_radius_km'         : r_proj * 1e-3,
                'isobaric_radius_km'     : R_ic * 1e-3,
                'u_ic_km_s'              : u_ic * 1e-3,
                'rise_time'              : tau_rise,
            }
        )
    return P_eff
