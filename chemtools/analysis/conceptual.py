# -*- coding: utf-8 -*-
# ChemTools is a collection of interpretive chemical tools for
# analyzing outputs of the quantum chemistry calculations.
#
# Copyright (C) 2014-2015 The ChemTools Development Team
#
# This file is part of ChemTools.
#
# ChemTools is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# ChemTools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --
'''Module for Conceptual Density Functional Theory Analysis of Quantum Chemistry Output Files.

   This modules contains wrappers which take outputs of quantum chemistry softwares and
   compute various conceptual density functional theory (DFT) descriptive tools.
'''

import numpy as np
from horton import IOData
from chemtools.tool.globaltool import LinearGlobalTool, QuadraticGlobalTool, ExponentialGlobalTool, RationalGlobalTool



class ConceptualDFT_1File(object):
    '''
    Class for conceptual density functional theory (DFT) analysis of one quantum
    chemistry output file using the frontiner molecular orbital (FMO) approach.
    '''
    def __init__(self, molecule_filename, model='quadratic', energy_expr=None):
        '''
        Parameters
        ----------
        molecule_filename : str
            The path to the molecule's file.
        model : str, default='quadratic'
            Energy model used to calculate descriptive tools.
            The available models include:
            * 'linear'; refer to :py:class:`chemtools.tool.globaltool.LinearGlobalTool` for more information.
            * 'quadratic'; refer to :py:class:`chemtools.tool.globaltool.QuadraticGlobalTool` for more information.
            * 'exponential'; refer to :py:class:`chemtools.tool.globaltool.ExponentialGlobalTool` for more information.
            * 'rational'; refer to :py:class:`chemtools.tool.globaltool.RationalGlobalTool` for more information.
            * 'general'; refer to :py:class:`chemtools.tool.globaltool.GeneralGlobalTool` for more information.
            If 'general' model is selected, an energy expression should be given.
        energy_expr : ``Sympy.expr``, default=None
            Energy expresion used, if 'general' model is selected.
        '''
        mol = IOData.from_file(molecule_filename)
        self._mol = mol
        if model not in ['linear', 'quadratic', 'exponential', 'rational', 'general']:
            raise ValueError('Argument model={0} is not supported.'.format(model))
        if model is 'general' and energy_expr is None:
            raise ValueError('Argument energy_expr is required when model=\'general\'.')
        self._model = model
        self.energy_expr = energy_expr

        # TODO: Some attributes of the self._mol should become the class attribute
        #       like coordinates, numbers, energy, etc.

        # Get E(HOMO), E(LUMO) & number of electrons
        homo_energy = self._mol.exp_alpha.homo_energy
        lumo_energy = self._mol.exp_alpha.lumo_energy
        n_elec = int(np.sum(self._mol.exp_alpha.occupations))

        # HACK: self._mol might not have the exp_beta attribute, making it crash
        if hasattr(self._mol, 'exp_beta'):
            if self._mol.exp_beta is not None:
                n_elec += int(np.sum(self._mol.exp_beta.occupations))
                if self._mol.exp_beta.homo_energy > homo_energy:
                    homo_energy = self._mol.exp_beta.homo_energy
                if self._mol.exp_beta.lumo_energy < lumo_energy:
                    lumo_energy = self._mol.exp_beta.lumo_energy

        # Temporary check as HORTON does not store energy when reading WFN files.
        if hasattr(self._mol, 'energy'):
            # Compute E(N), E(N+1), & E(N-1)
            energy_zero = self._mol.energy
            energy_plus = energy_zero - lumo_energy
            energy_minus = energy_zero - homo_energy
        else:
            raise ValueError('Argument molecule_filename does not contain energy value!')

        # Define global tool
        if model == 'linear':
            self._globaltool = LinearGlobalTool(energy_zero, energy_plus, energy_minus, n_elec)
        elif model == 'quadratic':
            self._globaltool = QuadraticGlobalTool(energy_zero, energy_plus, energy_minus, n_elec)
        elif model == 'exponential':
            self._globaltool = ExponentialGlobalTool(energy_zero, energy_plus, energy_minus, n_elec)
        elif model == 'rational':
            self._globaltool = RationalGlobalTool(energy_zero, energy_plus, energy_minus, n_elec)
        elif model == 'general':
            pass

    @property
    def model(self):
        '''
        Energy model used to calculate descriptive tools.
        '''
        return self._model

    @property
    def globaltool(self):
        '''
        Instance of one of the gloabl reactivity tool classes.
        '''
        return self._globaltool
