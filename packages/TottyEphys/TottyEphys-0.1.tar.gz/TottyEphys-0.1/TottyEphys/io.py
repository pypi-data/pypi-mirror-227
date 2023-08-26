
# add dependencies
import numpy as np
import matplotlib.pyplot as plt
import pynapple as nap
import pandas as pd
import circstats

def load_nex(files, raw_data_path, subject_ids, groups):

    # initialize file lists
    SPK2load = []
    LFP2load = []
    
    # seperate .spk and .lfp files
    for file in files:
        if ".SPK.nex" in file:
            SPK2load.append(file.strip()) # strip /n from name
            
        if ".LFP.nex" in file:
            LFP2load.append(file.strip()) # strip /n from name
            
    
    # initialize lists
    total_units = []
    total_unit_names = []
    subject_list = []
    group_list = []
    
    # loop through SPK files
    for n, file in enumerate(SPK2load):
        
        #=========================
        # Read in data
        #=========================
        # path to file
        SPK2load_path = raw_data_path / str(file)
        
        # read data
        reader = neo.io.NeuroExplorerIO(str(SPK2load_path))
        seg = reader.read_segment()  
        
        # Get start time of medPC (first event - 30 seconds).
        #   This will normalize the times such that we can use the same
        #   event times for all recordings. 
        for i in range(len(seg.events)): # find EVT02 events for each files
            if seg.events[i].name == 'EVT02':
                
                # start time of medPC
                start_time = seg.events[i].times[0]-30*pq.s
                
                # events for export
                events = seg.events[i].times-start_time
        
        # get desired units (not waveforms)
        all_units = []
        all_unit_names = []
        n_units = int(len(seg.spiketrains))
        for unit in range(0,n_units-1):
            if '_wf' not in seg.spiketrains[unit].name:
                all_units.append(nap.Ts(seg.spiketrains[unit].times - start_time, time_units = 's'))
                all_unit_names.append(seg.spiketrains[unit].name)
                
        # format data for pynapple
        subject_list.extend(np.array([subject_ids[n]]*len(all_units)))
        group_list.extend(np.array([groups[n]]*len(all_units)))
        total_units.extend(all_units)
        total_unit_names.extend(all_unit_names)
    
    # Make pynapple TsGroups
    units = {i: total_units[i] for i in range(len(total_units))}

    tsg = nap.TsGroup(units)
    tsg.set_info(unit_id = np.array(total_unit_names)) # add Unit ID
    tsg.set_info(rat_id = np.array(subject_list)) # add Rat ID
    tsg.set_info(group = np.array(group_list)) 
 
    return tsg, events

#%%

def analyze_neurons(neurons, tsg, save, save_dir):
    
    unit_ids = tsg.get_info('unit_id').values
    rat_ids = tsg.get_info('rat_id').values
    
    # Calculate the layout of the subplots
    num_neurons = len(neurons)
    num_cols = min(4, num_neurons)  # at most 4 columns
    num_rows = num_neurons // num_cols + int(num_neurons % num_cols != 0)  # round up

    # Create figure and axes
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(6*num_cols, 6*num_rows), subplot_kw={'projection': 'polar'})
    axs = np.array(axs)  # ensure axs is always a numpy array

    # Iterate over each neuron
    p_values = []
    MRLs = []
    for i, neuron in enumerate(neurons):
        ax = axs.flat[i]  # current axis

        times = neuron.index.to_numpy()  # extract timepoints
        firing_rates = neuron.to_numpy()  # extract firing rates

        # Convert times to phases of the theta cycle in radians.
        theta_period = 0.125  # period of theta cycle in seconds
        phases = (times % theta_period) / theta_period * 2*np.pi

        # To take into account firing rates, we need to duplicate each phase proportional to its firing rate
        phases_weighted = np.repeat(phases, np.round(firing_rates).astype(int))

        # Perform Rayleigh test for non-uniformity and calculate MRL.
        p_value = circstats.rayleightest(phases_weighted)
        R = np.sum(np.cos(phases_weighted))
        I = np.sum(np.sin(phases_weighted))
        N = len(phases_weighted)
        mrl = np.sqrt(R**2 + I**2) / N
        
        p_values.append(p_value)
        MRLs.append(mrl)

        # Compute circular mean to plot the MRL
        circ_mean = circstats.circmean(phases_weighted)

        print(rat_ids[i]+ ' ' +unit_ids[i]+ ": P-value ", p_value)

        # Compute histogram of phases, weighted by firing rates
        hist, bin_edges = np.histogram(phases_weighted, bins=np.linspace(0, 2*np.pi, num=50), density=True)

        # Compute bin centers
        bin_centers = (bin_edges[1:] + bin_edges[:-1]) / 2

        # Plot histogram
        ax.bar(bin_centers, hist, width=bin_edges[1] - bin_edges[0], edgecolor='k', alpha=0.5, color='k')

        # Add MRL
        ax.arrow(circ_mean, 0, 0, mrl, alpha=0.5, width=0.05,
                 edgecolor='red', facecolor='red', lw=2, zorder=5)

        ax.set_yticklabels([])  # hide radial ticks
        ax.set_theta_zero_location("N")  # theta=0 at the top
        ax.set_theta_direction(-1)  # theta increasing clockwise
        ax.tick_params(labelsize=20)
        
        ax.set_title(rat_ids[i]+ ' ' +unit_ids[i]+ f"\n (P-value: {p_value:.3f}, MRL: {mrl:.2f})", va='bottom', fontsize=20)

    # Remove empty subplots
    for ax in axs.flat[num_neurons:]:
        fig.delaxes(ax)

    plt.tight_layout()
    plt.show()

    if save == True:
        save_group = tsg.get_info('group').values[i]
        
        fig.savefig(str(save_dir)+'/' +'RosePlots_MRL_'+save_group+'.pdf',dpi=300)
        
        
    stats_dict = {'p_values': p_values, 'mrl': MRLs}
    stats_df = pd.DataFrame(stats_dict)
        
    return stats_df
