import timeit
import math
import logging
import time


def complex(fun):
    def wrapper(*args, **kwargs):
        test_data = fun(*args, **kwargs)
        result = analize_complexity(test_data)
        print("Zlozonosc algorytmu: {}".format(result))
        return result, test_data[0], test_data[1]
    return wrapper


class LogFun:
    def __init__(self, fun):
        self.function = fun

    def __call__(self, *args, **kwargs):
        logging.warning("Stating function: {}".format(self.function.__name__))
        result = self.function(*args, **kwargs)
        logging.warning("Ending function: {}".format(self.function.__name__))
        return result


class TimeOutException(Exception):
    def __init__(self, info):
        self.info = info

    def __str__(self):
        return self.info


@complex
@LogFun
def complexity(function, setup, inc_arg, precision, limit, timer_runs):

    num_args = [int(s) for s in setup.split() if s.isdigit()]
    time_results = []
    problems_size = []
    i = 0

    start = time.time()
    try:
        while i < timer_runs:
            t = timeit.Timer(stmt=function, setup=setup)
            time_results.append(min(t.repeat(precision, 1)))
            problems_size.append(num_args[0])

            i += 1

            if i > 2:
                predicted = predict_time(num_args[0] * inc_arg, analize_complexity((time_results, problems_size)),
                                         time_results[len(time_results) - 1], num_args[0])
                if (time.time() - start + predicted) > limit:
                    raise TimeOutException("Timeout, returning results from current data. "
                                           "Next step will cross your limit!")

            setup = setup.replace(str(num_args[0]), str(num_args[0] * inc_arg))
            num_args[0] *= inc_arg

    except TimeOutException:
        logging.exception("Exception catched! Timeout!")

    return time_results, problems_size


@LogFun
def analize_complexity(complex_results):

    time_results = complex_results[0]
    problems_size = complex_results[1]
    fault = 0.8

    num_tests = len(time_results) - 1

    check_n = 0
    more_n = 0

    for i in range(num_tests):
        x = (time_results[i] * (problems_size[i+1] / problems_size[i])) / time_results[i + 1]
        check_n += x
        if x < fault:
            more_n += 1

    check_n2 = 0
    more_n2 = 0
    for i in range(num_tests):
        x = (time_results[i] * pow((problems_size[i+1] / problems_size[i]), 2)) / time_results[i+1]
        check_n2 += x
        if x < fault:
            more_n2 += 1

    check_log = 0
    more_log = 0
    for i in range(num_tests):
        x = (time_results[i] * ((problems_size[i+1] * math.log10(problems_size[i+1]))
                                / (problems_size[i] * math.log10(problems_size[i])))) / time_results[i+1]
        check_log += x
        if x < fault:
            more_log += 1

    check_n /= num_tests
    check_log /= num_tests
    check_n2 /= num_tests

    check_n = abs(check_n - 1)
    check_log = abs(check_log - 1)
    check_n2 = abs(check_n2 - 1)

    if check_n < check_log and check_n < check_n2:
        return "n"
    if check_log < check_n and check_log < check_n2:
        return "nlog(n)"
    if check_n2 < check_n and check_n2 < check_log:
        return "n2"

    if more_n > 0 and more_log == 0:
        return "wieksza od n"
    if more_log > 0 and more_n2 == 0:
        return "wieksza od nlog(n)"
    if more_n == 0 and check_n == 0:
        return "< n"

    return "no info"


@LogFun
def predict_time(size, complexity, time_result, problem_size):
    if complexity == "n":
        return time_result * (size / problem_size)
    if complexity == "nlog(n)":
        return time_result * ((size * math.log10(size)) / (problem_size * math.log10(problem_size)))
    if complexity == "n2":
        return time_result * pow((size / problem_size), 2)
    else:
        return size * (time_result / problem_size)


@LogFun
def run(function, setup, repeats):
    t = timeit.Timer(stmt=function, setup=setup)
    return min(t.repeat(repeats, 1))


@LogFun
def predict_problemsize(time, complex_results, function, setup, complexity, precision):
    time_result = complex_results[0][len(complex_results[0]) - 1]
    problem_size = complex_results[1][len(complex_results[1]) - 1]

    if complexity == "n":
        n = int((time / time_result) * problem_size)
    if complexity == "n2":
        n = int(math.sqrt((time / time_result)) * problem_size)
    else:
        n = int((time / time_result) * problem_size)

    if time < 60 and precision >= 2:
        tpo = time_result / problem_size
        time_down = 0.95 * time
        time_up = 1.00 * time
        args = [int(s) for s in setup.split() if s.isdigit()]

        run_setup = setup.replace(str(args[0]), str(n))
        etime = run(function, run_setup, precision)
        prev = n

        while not (time_down < etime and etime < time_up):
            if(etime < time):
                n += int((time - etime) / tpo)
            else:
                n -= int((etime - time) / tpo)
            run_setup = run_setup.replace(str(prev), str(n))
            etime = run(function, run_setup, precision)
            prev = n

        print("Exec time: {}".format(etime))

    return n
