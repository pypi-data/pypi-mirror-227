#%% Load imports
import numpy as np
import fnmatch
import os
import matplotlib.pyplot as plt
from typing import Dict, List
import plotly.graph_objects as go
import plotly.express as px

import salsa.plots.new_plots as new_plt
from salsa.helper_functions import log
from salsa.data import TemplateData

#%% Helper fns
def normalize_to_mean_preamble_template (myset,tk,norm_len=4) :
    one_mer_inds = np.where(tk==1)[0][:norm_len] 
    mean_one_mer = np.mean(myset[:,one_mer_inds])
    return myset/mean_one_mer

def normalize_to_mean_signal (myset) :
    mean_signal = np.mean(myset,axis=0)
    s_new = []    
    for i in range(np.shape(myset)[0]) :
        s = myset[i,:]
        fit = np.polyfit(s,mean_signal,deg=1)
        s_fit = s*fit[0]+fit[1]
        s_new.append(s_fit)        
    return np.squeeze(s_new)

def filter_by_RMS (sigmat, XYT, params) :
    mean_signal = np.median(sigmat,axis=0)
    residual = sigmat - mean_signal
    sum_square_res = np.sqrt(np.mean(residual*residual,axis=1))
    sort_indxs = np.argsort(sum_square_res)   
    sort_indxs_fraction = sort_indxs[:np.int(len(sum_square_res)*params['tool_noise_RMS_fraction'])]    
    return sigmat[sort_indxs_fraction][:], XYT[sort_indxs_fraction][:]

def tile_uniformity(signal, XYT,params) :  
    tiles = XYT[:,2].astype(int)
    # find uniformity coefficient file in rundmc_path
    ua_coeff_file = ''
    EC_coeff_file = ''
    coeff_file = None
    for root, dirs, files in os.walk(params['rundmc_path']):
        for name in files:
            if fnmatch.fnmatch(name, '*ua*uniformity*npy'):
                ua_coeff_file = os.path.join(root, name) 
            if fnmatch.fnmatch(name, '*EC*uniformity*npy'):
                EC_coeff_file = os.path.join(root, name) 
    if (ua_coeff_file) :
        coeff_file = ua_coeff_file
    elif (EC_coeff_file) :
        coeff_file = EC_coeff_file
    if (not coeff_file) :
        return signal
        
    coeff_data = np.load(coeff_file) # mean of signal per flow 
    tile_mean = coeff_data[:,:np.shape(signal)[1]]        
    new_signal = np.copy(signal)    
    unique_tiles = np.unique(tiles)
    mean_all_tiles = np.mean(coeff_data)
    # for each tile, find the relevant beads and scale to the mean per flow
    for j,tile in enumerate(unique_tiles) :        
        new_signal[tiles==tile] *= mean_all_tiles/tile_mean[tile-1,:]
    return new_signal

def set_mean (s,tk) :        
    no_fluct_s = np.copy(np.squeeze(s))    
    unique_tk = np.unique(tk)
    mean_s_nmer = np.zeros(len(unique_tk))
    # mean of n'mer
    for j,tkval in enumerate(unique_tk) :        
        ind = np.where(tk==tkval)[0]
        s_nmer = np.squeeze(s)[:,ind]
        mean_s_nmer[j] = np.mean(s_nmer)    
    
    for flow in range(np.shape(s)[1]) : #RS TODO: vectorize
        m_nmer = mean_s_nmer[np.where(unique_tk==tk[flow])[0]]
        m_flow = np.mean(no_fluct_s[:,flow])
        no_fluct_s[:,flow] *= m_nmer/m_flow
    
    return no_fluct_s

def append_template_signal(s,s_list,flows_list,name_list,base_string,tk,tkval,tname,params) :
    # add flows from s with low std to s_list
    agctind = np.arange(0,np.shape(s)[1]-3,4)
    for bid,btype in enumerate(base_string) :     
        agct_indices = agctind+bid
        tkval_flows = agct_indices[np.where(tk[agct_indices]==tkval)[0]]        
        std_s = np.std(s[:,tkval_flows],axis=0)
        flows = tkval_flows[np.where(std_s<np.percentile(std_s,params['tool_noise_low_std_percentile']))[0]]
        if (np.shape(flows)[0]==0) :
            continue
        #template_signal = s[:,flows] 
        for _,f in enumerate(flows) :
            s_list[bid].append(s[:,f])
            flows_list[bid].append(f)
            name_list[bid].append(tname)
            
    return s_list, name_list, flows_list

def unite_templates (s_list,base_string):    
    for bid,btype in enumerate(base_string) :    
        all_hists_mean = np.mean(np.concatenate(s_list[bid][:]))
        for flow_index in range(np.shape(s_list[bid])[0]) :
            signal = s_list[bid][flow_index]        
            signal *= all_hists_mean/np.mean(signal)  
            
def choose_flows (s_list,flows_list,base_string,params) :
    low_std_flows = [[],[],[],[]]
    #signals_in_flow = np.tile(np.array([]),(len(base_string),params['tool_noise_length'],1))
    signals_in_flow = []
    for i in range(params['tool_noise_length']):
        signals_in_flow.append([])
    for bid,btype in enumerate(base_string) :
        s_array = s_list[bid]
        std_flow = np.zeros(np.shape(s_array)[0])
        for signal_index in range(np.shape(s_array)[0]) :            
            std_flow[signal_index] = np.std(s_array[signal_index])
        # find template_index with low std
        percentil = params['tool_noise_low_std_percentile']
        flows_with_low_std = np.where(std_flow<np.percentile(std_flow,percentil))[0]
                               
        for j,f in enumerate(flows_with_low_std) :                    
            s_template_flow = s_array[f]
            low_std_flows[bid].append(s_template_flow)
            signals_in_flow[flows_list[bid][f]].append(s_template_flow)
            
    for j in range(np.shape(low_std_flows)[0]) :
        low_std_flows[j] = np.concatenate(low_std_flows[j])
                
    return low_std_flows, signals_in_flow  

def tool_noise_score(s0,s1) :
    mean_0 = np.mean(s0)
    mean_1 = np.mean(s1)
    std_0 = np.std(s0)
    std_1 = np.std(s1)        
    median_0 = np.median(s0)
    median_1 = np.median(s1)      
    # calculate scores: percentile, skewness
    separation = (median_1-median_0)/(np.percentile(s0,99.5)-median_0 + median_1 - np.percentile(s1,0.5))
    skewness_0 = (mean_0-median_0)/std_0
    skewness_1 = (mean_1-median_1)/std_1          
    return separation, skewness_0, skewness_1

def calculate_scores_per_flow(signals_in_flow_0mer,signals_in_flow_1mer,params):
    threshold = 1000
    scores = np.zeros(params['tool_noise_length'])
    for f in range(params['tool_noise_length']) :
        if (np.shape(signals_in_flow_0mer[f])[0] > 0 and np.shape(signals_in_flow_1mer[f])[0] > 0) :
            s_0mer = np.concatenate(signals_in_flow_0mer[f])
            s_1mer = np.concatenate(signals_in_flow_1mer[f])
            if (len(s_0mer) > threshold and len(s_1mer) > threshold) :                        
                separation,_,_ = tool_noise_score(s_0mer, s_1mer)
                scores[f] = separation
    
    return scores

#%% Plotting fns
#def save_plot(fig, fbase, params=None, plot_dir=None, dark_png=False):
    #if dark_png is True:
        #png_fn = f"{params['save_loc']}plots/{fbase}_dark.png"
        #fig.set_size_inches(6, 6)
        #plt.savefig(png_fn)
        #plt.close()
        #return 0
    #else:
        #png_fn = f"{params['save_loc']}plots/{fbase}.png"

    
    ##if MPLD3:
        
        ##json_fn = plot_fname(fbase+'.json', params, plot_dir=plot_dir)
        ##html_fn = plot_fname(fbase+'.html', params, plot_dir=plot_dir)
        ### mpld3_default = os.path.join(mpld3.__path__[0], '_default.py')
        ##try:
            ##mpld3.save_json(fig, json_fn)
        ##except Exception as ex:
            ##_ = ef.write_log(f"Cannot save {json_fn}.", np.zeros([1,1]), params)
            ##_ = ef.write_log(repr(ex), np.zeros([1,1]), params)
            ##pass

        ##try:
            ##mpld3.save_html(fig, html_fn)
        ##except Exception as ex:
            ##_ = ef.write_log(f"Cannot save {html_fn}.", np.zeros([1,1]), params)
            ##_ = ef.write_log(repr(ex), np.zeros([1,1]), params)
            ##pass
        
        ##plt.savefig(png_fn)

    ##else:
        ##_ = ef.write_log("WARNING: mpld3 not available. Saving as .png", np.zeros([1,1]), params)
        ##plt.savefig(png_fn)
        
    #plt.savefig(png_fn)  # take from else loop
    #plt.close()
    #return 0

def base_colors(params=None, flow_base=None):
    if params:
        flow_base = params['flow_base']
    elif not flow_base:
        flow_base = 'TACG'

    colors = []
    for bs in flow_base:
        if bs=='A': # green
            colors.append('g')
        elif bs=='C': # blue
            colors.append('b')
        elif bs=='G': # black
            colors.append('k')
        elif bs=='T': # red
            colors.append('r')
        else:
            #_ = ef.write_log('Base not recognized')
            log('warning', 'Base not recognized')

    if len(colors)==len(flow_base):
        return colors
    else:
        #_ = ef.write_log('Not all bases identified')
        log('warning', 'Not all bases identified')

    return []

def plot_tool_noise(base_string,signals_0mer,signals_1mer,separation,params,dark_png=False):
    data_dict = {}
    
    fig = new_plt.SubPlot(rows = 2, cols = 2,
                          subplot_titles=("T", "G", "C", "A"),
                          horizontal_spacing=0.15)
    
    position = {'T': {'row': 1, 'col': 1},
                'G': {'row': 1, 'col': 2},
                'C': {'row': 2, 'col': 1},
                'A': {'row': 2, 'col': 2}}
    
    for bid,btype in enumerate(base_string):
        all_templates_0mer = signals_0mer[bid]
        all_templates_1mer = signals_1mer[bid]
        # calculate scores: percentile, skewness
        sep_all_flows, skewness_0, skewness_1 = tool_noise_score(all_templates_0mer, all_templates_1mer)
        data_dict[f'TNS_{btype}'] = sep_all_flows
        data_dict[f'TNS_0mer_samples_{btype}'] = len(all_templates_0mer)
        data_dict[f'TNS_1mer_samples_{btype}'] = len(all_templates_1mer)
        data_dict[f'TNS_0mer_CV_{btype}'] = np.std(all_templates_0mer)/np.mean(all_templates_0mer)
        data_dict[f'TNS_1mer_CV_{btype}'] = np.std(all_templates_1mer)/np.mean(all_templates_1mer)
        data_dict[f'TNS_0mer_skewness_{btype}'] = skewness_0
        data_dict[f'TNS_1mer_skewness_{btype}'] = skewness_1
        
        counts0, bins0 = np.histogram(all_templates_0mer, bins=150)
        fig.add_trace(go.Scatter(
            x = bins0[:-1],
            y = counts0,
            line=dict(color=px.colors.qualitative.Plotly[0]),
            showlegend = (btype == 'T'),
            name = '0mer',
        ), **(position[btype]))
                                                                        
        counts1, bins1 = np.histogram(all_templates_1mer, bins=150)
        fig.add_trace(go.Scatter(
            x = bins1[:-1],
            y = counts1,
            line=dict(color=px.colors.qualitative.Plotly[1]),
            showlegend = (btype == 'T'),
            name = '1mer',
        ), **(position[btype]))

        fig.update_xaxes(title_text = 'Normalized Signal', **(position[btype]))
        fig.update_yaxes(title_text = 'Count', type = 'log', **(position[btype]))
    fig.set_name(f"TNS separation - {params['runid']}")
    fig.update_layout(title_text = fig.name, hovermode = 'x')
    fig.append_to_html(interactive = False)
    
    #%% SEPARATION PLOT
    #figsize=(8,6)
                   
    #cycle_len = len(params['flow_order'])
    #if 'npreamble' in params:
        #start_flow = params['npreamble']
    #else:
        #start_flow = 32
    #base_shift = start_flow % cycle_len
   
    #flow_base = '{}{}'.format(params['flow_order'][base_shift:], params['flow_order'][:base_shift])
    #colors = base_colors(flow_base=flow_base)
    #max_flows = params['tool_noise_length']
   
    #fig, ax = plt.subplots(figsize=figsize)    
    #lns = []
    #ptlabels = []
    
    #for i, [bs, c] in enumerate(zip(flow_base, colors)):
        #flows = np.arange(start_flow+i, start_flow+max_flows, cycle_len)
        #y = separation[i::cycle_len]
        #locsy = np.where( y!=0 )[0]
        #ln = plt.plot(flows[locsy]+1, y[locsy], 'o-', color=c, markersize=4, linewidth=3, label=bs+' separation')
        #lns.append(ln) 
        
    #plt.xlabel('Flows', size='x-large')
    #plt.grid()
    #plt.title(f"Tool Noise: Separation - {params['runid']}")
    #plt.ylabel('Separation', size='x-large')
    #plt.legend(loc=4, fontsize='large')
    ## save plot
    #fbase = f"{params['runid']}_tool_noise_separation"
    #save_plot(fig, fbase, params, dark_png=dark_png)         
    return data_dict

#%% Function def
def tool_noise(templates: List[TemplateData], params):
    

    signal_0mer = [[],[],[],[]]
    signal_1mer = [[],[],[],[]]
    flows_0mer = [[],[],[],[]]
    flows_1mer = [[],[],[],[]]
    names_0mer = [[],[],[],[]] 
    names_1mer = [[],[],[],[]]    
    global_base_string = params['flow_order']
    for template_data in templates:        
        # load data
        signal = template_data.sigmat[:,:params['tool_noise_length']]
        #tid = np.int(np.unique(template['temp_ind']))
        template_name = template_data.name
        tk = template_data.template_tk[:params['tool_noise_length']]
        XYT = template_data.XYT
            
        # normalize by preamble
        signal = normalize_to_mean_preamble_template(signal, tk)    
        
        # normalize to mean signal
        signal = normalize_to_mean_signal(signal)        
        
        # filter by RMS
        signal, XYT = filter_by_RMS (signal, XYT, params)
        
        # tile uniformity correction
        signal = tile_uniformity (signal, XYT, params)
                    
        # remove context, phasing            
        signal = set_mean(signal, tk)
                            
        # get signal from low std flows, append signal from this template to list
        signal_0mer, names_0mer, flows_0mer = append_template_signal(signal,signal_0mer,flows_0mer,names_0mer,global_base_string,tk,0,template_name,params)
        signal_1mer, names_1mer, flows_1mer = append_template_signal(signal,signal_1mer,flows_1mer,names_1mer,global_base_string,tk,1,template_name,params)
    
    unite_templates(signal_0mer,global_base_string)
    unite_templates(signal_1mer,global_base_string)
    
    low_std_flows_0, signals_in_flow_0mer = choose_flows(signal_0mer,flows_0mer,global_base_string,params)
    low_std_flows_1, signals_in_flow_1mer = choose_flows(signal_1mer,flows_1mer,global_base_string,params)      
    
    separation = calculate_scores_per_flow(signals_in_flow_0mer,signals_in_flow_1mer,params)    
    
    data_dict ={}
    data_dict['base_string'] = global_base_string
    data_dict['signals_0mer'] = low_std_flows_0
    data_dict['signals_1mer'] = low_std_flows_1
    data_dict['separation'] = separation
    
    # for l in data_dict:
    #     s = data_dict[l]
    #     for j in range(0,len(s)):   
    #         counts, bins, _ = plt.hist(s[j],bins='auto',histtype='step',log=True,density=True)            
    #         histdata = np.stack((bins[:-1],counts),axis=1)
    #         ef.save_final_table(histdata, params, f'template_summary_tool_noise_{l}_{global_base_string[j]}.csv')   
    # for l in list(data_dict)[3:]:
    #     ef.save_final_table(data_dict[l], params, f'template_summary_tool_noise_per_flow_{l}.csv')    
    
    TNS_data = plot_tool_noise(global_base_string, low_std_flows_0, low_std_flows_1, separation, params)

    return TNS_data