from __future__ import division
from numpy.testing import assert_equal, assert_allclose
from nose.tools import raises, with_setup, eq_
from ..util import read_param_file, scale_samples, read_group_file
import os
import numpy as np


def setup_function():
    filename = "SALib/tests/test_params.txt"
    with open(filename, "w") as ofile:
         ofile.write("Test1 0.0 100.0\n")
         ofile.write("Test2 5.0 51.0\n")
         

def setup_param_file_with_groups():
    filename = "SALib/tests/test_params_with_groups.txt"
    with open(filename, "w") as ofile:
         ofile.write("Test1 0.0 1.0 group1\n")
         ofile.write("Test2 5.0 51.0 group2\n")
         ofile.write("Test3 0.1 1.0 group2\n")


def setup_param_file_with_partial_groups_defined():
    filename = "SALib/tests/test_params_with_partial_groups.txt"
    with open(filename, "w") as ofile:
         ofile.write("Test1,0.0,1.0,\n")
         ofile.write("Test2,5.0,51.0,group2\n")
         ofile.write("Test3,0.1,1.0,group2\n")


def setup_param_file_with_no_groups_defined():
    filename = "SALib/tests/test_params_with_no_groups.txt"
    with open(filename, "w") as ofile:
         ofile.write("Test1,0.0,1.0\n")
         ofile.write("Test2,5.0,51.0\n")
         ofile.write("Test3,0.1,1.0\n")


def setup_csv_param_file_with_whitespace_in_names():
    filename = "SALib/tests/test_params_csv_whitespace.txt"
    with open(filename, "w") as ofile:
         ofile.write("Test 1,0.0,100.0\n")
         ofile.write("Test 2,5.0,51.0\n")


def setup_tab_param_file_with_whitespace_in_names():
    filename = "SALib/tests/test_params_tab_whitespace.txt"
    with open(filename, "w") as ofile:
         ofile.write("Test 1\t0.0\t100.0\n")
         ofile.write("Test 2\t5.0\t51.0\n")


def setup_csv_param_file_with_whitespace_in_names_comments():
    filename = "SALib/tests/test_params_csv_whitespace_comments.txt"
    with open(filename, "w") as ofile:
         ofile.write("# Here is a comment\n")
         ofile.write("'Test 1',0.0,100.0\n")
         ofile.write("'Test 2',5.0,51.0\n")


def setup_group_file():
    filename = "SALib/tests/test_group_file.csv"
    with open(filename, "w") as ofile:
         ofile.write("'Group 1','Test 1'\n")
         ofile.write("'Group 2','Test 2','Test 3'\n")


def teardown():
    [os.remove("SALib/tests/%s" % f) for f in os.listdir("SALib/tests/") if f.endswith(".txt")]
    [os.remove("SALib/tests/%s" % f) for f in os.listdir("SALib/tests/") if f.endswith(".csv")]
    [os.remove("SALib/tests/%s" % f) for f in os.listdir("SALib/tests/") if f.endswith(".tab")]

@with_setup(setup_function, teardown)
def test_readfile():
    '''
    Tests a standard parameter file is read correctly
    '''

    filename = "SALib/tests/test_params.txt"
    pf = read_param_file(filename)

    assert_equal(pf['bounds'], [[0, 100], [5, 51]])
    assert_equal(pf['num_vars'], 2)
    assert_equal(pf['names'], ['Test1', 'Test2'])


@with_setup(setup_csv_param_file_with_whitespace_in_names, teardown)
def test_csv_readfile_with_whitespace():
    '''
    A comma delimited parameter file with whitespace in the names
    '''

    filename = "SALib/tests/test_params_csv_whitespace.txt"
    pf = read_param_file(filename)

    assert_equal(pf['bounds'], [[0, 100], [5, 51]])
    assert_equal(pf['num_vars'], 2)
    assert_equal(pf['names'], ['Test 1', 'Test 2'])


@with_setup(setup_tab_param_file_with_whitespace_in_names, teardown)
def test_tab_readfile_with_whitespace():
    '''
    A tab delimited parameter file with whitespace in the names
    '''

    filename = "SALib/tests/test_params_tab_whitespace.txt"
    pf = read_param_file(filename)

    assert_equal(pf['bounds'], [[0, 100], [5, 51]])
    assert_equal(pf['num_vars'], 2)
    assert_equal(pf['names'], ['Test 1', 'Test 2'])


@with_setup(setup_csv_param_file_with_whitespace_in_names_comments, teardown)
def test_csv_readfile_with_comments():
    '''
    '''

    filename = "SALib/tests/test_params_csv_whitespace_comments.txt"

    pf = read_param_file(filename)

    print(pf['bounds'], pf['num_vars'], pf['names'])

    assert_equal(pf['bounds'], [[0, 100], [5, 51]])
    assert_equal(pf['num_vars'], 2)
    assert_equal(pf['names'], ['Test 1', 'Test 2'])


@with_setup(setup_group_file, teardown)
def test_read_groupfile():
    '''
    Tests that a group file is read correctly
    '''
    group_file = "SALib/tests/test_group_file.csv"

    gf = read_group_file(group_file)

    desired = [['Group 1', ['Test 1']],['Group 2', ['Test 2', 'Test 3']]]
    actual = gf['groups']

    eq_(actual, desired)


# Test scale samples
def test_scale_samples():
    '''
    Simple test to ensure that samples are correctly scaled
    '''

    params = np.arange(0,1.1,0.1).repeat(2).reshape((11,2))

    bounds = [[10,20],[-10,10]]

    desired = np.array([np.arange(10,21,1), np.arange(-10,12,2)],dtype=np.float).T
    scale_samples(params, bounds)
    assert_allclose(params, desired, atol=1e-03, rtol=1e-03)


@raises(ValueError)
def test_scale_samples_upper_lt_lower():
    '''
    Raise ValueError if upper bound lower than lower bound
    '''
    params = np.array([[0, 0],[0.1,0.1],[0.2,0.2]])
    bounds = [[10,9],[-10,10]]
    scale_samples(params, bounds)


@raises(ValueError)
def test_scale_samples_upper_eq_lower():
    '''
    Raise ValueError if upper bound lower equal to lower bound
    '''
    params = np.array([[0, 0],[0.1,0.1],[0.2,0.2]])
    bounds = [[10,10],[-10,10]]
    scale_samples(params, bounds)


@with_setup(setup_param_file_with_groups, teardown)
def test_param_file_groups():
    '''
    '''
    filename = "SALib/tests/test_params_with_groups.txt"
    pf = read_param_file(filename, True)
    
    desired = ['group1','group2','group2']
    actual = pf['groups']
    eq_(actual, desired)
    
    desired = [[0.0, 1.0],[5.0,51.0],[0.1,1.0]]
    actual = pf['bounds']
    eq_(actual, desired)
    
    desired = ['Test1','Test2','Test3']
    actual = pf['names']
    eq_(actual, desired)
    
    
@with_setup(setup_param_file_with_partial_groups_defined)
def test_param_file_with_partial_groups():
    '''
    '''
    filename = "SALib/tests/test_params_with_partial_groups.txt"
    pf = read_param_file(filename, True)
    
    desired = ['Test1','group2','group2']
    actual = pf['groups']
    eq_(actual, desired)
    
    desired = [[0.0, 1.0],[5.0,51.0],[0.1,1.0]]
    actual = pf['bounds']
    eq_(actual, desired)
    
    desired = ['Test1','Test2','Test3']
    actual = pf['names']
    eq_(actual, desired)  
    

@with_setup(setup_param_file_with_no_groups_defined, teardown)
def test_param_file_with_no_groups():
    '''
    '''
    filename = "SALib/tests/test_params_with_no_groups.txt"
    pf = read_param_file(filename, True)
    
    desired = ['Test1','Test2','Test3']
    actual = pf['groups']
    eq_(actual, desired)
    
    desired = [[0.0, 1.0],[5.0,51.0],[0.1,1.0]]
    actual = pf['bounds']
    eq_(actual, desired)
    
    desired = ['Test1','Test2','Test3']
    actual = pf['names']
    eq_(actual, desired)
 
 
def setup_complex_parameter_file_with_groups():
    filename = "SALib/tests/test_params_complex.txt"
    with open(filename, "w") as ofile:
        ofile.write("u_ProductIndices_Simulated.Petrol.Resource Cost.Reference Case;0.86;1.86;Liquid Fuel Resource Cost\n")
        ofile.write("u_ProductIndices_Simulated.Coal.Resource Cost.Reference Case;0.64;1.64;Coal Resource Cost\n")
        ofile.write("u_ProductIndices_Simulated.Dry Waste.Resource Cost.Reference Case;0.5;1.5;Dry Waste Resource Cost\n")
        ofile.write("u_ProductIndices_Simulated.Diesel.Resource Cost.Reference Case;0.87;1.87;Liquid Fuels Resource Cost\n")
 
 
@with_setup(setup_complex_parameter_file_with_groups, teardown)
def test_complex_param_file_with_groups():
    filename = "SALib/tests/test_params_complex.txt"
    pf = read_param_file(filename, True,delimiter=';')

    desired = ['u_ProductIndices_Simulated.Petrol.Resource Cost.Reference Case',
               'u_ProductIndices_Simulated.Coal.Resource Cost.Reference Case',
               'u_ProductIndices_Simulated.Dry Waste.Resource Cost.Reference Case',
               'u_ProductIndices_Simulated.Diesel.Resource Cost.Reference Case']
    actual = pf['names']
    assert_equal(actual, desired)
    
    desired = [[0.86, 1.86],[0.64,1.64],[0.5,1.5],[0.87,1.87]]
    actual = pf['bounds']
    assert_equal(actual, desired)
    
    desired = ['Liquid Fuel Resource Cost',
               'Coal Resource Cost',
               'Dry Waste Resource Cost',
               'Liquid Fuels Resource Cost']
    actual = pf['groups']
    assert_equal(actual, desired)              
          
