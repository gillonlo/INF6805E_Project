import pandas as pd
import sys

def metp2postfix(l):
    if l:
        return f'{l["n_clusters"]}_{l["speed"]}_{l["move_type"]}_{l["p_i_infected"]}_{l["p_p_infected"]}_{l["p_p_i_barrier"]}{"_"+str(l.get("t_infectious","")) if l.get("t_infectious",False) else ""}'
    return ""

name2data = lambda x:x
name2fig = lambda x,f:x+"/"+f+".png"
name2pkl = lambda x,f:x.split("/")[0]+"/"+f+"_"+"_".join(x.split("/")[-1].split("_")[1:]).split(".")[0]+".pkl"

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

def craft_ds(filename,plot_type):
        
    if plot_type[:len("single_infected")]=="single_infected":
        data =pd.read_csv(name2data(filename),delimiter=';')
        ds = draw_exp(data,"infected")
    elif plot_type[:len("single_removed")]=="single_removed":
        data =pd.read_csv(name2data(filename),delimiter=';')
        ds = draw_exp(data,"removed")
    else:
        raise Exception(f"Unrecognized plot type {plot_type}")
    return ds

def lazy_load(filename,plot_type):
    try:
        ds = pd.read_pickle(name2pkl(filename,plot_type))
        print(f"{name2pkl(filename,plot_type)} is already there.")
    except:
        ds = craft_ds(filename,plot_type)
        ds.to_pickle(name2pkl(filename,plot_type)) 
        print(f"loaded from {filename} and saved.")
    return ds

if __name__ == "__main__":
    filename = sys.argv[-2]
    plot_type = sys.argv[-1]
    lazy_load(filename,plot_type)