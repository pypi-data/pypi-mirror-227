import numpy as np
from scipy.special import comb

def bernstein_poly(i, n, t):
    """
    The Bernstein polynomial of n, i as a function of t
    """
    return comb(n, i) * ( t**(n-i) ) * (1 - t)**i


def bezier_curve(control_points, n_times=1000):
    """
    Calculates the bezier curve formed by the given control points and returns n_times points evenly distrubeted across the curve
    """
    n_points = len(control_points)
    x_points = np.array([p[0] for p in control_points])
    y_points = np.array([p[1] for p in control_points])
    z_points = np.array([p[2] for p in control_points])

    t = np.linspace(0.0, 1.0, n_times)

    polynomial_array = np.array([bernstein_poly(i, n_points-1, t) for i in range(n_points)])

    x_vals = np.dot(x_points, polynomial_array)
    y_vals = np.dot(y_points, polynomial_array)
    z_vals = np.dot(z_points, polynomial_array)

    return np.array([x_vals, y_vals, z_vals]).T