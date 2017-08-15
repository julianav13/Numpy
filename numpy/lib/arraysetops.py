"""
Set operations for arrays based on sorting.

:Contains:
  unique,
  isin,
  ediff1d,
  intersect1d,
  setxor1d,
  in1d,
  union1d,
  setdiff1d

:Notes:

For floating point arrays, inaccurate results may appear due to usual round-off
and floating point comparison issues.

Speed could be gained in some operations by an implementation of
sort(), that can provide directly the permutation vectors, avoiding
thus calls to argsort().

To do: Optionally return indices analogously to unique for all functions.

:Author: Robert Cimrman

"""
from __future__ import division, absolute_import, print_function

import numpy as np


__all__ = [
    'ediff1d', 'intersect1d', 'setxor1d', 'union1d', 'setdiff1d', 'unique',
    'in1d', 'isin'
    ]


def ediff1d(ary, to_end=None, to_begin=None):
    """
    The differences between consecutive elements of an array.

    Parameters
    ----------
    ary : array_like
        If necessary, will be flattened before the differences are taken.
    to_end : array_like, optional
        Number(s) to append at the end of the returned differences.
    to_begin : array_like, optional
        Number(s) to prepend at the beginning of the returned differences.

    Returns
    -------
    ediff1d : ndarray
        The differences. Loosely, this is ``ary.flat[1:] - ary.flat[:-1]``.

    See Also
    --------
    diff, gradient

    Notes
    -----
    When applied to masked arrays, this function drops the mask information
    if the `to_begin` and/or `to_end` parameters are used.

    Examples
    --------
    >>> x = np.array([1, 2, 4, 7, 0])
    >>> np.ediff1d(x)
    array([ 1,  2,  3, -7])

    >>> np.ediff1d(x, to_begin=-99, to_end=np.array([88, 99]))
    array([-99,   1,   2,   3,  -7,  88,  99])

    The returned array is always 1D.

    >>> y = [[1, 2, 4], [1, 6, 24]]
    >>> np.ediff1d(y)
    array([ 1,  2, -3,  5, 18])

    """
    # force a 1d array
    ary = np.asanyarray(ary).ravel()

    # fast track default case
    if to_begin is None and to_end is None:
        return ary[1:] - ary[:-1]

    if to_begin is None:
        l_begin = 0
    else:
        to_begin = np.asanyarray(to_begin).ravel()
        l_begin = len(to_begin)

    if to_end is None:
        l_end = 0
    else:
        to_end = np.asanyarray(to_end).ravel()
        l_end = len(to_end)

    # do the calculation in place and copy to_begin and to_end
    l_diff = max(len(ary) - 1, 0)
    result = np.empty(l_diff + l_begin + l_end, dtype=ary.dtype)
    result = ary.__array_wrap__(result)
    if l_begin > 0:
        result[:l_begin] = to_begin
    if l_end > 0:
        result[l_begin + l_diff:] = to_end
    np.subtract(ary[1:], ary[:-1], result[l_begin:l_begin + l_diff])
    return result


def unique(ar, return_index=False, return_inverse=False,
           return_counts=False, axis=None, return_mask=False,
           return_data=True, assume_sorted=False, sort_inplace=False):
    """
    Find the unique elements of an array.

    Returns the sorted unique elements of an array. There are four optional
    outputs in addition to the unique elements: the indices of the input array
    that give the unique values, the indices of the unique array that
    reconstruct the input array, the number of times each unique value
    comes up in the input array, and the mask of the input array that gives
    the unique values.

    If data comes presorted, some operations may be skipped, which can speed
    up the process and require less memory for temporary storage.

    Parameters
    ----------
    ar : array_like
        Input array. Unless `axis` is specified, this will be flattened if it
        is not already 1-D.
    return_index : bool, optional
        If True, also return the indices of `ar` (along the specified axis,
        if provided, or in the flattened array) that result in the unique array.
    return_inverse : bool, optional
        If True, also return the indices of the unique array (for the specified
        axis, if provided) that can be used to reconstruct `ar`.
    return_counts : bool, optional
        If True, also return the number of times each unique item appears
        in `ar`.
        .. versionadded:: 1.9.0
    axis : int or None, optional
        The axis to operate on. If None, `ar` will be flattened beforehand.
        Otherwise, duplicate items will be removed along the provided axis,
        with all the other axes belonging to the each of the unique elements.
        Object arrays or structured arrays that contain objects are not
        supported if the `axis` kwarg is used.
        .. versionadded:: 1.13.0
    return_mask : bool, optional
        If True, also return a mask of `ar` (along the specified axis,
        if provided, or in the flattened array) that result in the unique array.
    return_data : bool, optional
        If False, do not return the unique contents of the array. Useful only
        in conjunction with one of the other optional returns to avoid computing
        the actual unique data if not required by the caller.
    assume_sorted : bool, optional
        if True, the input will be assumed to be sorted in the relevant axis,
        and the sort operation will be skipped.
    sort_inplace : bool, optional
        if True, the input will be sorted in-place if needed to compute the
        result (ie: if not unique_indices, unique_inverse or unique_counts
        is specified), avoiding one temporary copy. For multi-dimensional
        arrays, a copy may still be needed, so the original array may still
        end up unsorted.


    Returns
    -------
    The return value will be a tuple iff more than one of the following
    is requested. Otherwise, it will simply return the result.

    unique : ndarray
        The sorted unique values.
    unique_indices : ndarray, optional
        The indices of the first occurrences of the unique values in the
        original array. Only provided if `return_index` is True.
    unique_inverse : ndarray, optional
        The indices to reconstruct the original array from the
        unique array. Only provided if `return_inverse` is True.
    unique_counts : ndarray, optional
        The number of times each of the unique values comes up in the
        original array. Only provided if `return_counts` is True.
        .. versionadded:: 1.9.0
    unique_mask : ndarray, optional
        The mask of the original array that yields the unique values.
        Only provided if `return_mask` is True.

    See Also
    --------
    numpy.lib.arraysetops : Module with a number of other functions for
                            performing set operations on arrays.

    Examples
    --------
    >>> np.unique([1, 1, 2, 2, 3, 3])
    array([1, 2, 3])
    >>> a = np.array([[1, 1], [2, 3]])
    >>> np.unique(a)
    array([1, 2, 3])

    Return the unique rows of a 2D array

    >>> a = np.array([[1, 0, 0], [1, 0, 0], [2, 3, 4]])
    >>> np.unique(a, axis=0)
    array([[1, 0, 0], [2, 3, 4]])

    Return the indices of the original array that give the unique values:

    >>> a = np.array(['a', 'b', 'b', 'c', 'a'])
    >>> u, indices = np.unique(a, return_index=True)
    >>> u
    array(['a', 'b', 'c'],
           dtype='|S1')
    >>> indices
    array([0, 1, 3])
    >>> a[indices]
    array(['a', 'b', 'c'],
           dtype='|S1')

    Return a mask of the original array that give the unique values:

    >>> a = np.array(['a', 'b', 'b', 'c', 'a'])
    >>> indices = np.unique(a, return_mask=True, return_data=False)
    >>> indices
    array([True, True, False, True, False],
           dtype=bool)
    >>> a[indices]
    array(['a', 'b', 'c'],
           dtype='|S1')

    Reconstruct the input array from the unique values:

    >>> a = np.array([1, 2, 6, 4, 2, 3, 2])
    >>> u, indices = np.unique(a, return_inverse=True)
    >>> u
    array([1, 2, 3, 4, 6])
    >>> indices
    array([0, 1, 4, 3, 1, 2, 1])
    >>> u[indices]
    array([1, 2, 6, 4, 2, 3, 2])

    Obtain unique occurrences with the least amount of overhead
    (sort in-place, instead on a temporary copy):

    >>> a = np.array([1, 2, 3, 1, 2, 3, 1, 2, 3])
    >>> a.sort()
    >>> u = np.unique(a, assume_sorted=True)
    >>> u
    array([1,2,3])

    >>> a = np.array([1, 2, 3, 1, 2, 3, 1, 2, 3])
    >>> u = np.unique(a, sort_inplace=True)
    >>> u
    array([1,2,3])
    >>> a
    array([1,1,1,2,2,2,3,3,3])

    """
    orig_ar = ar
    ar = np.asanyarray(ar)
    if axis is None:
        return _unique1d(ar, return_index, return_inverse, return_counts,
                         return_mask, return_data, assume_sorted,
                         sort_inplace, assume_sorted or sort_inplace)
    if not (-ar.ndim <= axis < ar.ndim):
        raise ValueError('Invalid axis kwarg specified for unique')

    ar = np.swapaxes(ar, axis, 0)
    orig_shape, orig_dtype = ar.shape, ar.dtype
    # Must reshape to a contiguous 2D array for this to work...
    ar = ar.reshape(orig_shape[0], -1)
    ar = np.ascontiguousarray(ar)

    if ar.dtype.char in (np.typecodes['AllInteger'] +
                         np.typecodes['Datetime'] + 'S'):
        # Optimization: Creating a view of your data with a np.void data type of
        # size the number of bytes in a full row. Handles any type where items
        # have a unique binary representation, i.e. 0 is only 0, not +0 and -0.
        dtype = np.dtype((np.void, ar.dtype.itemsize * ar.shape[1]))
    else:
        dtype = [('f{i}'.format(i=i), ar.dtype) for i in range(ar.shape[1])]

    try:
        consolidated = ar.view(dtype)
    except TypeError:
        # There's no good way to do this for object arrays, etc...
        msg = 'The axis argument to unique is not supported for dtype {dt}'
        raise TypeError(msg.format(dt=ar.dtype))

    def reshape_uniq(uniq):
        uniq = uniq.view(orig_dtype)
        uniq = uniq.reshape(-1, *orig_shape[1:])
        uniq = np.swapaxes(uniq, 0, axis)
        return uniq

    orig_base = consolidated
    while (orig_base.base is not None and orig_base is not orig_ar
           and orig_base.base is not orig_ar):
        orig_base = orig_base.base
    if ((orig_base is orig_ar or orig_base.base is orig_ar)
        and not (return_index or return_inverse)):
        # We're operating on a view
        mask_is_sorted = assume_sorted or sort_inplace
    else:
        # We're operating on a copy, so we might as well
        # do an in-place sort on that copy
        sort_inplace = True
        mask_is_sorted = assume_sorted

    output = _unique1d(consolidated, return_index,
                       return_inverse, return_counts,
                       return_mask, return_data, assume_sorted,
                       sort_inplace, mask_is_sorted)
    if not (return_index or return_inverse or return_counts
            or return_mask):
        return reshape_uniq(output)
    elif return_data:
        uniq = reshape_uniq(output[0])
        return (uniq,) + output[1:]
    else:
        return output

def _unique1d(ar, return_index=False, return_inverse=False,
              return_counts=False, return_mask=False,
              return_data=True, assume_sorted=False,
              sort_inplace=False, mask_is_sorted=False):
    """
    Find the unique elements of an array, ignoring shape.
    """
    ar = np.asanyarray(ar)

    optional_indices = return_index or return_inverse
    optional_returns = (optional_indices or return_counts
                        or return_mask or not return_data)

    if (not optional_indices and not assume_sorted
        and return_mask and not mask_is_sorted):
        # Will need the permutation to compute masks
        optional_indices = True
    if ((not optional_indices and not assume_sorted and not sort_inplace)
        or len(ar.shape) != 1):
        # Otherwise, we don't need to make a copy
        if sort_inplace and len(ar.shape) == 2 and ar.shape[1] == 1:
            # consolidated (n x 1) matrix, no need to copy
            ar = ar.reshape(ar.size)
        else:
            ar = ar.flatten()
            if mask_is_sorted and not assume_sorted:
                # We'll work on a copy, so mask cannot be sorted
                mask_is_sorted = False
                if return_mask:
                    optional_indices = True

    if ar.size == 0:
        ret = ()
        if return_data:
            ret = (ar,)
        if return_index:
            ret += (np.empty(0, np.intp),)
        if return_inverse:
            ret += (np.empty(0, np.intp),)
        if return_counts:
            ret += (np.empty(0, np.intp),)
        if return_mask:
            ret += (np.empty(0, np.bool_),)
        if len(ret) == 1:
            ret = ret[0]
        return ret

    shape = ar.shape
    size = ar.size
    if optional_indices:
        perm = ar.argsort(kind='mergesort' if return_index else 'quicksort')
        ar = ar[perm]
    elif not assume_sorted:
        ar.sort()
    mask = np.concatenate(([True], ar[1:] != ar[:-1]))

    if not optional_returns:
        ret = ar[mask]
    else:
        ret = ()
        if return_data:
            ret = (ar[mask],)
        del ar
        if return_index or (return_mask and not assume_sorted
                            and not mask_is_sorted):
            idx = perm[mask]
            if return_index:
                ret += (idx,)
        if return_inverse:
            imask = np.cumsum(mask) - 1
            inv_idx = np.empty(shape, dtype=np.intp)
            inv_idx[perm] = imask
            ret += (inv_idx,)
        perm = None
        if return_counts:
            cidx = np.concatenate(np.nonzero(mask) + ([size],))
            ret += (np.diff(cidx),)
            del cidx
        if return_mask:
            if assume_sorted or mask_is_sorted:
                # Mask is already in input order
                imask = mask
            else:
                # Build a mask in input order
                imask = np.zeros(shape, np.bool_)
                imask[idx] = True
            ret += (imask,)
        if len(ret) == 1:
            ret = ret[0]
    return ret

def intersect1d(ar1, ar2, assume_unique=False):
    """
    Find the intersection of two arrays.

    Return the sorted, unique values that are in both of the input arrays.

    Parameters
    ----------
    ar1, ar2 : array_like
        Input arrays.
    assume_unique : bool
        If True, the input arrays are both assumed to be unique, which
        can speed up the calculation.  Default is False.

    Returns
    -------
    intersect1d : ndarray
        Sorted 1D array of common and unique elements.

    See Also
    --------
    numpy.lib.arraysetops : Module with a number of other functions for
                            performing set operations on arrays.

    Examples
    --------
    >>> np.intersect1d([1, 3, 4, 3], [3, 1, 2, 1])
    array([1, 3])

    To intersect more than two arrays, use functools.reduce:

    >>> from functools import reduce
    >>> reduce(np.intersect1d, ([1, 3, 4, 3], [3, 1, 2, 1], [6, 3, 4, 2]))
    array([3])
    """
    if not assume_unique:
        # Might be faster than unique( intersect1d( ar1, ar2 ) )?
        ar1 = unique(ar1)
        ar2 = unique(ar2)
    aux = np.concatenate((ar1, ar2))
    aux.sort()
    return aux[:-1][aux[1:] == aux[:-1]]

def setxor1d(ar1, ar2, assume_unique=False):
    """
    Find the set exclusive-or of two arrays.

    Return the sorted, unique values that are in only one (not both) of the
    input arrays.

    Parameters
    ----------
    ar1, ar2 : array_like
        Input arrays.
    assume_unique : bool
        If True, the input arrays are both assumed to be unique, which
        can speed up the calculation.  Default is False.

    Returns
    -------
    setxor1d : ndarray
        Sorted 1D array of unique values that are in only one of the input
        arrays.

    Examples
    --------
    >>> a = np.array([1, 2, 3, 2, 4])
    >>> b = np.array([2, 3, 5, 7, 5])
    >>> np.setxor1d(a,b)
    array([1, 4, 5, 7])

    """
    if not assume_unique:
        ar1 = unique(ar1)
        ar2 = unique(ar2)

    aux = np.concatenate((ar1, ar2))
    if aux.size == 0:
        return aux

    aux.sort()
    flag = np.concatenate(([True], aux[1:] != aux[:-1], [True]))
    return aux[flag[1:] & flag[:-1]]


def in1d(ar1, ar2, assume_unique=False, invert=False):
    """
    Test whether each element of a 1-D array is also present in a second array.

    Returns a boolean array the same length as `ar1` that is True
    where an element of `ar1` is in `ar2` and False otherwise.

    We recommend using :func:`isin` instead of `in1d` for new code.

    Parameters
    ----------
    ar1 : (M,) array_like
        Input array.
    ar2 : array_like
        The values against which to test each value of `ar1`.
    assume_unique : bool, optional
        If True, the input arrays are both assumed to be unique, which
        can speed up the calculation.  Default is False.
    invert : bool, optional
        If True, the values in the returned array are inverted (that is,
        False where an element of `ar1` is in `ar2` and True otherwise).
        Default is False. ``np.in1d(a, b, invert=True)`` is equivalent
        to (but is faster than) ``np.invert(in1d(a, b))``.

        .. versionadded:: 1.8.0

    Returns
    -------
    in1d : (M,) ndarray, bool
        The values `ar1[in1d]` are in `ar2`.

    See Also
    --------
    isin                  : Version of this function that preserves the
                            shape of ar1.
    numpy.lib.arraysetops : Module with a number of other functions for
                            performing set operations on arrays.

    Notes
    -----
    `in1d` can be considered as an element-wise function version of the
    python keyword `in`, for 1-D sequences. ``in1d(a, b)`` is roughly
    equivalent to ``np.array([item in b for item in a])``.
    However, this idea fails if `ar2` is a set, or similar (non-sequence)
    container:  As ``ar2`` is converted to an array, in those cases
    ``asarray(ar2)`` is an object array rather than the expected array of
    contained values.

    .. versionadded:: 1.4.0

    Examples
    --------
    >>> test = np.array([0, 1, 2, 5, 0])
    >>> states = [0, 2]
    >>> mask = np.in1d(test, states)
    >>> mask
    array([ True, False,  True, False,  True], dtype=bool)
    >>> test[mask]
    array([0, 2, 0])
    >>> mask = np.in1d(test, states, invert=True)
    >>> mask
    array([False,  True, False,  True, False], dtype=bool)
    >>> test[mask]
    array([1, 5])
    """
    # Ravel both arrays, behavior for the first array could be different
    ar1 = np.asarray(ar1).ravel()
    ar2 = np.asarray(ar2).ravel()

    # This code is significantly faster when the condition is satisfied.
    if len(ar2) < 10 * len(ar1) ** 0.145:
        if invert:
            mask = np.ones(len(ar1), dtype=bool)
            for a in ar2:
                mask &= (ar1 != a)
        else:
            mask = np.zeros(len(ar1), dtype=bool)
            for a in ar2:
                mask |= (ar1 == a)
        return mask

    # Otherwise use sorting
    if not assume_unique:
        ar1, rev_idx = np.unique(ar1, return_inverse=True)
        ar2 = np.unique(ar2)

    ar = np.concatenate((ar1, ar2))
    # We need this to be a stable sort, so always use 'mergesort'
    # here. The values from the first array should always come before
    # the values from the second array.
    order = ar.argsort(kind='mergesort')
    sar = ar[order]
    if invert:
        bool_ar = (sar[1:] != sar[:-1])
    else:
        bool_ar = (sar[1:] == sar[:-1])
    flag = np.concatenate((bool_ar, [invert]))
    ret = np.empty(ar.shape, dtype=bool)
    ret[order] = flag

    if assume_unique:
        return ret[:len(ar1)]
    else:
        return ret[rev_idx]


def isin(element, test_elements, assume_unique=False, invert=False):
    """
    Calculates `element in test_elements`, broadcasting over `element` only.
    Returns a boolean array of the same shape as `element` that is True
    where an element of `element` is in `test_elements` and False otherwise.

    Parameters
    ----------
    element : array_like
        Input array.
    test_elements : array_like
        The values against which to test each value of `element`.
        This argument is flattened if it is an array or array_like.
        See notes for behavior with non-array-like parameters.
    assume_unique : bool, optional
        If True, the input arrays are both assumed to be unique, which
        can speed up the calculation.  Default is False.
    invert : bool, optional
        If True, the values in the returned array are inverted, as if
        calculating `element not in test_elements`. Default is False.
        ``np.isin(a, b, invert=True)`` is equivalent to (but faster
        than) ``np.invert(np.isin(a, b))``.

    Returns
    -------
    isin : ndarray, bool
        Has the same shape as `element`. The values `element[isin]`
        are in `test_elements`.

    See Also
    --------
    in1d                  : Flattened version of this function.
    numpy.lib.arraysetops : Module with a number of other functions for
                            performing set operations on arrays.

    Notes
    -----

    `isin` is an element-wise function version of the python keyword `in`.
    ``isin(a, b)`` is roughly equivalent to
    ``np.array([item in b for item in a])`` if `a` and `b` are 1-D sequences.

    `element` and `test_elements` are converted to arrays if they are not
    already. If `test_elements` is a set (or other non-sequence collection)
    it will be converted to an object array with one element, rather than an
    array of the values contained in `test_elements`. This is a consequence
    of the `array` constructor's way of handling non-sequence collections.
    Converting the set to a list usually gives the desired behavior.

    .. versionadded:: 1.13.0

    Examples
    --------
    >>> element = 2*np.arange(4).reshape((2, 2))
    >>> element
    array([[0, 2],
           [4, 6]])
    >>> test_elements = [1, 2, 4, 8]
    >>> mask = np.isin(element, test_elements)
    >>> mask
    array([[ False,  True],
           [ True,  False]], dtype=bool)
    >>> element[mask]
    array([2, 4])
    >>> mask = np.isin(element, test_elements, invert=True)
    >>> mask
    array([[ True, False],
           [ False, True]], dtype=bool)
    >>> element[mask]
    array([0, 6])

    Because of how `array` handles sets, the following does not
    work as expected:

    >>> test_set = {1, 2, 4, 8}
    >>> np.isin(element, test_set)
    array([[ False, False],
           [ False, False]], dtype=bool)

    Casting the set to a list gives the expected result:

    >>> np.isin(element, list(test_set))
    array([[ False,  True],
           [ True,  False]], dtype=bool)
    """
    element = np.asarray(element)
    return in1d(element, test_elements, assume_unique=assume_unique,
                invert=invert).reshape(element.shape)


def union1d(ar1, ar2):
    """
    Find the union of two arrays.

    Return the unique, sorted array of values that are in either of the two
    input arrays.

    Parameters
    ----------
    ar1, ar2 : array_like
        Input arrays. They are flattened if they are not already 1D.

    Returns
    -------
    union1d : ndarray
        Unique, sorted union of the input arrays.

    See Also
    --------
    numpy.lib.arraysetops : Module with a number of other functions for
                            performing set operations on arrays.

    Examples
    --------
    >>> np.union1d([-1, 0, 1], [-2, 0, 2])
    array([-2, -1,  0,  1,  2])

    To find the union of more than two arrays, use functools.reduce:

    >>> from functools import reduce
    >>> reduce(np.union1d, ([1, 3, 4, 3], [3, 1, 2, 1], [6, 3, 4, 2]))
    array([1, 2, 3, 4, 6])
    """
    return unique(np.concatenate((ar1, ar2)))

def setdiff1d(ar1, ar2, assume_unique=False):
    """
    Find the set difference of two arrays.

    Return the sorted, unique values in `ar1` that are not in `ar2`.

    Parameters
    ----------
    ar1 : array_like
        Input array.
    ar2 : array_like
        Input comparison array.
    assume_unique : bool
        If True, the input arrays are both assumed to be unique, which
        can speed up the calculation.  Default is False.

    Returns
    -------
    setdiff1d : ndarray
        Sorted 1D array of values in `ar1` that are not in `ar2`.

    See Also
    --------
    numpy.lib.arraysetops : Module with a number of other functions for
                            performing set operations on arrays.

    Examples
    --------
    >>> a = np.array([1, 2, 3, 2, 4, 1])
    >>> b = np.array([3, 4, 5, 6])
    >>> np.setdiff1d(a, b)
    array([1, 2])

    """
    if assume_unique:
        ar1 = np.asarray(ar1).ravel()
    else:
        ar1 = unique(ar1)
        ar2 = unique(ar2)
    return ar1[in1d(ar1, ar2, assume_unique=True, invert=True)]
