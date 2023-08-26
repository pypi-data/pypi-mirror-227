"""
Created on 25.10.2021

@author: fischsam
"""


from functools import partial
import logging

from pybobyqa import controller

import numpy as np


ORIGINAL_initialise_coordinate_directions = (
    controller.Controller.initialise_coordinate_directions
)


class PreconditionedFunction:
    def __init__(
        self,
        fun,
        x0,
        bounds,
        acceptanceBounds=None,
        initStep=0.1,
        maxSteps=5,
        f0=None,
        args=[],
        assertedMinDifference=2,
        printStochasticityInfo=True,
        **kwargs
    ):
        self.fun = partial(fun, *args, **kwargs)

        self.scalingFactors = np.ones(len(x0))

        if f0 is None:
            f0 = self(x0)

        if acceptanceBounds is None:
            sample = [fun(x0) for _ in range(10)]
            stdDev = np.std(sample, ddof=1)
            self.stdDev = stdDev
            acceptanceBounds = (2 * stdDev, 10 * stdDev)
            if printStochasticityInfo:
                print("Mean               = {:8.2f}".format(np.mean(sample)))
                print("Standard deviation = {:8.2f}".format(stdDev))
                print("Min                = {:8.2f}".format(np.min(sample)))
                print("Max                = {:8.2f}".format(np.max(sample)))
                print("Range              = {:8.2f}".format(np.max(sample) - np.min(sample)))
        else:
            self.stdDev = None

        minAcceptedDiff, maxAcceptedDiff = acceptanceBounds

        for i, (lowerBound, upperBound) in enumerate(bounds):
            step = (upperBound - lowerBound) * initStep

            currentUpperBound = upperBound - x0[i]
            currentLowerBound = 0

            x = np.array(x0, copy=True)
            reachedBound = False
            for j in range(maxSteps):
                if (
                    np.abs((upperBound - lowerBound) / (currentLowerBound + 1e-200))
                    < assertedMinDifference
                ):
                    break

                if x0[i] + step > upperBound:
                    if x0[i] - step < lowerBound:
                        reachedBound = True
                        if x0[i] + step - upperBound > lowerBound - (x0[i] - step):
                            step = upperBound - x0[i]
                        else:
                            step = x0[i] - lowerBound
                    else:
                        step = -step

                    if step < 0:
                        currentLowerBound = 0
                        currentUpperBound = lowerBound - x0[i]

                x[i] = x0[i] + step

                f = self.fun(x)
                diff = np.abs(f0 - f)
                if diff > maxAcceptedDiff:
                    currentUpperBound = step
                elif diff < minAcceptedDiff:
                    if reachedBound:
                        break
                    currentLowerBound = step
                else:
                    break

                step = (currentUpperBound + currentLowerBound) / 2
            else:
                if diff > maxAcceptedDiff:
                    step = x[i] - x0[i]
                else:
                    step = currentUpperBound

            if np.abs((upperBound - lowerBound) / step) < assertedMinDifference:
                step = (upperBound - lowerBound) / assertedMinDifference

            self.scalingFactors[i] = np.abs(step)

        self.x0 = self.scale_argument(x0)
        self.bounds = self.scale_argument(np.asarray(bounds).T).T

    def scale_argument(self, x):
        """Converts an argument from the original scale to the scale at
        which the preconditioned function works.

        Parameters
        ----------
        x : array[float]
            Argument vector

        Returns
        -------
        array[float]
            Converted argument vector
        """
        return x / self.scalingFactors

    def unscale_argument(self, x):
        """Converts an argument from the scale at which the preconditioned
        function works back to the original scale.

        Parameters
        ----------
        x : array[float]
            Argument vector in the preconditioned scale

        Returns
        -------
        array[float]
            Argument vector in the original scale
        """
        return self.scalingFactors * x

    def __call__(self, x):
        return self.fun(self.unscale_argument(x))


def initialise_coordinate_directions_binsearch(
    self,
    number_of_samples,
    num_directions,
    params,
    acceptanceBound,
    maxEvaluationsPerPoint,
    maxValue=np.inf,
):
    if self.do_logging:
        logging.debug("Initialising with coordinate directions")
    # self.model already has x0 evaluated, so only need to initialise the other points
    # num_directions = params("growing.ndirs_initial")
    assert (
        self.model.num_pts <= (self.n() + 1) * (self.n() + 2) // 2
    ), "prelim: must have npt <= (n+1)(n+2)/2"
    assert (
        1 <= num_directions < self.model.num_pts
    ), "Initialisation: must have 1 <= ndirs_initial < npt"

    at_lower_boundary = (
        self.model.sl > -0.01 * self.delta
    )  # sl = xl - x0, should be -ve, actually < -rhobeg
    at_upper_boundary = (
        self.model.su < 0.01 * self.delta
    )  # su = xu - x0, should be +ve, actually > rhobeg

    xpts_added = np.zeros((num_directions + 1, self.n()))
    for k in range(1, num_directions + 1):
        # k = 0 --> base point (xpt = 0)  [ not here]
        # k = 1, ..., 2n --> coordinate directions [1,...,n and n+1,...,2n]
        # k = 2n+1, ..., (n+1)(n+2)/2 --> off-diagonal directions
        if 1 <= k < self.n() + 1:  # first step along coord directions
            dirn = k - 1  # direction to move in (0,...,n-1)
            stepa = self.delta if not at_upper_boundary[dirn] else -self.delta
            stepb = None
            xpts_added[k, dirn] = stepa

        elif self.n() + 1 <= k < 2 * self.n() + 1:  # second step along coord directions
            dirn = k - self.n() - 1  # direction to move in (0,...,n-1)
            stepa = xpts_added[k - self.n(), dirn]
            stepb = -self.delta
            if at_lower_boundary[dirn]:
                stepb = min(
                    2.0 * self.delta, self.model.su[dirn]
                )  # su = xu - x0, should be +ve
            if at_upper_boundary[dirn]:
                stepb = max(
                    -2.0 * self.delta, self.model.sl[dirn]
                )  # sl = xl - x0, should be -ve
            xpts_added[k, dirn] = stepb

        else:  # k = 2n+1, ..., (n+1)(n+2)/2
            # p = (k - 1) % n + 1  # cycles through (1,...,n), starting at 2n+1 --> 1
            # l = (k - 2 * n - 1) / n + 1  # (1,...,1, 2, ..., 2, etc.) where each number appears n times
            # q = (p + l if p + l <= n else p + l - n)
            stepa = None
            stepb = None
            itemp = (k - self.n() - 1) // self.n()
            q = k - itemp * self.n() - self.n()
            p = q + itemp
            if p > self.n():
                p, q = q, p - self.n()  # does swap correctly in Python

            xpts_added[k, p - 1] = xpts_added[p, p - 1]
            xpts_added[k, q - 1] = xpts_added[q, q - 1]

        # Evaluate objective at this new point
        upper = np.zeros_like(xpts_added[k, :])
        upper[xpts_added[k, :] > 0] = self.model.su[xpts_added[k, :] > 0]
        upper[xpts_added[k, :] < 0] = self.model.sl[xpts_added[k, :] < 0]
        lower = np.zeros_like(xpts_added[k, :])

        previous_vals = None
        previous_xpts_added = 0
        previous_diff = 0
        for i in range(maxEvaluationsPerPoint):
            x = self.model.as_absolute_coordinates(xpts_added[k, :])
            f_list, num_samples_run, exit_info = self.evaluate_objective(
                x, number_of_samples, params
            )

            f_mean = np.mean(f_list[:num_samples_run])
            diff = np.abs(f_mean - self.last_run_fopt)

            # if change is bigger than minimal demanded change (noise level)
            if diff >= acceptanceBound[0]:
                if diff <= acceptanceBound[1] or f_mean < self.last_run_fopt:
                    break
                else:
                    if i == maxEvaluationsPerPoint - 1:
                        if previous_vals and f_mean >= maxValue:
                            f_list, num_samples_run, exit_info = previous_vals
                            xpts_added[k, :] = previous_xpts_added
                        break
                    upper = xpts_added[k, :] + 0
            else:
                if i == maxEvaluationsPerPoint - 1 or (upper <= xpts_added[k, :]).all():
                    if previous_vals and previous_diff > diff:
                        f_list, num_samples_run, exit_info = previous_vals
                        xpts_added[k, :] = previous_xpts_added
                    break
                lower = xpts_added[k, :] + 0

            if f_mean < maxValue:
                previous_vals = f_list, num_samples_run, exit_info
                previous_xpts_added = xpts_added[k, :] + 0
                previous_diff = diff

            xpts_added[k, :] = (upper + lower) / 2

        # Handle exit conditions (f < min obj value or maxfun reached)
        if exit_info is not None:
            if num_samples_run > 0:
                self.model.save_point(
                    x,
                    np.mean(f_list[:num_samples_run]),
                    num_samples_run,
                    x_in_abs_coords=True,
                )
            return exit_info  # return & quit

        # Otherwise, add new results (increments model.npt_so_far)
        self.model.change_point(
            k, x - self.model.xbase, f_list[0]
        )  # expect step, not absolute x
        for i in range(1, num_samples_run):
            self.model.add_new_sample(k, f_extra=f_list[i])

        # If k exceeds N+1, then the positions of the k-th and (k-N)-th interpolation
        # points may be switched, in order that the function value at the first of them
        # contributes to the off-diagonal second derivative terms of the initial quadratic model.
        # Note: this works because the steps for (k) and (k-n) points were in the same coordinate direction
        if self.n() + 1 <= k < 2 * self.n() + 1:
            # Only swap if steps were in different directions AND new pt has lower objective
            if stepa * stepb < 0.0 and self.model.fval(k) < self.model.fval(
                k - self.n()
            ):
                xpts_added[[k, k - self.n()]] = xpts_added[[k - self.n(), k]]

    return None  # return & continue


def set_pybobyqa_binsearch_init(acceptanceBound, maxEvaluationsPerPoint):
    def newFun(self, number_of_samples, num_directions, params):
        return initialise_coordinate_directions_binsearch(
            self,
            number_of_samples,
            num_directions,
            params,
            acceptanceBound,
            maxEvaluationsPerPoint,
        )

    setattr(controller.Controller, "initialise_coordinate_directions", newFun)


def set_pybobyqa_default_init():
    setattr(
        controller.Controller,
        "initialise_coordinate_directions",
        ORIGINAL_initialise_coordinate_directions,
    )


class use_pybobyqa_binsearch_init(object):
    def __init__(self, acceptanceBound, maxEvaluationsPerPoint):
        set_pybobyqa_binsearch_init(acceptanceBound, maxEvaluationsPerPoint)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        set_pybobyqa_default_init()


if __name__ == "__main__":
    pass
