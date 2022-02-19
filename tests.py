from Board.DealRecord.Sequence.tests import test as seq_test
from Board.DealRecord.PlayRecord.tests import test as play_record_test
from Board.DealRecord.tests import test as deal_record_test
from Board.Deal.tests import test as deal_test
from Board.tests import test as board_test

def launch_tests() :
    board_test()
    play_record_test()
    seq_test()
    deal_test()
    deal_record_test()