# -*- coding: utf-8 -*-
"""
Created on Fri Apr  28  17:15:24 2023

@title: Model

@author: avisive

@content: he PyMagnets package (to be used with the userscript.py) contains the useful functions to create a FE-model of a magnet of the ExpAreas, the functions are divided by classes which are themselves divided in 3 libraries.
Here, the library contains classes for everything that is independant from a magnet point of vue
"""

from operapy import opera2d  # imports the opera2d library
from operapy import canvas  # imports the canvas library
import numpy as _np # defines the numpy library as np
import pybdsim  # imports pybdsim for the BDSIM fieldmap
import os # imports os to remove files
from datetime import datetime # imports datetime to timestamp the the creation of the file to write it in the title (to make it unique)


class Model:
    def __init__(self):
        self.operaModel = opera2d.get_model_interface()  # creates a model from opera2d and defines-it as the attribute '.operaModel' of any object belonging to the class Model()  # Allows interaction with the model. Through these methods, the geometry can be built, modified and cleared.

    def Set_Units(self, units): # sets the units of the opera2d model
        if (units == 'SI_mm') or ('SI_with_cm') or (units == 'SI_mm_G') or ('SI_with_cm_G'): # if one wants SI units with mm for the length
            self.operaModel.use_unit(opera2d.Unit.Angle.Degree)
            self.operaModel.use_unit(opera2d.Unit.Cardinal.Integer)
            self.operaModel.use_unit(opera2d.Unit.Velocity.MetrePerSecond)
            self.operaModel.use_unit(opera2d.Unit.Temperature.Kelvin)
            self.operaModel.use_unit(opera2d.Unit.MagneticFieldStrength.AmperePerMetre)
            self.operaModel.use_unit(opera2d.Unit.MagneticScalarPotential.Ampere)
            self.operaModel.use_unit(opera2d.Unit.MagneticVectorPotential.WeberPerMetre)
            self.operaModel.use_unit(opera2d.Unit.ElectricFluxDensity.CoulombPerMetreSquared)
            self.operaModel.use_unit(opera2d.Unit.ElectricFieldStrength.VoltsPerMetre)
            self.operaModel.use_unit(opera2d.Unit.Conductivity.SiemensPerMetre)
            self.operaModel.use_unit(opera2d.Unit.Voltage.Volt)
            self.operaModel.use_unit(opera2d.Unit.CurrentDensity.AmperePerMetreSquared)
            self.operaModel.use_unit(opera2d.Unit.ChargeDensity.CoulombPerMetreCubed)
            self.operaModel.use_unit(opera2d.Unit.ThermalConductivity.WattPerMetrePerKelvin)
            self.operaModel.use_unit(opera2d.Unit.SpecificHeatCapacity.JoulePerKilogramPerKelvin)
            self.operaModel.use_unit(opera2d.Unit.Power.Watt)
            self.operaModel.use_unit(opera2d.Unit.Force.Newton)
            self.operaModel.use_unit(opera2d.Unit.Energy.Joule)
            self.operaModel.use_unit(opera2d.Unit.Mass.Kilogram)
            self.operaModel.use_unit(opera2d.Unit.Pressure.Pascal)
            self.operaModel.use_unit(opera2d.Unit.MassDensity.KilogramPerMetreCubed)
            self.operaModel.use_unit(opera2d.Unit.ThermalExpansion.PerKelvin)
            self.operaModel.use_unit(opera2d.Unit.Resistance.Ohm)
            self.operaModel.use_unit(opera2d.Unit.Capacitance.Farad)
            self.operaModel.use_unit(opera2d.Unit.Inductance.Henry)
            self.operaModel.use_unit(opera2d.Unit.Frequency.Hertz)
            self.operaModel.use_unit(opera2d.Unit.ResistancePerUnitLength.OhmPerMetre)
            self.operaModel.use_unit(opera2d.Unit.Time.Second)
            self.operaModel.use_unit(opera2d.Unit.RotationalVelocity.RevolutionPerMinute)
            self.operaModel.use_unit(opera2d.Unit.Current.Ampere)
            self.operaModel.use_unit(opera2d.Unit.Torque.NewtonMetre)
            self.operaModel.use_unit(opera2d.Unit.Inertia.KilogramMetreSquared)
            self.operaModel.use_unit(opera2d.Unit.Emission.AmperePerMetreSquaredPerKelvin)
            self.operaModel.use_unit(opera2d.Unit.HeatTransferCoefficient.WattPerMetreSquaredPerKelvin)
            if units == 'SI_mm': # if one wants SI units with mm for the length
                self.operaModel.use_unit(opera2d.Unit.Length.Millimetre)
                self.operaModel.use_unit(opera2d.Unit.MagneticFluxDensity.Tesla)
            if units == 'SI_cm': # if one wants SI units with cm for the length
                self.operaModel.use_unit(opera2d.Unit.Length.Centimetre)
                self.operaModel.use_unit(opera2d.Unit.MagneticFluxDensity.Tesla)
            if units == 'SI_mm_G': # if one wants SI units with mm for the length and Gauss for the magnetic flux density
                self.operaModel.use_unit(opera2d.Unit.Length.Millimetre)
                self.operaModel.use_unit(opera2d.Unit.MagneticFluxDensity.Gauss)
            if units == 'SI_cm_G': # if one wants SI units with cm for the length and Gauss for the magnetic flux density
                self.operaModel.use_unit(opera2d.Unit.Length.Centimetre)
                self.operaModel.use_unit(opera2d.MagneticFluxDensity.Gauss)

    def Set_Settings(self, symmetry_type, elements_type): # sets different settings of the opera2d model like the type of problem, the symmetry type, the form of the mesh, the sign of the rotations, the general mesh size
        self.operaModel.analysis_settings.physics_type = opera2d.PhysicsType.Magnetostatic  # sets the problem as magnetostatic
        if symmetry_type == 'Cartesian':  # according to the demand of the user sets the type of symmetry
            self.operaModel.general_settings.symmetry_type = opera2d.SymmetryType.XY # sets the symmetry type as Cartesian
        if symmetry_type == 'Axisymmetric':  # according to the demand of the user sets the type of symmetry
            self.operaModel.general_settings.symmetry_type = opera2d.SymmetryType.RZ # sets the symmetry type as Spheric/Axisymmetric
        if elements_type == 'Quadratic':  # according to the demand of the user sets the type/form of mesh
            self.operaModel.general_settings.element_type = opera2d.ElementType.Quadratic  # defines the mesh as quadratic elements
        if elements_type == 'Linear':  # according to the demand of the user sets the type/form of mesh
            self.operaModel.general_settings.element_type = opera2d.ElementType.linear  # defines the mesh as linear elements
        self.operaModel.general_settings.signed_rotations = (1.0, opera2d.PeriodicSign.Periodic)  # defines the sign of the rotations
        self.operaModel.general_settings.mesh_size = opera2d.ModelValue(200, opera2d.Unit.Length.Millimetre)  # defines an arbitrary value as the mesh size for the whole model

    def GenerateMesh(self): # generates the mesh for the opera2d model (ie any object of the Model() class)
        self.operaModel._flatten_geometry()  # flattens the geometry to be able to generate the mesh
        self.operaModel._generate_mesh(1e-06, True) # actual opera command to generate the mesh

    def Solve(self, path_model):
        self.operaModel.solve(path_model, overwrite=True, foreground=True)  # saves and solves the opera2d model (ie any object of the Model() class) in a certain path_model


class PostProcessing():
    def __init__(self, currentmodel):
        self.postprocessing = opera2d.get_post_processing_interface(currentmodel.operaModel) # creates a postprocessing element from a model of the classe Model() # Contains the commands for post-processing results, including creating maps, calculatingintegrals and exporting tables. Requires a model with a solution to be loaded.
        canvas.get_view().show_mesh = True  # Switches the mesh visibility on

    def Plot_DensityMap(self, field, nb_colours, file_path, coord_topleft, coord_bottomright, width, height):  # plots a density map with the default arguments (field='B', nb_colours=1000, maptype=opera2d.ContourMapType.Zones) or other arguments
        canvas.get_view().show_mesh = False  # Switches the mesh visibility off
        self.postprocessing.calculate_contour_map(field_expression=field, contour_count=nb_colours, type=opera2d.ContourMapType.Zones, name='Density map',display_material_boundaries=True)  # contour count = resolution of the map # display_material_boundaries to be able to see the limit of the bodies
        if file_path!=None:  # saves the plot if one wants but it needs to define the coordinates of the surface they wants to be printed
            canvas.export_image(file_path, coord_topleft, coord_bottomright,width, height)

    def Plot_FluxLines(self, field, nb_lines, file_path, coord_topleft, coord_bottomright, width, height):  #plots the flux lines with the default arguments (field='POT', nb_lines=25, maptype=opera2d.ContourMapType.Lines)
        canvas.get_view().show_mesh = False # Switches the mesh visibility off
        self.postprocessing.calculate_contour_map(field_expression=field, contour_count=nb_lines, type=opera2d.ContourMapType.Lines, name='Flux Lines',display_material_boundaries=True)  # contour count = number of lines that will be drawn # display_material_boundaries to be able to see the limit of the bodies
        if file_path!=None:  # saves the plot if one wants but it needs to define the coordinates of the surface they wants to be printed
            canvas.export_image(file_path, coord_topleft, coord_bottomright, width, height)

    def Plot_minmaxBDensityMap(self, file_path, minB, maxB):
        canvas.get_view().show_mesh = False  # Switch the mesh visibility off
        bminmax = self.postprocessing.calculate_contour_map(field_expression='B', contour_count=1000, type=opera2d.ContourMapType.Zones, name='Density plot with minB',  display_material_boundaries=True)  # plots a field map # contour count = resolution of the map # display_material_boundaries to be able to see the limit of the bodies
        if minB != None: # if a minimum value for the B range has been defined
            bminmax.use_autoscale_min = False # removes the autoscaling for the minimum
            bminmax.min = minB  # sets the minimum to the value asked by the user
        if maxB != None: # if a maximum value for the B range has been defined
            bminmax.use_autoscale_max = False  # removes the autoscaling for the maximum
            bminmax.max = maxB # sets the maximum to the value asked by the user
        canvas.export_image(file_path) # saves the image

    def Create_Fieldmap_TXTformat(self, currentmodel, fieldmap_units, path_of_directory, date, pymagnets_version, pymagnets_version_tuple, author, magnet_name, magnet_length, bhcurvename, benchmarking_avgErr, benchmarking_maxErr, current, meshsize_x, meshsize_y, xstart, ystart, xend, yend):  # creates a fieldmap with the txt format
        self.postprocessing.file_path = path_of_directory + magnet_name + '_fieldmapTXT_' + str(current) + 'A_pymagnetsV'+ str(pymagnets_version_tuple[0]) + '-' + str(pymagnets_version_tuple[1]) + '-' + str(pymagnets_version_tuple[2]) + '_'+ date +'.txt'  # sets the path where to save the fieldmap
        self.postprocessing.file_fieldmap = open(self.postprocessing.file_path, 'w', encoding='UTF8')  # opens the file where the fieldmap will be contained
        # Sets the headers of the file
        self.postprocessing.file_fieldmap.write('Date: ')  # writes date on top of the txt file
        self.postprocessing.file_fieldmap.write(date)
        self.postprocessing.file_fieldmap.write(', Author: ')  # writes author on top of the txt file
        self.postprocessing.file_fieldmap.write(author)
        self.postprocessing.file_fieldmap.write(', Version of PyMagnets used: ')  # writes version of pymagnets on top of the txt file
        self.postprocessing.file_fieldmap.write(pymagnets_version)
        self.postprocessing.file_fieldmap.write('\n\n\nMagnet: ')  # writes magnet name on top of the txt file
        self.postprocessing.file_fieldmap.write(magnet_name)
        self.postprocessing.file_fieldmap.write(', Length of the magnet: ')  # writes magnet length on top of the txt file
        self.postprocessing.file_fieldmap.write(f"{magnet_length}")
        self.postprocessing.file_fieldmap.write('mm\nName of the BH curve used: ')  # writes bh curve name on top of the txt file
        self.postprocessing.file_fieldmap.write(bhcurvename)
        self.postprocessing.file_fieldmap.write('\nBenchmarking -  Average error btw chosen bh curve and real MM: ')  # writes avg error on top of the txt file
        self.postprocessing.file_fieldmap.write(benchmarking_avgErr)
        self.postprocessing.file_fieldmap.write(', Max error btw chosen bh curve and real MM: ')  # writes  max error on top of the txt file
        self.postprocessing.file_fieldmap.write(benchmarking_maxErr)
        self.postprocessing.file_fieldmap.write('\n\nCurrent: ')  # writes current in the txt file
        self.postprocessing.file_fieldmap.write(f"{current}")
        self.postprocessing.file_fieldmap.write('A\n\nMesh size in x: ') # writes mesh size in the x direction in the txt file
        self.postprocessing.file_fieldmap.write(f"{meshsize_x}")
        self.postprocessing.file_fieldmap.write(', Mesh size in y: ')  # writes mesh size in the y direction in the txt file
        self.postprocessing.file_fieldmap.write(f"{meshsize_x}")
        self.postprocessing.file_fieldmap.write('\nx_start: ') # writes the x coordinate of the left bottom corner of the rectangle defining the zone of the fieldmap in the txt file
        self.postprocessing.file_fieldmap.write(f"{xstart}")
        self.postprocessing.file_fieldmap.write(', y_start: ') # writes the y coordinate of the left bottom corner of the rectangle defining the zone of the fieldmap in the txt file
        self.postprocessing.file_fieldmap.write(f"{ystart}")
        self.postprocessing.file_fieldmap.write(', x_end: ')  # writes the x coordinate of the right upper corner of the rectangle defining the zone of the fieldmap in the txt file
        self.postprocessing.file_fieldmap.write(f"{xend}")
        self.postprocessing.file_fieldmap.write(', y_end: ') # writes the y coordinate of the right upper corner of the rectangle defining the zone of the fieldmap in the txt file
        self.postprocessing.file_fieldmap.write(f"{yend} \n")
        if fieldmap_units == 'SI_with_mm':
            currentmodel.Set_Units(fieldmap_units)
            self.postprocessing.file_fieldmap.write('\nx[mm], y[mm], Bx[T], By[T], Bmod[T] \n')  # writes on the header the measures and their units
        if fieldmap_units == 'SI_with_mm_G':
            currentmodel.Set_Units(fieldmap_units)
            self.postprocessing.file_fieldmap.write('\nx[mm], y[mm], Bx[G], By[G], Bmod[G] \n')  # writes on the header the measures and their units
        if fieldmap_units == 'SI_with_cm':
            currentmodel.Set_Units(fieldmap_units)
            self.postprocessing.file_fieldmap.write('\nx[cm], y[cm], Bx[T], By[T], Bmod[T] \n')  # writes on the header the measures and their units
        if fieldmap_units == 'SI_with_cm_G':
            currentmodel.Set_Units(fieldmap_units)
            self.postprocessing.file_fieldmap.write('\nx[cm], y[cm], Bx[G], By[G], Bmod[G] \n')  # writes on the header the measures and their units
        self.postprocessing.fieldmap_zone = currentmodel.operaModel.create_rectangle((xstart, ystart), (xend, yend), name='zone for fieldmap', pp_body=True)  # creates the rectangle defining the zone of the fieldmap
        self.postprocessing.fieldmap_region = Region(self.postprocessing.fieldmap_zone)  # defines the region of this rectangle to be able to get the edges
        self.postprocessing.fieldmap_edges = Edges(self.postprocessing.fieldmap_region)  # defines the edges of this rectangle to get the number of points needed in x and y
        self.postprocessing.fieldmap_nb_points_x = int(self.postprocessing.fieldmap_edges.edges[0].length / meshsize_x)  # gets the number of points needed in the x direction
        self.postprocessing.fieldmap_nb_points_y = int(self.postprocessing.fieldmap_edges.edges[1].length / meshsize_y)  # gets the number of points needed in the y direction
        for i in range(0, self.postprocessing.fieldmap_nb_points_y + 1): # loop over all the number of points in y
            for j in range(0, self.postprocessing.fieldmap_nb_points_x + 1):  # loop over all the number of points in x
                self.postprocessing.fieldmap_x = xstart + j * meshsize_x  #sets the x coordinate for this point
                self.postprocessing.fieldmap_y = ystart + i * meshsize_y  #sets the y coordinate for this point
                self.postprocessing.fieldmap_Bx = self.postprocessing.calculate_field_at_point((self.postprocessing.fieldmap_x, self.postprocessing.fieldmap_y),field_expression='Bx').field_expression_result  # gets the value of Bx for this point
                self.postprocessing.fieldmap_By = self.postprocessing.calculate_field_at_point((self.postprocessing.fieldmap_x, self.postprocessing.fieldmap_y),field_expression='By').field_expression_result  # gets the value of By for this point
                self.postprocessing.fieldmap_Bmod = self.postprocessing.calculate_field_at_point((self.postprocessing.fieldmap_x, self.postprocessing.fieldmap_y),field_expression='B').field_expression_result  # gets the value of Bmod for this point
                self.postprocessing.file_fieldmap.write(f"{self.postprocessing.fieldmap_x}, {self.postprocessing.fieldmap_y}, {self.postprocessing.fieldmap_Bx}, {self.postprocessing.fieldmap_By}, {self.postprocessing.fieldmap_Bmod}\n")  # writes the coordinates and the values of Bx, By, Bmod for this point
        self.postprocessing.file_fieldmap.close()  # closes the fieldmap file

    def Create_Fieldmap_BDSIMformat(self, currentmodel, path_of_directory, date, pymagnets_version, pymagnets_version_tuple, author, magnet_name, magnet_length, bhcurvename, benchmarking_avgErr, benchmarking_maxErr, current, meshsize_x, meshsize_y, xstart, ystart, xend, yend):  # creates a fieldmap with the txt format
        path_tempfieldmap = path_of_directory + 'temporary_fieldmap.txt'
        temporary_fieldmap = open(path_tempfieldmap, 'w',encoding='UTF8')# creates and stock a local temporary fieldmap data to solve memory issues
        self.postprocessing.fieldzone = currentmodel.operaModel.create_rectangle((xstart, ystart), (xend, yend), name='zone for field map', pp_body=True)  # creates the zone where to define the fieldmap
        self.postprocessing.fieldzone_region = self.postprocessing.fieldzone.regions  # defines region for the zone for field map
        self.postprocessing.fieldzone_edges = self.postprocessing.fieldzone_region[0].edges  # defines a table with the edges of the zone for field map
        self.postprocessing.fieldmap_nb_points_x = int(self.postprocessing.fieldzone_edges[0].length / (meshsize_x)) # defines the number of points needed in x direction
        self.postprocessing.fieldmap_nb_points_y = int(self.postprocessing.fieldzone_edges[1].length / (meshsize_y)) # defines the number of points needed in y direction
        for xi in range(0, self.postprocessing.fieldmap_nb_points_x + 1): # gets the value of the field for each points in the x and the y direction
            for yi in range(0, self.postprocessing.fieldmap_nb_points_y + 1):
                fieldmap_x = xstart + xi * meshsize_x  # sets the x coordinate for this point
                fieldmap_y = ystart + yi * meshsize_y  # sets the y coordinate for this point
                field_Bx = self.postprocessing.calculate_field_at_point((fieldmap_x, fieldmap_y),field_expression='Bx').field_expression_result  # calculates the value of Bx in this point
                field_By = self.postprocessing.calculate_field_at_point((fieldmap_x, fieldmap_y),field_expression='By').field_expression_result  # calculates the value of By in this point
                temporary_fieldmap.write(f"{fieldmap_x / 10} {fieldmap_y / 10} {field_Bx} {field_By} {0.0}\n")  # writes the coordiantes and values of Bx By in the temporary file
                del field_Bx
                del field_By
                del fieldmap_x
                del fieldmap_y
        temporary_fieldmap.close()
        self.array_from_temporaryfiedmap = _np.genfromtxt(path_tempfieldmap)# generates a numpy array from the temporary fieldmap file
        os.remove(path_tempfieldmap)
        self.reconstructed_array = self.array_from_temporaryfiedmap.reshape((self.postprocessing.fieldmap_nb_points_x + 1, self.postprocessing.fieldmap_nb_points_y + 1, -1)) # reshapes it to the needed format
        self.postprocessing.fieldmapBDSIM = pybdsim.Field.Field2D(self.reconstructed_array, flip=True) # constructs a BDSIM format field object and write it out
        self.postprocessing.fieldmap_title = path_of_directory + magnet_name +'_fieldmapBDSIM_' + str(current) + 'A_pymagnetsV'+ str(pymagnets_version_tuple[0]) + '-' + str(pymagnets_version_tuple[1]) + '-' + str(pymagnets_version_tuple[2]) + '_'+ date +'.dat'  # sets the path where to save the fieldmap
        commentdate = 'Date: ' + date
        self.postprocessing.fieldmapBDSIM.AddComment(commentdate)  # writes date on top
        commentauthor = 'Author: ' + author
        self.postprocessing.fieldmapBDSIM.AddComment(commentauthor)  # writes author on top
        commentversion= 'Version of PyMagnets used: ' + pymagnets_version
        self.postprocessing.fieldmapBDSIM.AddComment(commentversion)  # writes author on top
        commentmagnet = 'Magnet: ' + magnet_name
        self.postprocessing.fieldmapBDSIM.AddComment(commentmagnet)  # writes magnet name on top
        commentlength = 'Length of the magnet: ' + str(magnet_length) + 'mm'
        self.postprocessing.fieldmapBDSIM.AddComment(commentlength)  # writes magnet length on top
        commentbh = 'Name of the BH curve used: ' + bhcurvename
        self.postprocessing.fieldmapBDSIM.AddComment(commentbh)  # writes bh curve name on top
        commentavgerr = 'Benchmarking - Average error btw the chosen bh curve and real MM: ' + benchmarking_avgErr
        self.postprocessing.fieldmapBDSIM.AddComment(commentavgerr) # writes avg error
        commentmaxerr = 'Benchmarking - Max error btw the chosen bh curve and real MM: ' + benchmarking_maxErr
        self.postprocessing.fieldmapBDSIM.AddComment(commentmaxerr) # writes  max error on top
        commentcurrent = 'Current: ' + str(current) + 'A'
        self.postprocessing.fieldmapBDSIM.AddComment(commentcurrent) # writes current
        commentmeshx = 'Mesh in x dir: ' + str(meshsize_x) + 'mm'
        self.postprocessing.fieldmapBDSIM.AddComment(commentmeshx) # writes mesh size in the x direction
        commentmeshy = 'Mesh in y dir: ' + str(meshsize_y) + 'mm'
        self.postprocessing.fieldmapBDSIM.AddComment(commentmeshy) # writes mesh size in the y direction
        self.postprocessing.fieldmapBDSIM.Write(self.postprocessing.fieldmap_title)


class Region():
    def __init__(self, body):  # Creates an opera region for a body and defines it as the '.region' attribute of any object of the Region() class
        self.region = body.regions[0]  # defines region for that body

    def AssignMaterials(self, material_of_body):  #Assigns a material (object from the MaterialLibrary) to the region of the body
        self.region.material = material_of_body.material

    def AssignCurrent(self, current):   # Assigns a current (object from the CurrentLibrary) to the region of the body
        self.region.properties = current


class Edges():
    def __init__(self, region):  # Creates an opera edges list for a region (object from the Region() class) and defines it as the '.edges' attribute of any object of the Edges() class
        self.edges = region.region.edges  # Defines a list with the edges of that region (as defined in the construction of the body that this region defines)

    def AssignMesh(self, i, meshsize, meshbias=0.5):  # Assigns a mesh to the edges of the region of the body  #if not indicated, the default value for the meshbias is 0.5
        self.edges[i].mesh_size = opera2d.ModelValue(meshsize, opera2d.Unit.Length.Millimetre)  #Assigns for this i edge the mesh size that one wants
        self.edges[i].mesh_bias = meshbias  # Assigns for this i edge the mesh bias

    def AssignBoundary(self, i, type_of_boundary):  # Assigns a boundary (object from the BoundaryType() class) to the edges of the region of the body
        self.edges[i].boundary_condition = type_of_boundary.boundary  # Assigns for this i edge the type of boundary condition that one wants


class CurrentLibrary:  # In this class, all the current used are defined
    def __init__(self, model):
        self.current = model.operaModel.create_properties('')  # Creates an opera current and defines it as the '.current' attribute of any object of the CurrentLibrary() class

    def Set_NoCurrent(self):  # Defines the Default/No Current
        self.current.name = 'No Current'  #sets its name

    def Set_CurrentPos(self, current, turns, area_coil):  # Defines the positive current
        self.current.name = 'Current pos'  #sets its name
        self.current.is_laminated = False  #current is not laminated
        self.current.packing_factor = opera2d.ModelValue(1.0, opera2d.Unit.Dimensionless.Unitless)  #sets the packing factor
        self.current.current_density = opera2d.ModelValue(current * turns / area_coil, opera2d.Unit.CurrentDensity.AmperePerMillimetreSquared)  #sets the value of the positive current density (=current*turns/area_coil)

    def Set_CurrentNeg(self, current, turns, area_coil):  # Defines the negative current
        self.current.name = 'Current neg'  #sets its name
        self.current.is_laminated = False  #current is not laminated
        self.current.packing_factor = opera2d.ModelValue(1.0, opera2d.Unit.Dimensionless.Unitless)  #sets the packing factor
        self.current.current_density = opera2d.ModelValue(-1 * current * turns / area_coil, opera2d.Unit.CurrentDensity.AmperePerMillimetreSquared)  #sets the value of the negative current density (=-current*turns/area_coil)


class BoundaryType: # In this class, the 2 types of boundary conditions (Neumann and Dirichlet) are defined
    def __init__(self, currentmodel):
        self.boundary = currentmodel.operaModel.create_boundary_condition('') # Creates an opera boundary condition and defines it as the '.boundary' attribute of any object of the BoundaryType() class

    def Set_Dirichlet(self):  # defines the Dirichlet boundary condition
        self.boundary.name = 'Dirichlet' # sets its name
        self.boundary.set_tangential_field_magnetic()  # sets the magnetic field as tangential, there is no normal flux

    def Set_Neumann(self):  # defines the Neumann boundary condition
        self.boundary.name = 'Neumann' # sets its name
        self.boundary.set_normal_field_magnetic()  # sets the magnetic field as normal to the edge

