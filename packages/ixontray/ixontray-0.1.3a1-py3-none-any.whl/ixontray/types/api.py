# ------------------------------------------------------------------
# Copyright (C) Smart Robotics - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly
# prohibited. All information contained herein is, and remains
# the property of Smart Robotics.
# ------------------------------------------------------------------
import pydantic


class VpnSession(pydantic.BaseModel):
    vpnAddress: str


class Link(pydantic.BaseModel):
    href: str
    rel: str


class Server(pydantic.BaseModel):
    name: str
    publicId: str
    type: str | None = None


class Agent(pydantic.BaseModel):
    activeVpnSession: VpnSession | None = None
    description: str | None = None
    links: list[Link] | None = None
    name: str
    publicId: str
    servers: list[Server] | None = None
    api_version: int | None = None
    company_id: str | None = None

    @property
    def online(self) -> bool:
        return self.activeVpnSession is not None

    @property
    def full_name(self) -> str:
        return f"{self.name} ({self.description})"


class AgentsResponse(pydantic.BaseModel):
    count: int | None = None
    data: list[Agent]
    links: list[Link] | None = None
    status: str
    type: str


class Company(pydantic.BaseModel):
    city: str | None = None
    country: str | None = None
    links: list[Link] | None = None
    name: str
    parentLevel: int | None = None
    publicId: str
    starred: bool | None = None


class CompaniesResponse(pydantic.BaseModel):
    count: int | None = None
    data: list[Company]
    links: list[Link] | None = None
    status: str | None = None
    type: str | None = None


IXapiApplicationID = "fSS22kPAe49p"
