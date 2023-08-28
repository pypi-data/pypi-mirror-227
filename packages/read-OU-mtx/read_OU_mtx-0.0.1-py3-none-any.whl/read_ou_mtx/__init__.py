# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16  2022

@author: from OU Lab. FAH,SYSU 
Wangchen wch_bioinformatics@163.com
"""
import sys,os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pathlib import Path, PurePath
import anndata
from anndata import read_mtx
def read_OU_mtx(
    path,
    var_names='gene_symbols',
    make_unique=True):
    """
    Read datasets that the features.tsv file only has gene symbols column 
    """
    path = Path(path)
    adata =read_mtx(path/'matrix.mtx.gz').T  # transpose the data # transpose the data
    genes = pd.read_csv(path/'features.tsv.gz', header=None, sep='\t')
    if var_names == 'gene_symbols':
        var_names = genes[0].values
        if make_unique:
            var_names = anndata.utils.make_index_unique(pd.Index(var_names))
        adata.var_names = var_names
        
    else:
        raise ValueError("`var_names` needs to be 'gene_symbols' or 'gene_ids'")
    
    adata.obs_names = pd.read_csv(path/'barcodes.tsv.gz', header=None)[0].values
    return adata
