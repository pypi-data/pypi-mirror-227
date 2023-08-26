# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Import libraries
import pandas as pd
import numpy as np
import transforms3d as t3d

def tongrade(df, begin, end, step, variable, acc):
    """
    TonXGrade chart lists creation function
    Params:
    :param df: dataset to be used (it can be a block model, drill holes, etc)
    :type df: DataFrame
    :param begin: Lower cut-off grade desired
    :type begin: float
    :param end: Upper cut-off grade desired
    :type end: float
    :param step: Cut-off increment
    :type step: float
    :param variable: Grade variable in the dataset (e.g. AU_fin, CU...)
    :type variable: string
    :param acc: Variable to be used to weight the grade (e.g. tonnage or volume)
    :type acc: string
    :return: The function will return four lists with the values accumulated by each cut-off, being that the cut-off, grade, tonnage, and proportion
    :rtype: list
    """
    cutoff = np.arange(begin, end, step)
    df['gacc'] = df[variable] * df[acc]
    grade = []
    ton = []
    prop = []

    for c in cutoff:
        df_ = df.loc[df[variable] >= c]
        if df_.empty:
            grade.append(np.nan)
            ton.append(0)
            prop.append(ton[len(ton) - 1])
        else:
            grade.append(df_['gacc'].sum() / df_[acc].sum())
            ton.append(df_[acc].sum())
            if len(prop) == 0:
                prop.append(1)
            else:
                prop.append(ton[len(ton) - 1] / ton[0])

    return cutoff, grade, ton, prop

def xyzrotate(df, xcol, ycol, zcol, xori, yori, zori, angle, rot):
    """
    Rotate/unrotate coordinates function
    Params:
    :param df: dataset to be used (it can be a block model, drill holes, etc)
    :type df: DataFrame
    :param xcol: name of the X coordinates column (e.g. 'XC')
    :type xcol: string
    :param ycol: name of the Y coordinates column (e.g. 'YC')
    :type ycol: string
    :param zcol: name of the Z coordinates column (e.g. 'ZC')
    :type zcol: string
    :param xori: X origin coordinate
    :type xori: float
    :param yori: Y origin coordinate
    :type yori: float
    :param zori: Z origin coordinate
    :type zori: float
    :param angle: rotation agle
    :type angle: float
    :param rot: method to be used (0: generate the unrotated coordinates from rotated file; 1: generate the rotated coordinates from unrotated file)
    :type rot: int
    :return: return the updated dataframe
    :rtype: DataFrame
    """
    mat = t3d.euler.euler2mat(ai=np.radians(angle), aj=0, ak=0, axes='szxz')
    rotxyz = np.dot(np.array(df[[xcol, ycol, zcol]]), mat)

    if rot == 1:
        rotxyz[:, 0] += xori
        rotxyz[:, 1] += yori
        rotxyz[:, 2] += zori

        df['XROT'] = rotxyz[:, 0]
        df['YROT'] = rotxyz[:, 1]
        df['ZROT'] = rotxyz[:, 2]

    if rot == 0:
        xyz.loc[:, xcol] -= xori
        xyz.loc[:, ycol] -= yori
        xyz.loc[:, zcol] -= zori
        new_xyz = np.dot(xyz, mat)
        df['XUROT'] = new_xyz[:, 0]
        df['YUROT'] = new_xyz[:, 1]
        df['ZUROT'] = new_xyz[:, 2]

    return df



