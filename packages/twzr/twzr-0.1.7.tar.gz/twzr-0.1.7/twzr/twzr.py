# twzr.py 

import pandas as pd 
import numpy as np 
import os 
import time  
import re 
from typing import Union


# read csv
def rc(fn,fd=None,fe=None,chdir:bool=True):
    if fe is not None:
        fn = fn+"."+fe
    if fd is not None:
        if chdir:
            os.chdir(fd)
        else:
            fn = os.path.join(fd,fn)
    return pd.read_csv(fn)


# filter 
f = lambda x,y: x.filter(regex=re.compile(y,re.IGNORECASE))


# value count
vc = lambda x,y,d=False,n=True: x[y].value_counts(dropna=d,normalize=n)


# weighted value count
def wvc(df,c,n=True):
    gb = df.groupby([c]).sum()
    if n:
        gb = gb/gb.sum()

    return gb 


cross = lambda x,y: x + " x " + y


def cross_col(df,x,y):
    df[cross(x,y)] = cross(df[x],df[y])


def ch_val(df,c,mask,nv): 

    df[c] = np.where(
        mask,
        nv,
        df[c]
        )


def ch_vals(df,c,masks:list,nvs:list):
    for mask,nv in zip(masks,nvs):
        ch_val(df,c,mask,nv)


def ch_val_from(df,c,ov,nv): 
    if not isinstance(ov,list):
        ov = [ov]
    
    ch_val(df,c, df[c].isin(ov),nv)


def ch_vals_from(df,c,ovs:list,nvs:list):
    for ov,nv in zip(ovs,nvs):
        ch_val_from(df,c,ov,nv)


def xt(df,row_col,col_col,w=None,n="index"):
    if w is not None:
        return pd.crosstab(
            df[row_col],
            df[col_col],
            df[w],
            aggfunc="sum",
            normalize=n
            )
    else:
        return pd.crosstab(
            df[row_col],
            df[col_col],
            normalize=n
            )


def move_col(df,col:Union[str,int],new_index:int=None):
    if isinstance(col,int):
        col = df.columns[col]
    if new_index is None:
        new_index = df.shape[1]-1
    xs = df.pop(col)
    df.insert(new_index,col,xs)


def ts():
    return time.strftime("_%Y%m%d-%H%M")


help_str = """
    current functions are:
        rc              pd.read_csv() with options for file directory (fd) and file extension (fe). if fd provided, chdir=True will change working directory.
        f               df.filter() wrapper function, case-insensitive. arguments: x: pd.DataFrame, y:str (column name)
        vc              df.value_counts() wrapper function. arguments: x: pd.DataFrame, y: str (column name), d=False:bool (dropna), n=True: bool (normalize)
        wvc             weighted value counts
        xt              pd.crosstab() wrapper function that readily handles weights. arguments: df,row_col,col_col,w=None:str (weight column),n="index":str (normalize argument)
        cross           cross two strings
        cross_col       cross two columns of strings and create a new column that is the variable names crossed
        ch_val          wrapper for numpy.where with a boolean mask, new value, dataframe, and given column
        ch_vals         for loop over `ch_val` with lists of masks and new values for a given column
        ch_val_from     wrapper for numpy.where with a (set of) previous values in place of a boolean mask
        ch_vals_from    for loop over `ch_val_from` with lists of old values and new values for a given column
        move_col        move a column. arguments: df, col:str|int (column label or index),new_index:int (desired column index)
        ts              generate a string with the current time
        """

def help(print_=True,return_=False):
    if print_:
        print(help_str)
    if return_:
        return(help_str)


