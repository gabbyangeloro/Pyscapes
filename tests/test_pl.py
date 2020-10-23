#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit test for PersistenceLandscapeExact
"""

import unittest 
import numpy as np

from PersistenceLandscape import PersistenceLandscape

class TestPersistenceLandscapeExact(unittest.TestCase):
    
#    def setUp(self):
#        self.diagrams = [np.array([[1.0, 5.0], [2.0, 8.0], 
#                           [3.0, 4.0], [5.0, 9.0], [6.0, 7.0]])]
#        self.homological_degree = 0
#        P = PersistenceLandscape(self.diagrams, self.homological_degree)
#        P.compute_landscape()
    
    def test_pl_critical_pairs(self):
        """
        Test example from Peter & Pavel's paper

        """
        P = PersistenceLandscape(
            diagrams=[np.array([[1.0, 5.0], [2.0, 8.0], [3.0, 4.0], [5.0, 9.0],
                                [6.0, 7.0]])],
            homological_degree=0)
        P.compute_landscape()
        self.assertEqual(P.critical_pairs, [[[1.0, 0],[3.0, 2.0],
        [3.5, 1.5],[5.0, 3.0],[6.5, 1.5],[7.0, 2.0],[9.0, 0]],
        [[2.0, 0], [3.5, 1.5], [5.0, 0], [6.5, 1.5], [8.0, 0]],
        [[3.0, 0], [3.5, 0.5], [4.0, 0], [6.0, 0], [6.5, 0.5],
        [7.0, 0]]])
        
    def test_pl_hom_degree(self):
        """
        Test homological degree
        """
        P = PersistenceLandscape(
            diagrams=[np.array([[1.0, 5.0], [2.0, 8.0], [3.0, 4.0], [5.0, 9.0],
                                [6.0, 7.0]])],
            homological_degree=0)
        self.assertEqual(P.homological_degree,0)

class PersistenceLandscapeBad(unittest.TestCase):
    # TODO: Add bad/error test cases here.
    
    # def test_pl_hom_degree(self):
    #    diagrams = []
    #    hom_deg = -1
    #    self.assertRaises
    pass

if __name__ == '__main__':
    unittest.main()
        