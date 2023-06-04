from typing import List, Optional, Union, Dict

from pydantic import BaseModel


class SauceNAORequest(BaseModel):
    api_key: str
    url: str = str()
    output_type: int
    testmode: int
    dbmaski: int
    db: int
    numres: int


class SauceNAOResponseIndexFields(BaseModel):
    status: int
    parent_id: int
    id: int
    results: Optional[int] = None


class SauceNAOResponseHeader(BaseModel):
    user_id: str
    account_type: str
    short_limit: str
    long_limit: str
    long_remaining: int
    short_remaining: int
    status: int
    results_requested: int
    index: Dict[str, SauceNAOResponseIndexFields]
    search_depth: str
    minimum_similarity: float
    query_image_display: str
    query_image: str
    results_returned: int


class SauceNAOResponseResultsHeader(BaseModel):
    similarity: str
    thumbnail: str
    index_id: int
    index_name: str
    dupes: int
    hidden: int


class SauceNAOResponseResultsData(BaseModel):
    ext_urls: Optional[List[str]] = None
    title: Optional[str] = None
    pixiv_id: Optional[int] = None
    member_name: Optional[str] = None
    member_id: Optional[int] = None
    published: Optional[str] = None
    service: Optional[str] = None
    service_name: Optional[str] = None
    id: Optional[str] = None
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    yandere_id: Optional[int] = None
    konachan_id: Optional[int] = None
    creator: Optional[Union[str, List[str]]] = None
    material: Optional[str] = None
    characters: Optional[str] = None
    source: Optional[str] = None
    danbooru_id: Optional[int] = None
    gelbooru_id: Optional[int] = None
    eng_name: Optional[str] = None
    jp_name: Optional[str] = None


class SauceNAOResponseResults(BaseModel):
    header: SauceNAOResponseResultsHeader
    data: SauceNAOResponseResultsData


class SauceNAOResponse(BaseModel):
    header: SauceNAOResponseHeader
    results: List[SauceNAOResponseResults]


class SauceNAOResult(BaseModel):
    similarity: str
    index_name: str
    url: str
