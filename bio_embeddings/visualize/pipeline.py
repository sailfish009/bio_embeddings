from copy import deepcopy
from pandas import read_csv
from bio_embeddings.utilities import InvalidParameterError, check_required, get_file_manager
from bio_embeddings.visualize.plotly_plots import render_3D_scatter_plotly, save_plotly_figure_to_html


def plotly(**kwargs):
    result_kwargs = deepcopy(kwargs)
    file_manager = get_file_manager(**kwargs)

    annotation_file = read_csv(result_kwargs['annotation_file']).set_index('identifier')

    # Save a copy of the annotation file with index set to identifier
    input_annotation_file_path = file_manager.create_file(kwargs.get('prefix'),
                                                          result_kwargs.get('stage_name'),
                                                          'input_annotation_file',
                                                          extension='.csv')

    annotation_file.to_csv(input_annotation_file_path)

    # Get projected_embeddings_file containing x,y,z coordinates and identifiers
    projected_embeddings_file = read_csv(result_kwargs['projected_embeddings_file'], index_col=0)

    # Merge annotation file and projected embedding file based on index or original id?
    result_kwargs['merge_via_index'] = result_kwargs.get('merge_via_index', False)

    if result_kwargs['merge_via_index']:
        merged_annotation_file = annotation_file.join(projected_embeddings_file)
    else:
        merged_annotation_file = annotation_file.join(projected_embeddings_file.set_index('original_id'))

    merged_annotation_file_path = file_manager.create_file(kwargs.get('prefix'),
                                                           result_kwargs.get('stage_name'),
                                                           'merged_annotation_file',
                                                           extension='.csv')

    merged_annotation_file.to_csv(merged_annotation_file_path)
    result_kwargs['merged_annotation_file'] = merged_annotation_file_path

    figure = render_3D_scatter_plotly(merged_annotation_file)

    plot_file_path = file_manager.create_file(kwargs.get('prefix'),
                                              result_kwargs.get('stage_name'),
                                              'plot_file',
                                              extension='.html')

    save_plotly_figure_to_html(figure, plot_file_path)
    result_kwargs['plot_file'] = plot_file_path

    return result_kwargs


# list of available projection protocols
PROTOCOLS = {
    "plotly": plotly,
}


def run(**kwargs):
    """
    Run visualize protocol

    Parameters
    ----------
    kwargs arguments (* denotes optional):
        projected_embeddings_file: A csv with columns: (index), original_id, x, y, z
        prefix: Output prefix for all generated files
        stage_name: The stage name
        protocol: Which plot to generate
        annotation_file: a csv with column: identifier, label

    Returns
    -------
    Dictionary with results of stage
    """
    check_required(kwargs, ['protocol', 'prefix', 'stage_name', 'projected_embeddings_file', 'annotation_file'])

    if kwargs["protocol"] not in PROTOCOLS:
        raise InvalidParameterError(
            "Invalid protocol selection: " +
            "{}. Valid protocols are: {}".format(
                kwargs["protocol"], ", ".join(PROTOCOLS.keys())
            )
        )

    return PROTOCOLS[kwargs["protocol"]](**kwargs)