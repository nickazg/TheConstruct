from construct.tests.common.StorageManagerTest import StorageManagerTest
from construct.tests.platform.FundingStageTest import FundingStageTest
from construct.tests.platform.SmartTokenShareTest import SmartTokenShareTest

def run_tests():

    # # Storage Manager Tests
    # smt = StorageManagerTest()
    # smt.test_get()
    # smt.test_put()
    # smt.test_delete()
    # smt.test_serialize_array()
    # smt.test_deserialize_array()

    # fst = FundingStageTest()
    # fst.test_create()
    # fst.test_read_from_storage()

    sts = SmartTokenShareTest()
    sts.test_create()
    sts.test_start_new_crowdfund()
    sts.test_crowdfund_available_amount()
    sts.test_add_to_crowdfund_circulation()
    sts.test_get_crowdfund_circulation()
