"""Map functions with tqdm progress bars for parallel processing.

p_tqdm_map:  Performs a parallel ordered map.
p_tqdm_umap: Performs a parallel unordered map.
"""

from typing import Any
from typing import Callable
from typing import Generator
from typing import Iterable
from typing import List


def __parallel(ordered: bool, function: Callable, *iterables: Iterable, **kwargs: Any) -> Generator:
    """Returns a generator for a parallel map.

    Arguments:
        ordered     bool        True for an ordered map, False for an unordered map.
        function    Callable    The function to apply to each element of the given Iterable.
        iterables   Iterable    One or more Iterables containing the data to be mapped.

    Returns:
        A generator which will apply the function to each element of the given Iterables
        in parallel in order.
    """
    import multiprocess as mp
    from typing import Sized

    from tqdm.auto import tqdm

    progress = kwargs.pop('progress', None)
    num_cpus = kwargs.pop('num_cpus', None)
    chunksize = kwargs.pop('chunksize', 1)
    initializer = kwargs.pop('initializer', None)
    initargs = kwargs.pop('initargs', None)

    if num_cpus is None:
        num_cpus = mp.cpu_count()
    elif type(num_cpus) == float:
        num_cpus = int(round(num_cpus * mp.cpu_count()))

    progress_needs_close = False
    if progress is None:
        # Determine length of tqdm (equal to length of the shortest iterable)
        total = kwargs.pop('total', min(len(iterable) for iterable in iterables if isinstance(iterable, Sized)))
        progress = tqdm(total=total, **kwargs)
        progress_needs_close = True

    # Create parallel generator
    map_type = 'imap' if ordered else 'imap_unordered'
    with mp.Pool(num_cpus, initializer=initializer, initargs=initargs) as pool:
        map_func = getattr(pool, map_type)

        for item in map_func(function, *iterables, chunksize=chunksize):
            yield item
            progress.update()

    if progress_needs_close:
        progress.close()


def p_tqdm_map(function: Callable, *iterables: Iterable, **kwargs: Any) -> List[Any]:
    """Performs a parallel ordered map."""
    return list(__parallel(True, function, *iterables, **kwargs))


def p_tqdm_umap(function: Callable, *iterables: Iterable, **kwargs: Any) -> List[Any]:
    """Performs a parallel unordered map."""
    return list(__parallel(False, function, *iterables, **kwargs))
