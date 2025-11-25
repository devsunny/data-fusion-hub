"""
Data Fusion Hub Service - Authentication Configuration Models
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class AuthConfigBase(BaseModel):
    """Base authentication configuration."""
    method: str = Field(..., description="Authentication method (jwt, username_password, api_key, etc.)")

class JWTAuthConfig(AuthConfigBase):
    """JWT Authentication Configuration."""
    method: str = "jwt"
    token_url: Optional[str] = Field(None, description="URL to obtain JWT token")
    client_id: Optional[str] = Field(None, description="Client ID for authentication")
    client_secret: Optional[str] = Field(None, description="Client secret for authentication") 
    audience: Optional[str] = Field(None, description="Audience for the JWT token")

class UsernamePasswordAuthConfig(AuthConfigBase):
    """Username/Password Authentication Configuration."""
    method: str = "username_password"
    username: str = Field(..., description="Username for authentication")
    password: str = Field(..., description="Password for authentication (will be encrypted)")

class APIKeyAuthConfig(AuthConfigBase):
    """API Key Authentication Configuration.""" 
    method: str = "api_key"
    api_key: str = Field(..., description="API key for authentication (will be encrypted)")
    header_name: Optional[str] = Field("Authorization", description="HTTP header name for the API key")

class PrivateKeyAuthConfig(AuthConfigBase):
    """Private Key Authentication Configuration."""
    method: str = "private_key"
    private_key: str = Field(..., description="Private key content (will be encrypted)")
    passphrase: Optional[str] = Field(None, description="Passphrase for the private key if needed")

class OAuth2AuthConfig(AuthConfigBase):
    """OAuth2 Authentication Configuration."""
    method: str = "oauth2"
    client_id: str = Field(..., description="Client ID")
    client_secret: str = Field(..., description="Client secret (will be encrypted)")
    token_url: str = Field(..., description="Token endpoint URL")
    redirect_uri: Optional[str] = Field(None, description="Redirect URI for OAuth2 flow")

class AuthConfig(AuthConfigBase):
    """Generic authentication configuration that can hold any specific auth type."""
    # This will be a union of all possible auth configurations
    jwt_config: Optional[JWTAuthConfig] = None
    username_password_config: Optional[UsernamePasswordAuthConfig] = None  
    api_key_config: Optional[APIKeyAuthConfig] = None
    private_key_config: Optional[PrivateKeyAuthConfig] = None
    oauth2_config: Optional[OAuth2AuthConfig] = None

# For simplicity in this implementation, we'll use a generic approach:
class GenericAuthConfig(BaseModel):
    """Generic authentication configuration that can hold any auth parameters."""
    method: str = Field(..., description="Authentication method")
    config: Dict[str, Any] = Field(..., description="Configuration parameters for the authentication method")

# This will be used in our main data connector model