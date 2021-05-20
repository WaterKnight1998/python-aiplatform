# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import abc
from typing import Awaitable, Callable, Dict, Optional, Sequence, Union
import packaging.version
import pkg_resources

import google.auth  # type: ignore
import google.api_core  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore

from google.cloud.aiplatform_v1beta1.types import study
from google.cloud.aiplatform_v1beta1.types import study as gca_study
from google.cloud.aiplatform_v1beta1.types import vizier_service
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-aiplatform",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()

try:
    # google.auth.__version__ was added in 1.26.0
    _GOOGLE_AUTH_VERSION = google.auth.__version__
except AttributeError:
    try:  # try pkg_resources if it is available
        _GOOGLE_AUTH_VERSION = pkg_resources.get_distribution("google-auth").version
    except pkg_resources.DistributionNotFound:  # pragma: NO COVER
        _GOOGLE_AUTH_VERSION = None

_API_CORE_VERSION = google.api_core.__version__


class VizierServiceTransport(abc.ABC):
    """Abstract transport class for VizierService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    DEFAULT_HOST: str = "aiplatform.googleapis.com"

    def __init__(
        self,
        *,
        host: str = DEFAULT_HOST,
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A list of scopes.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        scopes_kwargs = self._get_scopes_kwargs(self._host, scopes)

        # Save the scopes.
        self._scopes = scopes or self.AUTH_SCOPES

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials and credentials_file:
            raise core_exceptions.DuplicateCredentialArgs(
                "'credentials_file' and 'credentials' are mutually exclusive"
            )

        if credentials_file is not None:
            credentials, _ = google.auth.load_credentials_from_file(
                credentials_file, **scopes_kwargs, quota_project_id=quota_project_id
            )

        elif credentials is None:
            credentials, _ = google.auth.default(
                **scopes_kwargs, quota_project_id=quota_project_id
            )

        # Save the credentials.
        self._credentials = credentials

    # TODO(busunkim): These two class methods are in the base transport
    # to avoid duplicating code across the transport classes. These functions
    # should be deleted once the minimum required versions of google-api-core
    # and google-auth are increased.

    # TODO: Remove this function once google-auth >= 1.25.0 is required
    @classmethod
    def _get_scopes_kwargs(
        cls, host: str, scopes: Optional[Sequence[str]]
    ) -> Dict[str, Optional[Sequence[str]]]:
        """Returns scopes kwargs to pass to google-auth methods depending on the google-auth version"""

        scopes_kwargs = {}

        if _GOOGLE_AUTH_VERSION and (
            packaging.version.parse(_GOOGLE_AUTH_VERSION)
            >= packaging.version.parse("1.25.0")
        ):
            scopes_kwargs = {"scopes": scopes, "default_scopes": cls.AUTH_SCOPES}
        else:
            scopes_kwargs = {"scopes": scopes or cls.AUTH_SCOPES}

        return scopes_kwargs

    # TODO: Remove this function once google-api-core >= 1.26.0 is required
    @classmethod
    def _get_self_signed_jwt_kwargs(
        cls, host: str, scopes: Optional[Sequence[str]]
    ) -> Dict[str, Union[Optional[Sequence[str]], str]]:
        """Returns kwargs to pass to grpc_helpers.create_channel depending on the google-api-core version"""

        self_signed_jwt_kwargs: Dict[str, Union[Optional[Sequence[str]], str]] = {}

        if _API_CORE_VERSION and (
            packaging.version.parse(_API_CORE_VERSION)
            >= packaging.version.parse("1.26.0")
        ):
            self_signed_jwt_kwargs["default_scopes"] = cls.AUTH_SCOPES
            self_signed_jwt_kwargs["scopes"] = scopes
            self_signed_jwt_kwargs["default_host"] = cls.DEFAULT_HOST
        else:
            self_signed_jwt_kwargs["scopes"] = scopes or cls.AUTH_SCOPES

        return self_signed_jwt_kwargs

    def _prep_wrapped_messages(self, client_info):
        # Precompute the wrapped methods.
        self._wrapped_methods = {
            self.create_study: gapic_v1.method.wrap_method(
                self.create_study, default_timeout=5.0, client_info=client_info,
            ),
            self.get_study: gapic_v1.method.wrap_method(
                self.get_study, default_timeout=5.0, client_info=client_info,
            ),
            self.list_studies: gapic_v1.method.wrap_method(
                self.list_studies, default_timeout=5.0, client_info=client_info,
            ),
            self.delete_study: gapic_v1.method.wrap_method(
                self.delete_study, default_timeout=5.0, client_info=client_info,
            ),
            self.lookup_study: gapic_v1.method.wrap_method(
                self.lookup_study, default_timeout=5.0, client_info=client_info,
            ),
            self.suggest_trials: gapic_v1.method.wrap_method(
                self.suggest_trials, default_timeout=5.0, client_info=client_info,
            ),
            self.create_trial: gapic_v1.method.wrap_method(
                self.create_trial, default_timeout=5.0, client_info=client_info,
            ),
            self.get_trial: gapic_v1.method.wrap_method(
                self.get_trial, default_timeout=5.0, client_info=client_info,
            ),
            self.list_trials: gapic_v1.method.wrap_method(
                self.list_trials, default_timeout=5.0, client_info=client_info,
            ),
            self.add_trial_measurement: gapic_v1.method.wrap_method(
                self.add_trial_measurement,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.complete_trial: gapic_v1.method.wrap_method(
                self.complete_trial, default_timeout=5.0, client_info=client_info,
            ),
            self.delete_trial: gapic_v1.method.wrap_method(
                self.delete_trial, default_timeout=5.0, client_info=client_info,
            ),
            self.check_trial_early_stopping_state: gapic_v1.method.wrap_method(
                self.check_trial_early_stopping_state,
                default_timeout=5.0,
                client_info=client_info,
            ),
            self.stop_trial: gapic_v1.method.wrap_method(
                self.stop_trial, default_timeout=5.0, client_info=client_info,
            ),
            self.list_optimal_trials: gapic_v1.method.wrap_method(
                self.list_optimal_trials, default_timeout=5.0, client_info=client_info,
            ),
        }

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Return the client designed to process long-running operations."""
        raise NotImplementedError()

    @property
    def create_study(
        self,
    ) -> Callable[
        [vizier_service.CreateStudyRequest],
        Union[gca_study.Study, Awaitable[gca_study.Study]],
    ]:
        raise NotImplementedError()

    @property
    def get_study(
        self,
    ) -> Callable[
        [vizier_service.GetStudyRequest], Union[study.Study, Awaitable[study.Study]]
    ]:
        raise NotImplementedError()

    @property
    def list_studies(
        self,
    ) -> Callable[
        [vizier_service.ListStudiesRequest],
        Union[
            vizier_service.ListStudiesResponse,
            Awaitable[vizier_service.ListStudiesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_study(
        self,
    ) -> Callable[
        [vizier_service.DeleteStudyRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def lookup_study(
        self,
    ) -> Callable[
        [vizier_service.LookupStudyRequest], Union[study.Study, Awaitable[study.Study]]
    ]:
        raise NotImplementedError()

    @property
    def suggest_trials(
        self,
    ) -> Callable[
        [vizier_service.SuggestTrialsRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def create_trial(
        self,
    ) -> Callable[
        [vizier_service.CreateTrialRequest], Union[study.Trial, Awaitable[study.Trial]]
    ]:
        raise NotImplementedError()

    @property
    def get_trial(
        self,
    ) -> Callable[
        [vizier_service.GetTrialRequest], Union[study.Trial, Awaitable[study.Trial]]
    ]:
        raise NotImplementedError()

    @property
    def list_trials(
        self,
    ) -> Callable[
        [vizier_service.ListTrialsRequest],
        Union[
            vizier_service.ListTrialsResponse,
            Awaitable[vizier_service.ListTrialsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def add_trial_measurement(
        self,
    ) -> Callable[
        [vizier_service.AddTrialMeasurementRequest],
        Union[study.Trial, Awaitable[study.Trial]],
    ]:
        raise NotImplementedError()

    @property
    def complete_trial(
        self,
    ) -> Callable[
        [vizier_service.CompleteTrialRequest],
        Union[study.Trial, Awaitable[study.Trial]],
    ]:
        raise NotImplementedError()

    @property
    def delete_trial(
        self,
    ) -> Callable[
        [vizier_service.DeleteTrialRequest],
        Union[empty_pb2.Empty, Awaitable[empty_pb2.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def check_trial_early_stopping_state(
        self,
    ) -> Callable[
        [vizier_service.CheckTrialEarlyStoppingStateRequest],
        Union[operations_pb2.Operation, Awaitable[operations_pb2.Operation]],
    ]:
        raise NotImplementedError()

    @property
    def stop_trial(
        self,
    ) -> Callable[
        [vizier_service.StopTrialRequest], Union[study.Trial, Awaitable[study.Trial]]
    ]:
        raise NotImplementedError()

    @property
    def list_optimal_trials(
        self,
    ) -> Callable[
        [vizier_service.ListOptimalTrialsRequest],
        Union[
            vizier_service.ListOptimalTrialsResponse,
            Awaitable[vizier_service.ListOptimalTrialsResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("VizierServiceTransport",)