import logging
from typing import Dict

from numpy import ndarray

from webserver.tasks import task_keeper
from webserver.utilities.configuration import configuration

logger = logging.getLogger(__name__)

featureExtractor = None

if "seqvec_annotations" in configuration['celery']['celery_worker_type']:
    from bio_embeddings.extract.basic.BasicAnnotationExtractor import BasicAnnotationExtractor
    from bio_embeddings.utilities import convert_list_of_enum_to_string

    logger.info("Loading the feature extraction models...")

    featureExtractor = BasicAnnotationExtractor(
        "seqvec_from_publication",
        secondary_structure_checkpoint_file=configuration['seqvec']['secondary_structure_checkpoint_file'],
        subcellular_location_checkpoint_file=configuration['seqvec']['subcellular_location_checkpoint_file']
    )

    logger.info("Finished initializing.")


@task_keeper.task()
def get_seqvec_annotations_sync(embedding: ndarray) -> Dict[str, str]:
    annotations = featureExtractor.get_annotations(embedding)

    return {
        "predictedDSSP3": convert_list_of_enum_to_string(annotations.DSSP3),
        "predictedDSSP8": convert_list_of_enum_to_string(annotations.DSSP8),
        "predictedDisorder": convert_list_of_enum_to_string(annotations.disorder),
        "predictedMembrane": annotations.membrane.value,
        "predictedSubcellularLocalizations": annotations.localization.value,
    }
