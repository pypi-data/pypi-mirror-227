import numpy as np
from scipy.constants import c as clight

from .general import _print

import xtrack as xt
import xobjects as xo

def compensate_radiation_energy_loss(line, delta0=0, rtol_eneloss=1e-10, max_iter=100, **kwargs):

    assert isinstance(line._context, xo.ContextCpu), "Only CPU context is supported"
    assert line.particle_ref is not None, "Particle reference is not set"
    assert np.abs(line.particle_ref.q0) == 1, "Only |q0| = 1 is supported (for now)"

    if 'record_iterations' in kwargs:
        record_iterations = kwargs['record_iterations']
        kwargs.pop('record_iterations')
        line._tapering_iterations = []
    else:
        record_iterations = False

    _print("Compensating energy loss:")

    _print("  - Twiss with no radiation")
    line.configure_radiation(model=None)
    tw_no_rad = line.twiss(method='4d', freeze_longitudinal=True, **kwargs)

    _print("  - Identify multipoles and cavities")
    line_df = line.to_pandas()
    multipoles = line_df[line_df['element_type'] == 'Multipole']
    dipole_edges = line_df[line_df['element_type'] == 'DipoleEdge']
    cavities = line_df[line_df['element_type'] == 'Cavity'].copy()

    # save voltages
    cavities['voltage'] = [cc.voltage for cc in cavities.element.values]
    cavities['frequency'] = [cc.frequency for cc in cavities.element.values]
    cavities['eneloss_partitioning'] = cavities['voltage'] / cavities['voltage'].sum()

    # Put all cavities on crest and at zero frequency
    _print("  - Put all cavities on crest and set zero voltage and frequency")
    for cc in cavities.element.values:
        cc.lag = 90.
        cc.voltage = 0.
        cc.frequency = 0.

    line.configure_radiation(model='mean')

    _print("Share energy loss among cavities (repeat until energy loss is zero)")
    with xt.line._preserve_config(line):
        line.config.XTRACK_MULTIPOLE_TAPER = True
        line.config.XTRACK_DIPOLEEDGE_TAPER = True

        i_iter = 0
        while True:
            p_test = tw_no_rad.particle_on_co.copy()
            p_test.delta = delta0
            line.configure_radiation(model='mean')
            line.track(p_test, turn_by_turn_monitor='ONE_TURN_EBE')
            mon = line.record_last_track

            if record_iterations:
                line._tapering_iterations.append(mon)

            eloss = -(mon.ptau[0, -1] - mon.ptau[0, 0]) * p_test.p0c[0]
            _print(f"Energy loss: {eloss:.3f} eV             ", end='\r', flush=True)

            if eloss < p_test.energy0[0]*rtol_eneloss:
                break

            for ii in cavities.index:
                cc = cavities.loc[ii, 'element']
                eneloss_partitioning = cavities.loc[ii, 'eneloss_partitioning']
                cc.voltage += eloss * eneloss_partitioning

            i_iter += 1
            if i_iter > max_iter:
                raise RuntimeError("Maximum number of iterations reached")
    _print()
    delta_taper = mon.delta[0,:]

    _print("  - Adjust multipole strengths")
    i_multipoles = multipoles.index.values
    delta_taper_multipoles = ((mon.delta[0,:][i_multipoles+1] + mon.delta[0,:][i_multipoles]) / 2)
    for nn, dd in zip(multipoles['name'].values, delta_taper_multipoles):
        line.element_dict[nn].knl *= (1 + dd)
        line.element_dict[nn].ksl *= (1 + dd)

    _print("  - Adjust dipole edge strengths")
    i_dipole_edges = dipole_edges.index.values
    delta_taper_dipole_edges = ((mon.delta[0,:][i_dipole_edges+1] + mon.delta[0,:][i_dipole_edges]) / 2)
    for nn, dd in zip(dipole_edges['name'].values, delta_taper_dipole_edges):
        line.element_dict[nn].k *= (1 + dd)
        if hasattr(line.element_dict[nn], 'h'):
            line.element_dict[nn].h *= (1 + dd)


    _print("  - Restore cavity voltage and frequency. Set cavity lag")
    beta0 = p_test.beta0[0]
    for icav in cavities.index:
        if cavities.loc[icav, 'voltage'] == 0:
            vvrr = 0
        else:
            vvrr = (cavities.loc[icav, 'element'].voltage
                    / cavities.loc[icav, 'voltage'])
        assert np.abs(vvrr) < 1.
        inst_phase = np.arcsin(vvrr)
        freq = cavities.loc[icav, 'frequency']

        zeta = mon.zeta[0, icav]
        lag = 360.*(inst_phase / (2*np.pi) - freq*zeta/beta0/clight)
        lag = 180. - lag # we are above transition

        cavities.loc[icav, 'element'].lag = lag
        cavities.loc[icav, 'element'].frequency = freq
        cavities.loc[icav, 'element'].voltage = cavities.loc[icav, 'voltage']

    line.delta_taper = delta_taper
