#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test .transform() method with stored example diagram 
stored in PersistenceLandscape.example
"""
from PersistenceLandscape_Alist_Ldict import *

from PersistenceLandscapes import *

from PersistenceLandscape_Alist_Llist import *

dgm = PersistenceLandscape_Alist_Llist.example

P = PersistenceLandscape_Alist_Llist(dgm, 0)

P.transform()