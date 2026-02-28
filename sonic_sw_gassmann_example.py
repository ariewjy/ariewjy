"""Physics-based water saturation estimate from DTC/DTS using Gassmann + Wood mixing.

This script demonstrates a practical workflow:
1) Convert DTC/DTS to Vp/Vs and Ksat.
2) Calibrate dry-frame bulk modulus (Kdry) in a known water-bearing zone.
3) Invert fluid bulk modulus (Kf) in target zones.
4) Convert Kf to water saturation Sw with Wood/Reuss mixing.
"""

from __future__ import annotations

from dataclasses import dataclass

FT_TO_M = 0.3048


@dataclass
class ZoneInput:
    dtc_us_per_ft: float
    dts_us_per_ft: float
    rho_gcc: float
    phi: float


def velocities_from_sonic(dtc_us_per_ft: float, dts_us_per_ft: float) -> tuple[float, float]:
    """Return Vp, Vs in m/s from sonic slowness logs in us/ft."""
    vp = FT_TO_M * 1e6 / dtc_us_per_ft
    vs = FT_TO_M * 1e6 / dts_us_per_ft
    return vp, vs


def ksat_gpa(dtc_us_per_ft: float, dts_us_per_ft: float, rho_gcc: float) -> float:
    """Compute saturated bulk modulus Ksat in GPa."""
    vp, vs = velocities_from_sonic(dtc_us_per_ft, dts_us_per_ft)
    rho = rho_gcc * 1000.0
    ksat_pa = rho * (vp**2 - (4.0 / 3.0) * vs**2)
    return ksat_pa / 1e9


def gassmann_ksat(kdry: float, km: float, phi: float, kf: float) -> float:
    """Gassmann forward model, all moduli in GPa."""
    return kdry + ((1.0 - (kdry / km)) ** 2) / (
        (phi / kf) + ((1.0 - phi) / km) - (kdry / (km**2))
    )


def calibrate_kdry_from_water_zone(ksat_water: float, km: float, phi: float, kw: float) -> float:
    """Brute-force solve Kdry from known water-bearing zone (Sw~1)."""
    best_kdry, best_err = None, float("inf")
    for i in range(1, int(km * 1000)):
        kdry = i / 1000.0
        # stay below matrix modulus
        if kdry >= km:
            continue
        ksat_try = gassmann_ksat(kdry, km, phi, kw)
        err = abs(ksat_try - ksat_water)
        if err < best_err:
            best_kdry, best_err = kdry, err
    if best_kdry is None:
        raise ValueError("Unable to calibrate Kdry; check inputs.")
    return best_kdry


def invert_kf_from_ksat(ksat: float, kdry: float, km: float, phi: float) -> float:
    """Algebraic inversion of fluid bulk modulus Kf from Gassmann equation."""
    a = (1.0 - (kdry / km)) ** 2
    b = ksat - kdry
    if b == 0:
        raise ValueError("Ksat equals Kdry; inversion unstable.")
    den = a / b
    term = den - ((1.0 - phi) / km) + (kdry / (km**2))
    if term == 0:
        raise ValueError("Invalid inversion term; check rock/fluid assumptions.")
    return phi / term


def sw_from_wood(kf: float, kw: float, khc: float) -> float:
    """Water saturation from Wood/Reuss fluid mixing (2-phase brine-hydrocarbon)."""
    numerator = (1.0 / kf) - (1.0 / khc)
    denominator = (1.0 / kw) - (1.0 / khc)
    if denominator == 0:
        raise ValueError("Invalid fluid moduli for saturation calculation.")
    return numerator / denominator


def run_example() -> None:
    # Inputs (illustrative)
    km = 37.0  # matrix bulk modulus from mineral mix and Vsh, GPa
    kw = 2.6  # brine bulk modulus at reservoir P-T-salinity, GPa
    khc = 0.9  # oil bulk modulus, GPa

    water_zone = ZoneInput(dtc_us_per_ft=90.0, dts_us_per_ft=170.0, rho_gcc=2.32, phi=0.25)
    target_zone = ZoneInput(dtc_us_per_ft=92.0, dts_us_per_ft=170.0, rho_gcc=2.30, phi=0.25)

    ksat_water = ksat_gpa(water_zone.dtc_us_per_ft, water_zone.dts_us_per_ft, water_zone.rho_gcc)
    kdry = calibrate_kdry_from_water_zone(ksat_water, km=km, phi=water_zone.phi, kw=kw)

    ksat_target = ksat_gpa(target_zone.dtc_us_per_ft, target_zone.dts_us_per_ft, target_zone.rho_gcc)
    kf_target = invert_kf_from_ksat(ksat_target, kdry=kdry, km=km, phi=target_zone.phi)
    sw_target = sw_from_wood(kf_target, kw=kw, khc=khc)

    print("=== Sonic-based Sw estimation (Gassmann + Wood) ===")
    print(f"Ksat (water zone): {ksat_water:.3f} GPa")
    print(f"Calibrated Kdry:    {kdry:.3f} GPa")
    print(f"Ksat (target):      {ksat_target:.3f} GPa")
    print(f"Inverted Kf:        {kf_target:.3f} GPa")
    print(f"Estimated Sw:       {sw_target:.3f} (fraction)")


if __name__ == "__main__":
    run_example()
