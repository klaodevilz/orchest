"""Module to interact with the parameters inside the ``pipeline.json``."""
import json
from typing import Any, Dict

from orchest.config import Config
from orchest.errors import StepUUIDResolveError
from orchest.pipeline import Pipeline
from orchest.utils import get_step_uuid


def get_params() -> Dict[str, Any]:
    """Gets the parameters of the current step.

    Returns:
        The parameters of the current step.
    """
    with open(Config.PIPELINE_DESCRIPTION_PATH, 'r') as f:
        pipeline_description = json.load(f)

    pipeline = Pipeline.from_json(pipeline_description)
    try:
        step_uuid = get_step_uuid(pipeline)
    except StepUUIDResolveError:
        raise StepUUIDResolveError('Failed to determine from where to get data.')

    step = pipeline.get_step_by_uuid(step_uuid)
    params = step.get_params()

    return params


def update_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """Updates the parameters of the current step.

    Additionally, you can set new parameters by giving parameters that
    do not yet exist in the current parameters of the pipeline step.

    Internally the updating is done by calling the ``dict.update``
    method. This further explains the behavior of this method.

    Args:
        params: The parameters to update. Either updating their values
            or adding new parameter keys.

    Returns:
        The updated parameters mapping.

    """
    with open(Config.PIPELINE_DESCRIPTION_PATH, 'r') as f:
        pipeline_description = json.load(f)

    pipeline = Pipeline.from_json(pipeline_description)
    try:
        step_uuid = get_step_uuid(pipeline)
    except StepUUIDResolveError:
        raise StepUUIDResolveError('Failed to determine from where to get data.')

    # TODO: This is inefficient, we could just use the `step_uuid` and
    #       update the params of the `pipeline_description` and write it
    #       back to the `pipeline.json`. However, I think it is good
    #       practice to use our own defined classes to do so.
    step = pipeline.get_step_by_uuid(step_uuid)
    curr_params = step.get_params()
    curr_params.update(params)

    with open(Config.PIPELINE_DESCRIPTION_PATH, 'w') as f:
        json.dump(pipeline.to_dict(), f)

    return curr_params
