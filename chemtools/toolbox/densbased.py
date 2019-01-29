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
# pragma pylint: disable=invalid-name
"""Density-Based Local Tools."""


from chemtools.denstools.densbased import DensityBasedTool
from chemtools.wrappers.molecule import Molecule


__all__ = ['DensityLocalTool']


class DensityLocalTool(DensityBasedTool):
    """Density Local Tool Class."""

    def __init__(self, molecule, spin='ab', index=None, points=None):
        r"""Initialize class using instance of `Molecule` and grid points.

        Parameters
        ----------
        molecule : Molecule
            An instance of `Molecule` class.
        spin
        index
        points : np.ndarray, optional
            Grid points, given as a 2D array with 3 columns, used for calculating local properties.
        """
        if points is None:
            raise NotImplementedError()
        super(DensityLocalTool, self).__init__(*molecule.compute_megga(points, spin, index))

    @classmethod
    def from_file(cls, filename, spin='ab', index=None, points=None):
        """Initialize class from file.

        Parameters
        ----------
        filename : str
            Path to molecule's files.
        spin
        index
        points : np.ndarray, optional
            Grid points, given as a 2D array with 3 columns, used for calculating local properties.
        """
        molecule = Molecule.from_file(filename)
        return cls(molecule, spin, index, points)