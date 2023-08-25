from collections import defaultdict
from typing import Iterator, List, Tuple, TypeVar, Union

from clarifai_grpc.grpc.api import resources_pb2

from clarifai.client.input import Inputs
from clarifai.datasets.upload.features import (TextFeatures, VisualClassificationFeatures,
                                               VisualDetectionFeatures, VisualSegmentationFeatures)

OutputFeaturesType = TypeVar(
    'OutputFeaturesType',
    bound=Union[TextFeatures, VisualClassificationFeatures, VisualDetectionFeatures,
                VisualSegmentationFeatures])


class ClarifaiDataset:
  """Clarifai datasets base class."""

  def __init__(self, datagen_object: Iterator, dataset_id: str, split: str) -> None:
    self.datagen_object = datagen_object
    self.dataset_id = dataset_id
    self.split = split
    self.all_input_ids = {}
    self._all_input_protos = {}
    self._all_annotation_protos = defaultdict(list)
    self.input_object = Inputs()

  def __len__(self) -> int:
    """Get size of all input protos"""
    return len(self.datagen_object)

  def _to_list(self, input_protos: Iterator) -> List:
    """Parse protos iterator to list."""
    return list(input_protos)

  def _extract_protos(self) -> None:
    """Create input image protos for each data generator item."""
    raise NotImplementedError()

  def get_protos(self, input_ids: List[int]
                ) -> Tuple[List[resources_pb2.Input], List[resources_pb2.Annotation]]:
    """Get input and annotation protos based on input_ids.
    Args:
      input_ids: List of input IDs to retrieve the protos for.
    Returns:
      Input and Annotation proto iterators for the specified input IDs.
    """
    input_protos, annotation_protos = self._extract_protos(input_ids)

    return input_protos, annotation_protos


class ClarifaiDataLoader:
  """Clarifai data loader base class."""

  def __init__(self, split: str) -> None:
    pass

  def load_data(self) -> None:
    raise NotImplementedError()

  def __len__(self) -> int:
    raise NotImplementedError()

  def __getitem__(self, index: int) -> OutputFeaturesType:
    raise NotImplementedError()
