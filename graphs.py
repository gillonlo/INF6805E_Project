import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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

    return ds

def lazy_load(filename,plot_type,**kwargs):
    try:
        ds = pd.read_pickle(name2pkl(filename,plot_type))
        print(f"loaded from {name2pkl(filename,plot_type)}")
    except:
        ds = craft_ds(filename,plot_type,**kwargs)
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
    
        infected["nb_state"][:10000].plot(label=f"{varying_parameter}={kwargs[varying_parameter]}")

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
    
        infected["nb_state"][:10000].plot(label=f"{varying_parameter}={kwargs[varying_parameter]}")


    #plt.xscale("log")
    #plt.yscale("log")
    plt.title(f"Removed evolution \nfor various values of {varying_parameter}")
    plt.legend()
    plt.grid()
    plt.savefig(name2fig(filename,plot_type))
    plt.clf()


def gen_meta_meta(varying_parameter,values,exclusion=[],default={}):
    met={
        "n_clusters":4,
        "speed":10,
        "move_type":1,
        "p_i_infected":10,
        "p_p_infected":5,
        "p_p_i_barrier":75,
        "t_infectious":500,
        "t_removed":250
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
    

#m_plot_infection_evolution("EXP1","p_i_infected",gen_meta_meta("p_i_infected",[10,20,30],["t_infectious","t_removed"]))
#m_plot_infection_evolution("EXP3","t_infectious",gen_meta_meta("t_infectious",[100,250,500],["t_removed"]))
#m_plot_removed_evolution("EXP3","t_infectious",gen_meta_meta("t_infectious",[100,250,500],["t_removed"]))
m_plot_infection_evolution("EXP4","t_removed",gen_meta_meta("t_removed",[50,100,250,1000]))