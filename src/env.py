# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:43:11 2020

@author: Christian
"""


class defaultEnvironment:
    """
    
    The environment stores conditions universal to all individuals. 
    
    For example, some problems may require comparing to data found in a file.
    The environment could be used to read that file data, allowing each 
    solution to have access to that data.   
    
    """
    
    def __init__(self):
        """
        The generic problem doesn't need an environment
        """

        pass