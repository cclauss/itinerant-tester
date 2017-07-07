# Copyright (c) 2016 IBM. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
This module contains some of the standard features that are extracted from
spectrograms and auto-correlation calculations from the raw SETI data.

Some functions are merely wrappers around Numpy-based operations, but
contain documentation that explicitly show how they are used with SETI data.

'''

import numpy as np
import scipy.stats
import math


def difference(arr, n=1, axis=0, **kwargs):
  '''
  Assuming that `arr` is a 2D spectrogram returned by
  ibmseti.dsp.raw_to_spectrogram(data), this function
  uses the Numpy.diff function to calculate the nth
  difference along either time or frequency.

  If axis = 0 and n=1, then the first difference is taken
  between subsequent time samples

  If axis = 1 and n=1, then the first difference is taken
  between frequency bins.

  For example:

    //each column is a frequency bin
    x = np.array([
       [ 1,  3,  6, 10],   //each row is a time sample
       [ 0,  5,  6,  8],
       [ 2,  6,  9, 12]])

    ibmseti.features.first_difference(x, axis=1)
    >>> array([[2, 3, 4],
               [5, 1, 2],
               [4, 3, 3]])

    ibmseti.features.first_difference(x, axis=0)
    >>> array([[-1,  2,  0, -2],
               [ 2,  1,  3,  4]])

  '''
  return np.diff(arr, n=n, axis=axis, **kwargs)


def projection(arr, axis=0, **kwargs):
  '''
  Assuming that `arr` is a 2D spectrogram returned by
  ibmseti.dsp.raw_to_spectrogram(data), where each row
  of the `arr` is a power spectrum at a particular time,
  this function uses the numpy.sum function to project the
  data onto the time or frequency axis into a 1D array.

  If axis = 0, then the projection is onto the frequency axis
  (the sum is along the time axis)

  If axis = 1, then the projection is onto the time axis.
  (the sum is along the frequency axis)

  For example:

    //each column is a frequency bin
    x = np.array([
       [ 1,  3,  6, 10],   //each row is a time sample
       [ 0,  5,  6,  8],
       [ 2,  6,  9, 12]])

    ibmseti.features.projection(x, axis=1)
    >>> array([20, 19, 29])

    ibmseti.features.projection(x, axis=0)
    >>> array([ 3, 14, 21, 30])

  One interesting kwarg that you may wish to use is `keepdims`.
  See the documentation on numpy.sum for more information.

  '''
  return np.sum(arr, axis=axis, **kwargs)


def moment(arr, moment=1, axis=0, **kwargs):
  '''
  Uses the scipy.stats.moment to calculate the Nth central
  moment about the mean.

  If `arr` is a 2D spectrogram returned by
  ibmseti.dsp.raw_to_spectrogram(data), where each row
  of the `arr` is a power spectrum at a particular time,
  this function, then the Nth moment along each axis
  will be computed.

  If axis = 0, then Nth moment for the data in each
  frequency bin will be computed. (The calculation is done
    *along* the 0th axis, which is the time axis.)

  If axis = 1, then Nth moment for the data in each
  time bin will be computed. (The calculation is done
    *along* the 1st axis, which is the frequency axis.)

  For example, consider the 2nd moment:

    //each column is a frequency bin
    x = array([[  1.,   3.,   6.,  10.], //each row is a time sample
               [  0.,   5.,   6.,   8.],
               [  2.,   6.,   9.,  12.]])

    ibmseti.features.mement(x, moment=2, axis=0) //the returned array is of size 4, the number of columns / frequency bins.
    >>>  array([ 0.66666667,  1.55555556,  2.,  2.66666667])

    ibmseti.features.mement(x, moment=2, axis=1) //the returned array is of size 3, the number of rows / time bins.
    >>>  array([ 11.5 ,  8.6875, 13.6875])

  If `arr` is a 1D array, such as what you'd get if you projected
  the spectrogram onto the time or frequency axis, then you must
  use axis=0.

  '''
  return scipy.stats.moment(arr, moment=moment, axis=axis, **kwargs)


def first_order_gradient(arr, axis=0):
  '''
  Returns the gradient of arr along a particular axis using
  the first order forward-difference.
  Additionally, the result is padded with 0 so that the
  returned array is the same shape as in input array.
  '''
  grad_arr = difference(arr, n=1, axis=axis)
  return np.insert(grad_arr, grad_arr.shape[axis], 0, axis=axis)


def total_variation(arr):
  '''
  If arr is a 2D array (N X M), assumes that arr is a spectrogram with time along axis=0.

  Calculates the 1D total variation in time for each frequency and returns an array
  of size M.

  If arr is a 1D array, calculates total variation and returns a scalar.

  Sum ( Abs(arr_i+1,j  - arr_ij) )

  If arr is a 2D array, it's common to take the mean of the resulting M-sized array
  to calculate a scalar feature.
  '''
  return np.sum(np.abs(np.diff(arr, axis=0)), axis=0)


def maximum_variation(arr):
  '''
  return np.max(arr, axis=0) - np.min(arr, axis=0)

  If `arr` is a 1D array, a scalar is returned.

  If `arr` is a 2D array (N x M), an array of length M is returned.
  '''
  return np.max(arr, axis=0) - np.min(arr, axis=0)


def tv_2d_isotropic(grad_0_arr, grad_1_arr):
  '''
  Calculates the Total Variation

  Assumes a 2D array.

  grad_0_arr is the gradient along the 0th axis of arr.
  grad_1_arr is the gradient along the 1st axis of arr.

  You can use the 1st order forward-difference measure
  of the gradient (the standard calculation). Or you
  can use the second_order central gradient.

  '''
  return np.sqrt(grad_0_arr**2 + grad_1_arr**2).sum()


def entropy(p, w):
  '''
  Computes the entropy for a discrete probability distribution function, as
  represented by a histogram, `p`, with bin sizes `w`,

   h_p = Sum -1 * p_i * ln(p_i / w_i)

  Also computes the maximum allowed entropy for a histogram with bin sizes `w`.

    h_max = ln( Sum w_i )

  and returns both as a tuple (h_p , h_max ). The entropy is in 'natural' units.

  Both `p` and `w` must be Numpy arrays.

  If `p` is normalized to 1 ( Sum p_i * w_i = 1), then
  the normalized entropy is equal toh_p / h_max and will
  be in the range [0, 1].

  For example, if `p` is a completely flat PDF (a uniform distribution), then
  the normalized entropy will equal 1, indicating maximum amount of disorder.
  (This is easily shown for the case where w_i = 1.)

  If the `p_i` is zero for all i except j and p_j = 1, then the entropy will be 0,
  indicating no disorder.

  One can use this entropy measurement to search for signals in the spectrogram.
  First we need to build a histogram of the measured power values in the spectrogram.
  This histogram represents an estimate of the probability distribution function of the
  observed power in the spectrogram.

  If the spectrogram is entirely noise, the resulting histogram should be quite flat and
  the normalized entropy ( h_p / h_max ) will approach 1. If there is a significant signal
  in the spectrogram, then the histogram will not be flat and the normalized entropy will
  be less than 1.

  The decision that needs to be made is the number of bins and the bin size. And unfortunately,
  the resulting entropy calculated will depend on the binning.

  Based on testing and interpretibility, we recommend to use a fixed number of bins that either
  span the full range of the power values in the spectrogram (0 to spectrogram.max()),
  or span a fixed range (for example, from 0 to 500).

  For example, you may set the range equal to the range of the values in the spectrogram.

    bin_edges = range(0,int(spectrogram.max()) + 2) #add 1 to round up, and one to set the right bin edge.
    p, _ = np.histogram(spectrogram.flatten(), bins=bin_edges, density=True)
    w = np.diff(bin_edges)
    h_p, h_max = ibmseti.features.entropy(p,w)

  If you choose to fix the range of the histogram, it is highly recommended that you use
  `numpy.clip` to ensure that any of the values in the spectrogram that are greater than
  your largest bin are not thrown away!

  For example, if you decide on a fixed range between 0 and 500, and your spectrogram
  contains a value of 777, the following code would produce a histogram where that 777 value
  is not present in the count.

    bin_edges = range(0,501)
    p, _ = np.histogram(spectrogram.flatten(), bins=bin_edges, density=True)
    w = np.diff(bin_edges)
    h_p, h_max = ibmseti.features.entropy(p,w)

  But if you clip the spectrogram, you can interpret the last bin as being "the number
  of spectrogram values equal to or greater than the lower bin edge".

    bin_edges = range(0,501)
    p, _ = np.histogram(np.clip(spectrogram.flatten(), 0, 500), bins=bin_edges, density=True)
    w = np.diff(bin_edges)
    h_p, h_max = ibmseti.features.entropy(p,w)

  You can also choose to fix the number of bins

    bins = 50
    p, bin_edges = np.histogram(spectrogram.flatten(), bins=bins, density=True)
    w = np.diff(bin_edges)
    h_p, h_max = ibmseti.features.entropy(p,w)

  It is suggested to use any of the following measures as features:

    bin range, spectrogram.min, spectrogram.max, number_of_bins, log(number_of_bins)
    entropy, max_entropy, normalized_entropy.

  Automatic Binning:

  While Numpy and AstroML offer ways of automatically binning the data, it is unclear if this
  is a good approach for entropy calculation -- especially when wishing to compare the value
  across different spectrogram. The automatic binning tends to remove disorder in
  the set of values, making the histogram smoother and more ordered than the data actually are.
  This is true of automatic binning with fixed sizes (such as with the 'rice', and 'fd' options in
  numpy.histogram), or with the variable sized arrays as can be calculated with Bayesian Blocks
  with astroML. However, nothing is ruled out. In preliminary testing,
  the calculated entropy from a histogram calculated with Bayesian Block binning seemed to be more
  sensitive to a simulated signal than using fixed binning. However, it's unclear how to
  interpret the results because "h_p/h_max" *increased* with the presence of a signal and exceeded 1.

  **It is likely that the calculation of h_max is done incorrectly. Please check my work!**

  It may even be that the total number of bins created by the Bayesian Block method would
  be a suitable feature. For a completely flat distribution, there will only be one bin. If the
  data contains significant variation in power levels, the Bayesian Block method will produce more
  bins.  More testing is required and your mileage may vary.

    import astroML.plotting

    bin_edges = astroML.density_estimation.bayesian_blocks(spectrogram.flatten())
    p, _ = np.histogram(spectrogram.flatten(), bins=bin_edges, density=True)
    w = np.diff(bin_edges)

    h_p, h_max = ibmseti.features.entropy(p,w)

  Also to note: Using astroML.density_estimation.bayesian_blocks takes prohibitively long!

  "Entropy" of raw data.

  If `p` is NOT a PDF, then you're on your own to interpret the results. In this case, you
  may set `w` = None and the calculation will assume w_i = 1 for all i.

  For example,

    h_p, _ = ibmseti.features.entropy(spectrogram.flatten(), None)

  '''
  if w is None:
    w = np.ones(len(p))

  h_p = np.sum(map(lambda x: -x[0]*math.log(x[0]/x[1]) if x[0] else 0, zip(p, w)))
  h_max = math.log(np.sum(w))

  return h_p, h_max


def asymmetry(spectrogram_L, spectrogram_R):
  '''
  returns (spectogram_L - spectrogram_R) / (spectogram_L + spectrogram_R)

  The asymmetry measure should be used for both polarizations recorded for a particular observation.

  On can then perform analysis such as integrating the returned spectrogram to determine if the
  asymmetry of the signals are close to zero, indicating equal signal in both polarizations, or
  close to +-1, indicating a strong asymmetry in the L or R polarization.

  spectrogram_L and spectrogram_R should be Numpy arrays.
  '''
  return (spectrogram_L - spectrogram_R) / (spectrogram_L + spectrogram_R)
