import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

EXP_LENGTH=5000*2

def metp2postfix(l):
    has = lambda x:("_"+str(l.get(x,"")) if l.get(x,False) else "")
    if l:
        return f'{l["n_clusters"]}_{l["speed"]}_{l["move_type"]}_{l["p_i_infected"]}_{l["p_p_infected"]}_{l["p_p_i_barrier"]}{has("t_infectious")}{has("t_removed")}'
    return ""

name2data = lambda x,b:x+"/data_"+metp2postfix(b)+".csv"
name2fig = lambda x,f:x+"/"+f+".png"
name2pkl = lambda x,f:x+"/"+f+".pkl"

def sum_per_step(df,state):
    steps = []
    sum = []
    for step in df["step"].unique():
        steps.append(step)
        sum.append(len(df[(df.step==step) & (df.state == state) ]))
    return steps,sum

def draw_exp(df,state):
    sums= []
    steps=[]
    for exp in df.exp.unique():
        step, sum = sum_per_step(df[df.exp==exp],state)
        sums.extend(sum)
        steps.extend(step)


    d = {'step': steps, 'nb_state': sums}

    df = pd.DataFrame(data=d)  
    return df

def craft_ds(filename,plot_type,**kwargs):
        
    if plot_type[:len("single_infected")]=="single_infected":
        data =pd.read_csv(name2data(filename,kwargs),delimiter=';')
        ds = draw_exp(data,"infected")
    elif plot_type[:len("single_removed")]=="single_removed":
        data =pd.read_csv(name2data(filename,kwargs),delimiter=';')
        ds = draw_exp(data,"removed")
    elif plot_type[:len("zombie")]=="zombie":
        data =pd.read_csv(name2data(filename,kwargs),delimiter=';')
        ds = draw_exp(data,"zombie")

    return ds

def lazy_load(filename,plot_type,**kwargs):
    try:
        ds = pd.read_pickle(name2pkl(filename,plot_type))
        print(f"loaded from {name2pkl(filename,plot_type)}")
    except:
        ds = craft_ds(filename,plot_type if filename!="EXP5" else "zombie",**kwargs)
        ds.to_pickle(name2pkl(filename,plot_type)) 
        print(f"loaded from {name2data(filename,kwargs)}")
    return ds

def plot_infection_evolution(filename,**kwargs):
    plot_type = "single_infected_"+metp2postfix(kwargs)
    infected = lazy_load(filename,plot_type,**kwargs)
    
    infected["nb_state"].plot()
    plt.xscale("log")
    plt.title(metp2postfix(kwargs))
    plt.savefig(name2fig(filename,plot_type))
    plt.clf()

def m_plot_infection_evolution(filename, varying_parameter, list_of_mparam):

    plot_type=f"multi_infection_{varying_parameter}"

    for kwargs in list_of_mparam:
        subplot_type = "single_infected_"+metp2postfix(kwargs)
        infected = lazy_load(filename,subplot_type,**kwargs)
    
        infected["nb_state"][:EXP_LENGTH].plot(label=f"{varying_parameter}={kwargs[varying_parameter]}")
        plt.fill_between(np.arange(0,EXP_LENGTH,1),0,infected["nb_state"][:EXP_LENGTH],alpha=.1)

    #plt.xscale("log")
    #plt.yscale("log")
    plt.title(f"Infection evolution \nfor various values of {varying_parameter}")
    plt.legend()
    plt.grid()
    plt.savefig(name2fig(filename,plot_type))
    plt.clf()

def m_plot_removed_evolution(filename, varying_parameter, list_of_mparam):

    plot_type=f"multi_removed_{varying_parameter}"

    for kwargs in list_of_mparam:
        subplot_type = "single_removed_"+metp2postfix(kwargs)
        infected = lazy_load(filename,subplot_type,**kwargs)
    
        infected["nb_state"][:EXP_LENGTH].plot(label=f"{varying_parameter}={kwargs[varying_parameter]}")


    #plt.xscale("log")
    #plt.yscale("log")
    plt.title(f"Removed evolution \nfor various values of {varying_parameter}")
    plt.legend()
    plt.grid()
    plt.savefig(name2fig(filename,plot_type))
    plt.clf()

def m_mixed_infection_evolution(filenames, list_of_mparam):
    plot_type =f"mixed_infection_{'_'.join(filenames)}"

    for i,kwargs in enumerate(list_of_mparam):
        subplot_type = "single_infected_"+metp2postfix(kwargs)
        infected = lazy_load(filenames[i],subplot_type,**kwargs)
        infected["nb_state"][:EXP_LENGTH].plot(label=f"{filenames[i]}")
        plt.fill_between(np.arange(0,EXP_LENGTH,1),0,infected["nb_state"][:EXP_LENGTH],alpha=.1)  

    plt.title(f"Removed evolution \nfor various models")
    plt.legend()
    plt.grid()
    plt.savefig(name2fig(".",plot_type))
    plt.clf() 

def gen_meta_meta(varying_parameter,values,exclusion=[],default={}):
    met={
        "n_clusters":4,
        "speed":10,
        "move_type":1,
        "p_i_infected":10,
        "p_p_infected":5,
        "p_p_i_barrier":75,
        "t_infectious":250,
        "t_removed":100
    }
    l=[]
    for x in values:
        tmp_m = {}
        for k,v in met.items():
            if k in exclusion:
                continue
            if k!=varying_parameter:
                tmp_m[k]=default.get(k,v)
            else:
                tmp_m[k]=x
        l.append(tmp_m)
    return l


"""
"p_p_i_barrier":75,
        "t_infectious":500,
        "t_removed":250
"""
## EXP1
"""
m_plot_infection_evolution("EXP1","p_p_i_barrier",gen_meta_meta("p_p_i_barrier",[25,50,75,100],["t_infectious","t_removed"]))
m_plot_infection_evolution("EXP1","n_clusters",gen_meta_meta("n_clusters",[2,3,4],["t_infectious","t_removed"]))
m_plot_infection_evolution("EXP1","p_p_infected",gen_meta_meta("p_p_infected",[2,5,7,10,25],["t_infectious","t_removed"]))
m_plot_infection_evolution("EXP1","p_i_infected",gen_meta_meta("p_i_infected",[10,20,30,50],["t_infectious","t_removed"]))
"""

## EXP2
#m_plot_infection_evolution("EXP2","t_infectious",gen_meta_meta("t_infectious",[100,250,500,1000],["t_removed"]))
#m_plot_infection_evolution("EXP2","p_p_infected",gen_meta_meta("p_p_infected",[2,5,7,10,25],["t_removed"]))
#m_plot_infection_evolution("EXP2","p_p_i_barrier",gen_meta_meta("p_p_i_barrier",[25,50,75,100],["t_removed"]))

## EXP3
#m_plot_infection_evolution("EXP3","p_p_i_barrier",gen_meta_meta("p_p_i_barrier",[25,50,75,100],["t_removed"]))
#m_plot_infection_evolution("EXP3","p_p_infected",gen_meta_meta("p_p_infected",[2,5,7,10,25],["t_removed"]))
#m_plot_infection_evolution("EXP3","t_infectious",gen_meta_meta("t_infectious",[100,250,500,1000],["t_removed"]))

# Mixed
#m_mixed_infection_evolution(["EXP2","EXP3"],[gen_meta_meta("t_infectious",[500],["t_removed"])[0],gen_meta_meta("t_infectious",[500],["t_removed"])[0]])

## EXP4
dflt = {
    "p_p_i_barrier":75,
    "t_infectious":500,
    "t_removed":250
}
m_plot_infection_evolution("EXP4","t_infectious",gen_meta_meta("t_infectious",[100,250,500,1000],default=dflt))
m_plot_infection_evolution("EXP4","p_p_i_barrier",gen_meta_meta("p_p_i_barrier",[25,50,75,100],default=dflt))
m_plot_infection_evolution("EXP4","p_p_infected",gen_meta_meta("p_p_infected",[2,5,7,10,25],default=dflt))
m_plot_infection_evolution("EXP4","t_removed",gen_meta_meta("t_removed",[50,100,250,500,1000],default=dflt))


# EXP5
#m_plot_infection_evolution("EXP5","t_infectious",gen_meta_meta("t_infectious",[100,250,500,1000],["t_removed"]))
#m_plot_infection_evolution("EXP5","p_p_infected",gen_meta_meta("p_p_infected",[2,5,7,10,25],["t_removed"]))
#m_plot_infection_evolution("EXP5","p_p_i_barrier",gen_meta_meta("p_p_i_barrier",[10,25,50,75],["t_removed"]))
#m_plot_infection_evolution("EXP5","p_i_infected",gen_meta_meta("p_i_infected",[5,10,20,30,50],["t_removed"]))
