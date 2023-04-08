# INF6805E_Project

## Stats

### File nomenclature

Generated datasets are postfixed by the metaparameters values used in the following order : 
-`<n_clusters>` : the number of clusters
-`<speed>` : the speed of the robots
-`<move_type>` : the movement type (`0` means random, `1` means clusterized)
-`<p_i_infected>` : the initial proportion of infected agents (%)
-`<p_p_infected>` : the probability of transmitting the disease (%)
-`<p_p_i_barrier>` : the probability of resisting to an infection (%) 
-`<t_infectious>` : the time an agent remains infectious _(only for SIS and SIS)_
-`<t_removed>` : the removed time _(only for SIR)_

### Procedure for generating datasets

**Please note that the generated .csv are ignored by the git repository**

#### Running experiments in buzz
In each folder (*EXPX*) you have `.bzz` scripts for running experiments for each epidemic model (*BM,SI,SIS,SIR,SZR*).

Simply tweak the metaparameters at the beginning of the script an run the experiment accordingly for at least `5000` iterations.

`.csv` files will be generated accordingly.

#### Processing and saving the data

Once you have generated `.csv` files for your experiments (usually to observe the variation of a single metaparameter) please run:
`python3 process.py <EXPx/data_xxx>.csv single_infected`
to generate `.pkl` files.

#### Plotting the data

`graphs.py` is where the magic happens...

 
