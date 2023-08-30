#a wrapper for each folder
from graphy_test_zhaohany.code_gen import *
from graphy_test_zhaohany.GAS_API import *
from graphy_test_zhaohany.new_script import *

def test():
    print("hello world")

def test_ref(mod_name, func_name):
    modu = globals()[mod_name]
    func_attr = getattr(modu, func_name)
    func_attr()

# test()
# test_ref('code_gen_test','test')
# test_ref('gas_api_test','test')
# test_ref('new_script_test','test')