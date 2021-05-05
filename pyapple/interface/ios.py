from datetime import datetime
from typing import Optional, Union

from dateutil import tz
from hurry.filesize import alternative, size


class BaseModel:
    def __repr__(self) -> str:
        return str(self.__dict__)

    def __str__(self) -> str:
        return str(self.__dict__)


def to_dt(time: Optional[str]):
    if time is None:
        return time  # early return

    dest = tz.tzutc()
    obj = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    obj = obj.replace(tzinfo=dest)
    return obj


class IPSW(BaseModel):
    """
    A Python class for Regular IPSW files.

    Arguments:
    identifier: iDevice identifier for IPSW
    buildid: Build ID of IPSW
    version: OS Version of IPSW
    url: Download link of IPSW
    filesize: Size of IPSW file (in integer)
    sha1: SHA1 sum of IPSW file
    md5: MD5 sum of IPSW file
    releasedate: Released date of IPSW (in string)
    uploaddate: Uploaded date of IPSW (in string)
    signed: A bool whether tells IPSW is still signed
    """

    def __init__(
        self,
        identifier: str,
        buildid: str,
        version: str,
        url: str,
        filesize: int,
        sha1sum: str,
        md5sum: str,
        releasedate: Union[
            str, None
        ],  # sometimes Apple gives firmware release date as null, fuck
        uploaddate: Union[
            str, None
        ],  # sometimes Apple gives firmware release date as null, fuck
        signed: bool,
    ) -> None:
        self.identifier = identifier
        self.buildid = buildid
        self.version = version
        self.uri = url
        self.filesize = (filesize, size(filesize, system=alternative))
        self.sha1sum = sha1sum
        self.md5sum = md5sum
        self.signed = signed
        self.releasedate = to_dt(releasedate)
        self.uploaddate = to_dt(uploaddate)


class KeysObject(BaseModel):
    def __init__(
        self,
        image: str,
        filename: str,
        kbag: str,
        key: str,
        iv: str,
        date: Optional[str],
    ) -> None:
        self.image = image
        self.filename = filename
        self.kbag = kbag
        self.key = key
        self.iv = iv
        self.date = to_dt(date)


class IPSWKeys(BaseModel):
    def __init__(
        self,
        identifier: str,
        buildid: str,
        codename: str,
        baseband: Optional[str],
        updateramdiskexists: bool,
        restoreramdiskexists: bool,
        keys: Optional[list],
    ) -> None:
        self.identifier = identifier
        self.buildid = buildid
        self.codename = codename
        self.baseband = baseband
        self.updateramdiskexists = updateramdiskexists
        self.restoreramdiskexists = restoreramdiskexists
        self.keys = keys


class OTAIPSW(BaseModel):
    def __init__(
        self,
        identifier: str,
        buildid: str,
        version: str,
        url: str,
        filesize: int,
        prerequisitebuildid: str,
        prerequisiteversion: str,
        release_type: str,
        uploaddate: Union[
            str, None
        ],  # sometimes Apple gives firmware release date as null, fuck
        releasedate: Union[
            str, None
        ],  # sometimes Apple gives firmware release date as null, fuck
        signed: bool,
    ) -> None:
        self.identifier = identifier
        self.buildid = buildid
        self.version = version
        self.uri = url
        self.filesize = (filesize, size(filesize, system=alternative))
        self.prerequisitebuildid = prerequisitebuildid
        self.prerequisiteversion = prerequisiteversion
        self.release_type = release_type
        self.upload_date = to_dt(uploaddate)
        self.release_date = to_dt(releasedate)
        self.signed = signed


class iDevice(BaseModel):
    """
    A Python class for an iDevice.

    Arguments:
    name: Name of iDevice
    identifier: Identifier of iDevice
    boardconfig: Boardconfig of iDevice
    platform: CPU Platform of iDevice
    cpid: CPID of iDevice
    bdid: BDID of iDevice
    firmwares: List of available firmwares of iDevice
    """

    def __init__(
        self,
        name: str,
        identifier: str,
        boardconfig: str,
        platform: str,
        cpid: str,
        bdid: str,
        firmwares: Optional[list],
        boards: Optional[list],
    ) -> None:
        self.name = name
        self.identifier = identifier
        self.boardconfig = boardconfig
        self.platform = platform
        self.cpid = cpid
        self.bdid = bdid
        self.firmwares = firmwares
        self.boards = boards


class IntelMacOS(BaseModel):
    """
    A Python class for an Intel-based macOS Installation.

    Arguments:
    product_id: A product id of macOS Installation
    """

    def __init__(self, product_id) -> None:
        self.product_id = product_id
        self.title = ""
        self.version = ""
        self.build = ""
        self.postdate = ""
        self.packages = []


class IntelMacOSPkg(BaseModel):
    def __init__(self, url: str, filesize: int) -> None:
        self.filename = url.split("/")[-1]
        self.uri = url
        self.filesize = (filesize, size(filesize, system=alternative))


class CydiaPackage(BaseModel):
    def __init__(self) -> None:
        pass