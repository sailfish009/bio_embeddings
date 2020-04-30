In this folder you will find a couple examples of how to use the pipeline or it's outputs.

You will also find the `parameters_blueprint.yml` file. This file contains all possible parameters for the pipeline with details about their functionality.


### Pipeline examples:

To run the example, cd in the directory (e.g. `cd use_case_one`) and execute `bio_embeddings config.yml`

- `use_case_one`

  You have a set of proteins (in FASTA format) and want to create amino acid-level embeddings, as well as protein-level embeddings.
  Additionally, you have an annotation file with some property for some of the proteins in your dataset. For these, you want to produce a t-sne plot.
    
- `use_case_two`

  You have a set of proteins (in FASTA format) and want to create amino acid-level embeddings, as well as protein-level embeddings.
  Additionally, you have an annotation file with some property for some of the proteins in your dataset. For these, you want to produce a t-sne plot.

  This time around: you downloaded the models locally (faster execution) and want to provide the path to the model's weights and options.
  You also annotated your proteins using an md5 hash of the sequence instead of arbitrary identifiers.
  
- `use_case_three`

  You already have per-protein embeddings of a certain dataset and want to produce various t-sne plots, using both different annotation files and different t-sne parameters.
  
  Files you will need:
  
    - Reduced embeddings file: a per-protein embedding file in hdf5 format
    - Mapping file: a file containing a mapping from md5 hash of the sequence to an arbitrary identifier (e.g. the one used in an annotation file)
    - Annotation file(s): CSV files containing annotations for the proteins in the reduced embeddings file
    
  *Note*: While it is possible to use the pipeline to produce many visualizations for many different annotations, it may be more efficient to use a Notebook for this.
  We include a notebook (`project_visualize_pipeline_embeddings`) covering the same use case as the one presented here in the `notebooks` folder at the root of this project.