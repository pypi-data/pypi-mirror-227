# -*- coding: utf-8 -*-
"""
Created on Fri Apr  28  17:15:24 2023

@title: Material

@author: avisive

@content: The PyMagnets package (to be used with the userscript.py) contains the useful functions to create a FE-model of a magnet of the ExpAreas, the functions are divided by classes which are themselves divided in 3 libraries.
Here, the library contains classes for material and bh curves
"""

from operapy import opera2d  # import the opera2d library




class MaterialLibrary: # In this class, all the materials are defined
    def __init__(self, currentmodel):
        self.material = currentmodel.operaModel.create_material('')  # creates an opera material and defines it as the '.material' attribute of any object of the MaterialLibrary() class

    def Set_Air(self): # Defines the Air/Default material
        self.material.name = 'Air-Default' # set its name
        self.material.permeability_type = opera2d.MaterialPermeabilityType.Linear  # sets the type of permeability as linear
        self.material.directionality = opera2d.Directionality.Isotropic  # sets the directionality as isotropic
        self.material.electrical_conductivity = opera2d.ModelValue(0.0, opera2d.Unit.Conductivity.SiemensPerMetre)  # sets the conductivity as null since it's air
        self.material.color = '#ffffff' # sets a color to be easily identifiable in the interface (white) # the colors are set to be able to be differentiate with the mesh and the colors of the density plots and lines
        # CHECK if enough info

    def Set_Copper(self):  # Defines the Copper material
        self.material.name = 'Copper'  # sets its name
        self.material.permeability_type = opera2d.MaterialPermeabilityType.Linear  # sets the type of permeability as linear
        self.material.directionality = opera2d.Directionality.Isotropic  # sets the directionality as isotropic
        self.material.electrical_conductivity = opera2d.ModelValue('58E+06', opera2d.Unit.Conductivity.SiemensPerMetre)  # sets the value of the conductivity
        self.material.color = '#ff7b7d' # sets a color to be easily identifiable in the interface (light red) # the colors are set to be able to be differentiate with the mesh and the colors of the density plots and lines
        # CHECK if enough info

    def Set_Steel(self, bh_curve_steel):  # Defines the Steel material with a certain bh curve
        self.material.name = 'Steel'  # sets its name
        self.material.permeability_type = opera2d.MaterialPermeabilityType.Nonlinear  # sets the type of permeability as non-linear
        self.material.directionality = opera2d.Directionality.Isotropic  # sets the directionality as isotropic
        self.material.electrical_conductivity = opera2d.ModelValue('8.41E+06', opera2d.Unit.Conductivity.SiemensPerMetre)  # sets the value of the conductivity
        self.material.bh_curve = bh_curve_steel.bh_curve # since the permeability is non-linear, one needs to define a certain bh curve as the one for this material
        self.material.color = '#aa0000'  # sets a color to be easily identifiable in the interface (dark red) # the colors are set to be able to be differentiate with the mesh and the colors of the density plots and lines


class BHcurveLibrary:  # In this class, all the bh curves used are defined
    def __init__(self, currentmodel, bh_path):
        self.bh_curve = currentmodel.operaModel.create_bh_curve('Steel BH Curve')  # Creates an opera bh curve and defines it as the '.bh_curve' attribute of any object of the BHcurveLibrary() class
        self.bh_path = bh_path  #path to the locally cloned git folder containing all the bh curves.

    def Set_Mildhigh(self):  # Defines the Midlhigh bh curve from Opera BH library
        path = self.bh_path + 'mildhigh.bh'
        self.bh_curve.load(path)  # loads this bh curve from its path

    def Set_Default(self):  # Defines the Default bh curve from Opera BH library
        path = self.bh_path + 'default.bh'
        self.bh_curve.load(path)  # loads this bh curve from its path

    def Set_MBGSteel(self):  # Defines the MBG Steel bh curve
        path = self.bh_path + 'MBG Steel.bh'
        self.bh_curve.load(path)  # loads this bh curve from its path

    def Set_Tenten(self):  # Defines the MBG Steel bh curve
        path = self.bh_path + 'tenten.bh'
        self.bh_curve.load(path)  # loads this bh curve from its path

    def Set_OtherBHcurve(self, filepath):
        self.bh_curve.load(filepath)  # loads this bh curve from its path
