# INF6805E_Project

## Stats

### Hyperparameters

3 hyperparameters have to be set :

- `DATA_FILE` : the name of the file in which the robots will store their state at each step
- `EPIDEMIC_TREE_FILE` : : the name of the file in which which robot infect which other robot is stored (only works for Branch and SIR and SZR)
- `EXP_NAME` : the name of the current experiment, used to calculate mean results

The idea is one file per hyperparameter value (so if the movement type, probabilities are canged, a new file needs to be dedicated) and one experiment name per run so that we have mean results.
If the file exists, new data is appended at the end, otherwise it is automaticaly created


 
