import datetime
import matplotlib.pyplot as plt
import numpy as np
import pathlib

from geospacelab import preferences as pref
import geospacelab.visualization.mpl as mpl

# pref.user_config['visualization']['mpl']['style'] = 'dark'  # or 'light'

import geospacelab.visualization.mpl.dashboards as dashboards
from geospacelab.visualization.mpl.dashboards import TSDashboard
from geospacelab.visualization.mpl.geomap.geodashboards import GeoDashboard
import geospacelab.observatory.earth.geodesy as gd
from geospacelab.observatory.orbit.utilities import LEOToolbox

fd_root = pathlib.Path('/home/lei/01-Work/01-Project/OY20-ISSI_IT/Event_201603/')


def overview_AC_DNSPOD(dt_fr, dt_to):
    fig = mpl.create_figure(figsize=(16, 9))
    
    db_1 = fig.add_dashboard(dashboard_class=TSDashboard, dt_fr=dt_fr, dt_to=dt_to)
    
    ds_sc_dns = db_1.dock(datasource_contents=['tud', 'swarm', 'dns_pod'], sat_id='A', product_version='v01',
                                  add_APEX=False, add_AACGM=False)
    ds_C_dns = db_1.dock(datasource_contents=['tud', 'swarm', 'dns_pod'], sat_id='C', product_version='v01',
                                  add_APEX=False, add_AACGM=False)

    
    ds_sc = ds_sc_dns.interp_evenly()
    ds_C = ds_C_dns.interp_evenly()
    ds_sym = db_1.dock(datasource_contents=['wdc', 'asysym'])
    ds_ae = db_1.dock(datasource_contents=['wdc', 'ae'])
    ds_sm = db_1.dock(datasource_contents=['supermag', 'indices'])
    
    # calc_diff_scB_Cy_time(ds_sc, ds_C)
    D = calc_d_Cetween_sc_scnd_C(ds_sc, ds_C)
    
    rho_scale = 1e12
    rho_unit = r'$\times 10^{-12}$ kg$\cdot$m$^{-3}$'
    rho_sc = ds_sc['rho_n']
    rho_C = ds_C['rho_n']
    rho_sc.visual.axis[1].data_scale = rho_scale
    rho_sc.visual.axis[1].unit = rho_unit
    rho_sc.visual.axis[1].label = r'$\rho$'
    rho_sc.visual.axis[2].label = 'Swarm-A'
    rho_sc.visual.plot_config.line = {'linestyle': '-', 'marker': '', 'alpha': 0.8}
    rho_C.visual.axis[1].data_scale = rho_scale
    rho_C.visual.axis[1].unit = rho_unit
    rho_C.visual.axis[2].label = 'Swarm-C'
    rho_C.visual.plot_config.line = {'linestyle': '-', 'marker': '', 'alpha': 0.8}
    # diff_rho = ds_sc['DIFF_rho_n_scBS']
    # diff_rho.visual.plot_config.line = {'linestyle': '-', 'marker': '', 'alpha': 0.5, 'color': 'grey'}
    # diff_rho_perc = ds_sc['PERC_DIFF_rho_n']

    glat_sc = db_1.assign_variable('SC_GEO_LAT', dataset=ds_sc)
    glat_C = db_1.assign_variable('SC_GEO_LAT', dataset=ds_C)
    glat_sc.visual.axis[2].label = 'Swarm-A'
    glat_C.visual.axis[2].label = 'Swarm-C'

    glon_sc = db_1.assign_variable('SC_GEO_LON', dataset=ds_sc)
    glon_C = db_1.assign_variable('SC_GEO_LON', dataset=ds_C)
    alt_sc = db_1.assign_variable('SC_GEO_ALT', dataset=ds_sc)
    alt_sc.label = 'h'
    alt_sc.visual.axis[1].lim = [440, 480]
    alt_sc.visual.axis[1].unit = 'km'
    alt_sc.visual.plot_config.line = {'linestyle': '-', 'marker': ''} 
    lst_sc = db_1.assign_variable('SC_GEO_LST', dataset=ds_sc)
    lst_sc.visual.plot_config.line = {'linestyle': '', 'marker': '.'} 
    lst_sc.visual.axis[1].label = 'LST'
    lst_sc.visual.axis[1].unit = 'h'

    glon_sc.visual.axis[2].label = 'Swarm-A'
    glon_C.visual.axis[2].label = 'Swarm-C'

    # Dock the dataset for the geomagnetic activity indices.
    sym_h = db_1.assign_variable('SYM_H', dataset=ds_sym)
    sym_h.visual.axis[1].label = 'SYM-H' 
    sme = db_1.assign_variable('SME', dataset=ds_sm)
    sme.visual.axis[1].label = 'SME'

    panel_layouts = [[sym_h, [sme]], [rho_sc, rho_C,], [glat_sc], [alt_sc, [lst_sc]]]
    db_1.set_layout(panel_layouts=panel_layouts, left=0.08, right=0.92, top=0.92, bottom=0.08      )
    db_1.draw()
    
    fd_res = fd_root / "Swarm"
    fd_res.mkdir(parents=True, exist_ok=True)
    fn_res = 'Swarm_overview_AC_DNS_POD_' + dt_fr.strftime("%Y%m%d_%H%M") + '-' + dt_to.strftime("%Y%m%d_%H%M") + '.png'
    fig.savefig(fd_res / fn_res, dpi=300)
    db_1.show()
    

def overview_single_DNSPOD(dt_fr, dt_to, sat_id):
    fig = mpl.create_figure(figsize=(16, 9))
    
    db_1 = fig.add_dashboard(dashboard_class=TSDashboard, dt_fr=dt_fr, dt_to=dt_to)
    
    ds_sc = db_1.dock(datasource_contents=['tud', 'swarm', 'dns_pod'], sat_id=sat_id, product_version='v01',
                                  add_APEX=False, add_AACGM=False)

    # ds_sc = ds_sc_dns.interp_evenly()
    ds_sym = db_1.dock(datasource_contents=['wdc', 'asysym'])
    ds_ae = db_1.dock(datasource_contents=['wdc', 'ae'])
    ds_sm = db_1.dock(datasource_contents=['supermag', 'indices'])
    
    # calc_diff_scB_Cy_time(ds_sc, ds_C)
    # D = calc_d_Cetween_sc_scnd_C(ds_sc, ds_C)
    
    rho_scale = 1e12
    rho_unit = r'$\times 10^{-12}$ kg$\cdot$m$^{-3}$'
    rho_sc = ds_sc['rho_n']
    rho_sc.visual.axis[1].data_scale = rho_scale
    rho_sc.visual.axis[1].unit = rho_unit
    rho_sc.visual.axis[1].label = r'$\rho$'
    rho_sc.visual.axis[2].label = 'Swarm-' + sat_id
    rho_sc.visual.plot_config.line = {'linestyle': '-', 'marker': '', 'alpha': 0.8}

    # diff_rho = ds_sc['DIFF_rho_n_scBS']
    # diff_rho.visual.plot_config.line = {'linestyle': '-', 'marker': '', 'alpha': 0.5, 'color': 'grey'}
    # diff_rho_perc = ds_sc['PERC_DIFF_rho_n']

    glat_sc = db_1.assign_variable('SC_GEO_LAT', dataset=ds_sc)
    glat_sc.visual.axis[2].label = 'Swarm-' + sat_id

    glon_sc = db_1.assign_variable('SC_GEO_LON', dataset=ds_sc)
    alt_sc = db_1.assign_variable('SC_GEO_ALT', dataset=ds_sc)
    alt_sc.label = 'h'
    if sat_id in ['A', 'C']:
        alt_range = [440, 480]
    else:
        alt_range = [500, 540] 
    alt_sc.visual.axis[1].lim = alt_range
    alt_sc.visual.axis[1].unit = 'km'
    alt_sc.visual.plot_config.line = {'linestyle': '-', 'marker': ''} 
    lst_sc = db_1.assign_variable('SC_GEO_LST', dataset=ds_sc)
    lst_sc.visual.plot_config.line = {'linestyle': '', 'marker': '.'} 
    lst_sc.visual.axis[1].label = 'LST'
    lst_sc.visual.axis[1].unit = 'h'

    glon_sc.visual.axis[2].label = 'Swarm-' + sat_id

    # Dock the dataset for the geomagnetic activity indices.
    sym_h = db_1.assign_variable('SYM_H', dataset=ds_sym)
    sym_h.visual.axis[1].label = 'SYM-H' 
    sme = db_1.assign_variable('SME', dataset=ds_sm)
    sme.visual.axis[1].label = 'SME'

    panel_layouts = [[sym_h, [sme]], [rho_sc], [glat_sc], [alt_sc, [lst_sc]]]
    db_1.set_layout(panel_layouts=panel_layouts, left=0.08, right=0.92, top=0.92, bottom=0.08      )
    db_1.draw()
    
    fd_res = fd_root / "Swarm"
    fd_res.mkdir(parents=True, exist_ok=True)
    fn_res = 'Swarm_overview_' + sat_id + '_DNS_POD_' + dt_fr.strftime("%Y%m%d_%H%M") + '-' + dt_to.strftime("%Y%m%d_%H%M") + '.png'
    fig.savefig(fd_res / fn_res, dpi=300)
    db_1.show()


def overview_ACC_POD(dt_fr, dt_to):
    fig = mpl.create_figure(figsize=(16, 9))
    
    db_1 = fig.add_dashboard(dashboard_class=TSDashboard, dt_fr=dt_fr, dt_to=dt_to)
    
    ds_pod = db_1.dock(datasource_contents=['tud', 'swarm', 'dns_pod'], sat_id='C', product_version='v01',
                                  add_APEX=False, add_AACGM=False)
    ds_acc = db_1.dock(datasource_contents=['tud', 'swarm', 'dns_acc'], sat_id='C', product_version='v01',
                                  add_APEX=False, add_AACGM=False)

    
    # ds_acc = ds_acc.interp_evenly()
    # ds_pod = ds_pod_dns.interp_evenly()
    ds_sym = db_1.dock(datasource_contents=['wdc', 'asysym'])
    ds_ae = db_1.dock(datasource_contents=['wdc', 'ae'])
    ds_sm = db_1.dock(datasource_contents=['supermag', 'indices'])
    
    # calc_diff_scB_Cy_time(ds_sc, ds_C)
    
    rho_scale = 1e12
    rho_unit = r'$\times 10^{-12}$ kg$\cdot$m$^{-3}$'
    rho_acc = ds_acc['rho_n']
    rho_pod = ds_pod['rho_n']
    rho_pod.visual.axis[1].data_scale = rho_scale
    rho_pod.visual.axis[1].unit = rho_unit
    rho_pod.visual.axis[1].label = r'$\rho$'
    rho_pod.visual.axis[2].label = 'POD'
    rho_pod.visual.plot_config.line = {'linestyle': '-', 'marker': '', 'alpha': 0.8}
    rho_acc.visual.axis[1].data_scale = rho_scale
    rho_acc.visual.axis[1].unit = rho_unit
    rho_acc.visual.axis[2].label = 'ACC'
    rho_acc.visual.plot_config.line = {'linestyle': '-', 'marker': '', 'alpha': 0.8}
    # diff_rho = ds_sc['DIFF_rho_n_scBS']
    # diff_rho.visual.plot_config.line = {'linestyle': '-', 'marker': '', 'alpha': 0.5, 'color': 'grey'}
    # diff_rho_perc = ds_sc['PERC_DIFF_rho_n']

    glat_pod = db_1.assign_variable('SC_GEO_LAT', dataset=ds_pod)

    glon_pod = db_1.assign_variable('SC_GEO_LON', dataset=ds_pod)
    alt_pod = db_1.assign_variable('SC_GEO_ALT', dataset=ds_pod)
    alt_pod.label = 'h'
    alt_pod.visual.axis[1].lim = [440, 480]
    alt_pod.visual.axis[1].unit = 'km'
    alt_pod.visual.plot_config.line = {'linestyle': '-', 'marker': ''} 
    lst_pod = db_1.assign_variable('SC_GEO_LST', dataset=ds_pod)
    lst_pod.visual.plot_config.line = {'linestyle': '', 'marker': '.'} 
    lst_pod.visual.axis[1].label = 'LST'
    lst_pod.visual.axis[1].unit = 'h'


    # Dock the dataset for the geomagnetic activity indices.
    sym_h = db_1.assign_variable('SYM_H', dataset=ds_sym)
    sym_h.visual.axis[1].label = 'SYM-H' 
    sme = db_1.assign_variable('SME', dataset=ds_sm)
    sme.visual.axis[1].label = 'SME'

    panel_layouts = [[sym_h, [sme]], [rho_pod, rho_acc,], [glat_pod], [alt_pod, [lst_pod]]]
    db_1.set_layout(panel_layouts=panel_layouts, left=0.08, right=0.92, top=0.92, bottom=0.08      )
    db_1.draw()
    
    fd_res = fd_root / "Swarm"
    fd_res.mkdir(parents=True, exist_ok=True)
    fn_res = 'Swarm_overview_C_POD_ACC_' + dt_fr.strftime("%Y%m%d_%H%M") + '-' + dt_to.strftime("%Y%m%d_%H%M") + '.png'
    fig.savefig(fd_res / fn_res, dpi=300)
    db_1.show()
   
   
def calc_d_Cetween_sc_scnd_C(ds_sc, ds_C):
    ds_sc = ds_sc
    ds_C = ds_C

    glat_1 = ds_sc['SC_GEO_LAT'].value
    glon_1 = ds_sc['SC_GEO_LON'].value
    alt_1 = ds_sc['SC_GEO_ALT'].value

    glat_2 = ds_C['SC_GEO_LAT'].value
    glon_2 = ds_C['SC_GEO_LON'].value
    alt_2 = ds_C['SC_GEO_ALT'].value

    r = 6371 + np.nanmean(alt_1.flatten())

    d = gd.calc_great_circle_distance(glat_1, glon_1, glat_2, glon_2, r=r)

    D = ds_sc.add_variable(var_name='d_AC', value=d)
    D.label = 'D_AC'
    D.unit = 'km'
    D.visual.axis[1].unit = 'km'
    D.visual.axis[1].lim = [0,400]
    D.visual.plot_config.style = '1noE'
    return D   


if __name__ == "__main__":
    dt_fr_1 = datetime.datetime(2016, 3, 14, 0)
    dt_to_1 = datetime.datetime(2016, 3, 21, 0)
    dt_fr_2 = datetime.datetime(2016, 3, 14, 12)
    dt_to_2 = datetime.datetime(2016, 3, 15, 10)
    # overview_AC_DNSPOD(dt_fr_1, dt_to_1)
    overview_single_DNSPOD(dt_fr_2, dt_to_2, sat_id='B')
    # overview_ACC_POD(dt_fr_1, dt_to_1)
    # overview_ACC_POD(dt_fr_2, dt_to_2) 
    # overview_with_maps()

 
    