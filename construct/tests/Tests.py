from construct.tests.common.StorageManagerTest import StorageManagerTest
from construct.tests.platform.FundingStageTest import FundingStageTest
from construct.tests.platform.SmartTokenShareTest import SmartTokenShareTest
from construct.tests.platform.TheConstructTest import TheConstructTest

def run_tests(operation, args):

    # print('TESTING StorageManagerTest')
    # smt = StorageManagerTest()
    # smt.test_get()
    # smt.test_put()
    # smt.test_delete()
    # smt.test_serialize_array()
    # smt.test_deserialize_array()

    # print('TESTING SmartTokenShareTest')
    # sts = SmartTokenShareTest()
    # sts.test_create()
    # sts.test_total_available_amount()
    # sts.test_add_to_total_circulation()
    # sts.test_get_total_circulation()

    # print('TESTING FundingStageTest')
    # fst = FundingStageTest()
    # fst.test_create()
    # fst.test_available_amount()
    # fst.test_add_to_circulation()
    # fst.test_get_circulation()
    # fst.test_calculate_can_exchange()
    # fst.test_can_exchange()
    # fst.test_exchange()

    tc = TheConstructTest()
    tc.test(operation, args)

    # return True

