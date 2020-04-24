import h5py
import numpy as np
from copy import deepcopy
from pandas import read_csv
from bio_embeddings.utilities import InvalidParameterError, check_required, get_file_manager
from bio_embeddings.project.tsne import tsne_reduce


def tsne(**kwargs):
    result_kwargs = deepcopy(kwargs)
    file_manager = get_file_manager(**kwargs)

    # Get sequence mapping to use as information source
    mapping = read_csv(result_kwargs['mapping_file'], index_col=0)

    reduced_embeddings_file_path = result_kwargs['reduced_embeddings_file']

    reduced_embeddings = []

    with h5py.File(reduced_embeddings_file_path, 'r') as f:
        for remapped_id in mapping.index:
            reduced_embeddings.append(np.array(f[remapped_id]))

    # Get parameters or set defaults
    result_kwargs['metric'] = kwargs.get('metric', 'cosine')
    result_kwargs['n_components'] = kwargs.get('n_components', 3)
    result_kwargs['perplexity'] = kwargs.get('perplexity', 6)
    result_kwargs['random_state'] = kwargs.get('random_state', 420)
    result_kwargs['n_iter'] = kwargs.get('n_iter', 15000)
    result_kwargs['verbose'] = kwargs.get('verbose', 1)
    result_kwargs['n_jobs'] = kwargs.get('n_jobs', -1)

    projected_embeddings = tsne_reduce(reduced_embeddings, **kwargs)

    mapping['x'] = projected_embeddings[:, 0]
    mapping['y'] = projected_embeddings[:, 1]
    mapping['z'] = projected_embeddings[:, 2]

    projected_embeddings_file_path = file_manager.create_file(kwargs.get('prefix'),
                                                              result_kwargs.get('stage_name'),
                                                              'projected_embeddings_file',
                                                              extension='.csv')

    mapping.to_csv(projected_embeddings_file_path)
    result_kwargs['projected_embeddings_file'] = projected_embeddings_file_path

    return result_kwargs


# list of available projection protocols
PROTOCOLS = {
    "tsne": tsne,
}


def run(**kwargs):
    """
    Run project protocol

    Parameters
    ----------
    kwargs arguments (* denotes optional):
        reduced_embeddings_file: Where per-protein embeddings live
        prefix: Output prefix for all generated files
        stage_name: The stage name
        protocol: Which projection technique to use
        mapping_file: the mapping file generated by the pipeline when remapping indexes

    Returns
    -------
    Dictionary with results of stage
    """
    check_required(kwargs, ['protocol', 'prefix', 'stage_name', 'reduced_embeddings_file', 'mapping_file'])

    if kwargs["protocol"] not in PROTOCOLS:
        raise InvalidParameterError(
            "Invalid protocol selection: " +
            "{}. Valid protocols are: {}".format(
                kwargs["protocol"], ", ".join(PROTOCOLS.keys())
            )
        )

    return PROTOCOLS[kwargs["protocol"]](**kwargs)