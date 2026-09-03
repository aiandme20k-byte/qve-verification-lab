import numpy as np
from scipy.stats import pearsonr
def correlation(x,y):
    if len(x)!=len(y) or len(x)<2: raise ValueError("Equal-length arrays with >=2 samples required")
    r,p=pearsonr(np.asarray(x,dtype=float),np.asarray(y,dtype=float))
    return {"method":"Pearson","r":float(r),"p_value":float(p),"sample_count":len(x),
            "interpretation":"Correlation does not establish causation."}
