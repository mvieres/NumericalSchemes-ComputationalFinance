import numpy as np


class IntegralApprox:

    @staticmethod
    def trapezoidal_rule(x, y) -> float:
        """
        Compute the integral using the trapezoidal rule.

        Parameters:
        - x: Array of x values (must be sorted).
        - y: Array of y values corresponding to x.

        Returns:
        - Integral value (float).
        """
        n = len(x)
        if n < 2:
            raise ValueError("x and y must have at least two points.")

        h = np.diff(x)  # Spacing between x values
        if not np.allclose(h, h[0]):  # Check for non-uniform spacing
            raise ValueError("x values must be evenly spaced for this implementation.")

        return 0.5 * h[0] * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
