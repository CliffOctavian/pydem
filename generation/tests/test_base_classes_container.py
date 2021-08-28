"""test cases for all the functionalities of the Container class in
base_classes module
"""


from generation import base_classes
import unittest
import numpy as np
from typing import Type, Union, Any
from geometry import two_dimensional_entities as shapes
from geometry import two_dimensional_operations as operations
import sys


class TestValidations(unittest.TestCase):
    """test cases for validations that need to take place while
    initializing the container
    """

    kaolinite_clay1 = {
        'type': 'kaolinite',
        'size_upper_bound': 3000,
        'size_lower_bound': 1000,
        'quantity': 1000
    }
    
    def test_simulation_type(self):
        """testing the validation of simulation type
        """
        
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 35000,
            width = 35000,
            simulation_type = 'tf',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
            )
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'TT')
    
    def test_length(self):
        """testing the validation of length parameter
        """

        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 0,
            width = 35000,
            simulation_type = 'ds',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
            )
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'ds',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'DS')

    def test_width(self):
        """testing the validation of width parameter
        """
        
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 35000,
            width = 0,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
            )
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'TT')

    def test_particle_type(self):
        """testing the validation of 'type' parameter in the particle
        info parameter
        """
        
        info = {k:v for k,v in self.kaolinite_clay1.items()}
        info['type'] = 'bent'
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [info],
            fluid_characteristics = None
            )
        info['type'] = 'quartz'
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'TT')

    def test_particle_info_data_type(self):
        """testing the validation of the data type of the particle_info
        array
        """
        
        info = {k:v for k,v in self.kaolinite_clay1.items()}
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = info,
            fluid_characteristics = None
            )
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [info],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'TT')

    def test_particle_essential_attributes(self):
        """testing the validation of particle_info array due to the
        essential attrirbutes that need to present in each dictionary
        """
        
        info = {k:v for k,v in self.kaolinite_clay1.items()}
        info.pop('type')
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [info],
            fluid_characteristics = None
            )
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'TT')

    def test_particle_size_bounds(self):
        """testing the validation of particle size bounds
        """
        
        info = {k:v for k,v in self.kaolinite_clay1.items()}
        info['size_upper_bound'] = 36000
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [info],
            fluid_characteristics = None
            )
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'TT')


class TestSimpleSetups(unittest.TestCase):
    """test cases for simple setups and attribute settings that take
    place at the beginning of the simulation
    """
    
    kaolinite_clay1 = {
        'type': 'kaolinite',
        'size_upper_bound': 2000,
        'size_lower_bound': 1000,
        'quantity': 500
    }
    kaolinite_clay2 = {
        'type': 'kaolinite',
        'size_upper_bound': 3000,
        'size_lower_bound': 2000,
        'quantity': 500
    }
    quartz_sand1 = {
        'type': 'quartz',
        'size_upper_bound': 10000,
        'size_lower_bound': 8000,
        'quantity': 50
    }
    
    def test_number_of_groups(self):
        """testing the 'number_of_groups' attribute of the Container
        class
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1, self.kaolinite_clay2, self.quartz_sand1],
            fluid_characteristics = None
        )
        self.assertEqual(container.number_of_groups, 3)

    def test_box_length_and_width1(self):
        """testing the 'box_length' and 'box_width' attribute of the
        Container class with one grop of particles given
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1],
            fluid_characteristics = None
        )
        self.assertEqual(container.box_length, [10000])
        self.assertEqual(container.box_width, [10000])
        
    def test_box_length_and_width2(self):
        """testing the 'box_length' and 'box_width' attribute of the
        Container class with one grop of particles given and the upper
        bound size for the given particle is a number that the container
        dimensions are not divisible by it
        """
        
        kaolinite = {k:v for k,v in self.kaolinite_clay2.items()}
        kaolinite['size_upper_bound'] = 2700
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [kaolinite],
            fluid_characteristics = None
        )
        self.assertEqual(len(container.box_length), 1)
        self.assertEqual(container.box_length, [3125])
        self.assertEqual(len(container.box_width), 1)
        self.assertEqual(container.box_width, [3125])
    
    def test_box_length_and_width3(self):
        """testing the 'box_length' and 'box_width' attribute of the
        Container class with one grop of particles given and the given
        length and width for the container not being proper numbers so
        the generated boxes become 
        """
        
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 100001,
            width = 100001,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1],
            fluid_characteristics = None
            )
    
    def test_box_length_and_width4(self):
        """testing the 'box_length' and 'box_width' attribute of the
        Container class with two grop of particles given
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1, self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(len(container.box_length), 2)
        self.assertEqual(container.box_length, [10000, 2000])
        self.assertEqual(len(container.box_width), 2)
        self.assertEqual(container.box_width, [10000, 2000])
    
    def test_box_length_and_width5(self):
        """testing the 'box_length' and 'box_width' attribute of the
        Container class with three grop of particles given
        """
    
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1, self.kaolinite_clay1, self.kaolinite_clay2],
            fluid_characteristics = None
        )
        self.assertEqual(len(container.box_length), 3)
        self.assertEqual(container.box_length, [10000, 5000, 2500])
        self.assertEqual(len(container.box_width), 3)
        self.assertEqual(container.box_width, [10000, 5000, 2500])

    def test_nr_nc1(self):
        """testing the 'nr' and 'nc' attribute of the Container class
        for one group of particles given
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1],
            fluid_characteristics = None
        )
        self.assertEqual(container.number_of_rows, [10])
        self.assertEqual(container.number_of_columns, [10])
    
    def test_nr_nc2(self):
        """testing the 'nr' and 'nc' attribute of the Container class
        for two group of particles given
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1, self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.number_of_rows, [10, 50])
        self.assertEqual(container.number_of_columns, [10, 50])
    
    def test_nr_nc3(self):
        """testing the 'nr' and 'nc' attribute of the Container class
        for three group of particles given
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay2, self.quartz_sand1, self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.number_of_rows, [10, 20, 40])
        self.assertEqual(container.number_of_columns, [10, 20, 40])
    
    def test_setup_walls1(self):
        """testing the 'setup_walls' method of the Container class with
        the 'simulation_type' parameter being "tt"
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1, self.kaolinite_clay1],
            fluid_characteristics = None
        )
        wall1 = base_classes.Wall(
            x = 0, y = 50000, inclination = np.math.pi/2, is_fixed = True, length = 100000)
        wall2 = base_classes.Wall(
            x = 50000, y = 100000, inclination = 0, is_fixed = False, length = 100000)
        wall3 = base_classes.Wall(
            x = 100000, y = 50000, inclination = np.math.pi/2, is_fixed = True, length = 100000)
        wall4 = base_classes.Wall(
            x = 50000, y = 0, inclination = 0, is_fixed = True, length = 100000)
        exp = [wall1, wall2, wall3, wall4]
        res = container.walls
        self.assertEqual(set(res), set(exp))
    
    def test_setup_walls2(self):
        """testing the 'setup_walls' method of the Container class with
        the 'simulation_type' parameter being "tt" and the length and
        width of the cotainer being different from each other
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 80000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1, self.kaolinite_clay1],
            fluid_characteristics = None
        )
        wall1 = base_classes.Wall(
            x = 0, y = 40000, inclination = np.math.pi/2, is_fixed = True, length = 80000)
        wall2 = base_classes.Wall(
            x = 50000, y = 80000, inclination = 0, is_fixed = False, length = 100000)
        wall3 = base_classes.Wall(
            x = 100000, y = 40000, inclination = np.math.pi/2, is_fixed = True, length = 80000)
        wall4 = base_classes.Wall(
            x = 50000, y = 0, inclination = 0, is_fixed = True, length = 100000)
        walls = [wall1, wall2, wall3, wall4]
        self.assertEqual(set(container.walls), set(walls))
    
    def test_number_of_clay_groups(self):
        """testing the 'number_of_clay_groups' attribute of the
        Container class
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 80000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1, self.kaolinite_clay1, self.kaolinite_clay2],
            fluid_characteristics = None
        )
        self.assertEqual(container.number_of_clay_groups, 2)
        

class TestMechanicalContacts(unittest.TestCase):
    """test cases for mechanical contact detection operations for
    different types of particles; contact lists for contacting
    particles with walls are also tested; stuff like tolerance and
    having multiple particle size hierarchies have been considered
    while writing these test cases
    """
    
    #particle info dictionaries used in test cases in this class
    kaolinite_clay1 = {
        'type': 'kaolinite',
        'size_upper_bound': 2000,
        'size_lower_bound': 1000,
        'quantity': 500
    }
    kaolinite_clay2 = {
        'type': 'kaolinite',
        'size_upper_bound': 3000,
        'size_lower_bound': 2000,
        'quantity': 500
    }
    quartz_sand1 = {
        'type': 'quartz',
        'size_upper_bound': 10000,
        'size_lower_bound': 8000,
        'quantity': 50
    }
    
    #quatrz particles to be appended to the container for test cases
    quartz1 = base_classes.Quartz(
        x = 10000, y = 10000, diameter = 8500, hierarchy = 0
    ) #touches 4 boxes, intersects with kaolinite2_6 and kaolinite1_5
    quartz2 = base_classes.Quartz(
        x = 50000, y = 10000, diameter = 9000, hierarchy = 0
    ) #touches 4 boxes, intersects with kaolinite2_5
    quartz3 = base_classes.Quartz(
        x = 30000, y = 25000, diameter = 9000, hierarchy = 0
    ) #touches 2 boxes, doesn't have any intersections
    quartz4 = base_classes.Quartz(
        x = 60000, y = 40000, diameter = 9000, hierarchy = 0
    ) #touches 4 boxes, doesn't have any intersections
    quartz5 = base_classes.Quartz(
        x = 30000, y = 50000, diameter = 8500, hierarchy = 0
    ) #touches 4 boxes, intersects with quartz15
    quartz6 = base_classes.Quartz(
        x = 82000, y = 1000, diameter = 8500, hierarchy = 0
    ) #intersects with the lower wall and touches two boxes
    quartz7 = base_classes.Quartz(
        x = 20000, y = 60000, diameter = 8500, hierarchy = 0
    ) #touches 4 boxes, intersects with quartz8 and quartz9
    quartz8 = base_classes.Quartz(
        x = 25000, y = 65000, diameter = 8500, hierarchy = 0
    ) #touches one box, intersects with quartz7
    quartz9 = base_classes.Quartz(
        x = 15000, y = 65000, diameter = 8500, hierarchy = 0
    ) #touches one box, intersects with quartz7
    quartz10 = base_classes.Quartz(
        x = 80000, y = 50000, diameter = 8500, hierarchy = 0
    ) #touches 4 boxes, wraps around quartz11
    quartz11 = base_classes.Quartz(
        x = 80000, y = 50000, diameter = 8100, hierarchy = 0
    ) #touches 4 boxes, located inside quartz10
    quartz12 = base_classes.Quartz(
        x = 75000, y = 30000, diameter = 8500, hierarchy = 0
    ) #touches two boxes, kaolinite2_2 is located completely inside this particle
    quartz13 = base_classes.Quartz(
        x = 55000, y = 55000, diameter = 8500, hierarchy = 0
    ) #touches only one box, intersects with kaolinite2_1
    quartz14 = base_classes.Quartz(
        x = 40000, y = 40000, diameter = 8500, hierarchy = 0
    ) #touches 4 boxes, kaolinite1_1 is located completely inside this particle
    quartz15 = base_classes.Quartz(
        x = 25000, y = 45000, diameter = 8500, hierarchy = 0
    ) #touches only one box, intersects with quartz5
    quartz16 = base_classes.Quartz(
        x = 0, y = 35000, diameter = 8500, hierarchy = 0
    ) #touches only one box, intersects with the left wall
    
    #first group of kaolinite particles to be appended to the container for test cases
    kaolinite1_1 = base_classes.Kaolinite(
        x = 38000, y = 38000, length = 1500, thickness = 2, inclination = np.math.pi/4, hierarchy = 2
    ) #located completely inside quartz14
    kaolinite1_2 = base_classes.Kaolinite(
        x = 45000, y = 45000, length = 1500, thickness = 2, inclination = np.math.pi/4, hierarchy = 2
    ) #intersects with kaolinite3
    kaolinite1_3 = base_classes.Kaolinite(
        x = 45000, y = 45000, length = 1500, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 2
    ) #intersects with kaolinite2
    kaolinite1_4 = base_classes.Kaolinite(
        x = 21000, y = 0, length = 1500, thickness = 2, inclination = np.math.pi/4, hierarchy = 2
    ) #intersects with the lower wall
    kaolinite1_5 = base_classes.Kaolinite(
        x = 8000, y = 8000, length = 1500, thickness = 2, inclination = np.math.pi/4, hierarchy = 2
    ) #intersects with quartz1 and kaolinite2_7
    kaolinite1_6 = base_classes.Kaolinite(
        x = 25000, y = 15000, length = 1500, thickness = 2, inclination = np.math.pi/4, hierarchy = 2
    ) #intersects with kaolinite2_8
    kaolinite1_7 = base_classes.Kaolinite(
        x = 33000, y = 48000, length = 1500, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 2
    ) #intersects with quartz5
    
    #second group of kaolinite particles to be appended to the container for test cases
    kaolinite2_1 = base_classes.Kaolinite(
        x = 53000, y = 53000, length = 2500, thickness = 2, inclination = np.math.pi/4, hierarchy = 1
    ) #intersects with quartz13
    kaolinite2_2 = base_classes.Kaolinite(
        x = 75000, y = 30000, length = 2500, thickness = 2, inclination = 0, hierarchy = 1
    ) #is located fully inside quartz12
    kaolinite2_3 = base_classes.Kaolinite(
        x = 35000, y = 15000, length = 2500, thickness = 2, inclination = np.math.pi/4, hierarchy = 1
    ) #intersects with kaolinite2_4
    kaolinite2_4 = base_classes.Kaolinite(
        x = 35000, y = 15000, length = 2500, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 1
    ) #intersects with kaolinite2_3
    kaolinite2_5 = base_classes.Kaolinite(
        x = 48000, y = 8000, length = 2500, thickness = 2, inclination = np.math.pi/4, hierarchy = 1
    ) #intersects with quartz2
    kaolinite2_6 = base_classes.Kaolinite(
        x = 12000, y = 8000, length = 2500, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 1
    ) #intersects with quartz1
    kaolinite2_7 = base_classes.Kaolinite(
        x = 7550, y = 7550, length = 2500, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 1
    ) #intersects with kaolinite1_5
    kaolinite2_8 = base_classes.Kaolinite(
        x = 25550, y = 15550, length = 2500, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 1
    ) #intersects with kaolinite1_6
    
    #container instance to run the tests on
    container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [kaolinite_clay1, kaolinite_clay2, quartz_sand1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
    )
    container.particles.extend([
        quartz1, quartz2, quartz3, quartz4, quartz5,
        quartz6, quartz7, quartz8, quartz8, quartz9,
        quartz10, quartz11, quartz12, quartz13, quartz14,
        quartz15, kaolinite1_1, kaolinite1_2, kaolinite1_3,
        kaolinite1_4, kaolinite1_5, kaolinite1_6, kaolinite1_7,
        kaolinite2_1, kaolinite2_2, kaolinite2_3, kaolinite2_4,
        kaolinite2_5, kaolinite2_6, kaolinite2_7, kaolinite2_8
    ])
    
    
    def test_touching_boxes1(self):
        """testing the "touching_boxes" method of the Container class
        given an instance of the Line class as its 'particle_shape'
        parameter
        """
        
        end1 = shapes.Point(17000, 27000)
        end2 = shapes.Point(14500, 21000)
        line = shapes.LineSegment(end1, end2)
        exp = [103, 82, 83]
        res = self.container.touching_boxes(particle_shape = line, index = 1, nb = 83)
        self.assertEqual(set(res), set(exp))
    
    def test_touching_boxes2(self):
        """testing the "touching_boxes" method of the Container class
        given an instance of the Circle class as its 'particle_shape'
        parameter
        """
        
        circle = shapes.Circle(shapes.Point(80000, 51000), 8000)
        exp = [47, 48, 57, 58]
        res = self.container.touching_boxes(circle, 0, 57)
        self.assertEqual(set(res), set(exp))
    
    def test_touching_boxes3(self):
        """testing the "touching_boxes" method of the Container class
        given an instance of the Rectangle class as its 'particle_shape'
        parameter
        """
        
        v1 = shapes.Point(99500, 2499)
        v2 = shapes.Point(99500, 2501)
        v3 = shapes.Point(100500, 2501)
        v4 = shapes.Point(100500, 2499)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        exp = [39, 79]
        res = self.container.touching_boxes(rec, 2, 39)
        self.assertEqual(set(res), set(exp))
    
    def test_update_mechanical_boxes1(self):
        """testing the "update_mechanical_boxes" method of the Container
        class appending some particles to the "particles" attribute of
        the container instance, while instantiated given only one
        particle group
        """

        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend([
            self.quartz7, self.quartz8, self.quartz9
        ])
        container.update_mechanical_boxes()
        self.assertEqual(len(container.mechanical_boxes), 1)
        self.assertEqual(container.mechanical_boxes[0][51], [self.quartz7])
        self.assertEqual(container.mechanical_boxes[0][61], [self.quartz7, self.quartz9])
        self.assertEqual(container.mechanical_boxes[0][62], [self.quartz7, self.quartz8])
    
    def test_update_mechanical_boxes2(self):
        """testing the "update_mechanical_boxes" method of the Container
        class appending some particles to the "particles" attribute of
        the container instance, while instantiated given two particle
        groups
        """

        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend([
            self.quartz1, self.kaolinite2_6
        ])
        container.update_mechanical_boxes()
        self.assertEqual(len(container.mechanical_boxes), 2)
        self.assertEqual(container.mechanical_boxes[0][0], [self.quartz1])
        self.assertEqual(container.mechanical_boxes[0][11], [self.quartz1])
        self.assertEqual(container.mechanical_boxes[1][204], [self.quartz1])
        self.assertEqual(container.mechanical_boxes[1][155], [self.quartz1, self.kaolinite2_6])
    
    def test_update_mechanical_boxes3(self):
        """testing the "update_mechanical_boxes" method of the Container
        class appending some particles to the "particles" attribute of
        the container instance, while instantiated given two particle
        groups but with different sizes than the previous test
        """

        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay2],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend([
            self.quartz1, self.kaolinite2_6
        ])
        container.update_mechanical_boxes()
        self.assertEqual(len(container.mechanical_boxes), 2)
        self.assertEqual(container.mechanical_boxes[0][0], [self.quartz1])
        self.assertEqual(container.mechanical_boxes[0][10], [self.quartz1])
        self.assertEqual(container.mechanical_boxes[1][42], [self.quartz1])
        self.assertEqual(container.mechanical_boxes[1][22], [self.quartz1, self.kaolinite2_6])
    
    def test_update_mechanical_boxes4(self):
        """testing the "update_mechanical_boxes" method of the Container
        class appending some particles to the "particles" attribute of
        the container instance, while instantiated given three particle
        groups
        """

        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay1, self.kaolinite_clay2],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend([
            self.quartz1, self.kaolinite2_7, self.kaolinite1_5
        ])
        container.update_mechanical_boxes()
        self.assertEqual(len(container.mechanical_boxes), 3)
        self.assertEqual(container.mechanical_boxes[0][11], [self.quartz1])
        self.assertEqual(container.mechanical_boxes[1][41], [self.quartz1])
        self.assertEqual(container.mechanical_boxes[1][21], [self.quartz1, self.kaolinite2_7])
        self.assertEqual(
            container.mechanical_boxes[2][123], [self.quartz1, self.kaolinite2_7, self.kaolinite1_5]
            )
        
    
    def test_single_particle_mechanical_contact_check1(self):
        """testing the "single_particle_mechanical_contact_check"
        method of the Container class appending some particles to the
        "particles" attribute of the container instance, while
        instantiated given only one particle group
        """

        pass
    
    def test_single_particle_mechanical_contact_check2(self):
        """testing the "single_particle_mechanical_contact_check"
        method of the Container class appending some particles to the
        "particles" attribute of the container instance, while
        instantiated given two particle groups
        """

        pass
    
    def test_single_particle_mechanical_contact_check3(self):
        """testing the "single_particle_mechanical_contact_check"
        method of the Container class appending some particles to the
        "particles" attribute of the container instance, while
        instantiated given three particle groups
        """

        pass
    
    def test_update_mechanical_contacts_dictionary1(self):
        """testing the "update_mechanical_contacts_dictionary"
        method of the Container class appending some particles to the
        "particles" attribute of the container instance, while
        instantiated given only one particle group
        """
        
        pass
    
    def test_update_mechanical_contacts_dictionary2(self):
        """testing the "update_mechanical_contacts_dictionary"
        method of the Container class appending some particles to the
        "particles" attribute of the container instance, while
        instantiated given two particle groups
        """
        
        pass
    
    def test_update_mechanical_contacts_dictionary3(self):
        """testing the "update_mechanical_contacts_dictionary"
        method of the Container class appending some particles to the
        "particles" attribute of the container instance, while
        instantiated given three particle groups
        """
        
        pass
    
    def test_particle_wall_contact_check(self):
        """testing the "particle_wall_contact_check" method of the
        Container class
        """
        
        pass
    
    def test_update_wall_contacts_list1(self):
        """testing the "update_wall_contacts_list" method of the
        Container class appending some particles to the "particles"
        attribute of the container instance, while instantiated given
        only one particle group
        """
        
        pass
    
    def test_update_wall_contacts_list2(self):
        """testing the "update_wall_contacts_list" method of the
        Container class appending some particles to the "particles"
        attribute of the container instance, while instantiated given
        two particle groups
        """
        
        pass
    
    def test_update_wall_contacts_list3(self):
        """testing the "update_wall_contacts_list" method of the
        Container class appending some particles to the "particles"
        attribute of the container instance, while instantiated given
        three particle groups
        """
        
        pass


class TestDDLandVDVcontancts(unittest.TestCase):
    """testing the ddl and van der vaals contact detection between two
    clay particles
    """
    
    pass


class TestParticleGeneration(unittest.TestCase):
    """test cases to see if the particle generation phase in the
    container takes place flawlessly
    """
    
    pass


class TestMechanicalForces(unittest.TestCase):
    """test cases for mechanical forces calculated between different
    types of particles
    """
    
    pass


class TestDDLandVDVforces(unittest.TestCase):
    """testing the ddl and van der vaals forces calculated for clay
    particles
    """
    
    pass


class TestUpdates(unittest.TestCase):
    """test cases to see if the container and particle's conditions are
    updated correctly after a relaxation phase
    """
    
    pass


if __name__ == '__main__':
    unittest.main()