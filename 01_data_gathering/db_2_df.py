#!/usr/bin/env python3

import sqlite3
import numpy as np
import pandas as pd
import pylab as plt


def connect_engine(engine_name="db.sqlite"):
    conn = sqlite3.connect(engine_name)
    c = conn.cursor()
    return (conn, c)

def main():
    conn, c = connect_engine()
    
    cmd = 'SELECT * FROM investing'
    df_invest = pd.read_sql(sql=cmd, con=conn)
    df_crypto.to_csv("df_crypto.csv")
    
    cmd = 'SELECT * FROM crypto'
    df_crypto = pd.read_sql(sql=cmd, con=conn)
    df_invest.to_csv("df_investing.csv")

if __name__=="__main__":
    main()

