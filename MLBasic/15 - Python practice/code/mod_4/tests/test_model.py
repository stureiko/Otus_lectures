import sys
# Add the folder path to the model
sys.path.append('./model/')

from model import Model

def test_great_list():
    args = [2, 1, 2, 3]
    model = Model()
    result, idx = model.predict(args)
    exp_result = True
    assert result == exp_result, 'fail great_list'

def test_negative_list():
    args = [0, -1, 2, -.3]
    model = Model()
    result, idx = model.predict(args)
    exp_result = False
    assert result == exp_result, 'fail negative_list'

def test_negative_index():
    args = [0, -1, 2, -.3]
    model = Model()
    result, idx = model.predict(args)
    exp_result = [1, 3]
    assert idx == exp_result, 'fail negative_list_indexes'