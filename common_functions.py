from datetime import timedelta
from math import sqrt, sin, cos


# def vector_module(x: float,
#                   y: float
#                   ):
#     module = sqrt(pow(x, 2) + pow(y, 2))
#     return module
#
#
# def vector_components(module: float,
#                       angle: float
#                       ):
#     x = module * cos(angle)
#     y = module * sin(angle)
#     return x, y


# def format_time(time):
#     output = str(timedelta(seconds=time))[:-3]
#     return output


def lerp(min_value: float,
         max_value: float,
         in_value: float
         ):
    if max_value > min_value:
        output = ((max_value - min_value) * in_value) + min_value
        output = max(min_value, min(output, max_value))
        return output
    else:
        output = ((min_value - max_value) * in_value) + max_value
        output = max(max_value, min(output, min_value))
        output = 1 - output
        return output
