"""Data Models used by SaxoOpenAPIClient."""

import json
from base64 import urlsafe_b64decode
from datetime import datetime
from enum import Enum
from re import compile
from time import time
from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, AnyUrl, BaseConfig, BaseModel, ConstrainedStr, Extra, Field, root_validator, validator

SIM_STREAMING_URL = "wss://streaming.saxobank.com/sim/openapi/streamingws"
LIVE_STREAMING_URL = "wss://streaming.saxobank.com/openapi/streamingws"


class ClientId(ConstrainedStr):
    """OAuth2.0 ClientId. 32 char string."""

    regex = compile(r"^[a-f0-9]{32}$")


class ClientSecret(ClientId):
    """OAuth2.0 CLientSecret. Same as ClientId."""

    pass


class HttpsUrl(AnyUrl):
    """HTTPS URL. Override AnyUrl to only allow for secure protocol."""

    allowed_schemes = {"https"}


class GrantType(Enum):
    """OAuth grant type. Only supported version is Code."""

    CODE = "Code"


class APIEnvironment(Enum):
    """OpenAPI Environment. SIM and LIVE are currently supported."""

    SIM = "SIM"
    LIVE = "LIVE"


class AuthorizationCode(ConstrainedStr):
    """Auth code. GUID."""

    regex = compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$")


class RefreshToken(AuthorizationCode):
    """Refresh token. Same as Auth code (GUID)."""

    pass


class AuthorizationType(Enum):
    """Supported auth types. Either a auth code or refresh token can be exercised."""

    CODE = "authorization_code"
    REFRESH_TOKEN = "refresh_token"


class OpenAPIAppConfig(BaseModel):
    """Dataclass for parsing and validating app config objects."""

    app_name: str = Field(..., alias="AppName")
    grant_type: GrantType = Field(..., alias="GrantType")
    client_id: ClientId = Field(..., alias="AppKey")
    client_secret: ClientSecret = Field(..., alias="AppSecret")
    auth_endpoint: HttpsUrl = Field(..., alias="AuthorizationEndpoint")
    token_endpoint: HttpsUrl = Field(..., alias="TokenEndpoint")
    api_base_url: HttpsUrl = Field(..., alias="OpenApiBaseUrl")
    streaming_url: Optional[HttpsUrl]
    redirect_urls: List[AnyHttpUrl] = Field(..., alias="RedirectUrls")
    env: Optional[APIEnvironment]

    @root_validator
    def validate_redirect_urls_contains_localhost(cls, values: Dict) -> Dict:
        """Redirect URLs must at least have 1 localhost available."""
        available_hosts = [url.host for url in values["redirect_urls"]]
        assert "localhost" in available_hosts, (
            "at least 1 'localhost' redirect URL required in app config - " f"hosts: {available_hosts}"
        )
        return values

    @root_validator
    def validate_port_configuration_redirect_urls(cls, values: Dict) -> Dict:
        """Port should always be configured for redirect URLs."""
        assert all([url.port for url in values["redirect_urls"]]), (
            "one or more redirect URLs have no port configured, which is required "
            "for grant type 'Code' - ensure a port is configured in the app config "
            "object for each URL (example: http://localhost:23432/redirect) - "
            f"URLs: {[str(url) for url in values['redirect_urls']]}"
        )
        return values

    @root_validator
    def strip_base_url_suffix(cls, values: Dict) -> Dict:
        """Strip forward slash form base URL."""
        values["api_base_url"] = values["api_base_url"].rstrip("/")
        return values

    @root_validator
    def derive_env_fields(cls, values: Dict) -> Dict:
        """Set environment and streaming URL based on environment."""
        if "sim.logonvalidation" in values["auth_endpoint"]:
            values["env"] = APIEnvironment.SIM
            values["streaming_url"] = SIM_STREAMING_URL
        if "live.logonvalidation" in values["auth_endpoint"]:
            values["env"] = APIEnvironment.LIVE
            values["streaming_url"] = LIVE_STREAMING_URL
        return values

    class Config(BaseConfig):
        """No extra config items required."""

        extra = Extra.forbid

    def __str__(self) -> str:
        """Print app config safely for logging without exposing client secret themselves."""
        return str(self.dict(exclude={"client_secret"}))


class TokenData(BaseModel):
    """Dataclass for parsing token data."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: RefreshToken
    refresh_token_expires_in: int
    base_uri: Optional[HttpsUrl]
    access_token_expiry: Optional[int] = None
    refresh_token_expiry: Optional[int] = None
    client_key: Optional[str] = None
    user_key: Optional[str] = None
    session_id: Optional[str] = None
    write_permission: Optional[bool] = None

    @root_validator(pre=True)
    def set_fields_from_token_payload(cls, values: Dict) -> Dict:
        """Set fields from token claims."""
        token_bytes = values["access_token"].encode("utf-8")
        payload = token_bytes.split(b".")[1]
        padded = payload + b"=" * divmod(len(payload), 4)[1]
        decoded = urlsafe_b64decode(padded)
        claims = json.loads(decoded.decode("utf-8"))

        values["access_token_expiry"] = claims["exp"]
        values["refresh_token_expiry"] = int(time()) + values["refresh_token_expires_in"]
        values["client_key"] = claims["cid"]
        values["user_key"] = claims["uid"]
        values["session_id"] = claims["sid"]
        values["write_permission"] = True if claims["oaa"] == "77770" else False

        return values

    def __str__(self) -> str:
        """Print token (claims) data safely for logging without exposing tokens themselves."""
        return str(self.dict(exclude={"access_token", "refresh_token"}))


class StreamingMessage(BaseModel):
    """Streaming Message."""

    msg_id: int
    ref_id: str
    data: Any
    ts: Optional[datetime] = None

    @validator("ts", pre=True, always=True)
    def set_ts_now(cls, v: datetime) -> datetime:
        """Set datetime automatically for each message."""
        return datetime.utcnow()


class NotLoggedInError(Exception):
    """Client is not logged in."""

    pass


class TokenExpiredError(Exception):
    """Token has expired and can no longer be used."""

    pass


class APIResponseError(Exception):
    """An error occurred while executing the OpenAPI request."""

    pass
