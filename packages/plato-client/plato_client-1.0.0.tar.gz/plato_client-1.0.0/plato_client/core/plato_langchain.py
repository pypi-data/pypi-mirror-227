import logging
from typing import Any, Dict, List, Mapping, Optional, Union, Generator

from langchain.callbacks.manager import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain.llms.base import LLM, Generation, LLMResult
from pydantic import BaseModel

logger = logging.getLogger(__name__)


def merge_dicts(d1: Optional[Dict] = None, d2: Optional[Dict] = None):
    if d2 is None:
        return d1
    if d1 is None and d2 is not None:
        return d2
    d1 = d1.copy()
    for key, value in d2.items():
        if value is not None:
            d1[key] = value
    return d1


class PlatoMeta(BaseModel):
    tokens_sent: Optional[int] = 0
    tokens_received: Optional[int] = 0
    cost: Optional[float] = 0.0
    latency: Optional[float] = 0.0
    params: Optional[Dict] = {}


class PlatoResult(BaseModel):
    result: Optional[Union[str, List[str], List[List[float]]]] = None
    raw: Dict[str, Any] = {}
    meta: PlatoMeta = PlatoMeta()
    cached: Optional[bool] = False
    moderated: Optional[bool] = False
    anonymized: Optional[bool] = False


class _PlatoCommon(BaseModel):
    client: Any
    default_model_family: Optional[str] = None
    default_params: Optional[Dict[str, Any]] = None
    default_runtime_config: Optional[Dict[str, Any]] = None


class PlatoLLM(_PlatoCommon, LLM):
    
    streaming: bool = False
    """Whether to stream the results or not."""

    @property
    def _llm_type(self) -> str:
        return "plato-llm"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {}

    def _call(
        self,
        prompt,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs,
    ):
        try:
            # no stream
            params = {
                "user_id": kwargs.get("user_id", None),
                "model_family": kwargs.get("model_family", None)
                if kwargs.get("model_family", None) is not None
                else self.default_model_family,
                "prompt": prompt,
                "context": kwargs.get("context", None),
                "image": kwargs.get("image", None),
                "mask": kwargs.get("mask", None),
                "audio": kwargs.get("audio", None),
                "model_params": merge_dicts(
                    self.default_params, kwargs.get("model_params", None)
                ),
                "operation": "auto",
                "runtime_config": merge_dicts(
                    self.default_runtime_config, kwargs.get("runtime_config", None)
                ),
                "verbose": True,
            }

            response = PlatoResult(**self.client.generate_text(**params))

            if run_manager is not None and hasattr(run_manager, "on_llm_end"):
                # Map PlatoResult -> LLMResult
                if isinstance(response.result, list):
                    # this maping needs to be validated; im not sure if response.raw would also be a list of dict in this case
                    generations = [
                        Generation(text=generation, generation_info=response.raw)
                        for generation in response.result
                    ]
                elif isinstance(response.result, str):
                    generations = [
                        Generation(text=response.result, generation_info=response.raw)
                    ]
                else:
                    raise ValueError(
                        f"Unsupported type for Plato response returned by PlatoClient: {type(response.result)} - must be str or List[str]"
                    )
                llm_result = LLMResult(
                    generations=[generations], llm_output=response.raw
                )
                run_manager.on_llm_end(llm_result)

            if isinstance(response.result, list) and len(response.result) == 1:
                return response.result[0]
            else:
                return response.result

        except Exception as e:
            if run_manager:
                run_manager.on_llm_error(e)
            raise e

    async def _acall(
        self,
        prompt,
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs,
    ):
        try:
            params = {
                "user_id": kwargs.get("user_id", None),
                "model_family": kwargs.get("model_family", None)
                if kwargs.get("model_family", None) is not None
                else self.default_model_family,
                "prompt": prompt,
                "context": kwargs.get("context", None),
                "image": kwargs.get("image", None),
                "mask": kwargs.get("mask", None),
                "audio": kwargs.get("audio", None),
                "model_params": merge_dicts(
                    self.default_params, kwargs.get("model_params", None)
                ),
                "operation": "auto",
                "runtime_config": merge_dicts(
                    self.default_runtime_config, kwargs.get("runtime_config", None)
                ),
                "verbose": True,
            }
            if kwargs["stream"] if (kwargs.get("stream", None) is not None) else self.streaming:
                response = []
                for resp in self.client.generate_text_stream(**params):
                    #_response = PlatoResult(**resp)
                    _response = PlatoResult(result = resp)
                    if run_manager:
                        if isinstance(_response.result, str):
                            await run_manager.on_llm_new_token(_response.result)
                        else:
                            raise ValueError(
                                f"Unsupported type for Plato response returned by PaltoClient: {type(_response.result)} - must be str or List[str]"
                            )
                    response.append(_response)
            else:
                # no stream
                response = PlatoResult(**self.client.generate_text(**params))

            if run_manager is not None and hasattr(run_manager, "on_llm_end"):
                # Map PlatoResult -> LLMResult
                if isinstance(response, PlatoResult):
                    response = [response]
                assert isinstance(
                    response, list
                ), f"Expected a List[PlatoResult], got {type(response)}"
                for resp in response:
                    if isinstance(resp.result, list):
                        # this maping needs to be validated; im not sure if resp.raw would also be a list of dict in this case
                        generations = [
                            Generation(text=generation, generation_info=resp.raw)
                            for generation in resp.result
                        ]
                    elif isinstance(resp.result, str):
                        generations = [
                            Generation(text=resp.result, generation_info=resp.raw)
                        ]
                    else:
                        raise ValueError(
                            f"Unsupported type for Plato response returned by PlatoClient: {type(resp.result)} - must be str or List[str]"
                        )
                    llm_result = LLMResult(
                        generations=[generations], llm_output=resp.raw
                    )
                await run_manager.on_llm_end(llm_result)

            if isinstance(response, list):
                processed_result = "".join([r for resp in response for r in resp.result])
            elif isinstance(response, PlatoResult):
                processed_result = "".join(r for r in response.result)  # could be a  alist
            else:
                raise ValueError(
                    f"Unsupported type for Plato response returned by PlatoClient: {type(response)} - must be str or List[str]"
                )

            if isinstance(processed_result, list) and len(processed_result) == 1:
                return processed_result[0]
            else:
                return processed_result

        except Exception as e:
            if run_manager:
                await run_manager.on_llm_error(e)
            raise e


    def stream(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> Generator:
        """Invoke PlatoLLM text streaming geenration and return the resulting generator.

        BETA: this is a beta feature while we figure out the right abstraction.
        Once that happens, this interface could change.

        Args:
            prompt: The prompts to pass into the model.
            stop: Optional list of stop words to use when generating.

        Returns:
            A generator representing the stream of tokens from underlying model.

        Example:
            .. code-block:: python

                generator = openai.stream("Tell me a joke.")
                for token in generator:
                    yield token
        """
        #params = self.prep_streaming_params(stop)
        #generator = self.client.create(prompt=prompt, **params)
        params = {
            "user_id": kwargs.get("user_id", None),
            "model_family": kwargs.get("model_family", None)
            if kwargs.get("model_family", None) is not None
            else self.default_model_family,
            "context": kwargs.get("context", None),
            "image": kwargs.get("image", None),
            "mask": kwargs.get("mask", None),
            "audio": kwargs.get("audio", None),
            "model_params": merge_dicts(
                self.default_params, kwargs.get("model_params", None)
            ),
            "operation": "auto",
            "runtime_config": merge_dicts(
                self.default_runtime_config, kwargs.get("runtime_config", None)
            ),
            "verbose": True,
        }
        r = self.client.generate_text_stream(prompt=prompt, **params)

        return r

