import pytest

import pandas as pd

from aggyrus.core.validations import descriptors

#[TEST]
#descriptors.MutableDescr
def test_MutableDescr_assignment():
    class Dummy:
        test_x = descriptors.MutableDescr()
    
    instance = Dummy()
    instance.test_x = 99
    assert instance.test_x == 99

    instance.test_x = pd.DataFrame([1, 2, 3])
    assert instance.test_x.equals(pd.DataFrame([1, 2, 3]))

    instance.test_x = "hello"
    assert instance.test_x == "hello"


def test_MutableDescr_not_assigned():
    class Dummy:
        test_x = descriptors.MutableDescr()

    instance = Dummy()
    with pytest.raises(ValueError):
        instance.test_x


#[TEST]
#descriptors.NonMutableDescr
@pytest.fixture
def single_assign_notype():
    class Dummy():
        test_descr = descriptors.NonMutableDescr()
    return Dummy()

def test_NonMutableDescr_case1(single_assign_notype):
    single_assign_notype.test_descr = 'hola'
    assert single_assign_notype.test_descr == 'hola'
    assert single_assign_notype._test_descr == single_assign_notype.test_descr
    with pytest.raises(ValueError, match='test_descr can only be assigned once'):
        single_assign_notype.test_descr = 'adios'


def test_NonMutableDescr_case2(single_assign_notype):
    df = pd.DataFrame()
    single_assign_notype.test_descr = df
    assert single_assign_notype.test_descr is df
    assert single_assign_notype._test_descr is single_assign_notype.test_descr

    with pytest.raises(ValueError, match='test_descr can only be assigned once'):
        single_assign_notype.test_descr = -56884
        single_assign_notype.test_descr = 'aaaalo'
        single_assign_notype.test_descr = 2j + 5


def test_NonMutableDescr_case3(single_assign_notype):
    single_assign_notype.test_descr = 3.1416
    assert single_assign_notype.test_descr == 3.1416
    assert single_assign_notype._test_descr == single_assign_notype.test_descr

    with pytest.raises(ValueError, match='test_descr can only be assigned once'):
        single_assign_notype.test_descr = 0



#[TEST]
#descriptors.TypedNonMutableDescr
def test_TypedNonMutableDescr_int():
    value = 10

    class Dummy():
        test_descr = descriptors.TypedNonMutableDescr(type(value))
    
    instance = Dummy()
    with pytest.raises(ValueError, match='Attribute test_descr have not being set'):
        instance.test_descr
    
    with pytest.raises(TypeError):
        instance.test_descr = str(value)
        instance.test_descr = float(value)
        instance.test_descr = pd.DataFrame([value])

    instance.test_descr = value
    assert instance.test_descr == value

    with pytest.raises(ValueError, match='test_descr can only be assigned once'):
        instance.test_descr = 2 * value
        instance.test_descr = 'a'


def test_TypedNonMutableDescr_df():
    value = pd.DataFrame([1, 2, 3])

    class Dummy():
        test_descr = descriptors.TypedNonMutableDescr(type(value))
    
    instance = Dummy()
    with pytest.raises(ValueError, match='Attribute test_descr have not being set'):
        instance.test_descr
    
    with pytest.raises(TypeError):
        instance.test_descr = str(value)
        instance.test_descr = 3.5
        instance.test_descr = 2

    instance.test_descr = value
    assert isinstance(instance.test_descr, pd.DataFrame)
    assert instance.test_descr is value

    fake_value = pd.DataFrame([1, 2, 3])
    assert not instance.test_descr is fake_value
    
    with pytest.raises(ValueError, match='test_descr can only be assigned once'):
        instance.test_descr = 2 * value
        instance.test_descr = 'a'
        instance.test_descr = fake_value


#[TEST]
#descriptors.TypedMutableDescr
def test_TypedMutableDescr_str():
    value1 = "hello"
    value2 = -10.4
    value3 = 'world'

    class Dummy():
        test_descr = descriptors.TypedMutableDescr(str)
    
    instance = Dummy()
    with pytest.raises(ValueError):
        instance.test_descr
    
    with pytest.raises(TypeError):
        instance.test_descr = 123
        instance.test_descr = 45.67
        instance.test_descr = pd.DataFrame([1, 2, 3])

    instance.test_descr = value1
    assert instance.test_descr == value1

    with pytest.raises(TypeError):
        instance.test_descr = value2

    instance.test_descr = value3
    assert instance.test_descr == value3