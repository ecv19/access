import sys
sys.path.append('../..')

import math
import unittest

import numpy as np
import pandas as pd
import geopandas as gpd
from access import access, weights
from access.util import testing as tu


class TestMisc(unittest.TestCase):

    def setUp(self):
        n = 5
        supply_grid = tu.create_nxn_grid(n)
        demand_grid = supply_grid.sample(1)
        cost_matrix = tu.create_cost_matrix(supply_grid, 'euclidean')

        self.model = access(demand_df = demand_grid, demand_index = 'id',
                            demand_value = 'value',
                            supply_df = supply_grid, supply_index = 'id',
                            supply_value = 'value',
                            cost_df   = cost_matrix, cost_origin  = 'origin',
                            cost_dest = 'dest',      cost_name = 'cost',
                            neighbor_cost_df   = cost_matrix, neighbor_cost_origin  = 'origin',
                            neighbor_cost_dest = 'dest',      neighbor_cost_name = 'cost')


    def test_score_half_weight_halves_original_value(self):
        self.model.raam()
        self.model.score(col_dict={"raam_value":.5})
        expected = self.model.access_df['raam_value'].iloc[0] / 2
        actual = self.model.access_df['score'].iloc[0]

        self.assertEqual(actual, expected)


    def test_set_cost_reconizes_column_newly_added(self):
        self.model.cost_names.append('new_cost')

        self.model.set_cost('new_cost')
        actual = self.model.default_cost

        self.assertEqual(actual, 'new_cost')


    def test_set_neighbor_cost(self):
        self.model.neighbor_cost_names.append('new_cost')

        self.model.set_neighbor_cost('new_cost')
        actual = self.model.neighbor_default_cost

        self.assertEqual(actual, 'new_cost')

    def test_user_cost_adds_new_column_to_cost_df(self):
        new_cost = self.model.cost_df.copy()
        new_cost['new_cost'] = 0

        self.model.user_cost(new_cost_df = new_cost,
                             name        = 'new_cost',
                             origin      = 'origin',
                             destination = 'dest')

        actual = 'new_cost' in self.model.cost_df.columns

        self.assertEqual(actual, True)


    def test_user_cost_adds_new_column_to_cost_names(self):
        new_cost = self.model.cost_df.copy()
        new_cost['new_cost'] = 0

        self.model.user_cost(new_cost_df = new_cost,
                             name        = 'new_cost',
                             origin      = 'origin',
                             destination = 'dest')

        actual = 'new_cost' in self.model.cost_names

        self.assertEqual(actual, True)


    def test_user_cost_neighbors_adds_new_column_to_neighbor_cost_df(self):
        new_cost = self.model.neighbor_cost_df.copy()
        new_cost['new_cost'] = 0

        self.model.user_cost_neighbors(new_cost_df = new_cost,
                                       name        = 'new_cost',
                                       origin      = 'origin',
                                       destination = 'dest')

        actual = 'new_cost' in self.model.neighbor_cost_df.columns

        self.assertEqual(actual, True)


    def test_user_cost_adds_new_column_to_cost_names(self):
        new_cost = self.model.neighbor_cost_df.copy()
        new_cost['new_cost'] = 0

        self.model.user_cost_neighbors(new_cost_df = new_cost,
                                       name        = 'new_cost',
                                       origin      = 'origin',
                                       destination = 'dest')

        actual = 'new_cost' in self.model.neighbor_cost_names

        self.assertEqual(actual, True)
