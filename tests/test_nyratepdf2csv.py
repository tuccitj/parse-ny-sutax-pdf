import sys
sys.path.append("./")
from src.nyratepdf2csv import *

def test_convert_rate():
    assert(convert_rate("81/2") == 0.08500)
    assert(convert_rate("8") == 0.08000)
    assert(convert_rate("random string") == 0.0)