# add dependencies
import numpy as np
import matplotlib.pyplot as plt
import pynapple as nap



def plot_autocorrelations(tsg, binsize=.01, windowsize=0.5, time_units='s'):
    
    # computer autocorrelations
    autocorrs = nap.compute_autocorrelogram(tsg,
                                            binsize,
                                            windowsize,                                     
                                            time_units,
                                            )
    
    # prepare metadata
    rat_ids = tsg.get_info('rat_id').values
    unit_ids = tsg.get_info('unit_id').values
    n_units = len(rat_ids)
    
    # get number of rows and columns for plot
    n_rows = int(np.floor(np.sqrt(n_units)))
    n_cols =int(np.ceil(np.sqrt(n_units)))
    
    # define plot
    fig, axes = plt.subplots(n_rows, n_cols, sharex=True, figsize=(15, 10))
    fig.suptitle('Autocorrelations')
    
    # loop through subplots
    for ax, unit, rat_id, unit_id in zip(axes.flatten(), tsg.index, rat_ids, unit_ids):
        ax.bar(autocorrs.index.values, autocorrs[unit], .01, label=tsg.get_info('group')[unit])
        ax.set(title=rat_id + ': '+ unit_id)  
        ax.legend()
    plt.tight_layout()

#%% PTSH

def plot_peth(tsg, start_tsd, minmax, bin_size, save, save_dir, time_units='s'):

    peth = nap.compute_perievent(tsg, start_tsd, minmax = minmax, time_unit = 's')
    
    rat_ids = tsg.get_info('rat_id').values
    unit_ids = tsg.get_info('unit_id').values
    
    average_peths = []

    for unit, rat_id, unit_id in zip(tsg.index, rat_ids, unit_ids):
        
        plt.figure(figsize=[12,12])
        
        # raster plot
        plt.subplot(211)
        for stim_index in peth[unit].keys():
            plt.plot(peth[unit][stim_index].as_units('s').fillna(stim_index), '|', markersize=5, color='k')
           
        plt.xlim(-2.5, 7.5)
        plt.xticks(np.arange(0, 6, 5.0), fontsize = 50)
        plt.yticks(fontsize = 50)
        #plt.axvline(0, color='k', linestyle="--")
        #plt.axvline(5, color='k', linestyle="--")
        plt.ylabel("Trials", fontsize = 50)
        plt.title(rat_id + ': '+ unit_id, fontsize=50)
        

        # PSTH
        peth_average = peth[unit].count(bin_size, time_units = 's').mean(1)/bin_size
        average_peths.append(peth_average)
        
        plt.subplot(212)
        plt.plot(peth_average, label=tsg.get_info('group')[unit], color='k')
        
        
        plt.xlim(-2.5, 7.5)
        plt.xticks(np.arange(0, 6, 5.0), fontsize = 50)
        plt.yticks(fontsize = 50)
        #plt.axvline(0, color='k', linestyle="--")
        #plt.axvline(5, color='k', linestyle="--")
        plt.xlabel("Time (s)", fontsize = 50)
        plt.ylabel('Firing Rate (Hz)', fontsize = 50)
        #plt.legend()
        plt.tight_layout()
        
        if save == True:
            save_group = tsg.get_info('group')[unit]
            save_rat = tsg.get_info('rat_id')[unit]
            save_unit = tsg.get_info('unit_id')[unit]
            
            plt.savefig(str(save_dir)+'/' +'PETHs_'+save_group+'_'+save_rat+'_'+save_unit+'.svg',dpi=300)
        
    return peth, average_peths