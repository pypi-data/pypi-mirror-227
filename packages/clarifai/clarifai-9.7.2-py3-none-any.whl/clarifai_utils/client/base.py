import os
from datetime import datetime
from typing import Any, Callable

from google.protobuf.json_format import MessageToDict  # noqa
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.wrappers_pb2 import BoolValue

from clarifai.client.auth import create_stub
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.errors import ApiError, UserError


class BaseClient:
  """BaseClient is the base class for all the classes interacting with Clarifai endpoints.

  Args:
      **kwargs: Additional keyword arguments to be passed to the ClarifaiAuthHelper.
          - user_id (str): A user ID for authentication.
          - app_id (str): An app ID for the application to interact with.
          - pat (str): A personal access token for authentication.
          - base (str): The base URL for the API endpoint. Defaults to 'https://api.clarifai.com'.
          - ui (str): The URL for the UI. Defaults to 'https://clarifai.com'.

  Attributes:
      auth_helper (ClarifaiAuthHelper): An instance of ClarifaiAuthHelper for authentication.
      STUB (Stub): The gRPC Stub object for API interaction.
      metadata (tuple): The gRPC metadata containing the personal access token.
      userDataObject (UserAppIDSet): The protobuf object representing user and app IDs.
      base (str): The base URL for the API endpoint.
  """

  def __init__(self, **kwargs):
    pat = os.environ.get('CLARIFAI_PAT', "")
    if pat == "":
      raise UserError("CLARIFAI_PAT must be set as env vars")
    self.auth_helper = ClarifaiAuthHelper(**kwargs, pat=pat, validate=False)
    self.STUB = create_stub(self.auth_helper)
    self.metadata = self.auth_helper.metadata
    self.user_app_id = self.auth_helper.get_user_app_id_proto()
    self.base = self.auth_helper.base

  def _grpc_request(self, method: Callable, argument: Any):
    """Makes a gRPC request to the API.

    Args:
        method (Callable): The gRPC method to call.
        argument (Any): The argument to pass to the gRPC method.

    Returns:
        res (Any): The result of the gRPC method call.
    """

    try:
      res = method(argument)
      # MessageToDict(res) TODO global debug logger
      return res
    except ApiError:
      raise Exception("ApiError")

  def convert_string_to_timestamp(self, date_str) -> Timestamp:
    """Converts a string to a Timestamp object.

    Args:
        date_str (str): The string to convert.

    Returns:
        Timestamp: The converted Timestamp object.
    """
    # Parse the string into a Python datetime object
    try:
      datetime_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
      datetime_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')

    # Convert the datetime object to a Timestamp object
    timestamp_obj = Timestamp()
    timestamp_obj.FromDatetime(datetime_obj)

    return timestamp_obj

  def process_response_keys(self, old_dict, listing_resource):
    """Converts keys in a response dictionary to resource proto format.

    Args:
        old_dict (dict): The dictionary to convert.

    Returns:
        new_dict (dict): The dictionary with processed keys.
    """
    old_dict[f'{listing_resource}_id'] = old_dict['id']
    old_dict.pop('id')

    def convert_recursive(item):
      if isinstance(item, dict):
        new_item = {}
        for key, value in item.items():
          if key in ['created_at', 'modified_at', 'completed_at']:
            value = self.convert_string_to_timestamp(value)
          elif key in ['workflow_recommended']:
            value = BoolValue(value=True)
          elif key in ['metadata', 'fields_map', 'params']:
            continue  # TODO Fix "app_duplication",proto struct
          new_item[key] = convert_recursive(value)
        return new_item
      elif isinstance(item, list):
        return [convert_recursive(element) for element in item]
      else:
        return item

    new_dict = convert_recursive(old_dict)
    return new_dict
