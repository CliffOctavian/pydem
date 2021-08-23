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
    
    
class TestMechanicalContacts(unittest.TestCase):
    """test cases for mechanical contact detection operations for
    different types of particles
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