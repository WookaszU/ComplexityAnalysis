import argparse
from complexity import complex
import logging


def is_valid_number(parser, arg):
    try:
        arg = int(arg)
    except ValueError:
        parser.error('Numerical arguments must be integers bigger than 0 ! You have inserted {} !'.format(arg))
    if arg <= 0:
        parser.error('Numerical arguments must be integers bigger than 0 ! You have inserted {} !'.format(arg))
    else:
        return arg


parser = argparse.ArgumentParser(description="Program for analizing algorithms complexities, predicting execution "
                                             "times and predicting size of data which can be solve in given time. ")

parser.add_argument("name", help="module.name of algorithm to analysis for example: "
                                 "test.qsort(x)", type=str)
parser.add_argument("st", help="imports and inicialization of necessary structures, next to changing number make space"
                               """for example: "import test; x = list(range( 100 ))" """, default=str)
parser.add_argument("--inc", "-b", help="the number which the algorithm argument will be multiplied", default=10,
                    type=lambda x: is_valid_number(parser, x))
parser.add_argument("--timeout", help="timeout in seconds", default=30, type=lambda x: is_valid_number(parser, x))
parser.add_argument("--prec", help="precision of analysis (number > 0)", default=1,
                    type=lambda x: is_valid_number(parser, x))
parser.add_argument("--pt", help="enter size of input to given algorithm to predict how much time it will take",
                    type=lambda x: is_valid_number(parser, x))
parser.add_argument("--ps", help="enter time in seconds to check how big input size can be executed in this time",
                    type=lambda x: is_valid_number(parser, x))
parser.add_argument("--tr", help="enter number of timer samples - how many times the base problem size "
                                 "will be multiplied", default=10, type=lambda x: is_valid_number(parser, x))

args = parser.parse_args()

FORMAT = '%(relativeCreated)d %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("Time control")
logger.warning("Created - lets begin")


function = args.name
setup = args.st
precision = args.prec
inc_arg = args.inc
timeout = args.timeout
timer_runs = args.tr

fun_complex = complex.complexity(function, setup, inc_arg, precision, timeout, timer_runs)

if args.pt is not None:
    print("Approximated time of executing algorithm with entered problem size: {}".format(complex.predict_time(
                                                              args.pt, fun_complex[0],
                                                              fun_complex[1][len(fun_complex[1]) - 1],
                                                              fun_complex[2][len(fun_complex[2]) - 1])))

if args.ps is not None:
    print("Size of problem solved in entered time: {}".format
          (complex.predict_problemsize(args.ps, (fun_complex[1], fun_complex[2]),
                                       function, setup, fun_complex, precision)))
