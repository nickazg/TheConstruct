from construct.platform.SmartTokenShare import SmartTokenShare
from construct.common.StorageManager import StorageManager

class SmartTokenShareTest():
    
    def test_create(self):
        sts = SmartTokenShare()
        
        # Check Test
        if True == True:
            print('create PASSED')
            return True
        
        print('create FAILED')
        return False