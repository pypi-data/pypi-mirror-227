import json
import logging
import os
import urllib.parse
from typing import Any, Dict, List, Optional, Union
from deprecated import deprecated
import requests
from plato_client import CACHE, CONFIG
from plato_client.core.auth import AuthProviderConfig, Plato_Auth
from plato_client.core.connection.broker import PlatoEnvironment
from plato_client.core.image.imageservice import ImageService
from plato_client.core.models import PlatoUser
from plato_client.core.text.textservice import TextService

SUPPORTED_MODELS = ["OpenAi", "Palm"]
DEFAULT_MODEL_FAMILY = "OpenAi"
logger = logging.getLogger(__name__)


class PlatoClient:
    """Plato Client to interact with Plato Core APIs

    Args:
        env (str, optional): Environment to point to. Defaults to None.
        app_credentials (AuthProviderConfig, optional): App credentials to use for authentication. Defaults to None.
        use_provider (bool, optional): Whether to use the provider or not. Defaults to True.
        endpoint (str, optional): Endpoint to use. Defaults choosing hardcoded value specified by `env`.

    Usage Examples:
    (Todo: expand them more)
        >>> from aag_plato import PlatoClient
        >>> client = PlatoClient(endpoint="http://0.0.0.0:8080/plato-broker")
        >>> client.generate_text(
        ...     user_id="testuser",
        ...     model_family="OpenAi",
        ...     prompt="Which artist sings Rap God?",
        ... )
    """

    def __init__(
        self,
        env: Union[str, PlatoEnvironment] = None,
        app_credentials: Optional[AuthProviderConfig] = None,
        use_provider: bool = True,
        endpoint: str = None,
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing Plato Client...")

        if env is None:
            env = CONFIG.get("env", PlatoEnvironment.DEVELOPMENT)
        assert (
            env in PlatoEnvironment.list()
        ), f"'env' value should be one of {PlatoEnvironment.list()}, provided: {env}"
        self.plato_core_url = endpoint or CONFIG.get(f"broker.url.{env}")

        self.logger.debug( f"Using environment: {env} with URL: {self.plato_core_url}" )

        self._text_service = TextService(self.plato_core_url)
        self._image_service = ImageService(self.plato_core_url)

        # Authenticate the app with the Plato Core using Client Credentials flow
        self.logger.debug("Authenticating App with Plato Core...")
        if app_credentials is not None:
            self.client_id = app_credentials.client_id
            self.auth = Plato_Auth(app_credentials)
            self.token = self.auth.get_token_client_credentials()
        else:
            self.logger.warning("Authentication disabled - some apis may not work!")
            self.client_id = None
            self.auth = None
            self.token = None

        self.use_provider = use_provider
        # self.app_id = self.auth.get_app_id()

    # -- helpers --
    def _send_request(
        self,
        path: str,
        method: str,
        json_data=None,
        data=None,
        files=None,
        stream: bool = False,
        **kwargs,
    ):
        """Helper function to send requests to Plato Core

        Args:
            path (str): path to send request to
            method (str): http method
            json_data (dict, optional): json data to send. Defaults to None.
            data (dict, optional): query params. Defaults to None.
            files (dict, optional): files to send. Defaults to None.

        """
        headers = {}
        if self.token is not None:
            headers = {"Authorization": f"Bearer {self.token}"}

        base_url = f"{self.plato_core_url}/{path}"

        payload = {}
        if json_data:
            payload.update(json_data)

        if data:
            base_url += "?" + urllib.parse.urlencode(data)

        logger.debug(
            f"request: {method.upper()} {base_url} headers={headers}, data={payload}, files={files}"
        )
        if files is not None:
            _files = dict([(file, open(pth, "rb")) for file, pth in files.items()])
        else:
            _files = None
        response = requests.request(
            method.upper(),
            base_url,
            headers=headers,
            json=payload,  # note that json param ensures 'Content-Type': 'application/json' header
            files=_files,
            stream=stream,
            **kwargs,
        )
        if _files is not None:
            for file in _files.values():
                file.close()
        if response.status_code == 200:
            if "chunked" in response.headers.get("Transfer-Encoding", ""):
                # streaming response
                return response.iter_content(decode_unicode=True)
            else:
                return response.json()
        else:
            self.logger.exception(
                f"Request failed with status code:{response.status_code}\n{response.text}"
            )
            return None

    def _prep_payload(
        self,
        user_id: Optional[str],
        model_family: str,
        prompt: Optional[str],
        context: Optional[Union[str, List[Dict[str, Any]]]],
        image: Optional[str],
        mask: Optional[str],
        audio: Optional[str],
        model_params: Dict[str, Any],
        operation: str,
        runtime_config: Optional[dict],
        stream=False,
    ):
        """
        Prepare payload for text/image generation request

        Args:
            user_id (Optional[str]): User ID to use for the request
            model_family (str): Model family to use for the request
            prompt (Optional[str]): Prompt to use for the request
            context (Optional[Union[str, List[Dict[str, Any]]]]): Context to use for the request
            image (Optional[str]): Image to use for the request
            mask (Optional[str]): Mask to use for the request
            audio (Optional[str]): Audio to use for the request
            model_params (Dict[str, Any]): Model params to use for the request
            operation (str): Operation to perform
            stream (bool, optional): Whether to stream the response or not. Defaults to False.

        Raises:
            Exception: If model family is not supported
        """
        if model_family is None:
            model_family = DEFAULT_MODEL_FAMILY
        assert (
            model_family in SUPPORTED_MODELS
        ), f"Model family should be one of {SUPPORTED_MODELS}, provided: {model_family}"
        files = {}
        if model_params is None:
            model_params = {}
        if stream:
            model_params["stream"] = True
        data = {
            "user_id": user_id,
            "model_family": model_family,
            "model_params": json.dumps(model_params),
            "operation": operation,
            "runtime_config": json.dumps(runtime_config),
        }
        if prompt is not None:
            data["prompt"] = prompt
        if context is not None:
            try:
                if isinstance(context, str):
                    data["context"] = context
                elif isinstance(context, list):
                    data["history"] = json.dumps(context)
            except Exception as exc:
                self.logger.error(
                    f"Invalid format for context provided; needs to be either a string or a list of dicts\n: {exc}"
                )
                raise
        # if image is not None:
        #     with open(image, 'rb') as f:
        #         files["image"] = (os.path.basename(image), f)
        # if mask is not None:
        #     with open(mask, 'rb') as f:
        #         files["mask"] = (os.path.basename(mask), f)
        # if audio is not None:
        #     with open(audio, 'rb') as f:
        #         files["audio"] = (os.path.basename(audio), f)

        if image is not None:
            files["image"] = image
        if mask is not None:
            files["mask"] = mask
        if audio is not None:
            files["audio"] = audio
        return data, files

    # -- user management --
    def get_user(self) -> Optional[PlatoUser]:
        """
        Get the current user info;
        If authentication is enabled and user is logged in then returns the user info else returns None

        Returns:
            Optional[PlatoUser]: PlatoUser object

        Raises:
            Exception: If authentication is not enabled
        """
        if self.auth is not None:
            return self.auth.get_user_info(use_provider=self.use_provider)
        else:
            return None

    # -- document management --
    def upload_documents(
        self,
        user_id: str,
        document_paths: List[str],
        file_types: List[str],
        semantic_search: bool = False,
        keyword_search: bool = False,
    ):
        """
        Upload documents to the user's library

        Args:
            user_id (str): User ID to use for the request
            document_paths (List[str]): List of paths to the documents to upload
            file_types (List[str]): List of file types for the documents to upload
            semantic_search (bool, optional): Whether to enable semantic search for the documents. Defaults to False.
            keyword_search (bool, optional): Whether to enable keyword search for the documents. Defaults to False.

        Returns:
            Dict: Response from the server

        """

        raise NotImplementedError(
            "Still under construction"
        )  # Todo: remove this line when Plato Core endpoint for this is ready

        self.logger.debug("Uploading documents...")
        assert len(document_paths) == len(file_types)
        res = self._send_request(
            "upload_documents",
            "POST",
            json={
                "user_id": user_id,
                "file_types": file_types,
                "semantic_search": semantic_search,
                "keyword_seach": keyword_search,
            },
            data={"document_paths": document_paths},
        )
        return {"response": res}

    def download_documents(
        self,
        user_id: str,
        document_ids: List[str],
    ) -> Dict:
        """
        Download documents from the user's library"

        Args:
            user_id (str): User ID to use for the request
            document_ids (List[str]): List of document IDs to download

        Returns:
            Dict: Response from the server

        """

        raise NotImplementedError(
            "Still under construction"
        )  # Todo: remove this line when Plato Core endpoint for this is ready

        self.logger.debug("Downloading documents...")
        downloaded_files = {}
        for document_id in document_ids:
            res = self._send_request(
                f"download_documents/{self.client_id}/{user_id}/{document_id}",
                "GET",
                json={
                    "user_id": user_id,
                    "document_id": document_id,
                },
            )
            if res is None:
                self.logger.error(f"Failed to download document: {document_id}")
                continue
            document_name = res.headers.get(
                "Content-Disposition", f"{document_id}.unknown"
            )
            download_path = os.path.join(CACHE, document_name)
            with open(download_path, "wb") as f:
                f.write(res.content)

            downloaded_files[document_id] = download_path

        return downloaded_files

    def find_documents(self, user_id: str, filter_expression: str) -> List[str]:
        """
        Find documents in the user's library

        Args:
            user_id (str): User ID to use for the request
            filter_expression (str): Filter to use for the request

        Returns:
            List[str]: List of document IDs that match the filter_expression

        """

        raise NotImplementedError(
            "Still under construction"
        )  # Todo: remove this line when Plato Core endpoint for this is ready

        self.logger.debug("Finding documents...")
        res = self._send_request(
            "find_documents",
            "POST",
            json={
                "user_id": user_id,
                "filter": filter_expression,
            },
        )
        return {"response": res}

    def delete_documents(self, user_id: str, document_ids: List[str]) -> None:
        """
        Delete documents from the user's library

        Args:
            user_id (str): User ID to use for the request
            document_ids (List[str]): List of document IDs to delete

        Returns:
            Dict: Response from the server

        """

        raise NotImplementedError(
            "Still under construction"
        )  # Todo: remove this line when Plato Core endpoint for this is ready

        self.logger.debug("Deleting documents...")
        res = self._send_request(
            "delete_documents",
            "DELETE",
            json={
                "user_id": user_id,
                "document_ids": document_ids,
            },
        )
        return {"response": res}

    # -- model training --
    def train_model(self, train_file_path: str, val_file_path: Optional[str] = None):
        """
        Train a model using Plato Core

        Args:
            train_file_path (str): Path to the training file
            val_file_path (Optional[str], optional): Path to the validation file. Defaults to None.

        Returns:
            Dict: Response from the server

        """

        raise NotImplementedError(
            "Still under construction"
        )  # Todo: remove this line when Plato Core endpoint for this is ready

        self.logger.debug("Training model...")
        # files = {"train": open(train_file_path, "rb"), "val": open(val_file_path, "rb")}
        res = self._send_request(
            "train_model",
            "POST",
            data={"train_file_path": train_file_path, "val_file_path": val_file_path},
        )

        return {"response": res}

    # -- content creation --
    @deprecated("Deprecated in favor of generate_text")
    def text_completion(self, text: str, **kwargs):
        """Generate text using Plato Core"""
        logger.warning(
            "text_completion is deprecated in favor of generate_text starting verison 0.1.0 and will be removed in future versions"
        )
        return self._text_service.text_completion(text=text, **kwargs)

    @deprecated("Deprecated in favor of generate_text")
    def chat_completion(self, **kwargs):
        """Generate chat using Plato Core"""
        logger.warning(
            "chat_completion is deprecated in favor of generate_text starting verison 0.1.0 and will be removed in future versions"
        )
        return self._text_service.chat_completion(**kwargs)

    @deprecated("Deprecated in favor of generate_image")
    def create_images(self, **kwargs):
        """Generate images using Plato Core"""
        logger.warning(
            "create_images is deprecated in favor of generate_image starting verison 0.1.0 and will be removed in future versions"
        )
        return self._image_service.create(**kwargs)

    def _post_process(self, res, verbose: bool):
        _res = []
        if isinstance(res, str):
            res = [res]

        for r in res:
            try:
                _res.append(json.loads(r))
            except:
                _res.append(r)

        if len(_res) == 1:
            if verbose:
                return _res[0]
            else:
                return (
                    _res[0]["result"][0]
                    if isinstance(_res[0]["result"], list)
                    and len(_res[0]["result"]) == 1
                    else _res[0]["result"]
                )
        else:
            if verbose:
                return _res
            else:
                return [
                    r["result"][0]
                    if isinstance(r["result"], list) and len(r["result"]) == 1
                    else r["result"]
                    for r in _res
                ]

    def generate_text_stream(
        self,
        user_id: Optional[str] = None,
        model_family: str = "OpenAI",
        prompt: Optional[str] = None,
        context: Optional[Union[str, List[Dict[str, Any]]]] = None,
        image: Optional[str] = None,
        mask: Optional[str] = None,
        audio: Optional[str] = None,
        model_params: Dict[str, Any] = None,
        operation: str = "auto",
        runtime_config: Optional[dict] = None,
        verbose: bool = False,
    ) -> Dict[str, Any]:
        """
        Generate streaming text using Plato Core

        Args:
            user_id (Optional[str], optional): User ID to use for the request. Defaults to None.
            model_family (str, optional): Model family to use for the request. Defaults to "OpenAI".
            prompt (Optional[str], optional): Prompt to use for the request. Defaults to None.
            context (Optional[Union[str, List[Dict[str, Any]]]], optional): Context to use for the request. Defaults to None.
            image (Optional[str], optional): Image to use for the request. Defaults to None.
            mask (Optional[str], optional): Mask to use for the request. Defaults to None.
            audio (Optional[str], optional): Audio to use for the request. Defaults to None.
            model_params (Dict[str, Any], optional): Model parameters to use for the request. Defaults to None.
            operation (str, optional): Operation to use for the request. Defaults to "auto".
            runtime_config (Optional[dict], optional): Runtime configuration to use for the request. Defaults to None.

        Returns:
            Dict[str, Any]: Response from the server

        Raises:
            ValueError: If the model family is not supported

        Example Usage:

            >>> from aag_plato import PlatoClient
            >>> client = PlatoClient()
            >>> for response in client.generate_text_stream(prompt="Tell me a story"):
            >>>     print(response)

        """
        self.logger.debug(f"Generating text via {model_family}...")

        data, files = self._prep_payload(
            user_id,
            model_family,
            prompt,
            context,
            image,
            mask,
            audio,
            model_params,
            operation,
            runtime_config,
            stream=True,
        )

        res = self._send_request(
            "generate/generate_text",
            "POST",
            data=data,
            files=files,
            stream=True,
        )

        for r in res:
            yield r
            # _r = json.loads(r)
            # if verbose:
            #     yield _r
            # else:
            #     yield _r["result"][0]

    def generate_text(
        self,
        user_id: Optional[str] = None,
        model_family: str = "OpenAI",
        prompt: Optional[str] = None,
        context: Optional[Union[str, List[Dict[str, Any]]]] = None,
        image: Optional[str] = None,
        mask: Optional[str] = None,
        audio: Optional[str] = None,
        model_params: Dict[str, Any] = None,
        operation: str = "auto",
        runtime_config: Optional[dict] = None,
        verbose: bool = False,
    ) -> Dict[str, Any] | str | List[str]:
        """
        Generate text using Plato Core

        Args:
            user_id (Optional[str], optional): User ID to use for the request. Defaults to None.
            model_family (str, optional): Model family to use for the request. Defaults to "OpenAI".
            prompt (Optional[str], optional): Prompt to use for the request. Defaults to None.
            context (Optional[Union[str, List[Dict[str, Any]]]], optional): Context to use for the request. Defaults to None.
            image (Optional[str], optional): Image to use for the request. Defaults to None.
            mask (Optional[str], optional): Mask to use for the request. Defaults to None.
            audio (Optional[str], optional): Audio to use for the request. Defaults to None.
            model_params (Dict[str, Any], optional): Model parameters to use for the request. Defaults to None.
            operation (str, optional): Operation to use for the request. Defaults to "auto".
                Must be one of the supported operations unders plato-broker/src/core/models.py:LmOperation or "auto"
                valid operation strings are:
                    TEXT_COMPLETION
                    TEXT_EDITING
                    TEXT_CHAT
                    AUDIO_TRANSCRIPTION
                    AUDIO_TRANSLATION
                    IMAGE_QNA
                    IMAGE_CAPTIONING
                    IMAGE_VARIATION
                    IMAGE_INPAINTING_WITH_MASK
                    IMAGE_INPAINTING
                    IMAGE_GENERATION
                    TEXT_EMBEDDING
                Note: It is best to just use "auto" and let the Plato framework identify the appropriate operation to perform based
                on your input combination, unless you have a very clear idea of what you are trying to do
            runtime_config (Optional[dict], optional): Runtime configuration to use for the request. Defaults to None.
            verbose (bool, optional): Whether to return the full response or just the generated text. Defaults to False.

        Returns:
            Dict[str, Any]: Response from the server

        Raises:
            ValueError: If the model family is not supported

        Example Usage:

            >>> from aag_plato import PlatoClient
            >>> client = PlatoClient()
            >>> client.generate_text(prompt="Tell me a funny story")

        """
        self.logger.debug(f"Generating text via {model_family}...")
        data, files = self._prep_payload(
            user_id,
            model_family,
            prompt,
            context,
            image,
            mask,
            audio,
            model_params,
            operation,
            runtime_config,
        )

        res = self._send_request(
            "generate/generate_text",
            "POST",
            data=data,
            files=files,
        )
        return self._post_process(res, verbose)

    def generate_image(
        self,
        user_id: Optional[str] = None,
        model_family: str = "OpenAI",
        prompt: Optional[str] = None,
        context: Optional[Union[str, List[Dict[str, Any]]]] = None,
        image: Optional[str] = None,
        mask: Optional[str] = None,
        audio: Optional[str] = None,
        model_params: Dict[str, Any] = None,
        operation: str = "auto",
        runtime_config: Optional[dict] = None,
        verbose: bool = False,
    ) -> Dict[str, Any] | str | List[str]:
        """
        Generate image using Plato Core

        Args:
            user_id (Optional[str], optional): User ID to use for the request. Defaults to None.
            model_family (str, optional): Model family to use for the request. Defaults to "OpenAI".
            prompt (Optional[str], optional): Prompt to use for the request. Defaults to None.
            context (Optional[Union[str, List[Dict[str, Any]]]], optional): Context to use for the request. Defaults to None.
            image (Optional[str], optional): Image to use for the request. Defaults to None.
            mask (Optional[str], optional): Mask to use for the request. Defaults to None.
            audio (Optional[str], optional): Audio to use for the request. Defaults to None.
            model_params (Dict[str, Any], optional): Model parameters to use for the request. Defaults to None.
            operation (str, optional): Operation to use for the request. Defaults to "auto".
                Must be one of the supported operations unders plato-broker/src/core/models.py:LmOperation or "auto"
                valid operation strings are:
                    TEXT_COMPLETION
                    TEXT_EDITING
                    TEXT_CHAT
                    AUDIO_TRANSCRIPTION
                    AUDIO_TRANSLATION
                    IMAGE_QNA
                    IMAGE_CAPTIONING
                    IMAGE_VARIATION
                    IMAGE_INPAINTING_WITH_MASK
                    IMAGE_INPAINTING
                    IMAGE_GENERATION
                    TEXT_EMBEDDING
                Note: It is best to just use "auto" and let the Plato framework identify the appropriate operation to perform based
                on your input combination, unless you have a very clear idea of what you are trying to do
            runtime_config (Optional[dict], optional): Runtime configuration to use for the request. Defaults to None.
            verbose (bool, optional): Whether to return the full response or just the generated text. Defaults to False.

        Returns:
            Dict[str, Any]: Response from the server

        Raises:
            ValueError: If the model family is not supported

        Example Usage:
            >>> from aag_plato import PlatoClient
            >>> client = PlatoClient()
            >>> client.generate_image(
            ...     model_family="OpenAi",
            ...     prompt="A painting of a cat",
            ... )

        """
        self.logger.debug(f"Generating image via {model_family}...")
        data, files = self._prep_payload(
            user_id,
            model_family,
            prompt,
            context,
            image,
            mask,
            audio,
            model_params,
            operation,
            runtime_config,
        )
        res = self._send_request(
            "generate/generate_image",
            "POST",
            data=data,
            files=files,
        )
        return self._post_process(res, verbose)

    def generate_embedding(
        self,
        user_id: Optional[str] = None,
        model_family: str = "OpenAI",
        prompt: Optional[str] = None,
        context: Optional[Union[str, List[Dict[str, Any]]]] = None,
        image: Optional[str] = None,
        mask: Optional[str] = None,
        audio: Optional[str] = None,
        model_params: Dict[str, Any] = None,
        operation: str = "auto",
        runtime_config: Optional[dict] = None,
        verbose: bool = False,
    ) -> Dict[str, Any] | float | List[float]:
        """
        Generate embedding using Plato Core; this is useful for downstream tasks such as classification or clustering of generated content.

        Args:
            user_id (Optional[str], optional): User ID to use for the request. Defaults to None.
            model_family (str, optional): Model family to use for the request. Defaults to "OpenAI".
            prompt (Optional[str], optional): Prompt to use for the request. Defaults to None.
            context (Optional[Union[str, List[Dict[str, Any]]]], optional): Context to use for the request. Defaults to None.
            image (Optional[str], optional): Image to use for the request. Defaults to None.
            mask (Optional[str], optional): Mask to use for the request. Defaults to None.
            audio (Optional[str], optional): Audio to use for the request. Defaults to None.
            model_params (Dict[str, Any], optional): Model parameters to use for the request. Defaults to None.
            operation (str, optional): Operation to use for the request. Defaults to "auto".
                Must be one of the supported operations unders plato-broker/src/core/models.py:LmOperation or "auto"
                valid operation strings are:
                    TEXT_COMPLETION
                    TEXT_EDITING
                    TEXT_CHAT
                    AUDIO_TRANSCRIPTION
                    AUDIO_TRANSLATION
                    IMAGE_QNA
                    IMAGE_CAPTIONING
                    IMAGE_VARIATION
                    IMAGE_INPAINTING_WITH_MASK
                    IMAGE_INPAINTING
                    IMAGE_GENERATION
                    TEXT_EMBEDDING
                Note: It is best to just use "auto" and let the Plato framework identify the appropriate operation to perform based
                on your input combination, unless you have a very clear idea of what you are trying to do
            runtime_config (Optional[dict], optional): Runtime configuration to use for the request. Defaults to None.
            verbose (bool, optional): Whether to return the full response or just the generated text. Defaults to False.

        Returns:
            Dict[str, Any]: Response from the server

        Raises:
            ValueError: If the model family is not supported

        Example Usage:
            >>> from aag_plato import PlatoClient
            >>> client = PlatoClient()
            >>> client.generate_embedding(
            ...     model_family="OpenAi",
            ...     prompt="Egypt reached the pinnacle of its power in the New Kingdom, ruling much of Nubia and a sizable portion of the Levant, after which it entered a period of slow decline. During the course of its history, Egypt was invaded or conquered by a number of foreign powers, including the Hyksos, the Libyans, the Nubians, the Assyrians, the Achaemenid Persians, and the Macedonians under Alexander the Great. The Greek Ptolemaic Kingdom, formed in the aftermath of Alexander's death, ruled Egypt until 30 BC, when, under Cleopatra, it fell to the Roman Empire and became a Roman province.",
            ... )
        """
        self.logger.debug(f"Generating embedding via {model_family}...")
        data, files = self._prep_payload(
            user_id,
            model_family,
            prompt,
            context,
            image,
            mask,
            audio,
            model_params,
            operation,
            runtime_config,
        )
        res = self._send_request(
            "generate/generate_embedding",
            "POST",
            data=data,
            files=files,
        )
        return self._post_process(res, verbose)

    def generate_audio(
        self,
        user_id: Optional[str] = None,
        model_family: str = "OpenAI",
        prompt: Optional[str] = None,
        context: Optional[Union[str, List[Dict[str, Any]]]] = None,
        image: Optional[str] = None,
        mask: Optional[str] = None,
        audio: Optional[str] = None,
        model_params: Dict[str, Any] = None,
        operation: str = "auto",
        verbose: bool = False,
    ) -> Dict[str, Any] | str | List[str]:
        raise NotImplementedError("Audio generation is not yet supported")

    def generate_video(
        self,
        user_id: Optional[str] = None,
        model_family: str = "OpenAI",
        prompt: Optional[str] = None,
        context: Optional[Union[str, List[Dict[str, Any]]]] = None,
        image: Optional[str] = None,
        mask: Optional[str] = None,
        audio: Optional[str] = None,
        model_params: Dict[str, Any] = None,
        operation: str = "auto",
        verbose: bool = False,
    ) -> Dict[str, Any] | str | List[str]:
        raise NotImplementedError("Video generation is not yet supported")
