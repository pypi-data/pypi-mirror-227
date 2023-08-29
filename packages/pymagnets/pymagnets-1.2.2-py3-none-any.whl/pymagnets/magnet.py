# -*- coding: utf-8 -*-
"""
Created on Fri Apr  28  17:15:24 2023

@title: Magnet

@author: avisive

@content: The PyMagnets package (to be used with the userscript.py) contains the useful functions to create a FE-model of a magnet of the ExpAreas, the functions are divided by classes which are themselves divided in 3 libraries.
Here, the library contains classes that contains everything personal to each magnet.
"""

import math # imports the math library to be able to make calculation and get functions such as pi and sqrt


from . import model as _model # imports the model library from the pymagnets package

from . import  material as _material  # imports the material library from the pymagnets package


class Bodies: # In this class, the bodies (yoke, coil(s), background) for the different magnets are defined
    def __init__(self, currentmodel):  # currentmodel is an object of the class Model()
        self.model = currentmodel.operaModel  #self.model is a model in the Opera sense of the term
        self.yoke = None  # a magnet has a yoke so it will be defined as the attribute '.yoke' of a object of the class Bodies()
        self.coil_1 = None  # a magnet has at least 1 coil so it will be defined as the attribute '.coil_1' of a object of the class Bodies()
        self.coil_2 = None  # a magnet can have a 2nd coil so it will be defined as the attribute '.coil_2' of a object of the class Bodies(), the attribute will be equal to None if there is only one coil
        self.background = None  # a magnet has a background so it will be defined as the attribute '.background' of a object of the class Bodies()
        self.tensionplate_1 = None # a magnet can have tension plates on the exterior border of the yoke so it will be defined as the attribute '.tensionplate_1' as a object of the class Bodies() (it will received the same material as the yoke and no current)
        self.tensionplate_2 = None  # a magnet can have tension plates on the exterior border of the yoke so it will be defined as the attribute '.tensionplate_2', in case a second tension plate needs to be defined, as a object of the class Bodies() (it will received the same material as the yoke and no current)
        # NB : None is a null object in python leaving the magnet the possibility to not have one of the attribute (in case of only 1 coil drawn for ex)


    ### DIPOLES ###
    def Set_Yoke_MCB(self):   # when called, this method draws the yoke of a MCB, see documentation
        self.yoke = self.model.create_polyline([(-742.0, 0.0), (-390.0, 0.0), (-390.0, 225.0)])  # draws [Y0,Y1] = edge0 and [Y1,Y2] = edge1
        self.yoke = self.model.create_polyline_arc((-385.0, 225.0), 5, 90, 90, extend=True)  # draws an arc between Y2 and Y3 = edge2
        self.yoke = self.model.create_polyline([(-385.0, 230.0), (-165.0, 230.0)], extend=True)  # draws [Y3,Y4] = edge3
        self.yoke = self.model.create_polyline_arc((-165.0, 225.0), 5, 90, -90, extend=True)  # draws an arc between Y4 and Y5 = edge4
        self.yoke = self.model.create_polyline([(-160.0, 225.0), (-160.0, 46.80), (-152.19, 38.99), (-122.87, 38.99), (-121.86, 40.0), (121.46, 40.0), (122.14, 38.99), (152.19, 38.99), (160.0, 46.8), (160.0, 148.0), (162.0, 150.0), (162.0, 180.0), (160.0, 182.0), (160.0, 500.0), (162.0, 502.0), (162.0, 578.46), (158.46, 582.0), (82.0, 582.0), (80.0, 580.0), (-662, 580.0), (-664, 582.0), (-740.57, 582.0), (-744.0, 578.46), (-744.0, 502.0), (-742.0, 500.0)], close=True, extend=True, name='Half-yoke')
        # draws [Y5,Y6] = edge5 and [Y6,Y7] = edge6 and [Y7,Y8] = edge7 and [Y8,Y9] = edge8 and [Y9,Y10] = edge9 and [Y10,Y11] = edge10 and [Y11,Y12] = edge11 and [Y12,Y13] = edge12 and [Y13,Y14] = edge13 and [Y14,Y15] = edge14 and [Y15,Y16] = edge15 and [Y16,Y17] = edge16 and [Y17,Y18] = edge17 and [Y18,Y19] = edge18 and [Y19,Y20] = edge19 and [Y20,Y21] = edge20 and [Y21,Y22] = edge21 and [Y22,Y23] = edge22 and [Y23,Y24] = edge23 and [Y24,Y25] = edge24 and [Y25,Y26] = edge25 and [Y26,Y27] = edge26 and [Y27,Y28] = edge27 and [Y28,Y29] = edge28 and [Y29,Y0] = edge29

    def Set_Coil_1_MCB(self):   # when called, this method draws the interieur coil of a MCB (defined as coil 1), see documentation
        self.coil_1 = self.model.create_polyline([(-378.26, 98.54), (-170.34, 98.54), (-170.34, 218.26), (-378.26, 218.26)], close=True, name='Coil  1')
        # draws [IC0,IC1] = edge0 and [IC1,IC2] = edge1 and [IC2,IC3] = edge2 and [IC3,IC0] = edge3

    def Set_Coil_2_MCB(self):   # when called, this method draws the exterieur coil of a MCB (defined as coil 2), see documentation
        self.coil_2 = self.model.create_polyline([(194.34, 98.54), (402.26, 98.54), (402.26, 218.26), (194.34, 218.26)], close=True, name='Coil  2')
        # draws [EC0,EC1] = edge0 and [EC1,EC2] = edge1 and [EC2,EC3] = edge2 and [EC3,EC0] = edge3

    def Set_Background_MCB(self):   # when called, this method draws the background of a MCB, see documentation
        self.background = self.model.create_polyline([(-742.0, 0.0), (-390.0, 0.0), (-170.34, 0.0), (194.34, 0.0), (402.26, 0.0), (744 * 2, 0.0),(744 * 2, 582 * 2), (-744 * 2, 582 * 2), (-744 * 2, 0.0)], close=True, name='background')
        # draws [B0,B1] = edge0 and [B1,B2] = edge1 and [B2,B3] = edge2 and [B3,B4] = edge3 and [B5,B6] = edge5 and [B6,B7] = edge6 and [B7,B8] = edge7 and [B8,B0] = edge8
        self.model.send_to_back(self.background)  # sends the background to the back, for a better visualisation on the GUI

    def Set_Yoke_MBW(self):  # when called, this method draws the yoke of a MBW, see documentation
        self.yoke = self.model.create_polyline([(251.0, 0.0), (412.0, 0.0), (412.0, 192.0)])  # draws [Y0,Y1] = edge0 and [Y1,Y2] = edge1
        self.yoke = self.model.create_polyline_arc((372.0, 192.0), 40, 0, 90, extend=True)  # draws an arc between Y2 and Y3 = edge2
        self.yoke = self.model.create_polyline([(372.0, 232.0), (0.0, 232.0), (0.0, 26.0), (105.424431565498, 26.0)],extend=True)  # draws [Y3,Y4] = edge3 and [Y4,Y5] = edge4 and [Y5,Y6] = edge5
        self.yoke = self.model.create_polyline_arc((105.424431565498, 34), 8, -90, 59.5345, extend=True)  # draws an arc between Y6 and Y7 = edge6
        drawing_edges = self.yoke.edges  # defines a intermediate table with the edges of the yoke
        drawing_point = drawing_edges[6].point_at(1.0) # gets the coordinates of the point Y7 (by getting the point at 100% of the edge 6)
        self.yoke = self.model.create_polyline([drawing_point, (127.680094713240, 56.056161012507)], extend=True)  # draws  [Y7,Y8] = edge7
        self.yoke = self.model.create_polyline_arc((134.575568434502, 52.0), 8, +90, 59.5345, extend=True)  # draws an arc between Y8 and Y9 = edge8
        self.yoke = self.model.create_polyline([(134.575568434502, 60), (138, 60), (138, 73), (251, 73), (251.0, 0.0)],close=True, extend=True, name='Quarter-yoke')
        # draws [Y9,Y10] = edge9 and [Y10,Y11] = edge10 and [Y11,Y12] = edge11 and [Y12,Y0] = edge12

    def Set_Coil_MBW(self):   # when called, this method draws the interior coil of a MBW (only coil in this case), see documentation
        self.coil_1 = self.model.create_polyline([(125.5, 2.5), (247, 2.5), (247, 69), (143, 69), (143, 42), (125.5, 42.0)], close=True, name='Coil')
        # draws [C0,C1] = edge0 and [C1,C2] = edge1 and [C2,C3] = edge2 and [C3,C4] = edge3 and [C4,C5] = edge4 and [C5,C0] = edge4

    def Set_Background_MBW(self):   # when called, this method draws the background of a MBW, see documentation
        self.background = self.model.create_polyline([(251.0, 0.0), (412.0, 0.0), (412.0 * 2, 0), (412.0 * 2, 232.0 * 2), (0.0, 232.0 * 2), (0.0, 232.0),(0.0, 26.0), (0.0, 0.0), (110.0, 0.0)], close=True, name='background')  # split the line of symmmetry into several ones for the meshing
        # draws [B0,B1] = edge0 and [B1,B2] = edge1 and [B2,B3] = edge2 and [B3,B4] = edge3 and [B5,B6] = edge5 and [B6,B7] = edge6 and [B7,B8] = edge7 and [B8,B0]=edge8
        self.model.send_to_back(self.background)  # sends the background to the back, for a better visualisation on the GUI of Opera

    ### QUADRUPOLES ###
    def Set_Yoke_QSL(self):  # when called, this method draws the yoke of a QSL, see documentation
        # gets the span angle, the start angle and the radius for the edge0
        span_ang0 = 180 / math.pi * math.asin((math.sqrt((22.6244 - 17.0) ** 2 + (55.8557 - 65.75) ** 2) / 2) / 30) * 2
        radius0 = math.sqrt((-5.795 - 17) ** 2 + (46.2465 - 65.75) ** 2)
        start_ang0 = 180 / math.pi * math.asin((math.sqrt(((-5.795 + radius0) - 17.0) ** 2 + (46.2465 - 65.75) ** 2) / 2) / 30) * 2
        ## actual drawing:
        self.yoke = self.model.create_polyline_arc((-5.795, 46.2465), radius0, start_ang0, -span_ang0,extend=True, name='Quarter-yoke')  # draws an arc between Y0 and Y1 = edge0
        # gets the start point (thanks to an intermediate table of the edges of the yoke), the span angle, the start angle and the radius for the edge1
        drawing_edges1 = self.yoke.edges  # defines a intermediate table with the edges of the yoke
        drawing_point1 = drawing_edges1[0].point_at(1.0)  # gets the coordinates of the point Y1 (by getting the point at 100% of the edge 0)
        span_ang1 = 180 / math.pi * math.asin((math.sqrt((drawing_point1[0] - 55.8557) ** 2 + (drawing_point1[1] - 22.6244) ** 2) / 2) / 53) * 2
        radius1 = math.sqrt((drawing_point1[0] - 72.832) ** 2 + (drawing_point1[1] - 72.832) ** 2)
        start_ang1 = -180 - 180 / math.pi * math.asin(-(math.sqrt((drawing_point1[0] - (72.832 - radius1)) ** 2 + (drawing_point1[1] - 72.832) ** 2) / 2) / 53) * 2
        ## actual drawing:
        self.yoke = self.model.create_polyline_arc((72.832, 72.832), radius1, start_ang1, span_ang1,extend=True)  # draws an arc between Y1 and Y2 = edge1
        # gets the start point (thanks to an intermediate table of the edges of the yoke), the span angle, the start angle and the radius for the edge2
        drawing_edges2 = self.yoke.edges  # defines a intermediate table with the edges of the yoke
        drawing_point2 = drawing_edges2[1].point_at(1.0)  # gets the coordinates of the point Y11 (by getting the point at 100% of the edge 10)
        span_ang2 = 180 / math.pi * math.asin((math.sqrt((drawing_point2[0] - 65.75) ** 2 + (drawing_point2[1] - 17.0) ** 2) / 2) / 30) * 2
        radius2 = math.sqrt((drawing_point2[0] - 46.2465) ** 2 + (drawing_point2[1] + 5.795) ** 2)
        start_ang2 =  90 - 180 / math.pi * math.asin((math.sqrt((46.2465 - drawing_point2[0]) ** 2 + ((-5.795 + radius2) - drawing_point2[1]) ** 2) / 2) / 30) * 2
        ## actual drawing:
        self.yoke = self.model.create_polyline_arc((46.2465, -5.795), radius2, start_ang2, -span_ang2, extend=True)  # draws an arc between Y2 and Y3 = edge2
        # gets the start point (thanks to an intermediate table of the edges of the yoke) for the edge3
        drawing_edges3 = self.yoke.edges  # defines a intermediate table with the edges of the yoke
        drawing_point3 = drawing_edges3[2].point_at(1.0)  # gets the coordinates of the point Y3 (by getting the point at 100% of the edge 2)
        ## actual drawing:
        self.yoke = self.model.create_polyline([drawing_point3, (70.033, 17.0), (112.2756, 59.2426)], extend=True)  # draws [Y3,Y4]=edge3 and [Y4,Y5] = edge4
        # gets the span angle and the radius for the edge5
        span_ang5 = 180 / math.pi * math.asin((math.sqrt((112.2756 - 116.5183) ** 2 + (59.2426 - 61.0) ** 2) / 2) / 6) * 2
        radius5 = math.sqrt((112.2756 - 116.5183) ** 2 + (59.2426 - 55.0) ** 2)
        ## actual drawing:
        self.yoke = self.model.create_polyline_arc((116.5183, 55.0), radius5, 90, span_ang5, extend=True)  # draws an arc between Y5 and Y6 = edge5
        # gets the start point (thanks to an intermediate table of the edges of the yoke) for the edge6
        drawing_edges6 = self.yoke.edges  # defines a intermediate table with the edges of the yoke
        drawing_point6 = drawing_edges6[5].point_at(1.0)  # gets the coordinates of the point Y6 (by getting the point at 100% of the edge5
        ## actual drawing:
        self.yoke = self.model.create_polyline([drawing_point6, (139.0, 61.0)], extend=True)  # draws [Y6,Y7] = edge6
        self.yoke = self.model.create_polyline_arc((139.0, 58.0), 3, 90, -90, extend=True)  # draws an arc between Y7 and Y8 = edge7
        # gets the start point (thanks to an intermediate table of the edges of the yoke) for the edge9
        drawing_edges8 = self.yoke.edges  # defines a intermediate table with the edges of the yoke
        drawing_point8 = drawing_edges8[7].point_at(1.0)  # gets the coordinates of the point Y9 (by getting the point at 100% of the edge8
        ## actual drawing:
        self.yoke = self.model.create_polyline([drawing_point8, (142.0, 0.0), (160.0, 0.0), (160.0, 260.0), (0.0, 260.0), (0.0, 142.0), (58.0, 142.0)], extend=True)  #  draws [Y8,Y9] = edge8 and draw [Y9,Y10]=edge9 [Y10,Y11] = edge10 and [Y11,Y12] = edge11 and [Y12,Y13] and [Y13,Y14] = edge13
        self.yoke = self.model.create_polyline_arc((58.0, 139.0), 3, 90, -90, extend=True)  # draws an arc between Y14 and Y15 = edge14
        self.yoke = self.model.create_polyline([(61.0, 139.0), (61.0, 116.5183)], extend=True)  # draws [Y15,Y16] = edge15
        self.yoke = self.model.create_polyline_arc((55.0, 116.5183), 6, 0, -45, extend=True)  # draws an arc between Y16 and Y17 = edge16
        # gets the start point (thanks to an intermediate table of the edges of the yoke) for the edge18
        drawing_edges17 = self.yoke.edges  # defines an intermediate table with the edges of the yoke
        drawing_point17 = drawing_edges17[16].point_at(1.0)  # gets the coordinates of the point Y18 (by getting the point at 100% of the edge 17)
        ## actual drawing:
        self.yoke = self.model.create_polyline([drawing_point17, (17.0, 70.033)], extend=True, close=True)  # draw [Y17,Y18]=edge17 and [Y18,Y0] = edge18

    def Set_Coil_1_QSL(self):  # when called, this method draws the lower coil of a QSL (here named as coil 1), see documentation
        self.coil_1 = self.model.create_polyline([(73.0, 3.0), (138.0, 3.0), (138.0, 57.0), (117.0, 57.0), (117.0, 46.0), (106.0, 46.0), (106.0, 35.0), (95.0, 35.0), (95.0, 24.0), (84.0, 24.0), (84.0, 13.0), (73.0, 13.0)], close=True, name='Lower Coil')
        # draws [LC0,LC1] = edge0 and [LC1,LC2] = edge1 and [LC2,LC3] = edge2 and [LC3,LC4] = edge3 and [LC4,LC5] = edge4 and [LC5,LC6] = edge5 and [LC6,LC7] = edge6 and [LC7,LC8] = edge7 and [LC8,LC9] = edge8 and [LC9,LC10] = edge9 and [LC10,LC11] = edge10 and [LC11,LC0] = edge11

    def Set_Coil_2_QSL(self):  # when called, this method draws the upper coil of a QSL (here named as coil 2), see documentation
        self.coil_2 = self.model.create_polyline([(3.0, 73.0), (3.0, 138.0), (57.0, 138.0), (57.0, 117.0), (46.0, 117.0), (46.0, 106.0), (35.0, 106.0), (35.0, 95.0), (24.0, 95.0), (24.0, 84.0), (13.0, 84.0), (13.0, 73.0)], close=True, name='Upper Coil')
        # draws [UC0,UC1] = edge0 and [UC1,UC2] = edge1 and [UC2,UC3] = edge2 and [UC3,UC4] = edge3 and [UC4,UC5] = edge4 and [UC5,UC6] = edge5 and [UC6,UC7] = edge6 and [UC7,UC8] = edge7 and [UC8,UC9] = edge8 and [UC9,UC10] = edge9 and [UC10,UC11] = edge10 and [UC11,UC0] = edge11

    def Set_Background_QSL(self):  # when called, this method draws the background of a QSL, see documentation
        self.background = self.model.create_polyline([(0.0, 0.0), (73.0, 0.0), (138, 0.0), (160.0, 0.0), (160.0 * 2, 0.0 * 2), (160.0 * 2, 260.0 * 2), (0.0, 260.0*2), (0.0, 260.0), (0.0,138.0), (0.0, 73.0)],  close=True, name='background')  # split the line of symmmetry into several ones for the meshing
        # draws [B0,B1] = edge0 and [B1,B2] = edge1 and [B2,B3] = edge2 and [B3,B4] = edge3 and [B5,B6] = edge5 and [B6,B7] = edge6 and [B7,B8] = edge7 and [B8,B9] = edge8 and [B10,B11] = edge10 and [B11,B10] = edge11
        self.model.send_to_back(self.background)  # sends the background to the back, for a better visualisation on the GUI

    def Set_Yoke_QNL(self):  # when called, this method draws the yoke of a QNL, see documentation
        # calculations of the points of the half-hyperbole, approximation by segment of 1mm (smaller than the mesh)
        list_hyperboleA = [] # creates a list where all the points of the first half hyperbole are stored
        list_hyperboleB = [] # creates a list where all the points of the first half hyperbole are stored
        xA = 14.55 # point A is Y0
        yA = 55
        xmid = 28.28 # the point in the middle of the hyperbole is given by the drawings, point Mid is Y1
        ymid = 28.28 # point B is Y2
        xB = 55
        yB = 14.55
        nbpoints = 55 - 28.28 # number of points one needs to get according to the resolution of the approximation
        for i in range (1, int(nbpoints)+2): # loop to calculate those points (there is 26 POINTS)
            list_hyperboleA.append((800/(yA-i), yA-i)) # adds points to the list according to the equation of the hyperbole (xy=800) (points for 54>=Y>=29)
            list_hyperboleB.append((yA-i,800/(yA-i))) # adds points to the list according to the equation of the hyperbole (xy=800) (points for 29<=X<=54)
        ## actual drawing:
        self.yoke = self.model.create_polyline([(xA,yA),list_hyperboleA[0],list_hyperboleA[1],list_hyperboleA[2],list_hyperboleA[3],list_hyperboleA[4],list_hyperboleA[5],list_hyperboleA[6], list_hyperboleA[7],list_hyperboleA[8], list_hyperboleA[9], list_hyperboleA[10],list_hyperboleA[11],list_hyperboleA[12], list_hyperboleA[13], list_hyperboleA[14],list_hyperboleA[15],list_hyperboleA[16], list_hyperboleA[17],list_hyperboleA[18], list_hyperboleA[19],list_hyperboleA[20],list_hyperboleA[21],list_hyperboleA[22], list_hyperboleA[23], list_hyperboleA[24],list_hyperboleA[25], (xmid,ymid)])
        # draws [Y0,Y1]=edge0
        self.yoke = self.model.create_polyline([(xmid,ymid),list_hyperboleB[25],list_hyperboleB[24],list_hyperboleB[23],list_hyperboleB[22],list_hyperboleB[21],list_hyperboleB[20],list_hyperboleB[19], list_hyperboleB[18],list_hyperboleB[17], list_hyperboleB[16], list_hyperboleB[15],list_hyperboleB[14],list_hyperboleB[13], list_hyperboleB[12], list_hyperboleB[11],list_hyperboleB[10],list_hyperboleB[9], list_hyperboleB[8],list_hyperboleB[7], list_hyperboleB[6],list_hyperboleB[5],list_hyperboleB[4],list_hyperboleB[3], list_hyperboleB[2], list_hyperboleB[1],list_hyperboleB[0], (xB,yB)], extend = True)
        # draws [Y1,Y2]=edge1
        self.yoke = self.model.create_polyline([(xB,yB), (65,11.9), (71.8,11.9), (219,85.5), (247,85.5), (247,0), (279,0), (279,35), (278,36), (278,329), (279,330), (279,397.46), (275.46,401), (225,401), (224,400), (36,400), (35,401), (0,401), (0,247), (85.5,247), (85.5,219), (11.9,71.8), (11.9,65)], close=True, extend=True, name='Quarter-yoke')
        # draws [Y2,Y3] = edge2 and [Y3,Y4] = edge3 and [Y4,Y5] = edge4 and [Y5,Y6] = edge5 and [Y6,Y7] = edge6 and [Y7,Y8] = edge7 and [Y8,Y9] = edge8 and [Y9,Y10] = edge9 and [Y10,Y11] = edge10 and [Y11,Y12] = edge11 and [Y12,Y13] = edge12 and [Y13,Y14] = edge13 and [Y14,Y15] = edge14 and [Y15,Y16] = edge15 and [Y16,Y0] = edge16

    def Set_Coil_1_QNL(self):  # when called, this method draws the horizontal coil of a QNL (here named as coil 1), see documentation
        self.coil_1 = self.model.create_polyline([(91.65,5.65), (91.65,16.85), (116.65,16.85), (116.65, 29.35), (141.65, 29.35), (141.65, 41.85), (166.65, 41.85), (166.65, 54.35), (191.65, 54.35), (191.65, 66.85), (216.65, 66.85), (216.65, 79.35),(240.35,79.35),(240.35,5.65)], close=True, name='Lower Coil')
        # draws [LC0,LC1] = edge0 and [LC1,LC2] = edge1 and [LC2,LC3] = edge2 and [LC3,LC4] = edge3 and [LC4,LC5] = edge4 and [LC5,LC6] = edge5 and [LC6,LC7] = edge6 and [LC7,LC8] = edge7 and [LC8,LC9] = edge8 and [LC9,LC10] = edge9 and [LC10,LC11] = edge10 and [LC11,LC12] = edge11 and [LC12,LC13] = edge12 and [LC13,LC0] = edge13

    def Set_Coil_2_QNL(self):  # when called, this method draws the vertical coil of a QNL (here named as coil 2), see documentation
        self.coil_2 = self.model.create_polyline([(5.65,91.65), (16.85,91.65), (16.85,116.65), (29.35,116.65), (29.35,141.65,), (41.85,141.65), (41.85,166.65), (54.35,166.65), (54.35,191.65), (66.85,191.65), (66.85,216.65), (79.35,216.65),(79.35,240.35),(5.65,240.35)], close=True, name='Upper Coil')
        # draws [UC0,UC1] = edge0 and [UC1,UC2] = edge1 and [UC2,UC3] = edge2 and [UC3,UC4] = edge3 and [UC4,UC5] = edge4 and [UC5,UC6] = edge5 and [UC6,UC7] = edge6 and [UC7,UC8] = edge7 and [UC8,UC9] = edge8 and [UC9,UC10] = edge9 and [UC10,UC11] = edge10 and [UC11,UC0] = edge11 and [UC12,UC13] = edge12 and [UC13,UC0] = edge13

    def Set_TensionPlate_1_QNL(self):  # when called, this method draw the vertical tension plate of a QNL (here named as tension plate 1), see documentation
        self.tensionplate_1 = self.model.create_polyline([(289,0), (299,0),(299,50),(289,50),(289,350),(279,350),(279,25),(289,25)], close=True, name='Tension Plate Long')
        # draws [TPL0,TPL1] = edge0 and [TPL1,TPL2] = edge1 and [TPL2,TPL3] = edge2 and [TPL3,TPL4] = edge3 and [TPL4,TPL5] = edge4 and [TPL5,TPL6] = edge5 and [TPL6,TPL7] = edge6 and [TPL7,TPL0] = edge7

    def Set_TensionPlate_2_QNL(self):   # when called, this method draws the horizontal tension plate of a QNL (here named as tension plate 2), see documentation
        self.tensionplate_2 = self.model.create_polyline([(0,411),(25,411),(25,401),(245,401),(245,411),(50,411), (50,421),(0,421)], close=True, name='Tension Plate Short')
        # draws [TPS0,TPS1] = edge0 and [TPS1,TPS2] = edge1 and [TPS2,TPS3] = edge2 and [TPS3,TPS4] = edge3 and [TPS4,TPS5] = edge4 and [TPS5,TPS6] = edge5 and [TPS6,TPS7] = edge6 and [TPS7,TPS0] = edge7

    def Set_Background_QNL(self):  #  when called, this method draws the background of a QNL
        self.background = self.model.create_polyline([(0.0, 0.0), (91.65,0), (240.35,0), (247,0), (279,0), (279.0 * 2, 0.0 * 2), (279.0 * 2, 401.0 * 2), (0.0, 401.0*2), (0,401), (0,247), (0,240.35), (0,91.65)],  close=True, name='background')  # split the line of symmmetry into several ones for the meshing
        # draws [B0,B1] = edge0 and [B1,B2] = edge1 and [B2,B3] = edge2 and [B3,B4] = edge3 and [B5,B6] = edge5 and [B6,B7] = edge6 and [B7,B8] = edge7 and [B8,B9] = edge8 and [B10,B11] = edge10 and [B11,B10] = edge11
        self.model.send_to_back(self.background)  # sends the background to the back, for a better visualisation on the GUI



class Magnet:  # In this class, the different magnets are actually build, defined : their bodies are given the right properties
    def __init__(self, currentmodel, globalmesh, meshfactor_yoke, meshfactor_coil, meshfactor_background, current, turns, area_coil, bhpath):
        self.model = currentmodel # currentmodel is an object of the class Model(), it is the model on which the magnet will be drawn and constructed
        self.globalmesh = globalmesh  # global mesh becomes a property of that magnet (o change th global density of the mesh)
        self.meshfactor_yoke = meshfactor_yoke  # the mesh factor of the yoke becomes a property of that magnet (one can use to make less/more dense the mesh in the yoke only)
        self.meshfactor_coil = meshfactor_coil  # the mesh factor of the coil(s) becomes a property of that magnet (one can use to make less/more dense the mesh in the coil(s) only)
        self.meshfactor_background = meshfactor_background  # the mesh factor of the background becomes a property of that magnet (one can use to make less/more dense the mesh in the background only)
        self.current = current  # the current of the coil (in Ampère) becomes a property of that magnet
        self.turns = turns  # the number of turns of its coil(s) becomes a property of that magnet (needed for the current density)
        self.area_coil = area_coil  # the area of its coil(s) becomes a property of that magnet (needed for the current density)
        self.bhpath = bhpath # the path to the git folder containing all the bh curves

    #########     MCB     #########
    def Set_MCB(self, yoke_bhcurve_path = None):  # this magnet object will be a MCB
        mcb = Bodies(self.model)  # creates for this current model, a mcb object from the class Bodies() that will be able to have yoke/background/coil_1/coil_2 attribute
        # Sets yoke, gives material, current & mesh
        mcb.Set_Yoke_MCB() # this mcb object yoke attribute is set as the yoke of the MCB
        self.yoke = mcb.yoke  # this magnet object from the class Magnet() is receiving a yoke attribute the value of the 'mcb.yoke'
        self.yoke_region = _model.Region(self.yoke)  # the region of the yoke is defined
        materialyoke = _material.MaterialLibrary(self.model)  # creates for this current model a material object 'materialyoke'
        #bhyoke = _material.BHcurveLibrary(self.model)  # creates for this current model a bh curve object 'bhyoke'
        bhyoke = _material.BHcurveLibrary(self.model,self.bhpath)  # creates for this current model a bh curve object 'bhyoke'
        if (yoke_bhcurve_path != None): # yoke_bhcurve_path is the path of the bh curve that one wants to defined for the new material that one is defining
            bhyoke.Set_OtherBHcurve(yoke_bhcurve_path)  # sets this 'bhyoke' object as the bh curve defined by the user (for which they gave the path to)
        else:
            bhyoke.Set_Default()  # sets this 'bhyoke' object as the default bh curve from Opera (best bh according to the comparison file)
        materialyoke.Set_Steel(bhyoke)  # sets this 'materialyoke' as a steel with the bh curve defined above
        self.yoke_region.AssignMaterials(materialyoke)  # gives the yoke region the steel defined above
        nocurrent = _model.CurrentLibrary(self.model)  # creates for this current model a current object 'nocurrent'
        nocurrent.Set_NoCurrent()  # sets this 'nocurrent' object as the absence of current (also used for the background)
        self.yoke_region.AssignCurrent(nocurrent.current)   # gives the no current property to the yoke region
        self.yoke_edges = _model.Edges(self.yoke_region)  # defines the edges of this yoke region
        self.yoke_edges.AssignMesh(0, 6 * self.globalmesh * self.meshfactor_yoke)  # attributes the mesh edge by edge
        self.yoke_edges.AssignMesh(1, 4 * self.globalmesh * self.meshfactor_yoke, 0.1)
        self.yoke_edges.AssignMesh(2, 4 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(3, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(4, 4 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(5, 4 * self.globalmesh * self.meshfactor_yoke, 0.9)
        self.yoke_edges.AssignMesh(6, 3 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(7, 3 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(8, 2 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(9, 3 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(10, 2 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(11, 3 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(12, 3 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(13, 4 * self.globalmesh * self.meshfactor_yoke, 0.1)
        self.yoke_edges.AssignMesh(14, 3 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(15, 4 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(16, 3 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(17, 5 * self.globalmesh * self.meshfactor_yoke, 0.1)
        self.yoke_edges.AssignMesh(18, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(19, 6 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(20, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(21, 6 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(22, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(23, 6 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(24, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(25, 6 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(26, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(27, 6 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(28, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(29, 5 * self.globalmesh * self.meshfactor_yoke, 0.9)
        # Sets coil 1, gives material, current & mesh
        mcb.Set_Coil_1_MCB() # this mcb object coil 1 attribute is set as the interieur coil of the MCB
        self.coil_1 = mcb.coil_1 # this magnet object from the class Magnet() is receiving a coil 1 attribute the value of the 'mcb.coil 1'
        self.coil_1_region = _model.Region(self.coil_1)  # the region of the coil_1 is defined
        materialcoil = _material.MaterialLibrary(self.model)  # creates for this current model a material object 'materialcoil'
        materialcoil.Set_Copper()  # sets this 'materialcoil' as copper
        self.coil_1_region.AssignMaterials(materialcoil)  # gives the coil_1 region the copper defined above
        currentcoil_1 = _model.CurrentLibrary(self.model)  # creates for this current model a current object 'currentcoil_1'
        currentcoil_1.Set_CurrentNeg(self.current, self.turns, self.area_coil)  # sets this 'currentcoil_1' object as self.current * self.turns / self.area_coil
        self.coil_1_region.AssignCurrent(currentcoil_1.current)   # gives this current property to the coil_1 region
        self.coil_1_edges = _model.Edges(self.coil_1_region)  # defines the edges of this coil_1 region
        self.coil_1_edges.AssignMesh(0, 3 * self.globalmesh * self.meshfactor_coil)  # attributes the mesh edge by edge
        self.coil_1_edges.AssignMesh(1, 4 * self.globalmesh * self.meshfactor_coil, 0.1)
        self.coil_1_edges.AssignMesh(2, 5 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(3, 4 * self.globalmesh * self.meshfactor_coil, 0.9)
        # Sets coil 2, gives material, current & mesh
        mcb.Set_Coil_2_MCB()  # this mcb object coil 2 attribute is set as the interior coil of the MCB
        self.coil_2 = mcb.coil_2   # this magnet object from the class Magnet() is receiving a coil 2 attribute the value of the 'mcb.coil 2'
        self.coil_2_region = _model.Region(self.coil_2)    # the region of the coil_2 is defined
        self.coil_2_region.AssignMaterials(materialcoil)  # gives the coil_2 region the copper defined above
        currentcoil_2 = _model.CurrentLibrary(self.model)  # creates for this current model a current object 'currentcoil_2'
        currentcoil_2.Set_CurrentPos(self.current, self.turns, self.area_coil)  # sets this 'currentcoil_2' object as self.current * self.turns / self.area_coil
        self.coil_2_region.AssignCurrent(currentcoil_2.current)   # gives this current property to the coil_2 region
        self.coil_2_edges = _model.Edges(self.coil_2_region)  # defines the edges of this coil_2 region
        self.coil_2_edges.AssignMesh(0, 3 * self.globalmesh * self.meshfactor_coil)  # attributes the mesh edge by edge
        self.coil_2_edges.AssignMesh(1, 4 * self.globalmesh * self.meshfactor_coil, 0.1)
        self.coil_2_edges.AssignMesh(2, 5 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(3, 4 * self.globalmesh * self.meshfactor_coil, 0.9)
        # Sets background, gives material, current & mesh
        mcb.Set_Background_MCB()  # this mcb object background attribute is set as the background of the MCB
        self.background = mcb.background  # this magnet object from the class Magnet() is receiving  abackground attribute the value of the 'mcb.background'
        self.background_region = _model.Region(self.background)  # the region of the background is defined
        materialbackground = _material.MaterialLibrary(self.model)  # creates for this current model a material object 'materialbackground'
        materialbackground.Set_Air()  # sets this 'materialbackground' as air
        self.background_region.AssignMaterials(materialbackground)  # gives thebackground region the 'air' material defined above
        self.background_region.AssignCurrent(nocurrent.current)   # gives the no current property to the background region
        self.background_edges = _model.Edges(self.background_region)  # defines the edges of this background region
        boundary_neumann = _model.BoundaryType(self.model)  # creates for this current model a boundary object 'boundary_neumann'
        boundary_neumann.Set_Neumann() # sets this 'boundary_neumann' as  a Neumann boundary condition
        boundary_dirichlet = _model.BoundaryType(self.model)  # creates for this current model a boundary object 'boundary_dirichlet'
        boundary_dirichlet.Set_Dirichlet() # sets this 'boundary_dirichlet' as  a Dirichlet boundary condition
        self.background_edges.AssignBoundary(0, boundary_neumann)  # attributes the Neumann boundary condition
        self.background_edges.AssignBoundary(1, boundary_neumann)
        self.background_edges.AssignBoundary(2, boundary_neumann)
        self.background_edges.AssignBoundary(3, boundary_neumann)
        self.background_edges.AssignBoundary(4, boundary_neumann)
        self.background_edges.AssignBoundary(5, boundary_dirichlet)  # attributes the Dirichlet boundary condition
        self.background_edges.AssignBoundary(6, boundary_dirichlet)
        self.background_edges.AssignBoundary(7, boundary_dirichlet)
        self.background_edges.AssignBoundary(8, boundary_neumann)   # attributes the Neumann boundary condition
        self.background_edges.AssignMesh(1, 5 * self.globalmesh * self.meshfactor_background)  # attributes the mesh edge by edge
        self.background_edges.AssignMesh(2, 3 * self.globalmesh * self.meshfactor_background)
        self.background_edges.AssignMesh(3, 5 * self.globalmesh * self.meshfactor_background)
        self.background_edges.AssignMesh(4, 15 * self.globalmesh * self.meshfactor_background, 0.1)
        self.background_edges.AssignMesh(5, 40 * self.globalmesh * self.meshfactor_background)
        self.background_edges.AssignMesh(6, 40 * self.globalmesh * self.meshfactor_background)
        self.background_edges.AssignMesh(7, 40 * self.globalmesh * self.meshfactor_background)
        self.background_edges.AssignMesh(8, 15 * self.globalmesh * self.meshfactor_background, 0.9)


    #########     MBW     #########
    def Set_MBW(self, yoke_bhcurve_path = None):   # this magnet object will be a MBW
        mbw = Bodies(self.model)  # create for this current model, a mbw object from the class Bodies() that will be able to have yoke/background/coil_1 attribute
        # Sets yoke, gives material, current & mesh
        mbw.Set_Yoke_MBW()  # this mbw object yoke attribute is set as the yoke of the MBW
        self.yoke = mbw.yoke    # this magnet object from the class Magnet() is receiving a yoke attribute the value of the 'mbw.yoke'
        self.yoke_region = _model.Region(self.yoke)  # the region of the yoke is defined
        materialyoke = _material.MaterialLibrary(self.model)  # creates for this current model a material object 'materialyoke'
        bhyoke = _material.BHcurveLibrary(self.model,self.bhpath)  # creates for this current model a bh curve object 'bhyoke'
        if (yoke_bhcurve_path != None): # yoke_bhcurve_path is the path of the bh curve that one wants to defined for the new material that one is defining
                bhyoke.Set_OtherBHcurve(yoke_bhcurve_path)  # sets this 'bhyoke' object as the bh curve defined by the user (for which they gave the path to)
        else:
            bhyoke.Set_Mildhigh()  # sets this 'bhyoke' object as the default bh curve from Opera (best bh according to the comparison file)
        materialyoke.Set_Steel(bhyoke)  # sets this 'materialyoke' as a steel with one the bh curve defined above
        self.yoke_region.AssignMaterials(materialyoke)  # gives the yoke region the steel defined above
        nocurrent = _model.CurrentLibrary(self.model)  # creates for this current model a current object 'nocurrent'
        nocurrent.Set_NoCurrent()  # sets this 'nocurrent' object as the absence of current (also used for the background)
        self.yoke_region.AssignCurrent(nocurrent.current)   # gives the no current property to the yoke region
        self.yoke_edges = _model.Edges(self.yoke_region)  # defines the edges of this yoke region
        self.yoke_edges.AssignMesh(0, 6 * self.globalmesh * self.meshfactor_yoke)  # attributes the mesh edge by edge
        self.yoke_edges.AssignMesh(1, 6 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(2, 6 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(3, 6 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(4, 6 * self.globalmesh * self.meshfactor_yoke, 0.9)
        self.yoke_edges.AssignMesh(5, 3 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(6, 4 * self.globalmesh * self.meshfactor_yoke, 0.1)
        self.yoke_edges.AssignMesh(7, 4 * self.globalmesh * self.meshfactor_yoke, 0.1)
        self.yoke_edges.AssignMesh(8, 4 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(9, 4 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(10, 4 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(11, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(12, 5 * self.globalmesh * self.meshfactor_yoke, 0.9)
        # Sets coil, gives material, current & mesh
        mbw.Set_Coil_MBW()  # this mbw object coil  attribute is set as the interieur coil of the MBW
        self.coil = mbw.coil_1 # this magnet object from the class Magnet() is receiving a coil attribute the value of the 'mbw.coil_1'
        self.coil_region = _model.Region(self.coil)  # the region of the coil is defined
        materialcoil = _material.MaterialLibrary(self.model)  # creates for this current model a material object 'materialcoil'
        materialcoil.Set_Copper()  # sets this 'materialcoil' as copper
        self.coil_region.AssignMaterials(materialcoil)  # gives the coil_1 region the copper defined above
        currentcoil = _model.CurrentLibrary(self.model)  # creates for this current model a current object 'currentcoil'
        currentcoil.Set_CurrentPos(self.current, self.turns, self.area_coil)  # sets this 'currentcoil' object as self.current * self.turns / self.area_coil
        self.coil_region.AssignCurrent(currentcoil.current)   # gives this current property to the coil region
        self.coil_edges = _model.Edges(self.coil_region)  # defines the edges of this coil region
        self.coil_edges.AssignMesh(0, 3 * self.globalmesh * self.meshfactor_coil)  # attributes the mesh edge by edge
        self.coil_edges.AssignMesh(1, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_edges.AssignMesh(2, 5 * self.globalmesh * self.meshfactor_coil)
        self.coil_edges.AssignMesh(3, 4 * self.globalmesh * self.meshfactor_coil, 0.9)
        self.coil_edges.AssignMesh(4, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_edges.AssignMesh(5, 3 * self.globalmesh * self.meshfactor_coil)
        # Sets background, gives material, current & mesh
        mbw.Set_Background_MBW()  # this mbw object background attribute is set as the background of the MBW
        self.background = mbw.background  # this magnet object from the class Magnet() is receiving  abackground attribute the value of the 'mbw.background'
        self.background_region = _model.Region(self.background)  # the region of the background is defined
        materialbackground = _material.MaterialLibrary(self.model)  # creates for this current model a material object 'materialbackground'
        materialbackground.Set_Air()  # sets this 'materialbackground' as air
        self.background_region.AssignMaterials(materialbackground)  # gives the background region the 'air' material defined above
        self.background_region.AssignCurrent(nocurrent.current)  # gives the no current property to the background region
        self.background_edges = _model.Edges(self.background_region)  # defines the edges of this background region
        boundary_neumann = _model.BoundaryType(self.model)  # creates for this current model a boundary object 'boundary_neumann'
        boundary_neumann.Set_Neumann()  # sets this 'boundary_neumann' as  a Neumann boundary condition
        boundary_dirichlet = _model.BoundaryType(self.model)  # creates for this current model a boundary object 'boundary_dirichlet'
        boundary_dirichlet.Set_Dirichlet()  # sets this 'boundary_dirichlet' as  a Dirichlet boundary condition
        self.background_edges.AssignBoundary(0, boundary_neumann)   # attributes the Neumann boundary condition
        self.background_edges.AssignBoundary(1, boundary_neumann)
        self.background_edges.AssignBoundary(2, boundary_dirichlet)  # attributes the Dirichlet boundary condition
        self.background_edges.AssignBoundary(3, boundary_dirichlet)
        self.background_edges.AssignBoundary(4, boundary_dirichlet)
        self.background_edges.AssignBoundary(5, boundary_dirichlet)
        self.background_edges.AssignBoundary(6, boundary_dirichlet)
        self.background_edges.AssignBoundary(7, boundary_neumann)   # attributes the Neumann boundary condition
        self.background_edges.AssignBoundary(8, boundary_neumann)
        self.background_edges.AssignMesh(1, 15 * self.globalmesh * self.meshfactor_yoke, 0.1)  # attributes the mesh edge by edge
        self.background_edges.AssignMesh(2, 40 * self.globalmesh * self.meshfactor_yoke)
        self.background_edges.AssignMesh(3, 40 * self.globalmesh * self.meshfactor_yoke)
        self.background_edges.AssignMesh(4, 15 * self.globalmesh * self.meshfactor_yoke, 0.9)
        self.background_edges.AssignMesh(6, 3 * self.globalmesh * self.meshfactor_yoke)
        self.background_edges.AssignMesh(7, 3 * self.globalmesh * self.meshfactor_yoke)
        self.background_edges.AssignMesh(8, 4 * self.globalmesh * self.meshfactor_yoke)


    #########     QSL     #########
    def Set_QSL(self, yoke_bhcurve_path = None):  # this magnet object will be a QSL
        qsl = Bodies(self.model)  # creates for this current model, a qsl object from the class Bodies() that will be able to have yoke/background/coil_1/coil_2 attribute
        # Sets yoke, gives material, current & mesh
        qsl.Set_Yoke_QSL() # this qsl object yoke attribute is set as the yoke of the QSL
        self.yoke = qsl.yoke  # this magnet object from the class Magnet() is receiving a yoke attribute the value of the 'qsl.yoke'
        self.yoke_region = _model.Region(self.yoke)  # the region of the yoke is defined
        materialyoke = _material.MaterialLibrary(self.model)  # creates for this current model a material object 'materialyoke'
        bhyoke = _material.BHcurveLibrary(self.model,self.bhpath)  # creates for this current model a bh curve object 'bhyoke'
        if (yoke_bhcurve_path != None): # yoke_bhcurve_path is the path of the bh curve that one wants to defined for the new material that one is defining
                bhyoke.Set_OtherBHcurve(yoke_bhcurve_path)  # sets this 'bhyoke' object as the bh curve defined by the user (for which they gave the path to)
        else:
            bhyoke.Set_Default()  # sets this 'bhyoke' object as the default bh curve from Opera (best bh according to the comparison file)
        materialyoke.Set_Steel(bhyoke)  # sets this 'materialyoke' as a steel with the bh curve defined above
        self.yoke_region.AssignMaterials(materialyoke)  # gives the yoke region the steel defined above
        nocurrent = _model.CurrentLibrary(self.model)  # creates for this current model a current object 'nocurrent'
        nocurrent.Set_NoCurrent()  # sets this 'nocurrent' object as the absence of current (also used for the background)
        self.yoke_region.AssignCurrent(nocurrent.current)   # gives the no current property to the yoke region
        self.yoke_edges = _model.Edges(self.yoke_region)  # defines the edges of this yoke region
        self.yoke_edges.AssignMesh(0, 3 * self.globalmesh * self.meshfactor_yoke)  # attributes the mesh edge by edge
        self.yoke_edges.AssignMesh(1, 3 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(2, 3 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(3, 3 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(4, 4 * self.globalmesh * self.meshfactor_yoke, 0.1)
        self.yoke_edges.AssignMesh(5, 5 * self.globalmesh * self.meshfactor_yoke, 0.1)
        self.yoke_edges.AssignMesh(6, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(7, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(8, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(9, 6 * self.globalmesh * self.meshfactor_yoke, 0.1)
        self.yoke_edges.AssignMesh(10, 6 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(11, 6 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(12, 6 * self.globalmesh * self.meshfactor_yoke, 0.9)
        self.yoke_edges.AssignMesh(13, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(14, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(15, 5 * self.globalmesh * self.meshfactor_yoke)
        self.yoke_edges.AssignMesh(16, 5 * self.globalmesh * self.meshfactor_yoke, 0.9)
        self.yoke_edges.AssignMesh(17, 4 * self.globalmesh * self.meshfactor_yoke, 0.9)
        self.yoke_edges.AssignMesh(18, 3 * self.globalmesh * self.meshfactor_yoke)
        # Sets coil 1, gives material, current & mesh
        qsl.Set_Coil_1_QSL() # this qsl object coil 1 attribute is set as the lower coil of a QSL
        self.coil_1 = qsl.coil_1 # this magnet object from the class Magnet() is receiving a coil 1 attribute the value of the 'qsl.coil 1'
        self.coil_1_region = _model.Region(self.coil_1)  # the region of the coil_1 is defined
        materialcoil = _material.MaterialLibrary(self.model)  # creates for this current model a material object 'materialcoil'
        materialcoil.Set_Copper()  # sets this 'materialcoil' as copper
        self.coil_1_region.AssignMaterials(materialcoil)  # gives the coil_1 region the copper defined above
        currentcoil_1 = _model.CurrentLibrary(self.model)  # creates for this current model a current object 'currentcoil_1'
        currentcoil_1.Set_CurrentPos(self.current, self.turns, self.area_coil)  # sets this 'currentcoil_1' object as self.current * self.turns / self.area_coil
        self.coil_1_region.AssignCurrent(currentcoil_1.current)   # gives this current property to the coil_1 region
        self.coil_1_edges = _model.Edges(self.coil_1_region)  # defines the edges of this coil_1 region
        self.coil_1_edges.AssignMesh(0, 4 * self.globalmesh * self.meshfactor_coil, 0.1)  # attributes the mesh edge by edge
        self.coil_1_edges.AssignMesh(1, 5 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(2, 4 * self.globalmesh * self.meshfactor_coil, 0.9)
        self.coil_1_edges.AssignMesh(3, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(4, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(5, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(6, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(7, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(8, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(9, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(10, 3 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(11, 3 * self.globalmesh * self.meshfactor_coil)
        # Sets coil 2, gives material, current & mesh
        qsl.Set_Coil_2_QSL()  # this qsl object coil 2 attribute is set as the upper coil of the QSL
        self.coil_2 = qsl.coil_2   # this magnet object from the class Magnet() is receiving a coil 2 attribute the value of the 'qsl.coil 2'
        self.coil_2_region = _model.Region(self.coil_2)    # the region of the coil_2 is defined
        self.coil_2_region.AssignMaterials(materialcoil)  # gives the coil_2 region the copper defined above
        currentcoil_2 = _model.CurrentLibrary(self.model)  # creates for this current model a current object 'currentcoil_2'
        currentcoil_2.Set_CurrentNeg(self.current, self.turns, self.area_coil)  # sets this 'currentcoil_2' object as self.current * self.turns / self.area_coil
        self.coil_2_region.AssignCurrent(currentcoil_2.current)   # gives this current property to the coil_2 region
        self.coil_2_edges = _model.Edges(self.coil_2_region)  # defines the edges of this coil_2 region
        self.coil_2_edges.AssignMesh(0, 4 * self.globalmesh * self.meshfactor_coil, 0.1)  # attributes the mesh edge by edge
        self.coil_2_edges.AssignMesh(1, 5 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(2, 4 * self.globalmesh * self.meshfactor_coil, 0.9)
        self.coil_2_edges.AssignMesh(3, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(4, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(5, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(6, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(7, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(8, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(9, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(10, 3 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(11, 3 * self.globalmesh * self.meshfactor_coil)
        # Sets background, gives material, current & mesh
        qsl.Set_Background_QSL()  # this qsl object background attribute is set as the background of the QSL
        self.background = qsl.background  # this magnet object from the class Magnet() is receiving  abackground attribute the value of the 'qsl.background'
        self.background_region = _model.Region(self.background)  # the region of the background is defined
        materialbackground = _material.MaterialLibrary(self.model)  # creates for this current model a material object 'materialbackground'
        materialbackground.Set_Air()  # sets this 'materialbackground' as air
        self.background_region.AssignMaterials(materialbackground)  # gives the background region the 'air' material defined above
        self.background_region.AssignCurrent(nocurrent.current)   # gives the no current property to the background region
        self.background_edges = _model.Edges(self.background_region)  # defines the edges of this background region
        boundary_neumann = _model.BoundaryType(self.model)  # creates for this current model a boundary object 'boundary_neumann'
        boundary_neumann.Set_Neumann() # set this 'boundary_neumann' as  a Neumann boundary condition
        boundary_dirichlet = _model.BoundaryType(self.model)  # creates for this current model a boundary object 'boundary_dirichlet'
        boundary_dirichlet.Set_Dirichlet() # sets this 'boundary_dirichlet' as  a Dirichlet boundary condition
        self.background_edges.AssignBoundary(0, boundary_neumann)  # attributes the Neumann boundary condition
        self.background_edges.AssignBoundary(1, boundary_neumann)
        self.background_edges.AssignBoundary(2, boundary_neumann)
        self.background_edges.AssignBoundary(3, boundary_neumann)
        self.background_edges.AssignBoundary(4, boundary_dirichlet) # attributes the Dirichlet boundary condition
        self.background_edges.AssignBoundary(5, boundary_dirichlet)
        self.background_edges.AssignBoundary(6, boundary_neumann)
        self.background_edges.AssignBoundary(7, boundary_neumann) # attributes the Neumann boundary condition
        self.background_edges.AssignBoundary(8, boundary_neumann)
        self.background_edges.AssignBoundary(9, boundary_neumann)
        self.background_edges.AssignMesh(0, 3 * self.globalmesh * self.meshfactor_background)  # attributes the mesh edge by edge
        self.background_edges.AssignMesh(1, 4 * self.globalmesh * self.meshfactor_background, 0.1)
        self.background_edges.AssignMesh(2, 6 * self.globalmesh * self.meshfactor_background, 0.1)
        self.background_edges.AssignMesh(3, 15 * self.globalmesh * self.meshfactor_background, 0.1)
        self.background_edges.AssignMesh(4, 40 * self.globalmesh * self.meshfactor_background)
        self.background_edges.AssignMesh(5, 40 * self.globalmesh * self.meshfactor_background)
        self.background_edges.AssignMesh(6, 15 * self.globalmesh * self.meshfactor_background, 0.9)
        self.background_edges.AssignMesh(7, 6 * self.globalmesh * self.meshfactor_background, 0.9)
        self.background_edges.AssignMesh(8, 4 * self.globalmesh * self.meshfactor_background, 0.9)
        self.background_edges.AssignMesh(9, 3 * self.globalmesh * self.meshfactor_background)

    #########     QNL     #########
    def Set_QNL(self, yoke_bhcurve_path = None):  # this magnet object will be a QNL
        qnl = Bodies(self.model)  # creates for this current model, a qsl object from the class Bodies() that will be able to have yoke/background/coil_1/coil_2 attribute
        # Sets yoke, gives material, current & mesh
        qnl.Set_Yoke_QNL() # this qnl object yoke attribute is set as the yoke of the QNL
        self.yoke = qnl.yoke  # this magnet object from the class Magnet() is receiving a yoke attribute the value of the 'qnl.yoke'
        self.yoke_region = _model.Region(self.yoke)  # the region of the yoke is defined
        materialyoke = _material.MaterialLibrary(self.model)  # creates for this current model a material object 'materialyoke'
        bhyoke = _material.BHcurveLibrary(self.model,self.bhpath)  # creates for this current model a bh curve object 'bhyoke'
        if (yoke_bhcurve_path != None):  # yoke_bhcurve_path is the path of the bh curve that one wants to defined for the new material that one is defining
            bhyoke.Set_OtherBHcurve(yoke_bhcurve_path)  # sets this 'bhyoke' object as the bh curve defined by the user (for which they gave the path to)
        else:
            bhyoke.Set_Tenten()  # sets this 'bhyoke' object as the default bh curve from Opera (best bh according to the comparison file)
        materialyoke.Set_Steel(bhyoke)  # sets this 'materialyoke' as a steel with the bh curve defined above
        self.yoke_region.AssignMaterials(materialyoke)  # gives the yoke region the steel defined above
        nocurrent = _model.CurrentLibrary(self.model)  # creates for this current model a current object 'nocurrent'
        nocurrent.Set_NoCurrent()  # sets this 'nocurrent' object as the absence of current (also used for the background)
        self.yoke_region.AssignCurrent(nocurrent.current)  # gives the no current property to the yoke region
        self.yoke_edges = _model.Edges(self.yoke_region)  # defines the edges of this yoke region
        self.yoke_edges.AssignMesh(0, 3 * self.globalmesh * self.meshfactor_yoke)  # attributes the mesh edge by edge, since we approximate the hyperbola to a series of segment we have our edge0 that correspond to edges[0,26] for Opera2D
        self.yoke_edges.AssignMesh(27, 3 * self.globalmesh * self.meshfactor_yoke) # since the hyperbola was approximated by a series of segment the edge1 corresponds to edges[27,53] for Opera2D
        self.yoke_edges.AssignMesh(54, 3 * self.globalmesh * self.meshfactor_yoke) # = edge2
        self.yoke_edges.AssignMesh(55, 3 * self.globalmesh * self.meshfactor_yoke) # = edge3
        self.yoke_edges.AssignMesh(56, 4 * self.globalmesh * self.meshfactor_yoke, 0.1) # = edge4
        self.yoke_edges.AssignMesh(57, 5 * self.globalmesh * self.meshfactor_yoke, 0.1) # = edge5
        self.yoke_edges.AssignMesh(58, 5 * self.globalmesh * self.meshfactor_yoke, 0.9) # = edge6
        self.yoke_edges.AssignMesh(59, 5 * self.globalmesh * self.meshfactor_yoke, 0.1) # = edge7
        self.yoke_edges.AssignMesh(60, 5 * self.globalmesh * self.meshfactor_yoke) # = edge8
        self.yoke_edges.AssignMesh(61, 5 * self.globalmesh * self.meshfactor_yoke)  # = edge9
        self.yoke_edges.AssignMesh(62, 6 * self.globalmesh * self.meshfactor_yoke)  # = edge10
        self.yoke_edges.AssignMesh(63, 6 * self.globalmesh * self.meshfactor_yoke, 0.9)  # = edge11
        self.yoke_edges.AssignMesh(64, 6 * self.globalmesh * self.meshfactor_yoke, 0.1)  # = edge12
        self.yoke_edges.AssignMesh(65, 6 * self.globalmesh * self.meshfactor_yoke, 0.9)  # = edge13
        self.yoke_edges.AssignMesh(66, 6 * self.globalmesh * self.meshfactor_yoke, 0.9)  # = edge14
        self.yoke_edges.AssignMesh(67, 6 * self.globalmesh * self.meshfactor_yoke)  # = edge15
        self.yoke_edges.AssignMesh(68, 6 * self.globalmesh * self.meshfactor_yoke, 0.9)  # = edge16
        self.yoke_edges.AssignMesh(69, 6 * self.globalmesh * self.meshfactor_yoke)  # = edge17
        self.yoke_edges.AssignMesh(70, 6 * self.globalmesh * self.meshfactor_yoke, 0.9)  # = edge18
        self.yoke_edges.AssignMesh(71, 5 * self.globalmesh * self.meshfactor_yoke, 0.1)  # = edge19
        self.yoke_edges.AssignMesh(72, 5 * self.globalmesh * self.meshfactor_yoke, 0.9)  # = edge20
        self.yoke_edges.AssignMesh(73, 4 * self.globalmesh * self.meshfactor_yoke, 0.9)  # = edge21
        self.yoke_edges.AssignMesh(74, 3 * self.globalmesh * self.meshfactor_yoke)  # = edge22
        self.yoke_edges.AssignMesh(75, 3 * self.globalmesh * self.meshfactor_yoke, 0.9)  # = edge23
        # Sets coil 1, gives material, current & mesh
        qnl.Set_Coil_1_QNL()  # this qnl object coil 1 attribute is set as the lower coil of the QNL
        self.coil_1 = qnl.coil_1  # this magnet object from the class Magnet() is receiving a coil 1 attribute the value of the 'qnl.coil 1'
        self.coil_1_region = _model.Region(self.coil_1)  # the region of the coil_1 is defined
        materialcoil = _material.MaterialLibrary(self.model)  # creates for this current model a material object 'materialcoil'
        materialcoil.Set_Copper()  # sets this 'materialcoil' as copper
        self.coil_1_region.AssignMaterials(materialcoil)  # gives the coil_1 region the copper defined above
        currentcoil_1 = _model.CurrentLibrary(self.model)  # creates for this current model a current object 'currentcoil_1'
        currentcoil_1.Set_CurrentPos(self.current, self.turns, self.area_coil)  # sets this 'currentcoil_1' object as self.current * self.turns / self.area_coil
        self.coil_1_region.AssignCurrent(currentcoil_1.current)   # gives this current property to the coil_1 region
        self.coil_1_edges = _model.Edges(self.coil_1_region)  # defines the edges of this coil_1 region
        self.coil_1_edges.AssignMesh(0, 3 * self.globalmesh * self.meshfactor_coil,0.1)  # attributes the mesh edge by edge
        self.coil_1_edges.AssignMesh(1, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(2, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(3, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(4, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(5, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(6, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(7, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(8, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(9, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(10, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(11, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_1_edges.AssignMesh(12, 5 * self.globalmesh * self.meshfactor_coil, 0.9)
        self.coil_1_edges.AssignMesh(13, 4 * self.globalmesh * self.meshfactor_coil, 0.9)
        # Sets coil 2, gives material, current & mesh
        qnl.Set_Coil_2_QNL()  # this qnl object coil 2 attribute is set as the upper coil of the QNL
        self.coil_2 = qnl.coil_2  # this magnet object from the class Magnet() is receiving a coil 2 attribute the value of the 'qnl.coil 2'
        self.coil_2_region = _model.Region(self.coil_2)    # the region of the coil_2 is defined
        self.coil_2_region.AssignMaterials(materialcoil)  # gives the coil_2 region the copper defined above
        currentcoil_2 = _model.CurrentLibrary(self.model)  # creates for this current model a current object 'currentcoil_2'
        currentcoil_2.Set_CurrentNeg(self.current, self.turns, self.area_coil)  # sets this 'currentcoil_2' object as self.current * self.turns / self.area_coil
        self.coil_2_region.AssignCurrent(currentcoil_2.current)   # gives this current property to the coil_2 region
        self.coil_2_edges = _model.Edges(self.coil_2_region)  # defines the edges of this coil_2 region
        self.coil_2_edges.AssignMesh(0, 3 * self.globalmesh * self.meshfactor_coil,0.1)  # attributes the mesh edge by edge
        self.coil_2_edges.AssignMesh(1, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(2, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(3, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(4, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(5, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(6, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(7, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(8, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(9, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(10, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(11, 4 * self.globalmesh * self.meshfactor_coil)
        self.coil_2_edges.AssignMesh(12, 5 * self.globalmesh * self.meshfactor_coil, 0.9)
        self.coil_2_edges.AssignMesh(13, 4 * self.globalmesh * self.meshfactor_coil, 0.9)
        # Sets background, gives material, current & mesh
        qnl.Set_Background_QNL()  # this qnl object background attribute is set as the background of the QNL
        self.background = qnl.background  # this magnet object from the class Magnet() is receiving  abackground attribute the value of the 'qnl.background'
        self.background_region = _model.Region(self.background)  # the region of the background is defined
        materialbackground = _material.MaterialLibrary(self.model)  # creates for this current model a material object 'materialbackground'
        materialbackground.Set_Air()  # sets this 'materialbackground' as air
        self.background_region.AssignMaterials(materialbackground)  # gives the background region the 'air' material defined above
        self.background_region.AssignCurrent(nocurrent.current)   # gives the no current property to the background region
        self.background_edges = _model.Edges(self.background_region)  # defines the edges of this background region
        boundary_neumann = _model.BoundaryType(self.model)  # creates for this current model a boundary object 'boundary_neumann'
        boundary_neumann.Set_Neumann() # sets this 'boundary_neumann' as  a Neumann boundary condition
        boundary_dirichlet = _model.BoundaryType(self.model)  # creates for this current model a boundary object 'boundary_dirichlet'
        boundary_dirichlet.Set_Dirichlet() # sets this 'boundary_dirichlet' as  a Dirichlet boundary condition
        self.background_edges.AssignBoundary(0, boundary_neumann)  # attributes the Neumann boundary condition
        self.background_edges.AssignBoundary(1, boundary_neumann)
        self.background_edges.AssignBoundary(2, boundary_neumann)
        self.background_edges.AssignBoundary(3, boundary_neumann)
        self.background_edges.AssignBoundary(4, boundary_neumann)
        self.background_edges.AssignBoundary(5, boundary_dirichlet) # attributes the Dirichlet boundary condition
        self.background_edges.AssignBoundary(6, boundary_dirichlet)
        self.background_edges.AssignBoundary(7, boundary_neumann) # attributes the Neumann boundary condition
        self.background_edges.AssignBoundary(8, boundary_neumann)
        self.background_edges.AssignBoundary(9, boundary_neumann)
        self.background_edges.AssignBoundary(10, boundary_neumann)
        self.background_edges.AssignBoundary(11, boundary_neumann)
        self.background_edges.AssignMesh(0, 3 * self.globalmesh * self.meshfactor_background)  # attributes the mesh edge by edge
        self.background_edges.AssignMesh(1, 4 * self.globalmesh * self.meshfactor_background, 0.1)
        self.background_edges.AssignMesh(2, 5 * self.globalmesh * self.meshfactor_background, 0.1)
        self.background_edges.AssignMesh(3, 6 * self.globalmesh * self.meshfactor_background, 0.1)
        self.background_edges.AssignMesh(4, 15 * self.globalmesh * self.meshfactor_background, 0.1)
        self.background_edges.AssignMesh(5, 40 * self.globalmesh * self.meshfactor_background)
        self.background_edges.AssignMesh(6, 40 * self.globalmesh * self.meshfactor_background)
        self.background_edges.AssignMesh(7, 15 * self.globalmesh * self.meshfactor_background, 0.9)
        self.background_edges.AssignMesh(8, 6 * self.globalmesh * self.meshfactor_background, 0.9)
        self.background_edges.AssignMesh(9, 5 * self.globalmesh * self.meshfactor_background, 0.9)
        self.background_edges.AssignMesh(10, 4 * self.globalmesh * self.meshfactor_background, 0.9)
        self.background_edges.AssignMesh(11, 3 * self.globalmesh * self.meshfactor_background)
        # Sets tensions plates gives material, current & mesh
        qnl.Set_TensionPlate_1_QNL()  # this qnl object tensionplate_1 attribute is set as the tensionplate of the QNL
        self.tensionplate_1 = qnl.tensionplate_1  # this magnet object from the class Magnet() is receiving  a tension plate 1 attribute the value of the 'qnl.tensionplate_1'
        self.tensionplate_1_region = _model.Region(self.tensionplate_1)  # the region of the tensionplate_1 is defined
        qnl.Set_TensionPlate_2_QNL()  # this qnl object tensionplate_2 attribute is set as the tensionplate of the QNL
        self.tensionplate_2 = qnl.tensionplate_2  # this magnet object from the class Magnet() is receiving  a tension plate 1 attribute the value of the 'qnl.tensionplate_2'
        self.tensionplate_2_region = _model.Region(self.tensionplate_2)  # the region of the tensionplate_2 is defined
        self.tensionplate_1_region.AssignMaterials(materialyoke) # gives the steel of the yoke to the tension plates regions
        self.tensionplate_2_region.AssignMaterials(materialyoke)
        self.tensionplate_1_region.AssignCurrent(nocurrent.current)  # gives the no current property to the tension plates regions
        self.tensionplate_2_region.AssignCurrent(nocurrent.current)
        self.tensionplate_1_edges = _model.Edges(self.tensionplate_1_region)  # defines the edges of this tension plates regions
        self.tensionplate_2_edges = _model.Edges(self.tensionplate_2_region)
        self.tensionplate_1_edges.AssignMesh(0, 9 * self.globalmesh * self.meshfactor_yoke,0.1)
        self.tensionplate_1_edges.AssignMesh(1, 9 * self.globalmesh * self.meshfactor_yoke)
        self.tensionplate_1_edges.AssignMesh(2, 9 * self.globalmesh * self.meshfactor_yoke,0.9)
        self.tensionplate_1_edges.AssignMesh(3, 9 * self.globalmesh * self.meshfactor_yoke)
        self.tensionplate_1_edges.AssignMesh(4, 8 * self.globalmesh * self.meshfactor_yoke,0.9)
        self.tensionplate_1_edges.AssignMesh(5, 6 * self.globalmesh * self.meshfactor_yoke)
        self.tensionplate_1_edges.AssignMesh(6, 8 * self.globalmesh * self.meshfactor_yoke,0.1)
        self.tensionplate_1_edges.AssignMesh(7, 7 * self.globalmesh * self.meshfactor_yoke)
        self.tensionplate_2_edges.AssignMesh(0, 9 * self.globalmesh * self.meshfactor_yoke)
        self.tensionplate_2_edges.AssignMesh(1, 8 * self.globalmesh * self.meshfactor_yoke, 0.9)
        self.tensionplate_2_edges.AssignMesh(2, 6 * self.globalmesh * self.meshfactor_yoke)
        self.tensionplate_2_edges.AssignMesh(3, 8 * self.globalmesh * self.meshfactor_yoke, 0.1)
        self.tensionplate_2_edges.AssignMesh(4, 9 * self.globalmesh * self.meshfactor_yoke)
        self.tensionplate_2_edges.AssignMesh(5, 9 * self.globalmesh * self.meshfactor_yoke, 0.1)
        self.tensionplate_2_edges.AssignMesh(6, 9 * self.globalmesh * self.meshfactor_yoke)
        self.tensionplate_2_edges.AssignMesh(7, 9 * self.globalmesh * self.meshfactor_yoke, 0.9)