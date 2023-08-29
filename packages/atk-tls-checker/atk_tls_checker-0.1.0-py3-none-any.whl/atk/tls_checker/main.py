from datetime import datetime
import ssl
from typing import Dict

from fastapi import FastAPI, HTTPException
import OpenSSL
from pydantic import BaseModel
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


class DistinguishedName(BaseModel):
    country_name: str | None
    state_or_province_name: str | None
    locality_name: str | None
    organization_name: str | None
    organizational_unit_name: str | None
    common_name: str
    email_address: str | None


class Certificate(BaseModel):
    subject: DistinguishedName
    issuer: DistinguishedName
    not_valid_before: datetime
    not_valid_after: datetime
    serial_number: str
    signature_algorithm: str
    version: int
    public_key: str


def x509Name_to_dn(x509Name) -> DistinguishedName:
    return DistinguishedName(
        country_name=x509Name.countryName,
        state_or_province_name=x509Name.stateOrProvinceName,
        locality_name=x509Name.localityName,
        organization_name=x509Name.organizationName,
        organizational_unit_name=x509Name.organizationalUnitName,
        common_name=x509Name.commonName,
        email_address=x509Name.emailAddress,
    )


def x509_to_certificate(x509) -> Certificate:
    return Certificate(
        subject=x509Name_to_dn(x509.get_subject()),
        issuer=x509Name_to_dn(x509.get_issuer()),
        not_valid_before=datetime.strptime(
            x509.get_notBefore().decode("utf-8"), "%Y%m%d%H%M%SZ"
        ),
        not_valid_after=datetime.strptime(
            x509.get_notAfter().decode("utf-8"), "%Y%m%d%H%M%SZ"
        ),
        serial_number=str(x509.get_serial_number()),
        signature_algorithm=x509.get_signature_algorithm(),
        version=x509.get_version(),
        public_key=x509.get_pubkey()
        .to_cryptography_key()
        .public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo,
        )
        .decode("utf-8"),
    )


app = FastAPI()

CACHE: Dict[str, Certificate] = {}


@app.get("/v0/certificate")
def get_certificate(hostname: str) -> Certificate:
    # validate hostname containes only alphanumeric characters and dots
    if not hostname.replace(".", "").isalnum():
        raise HTTPException(status_code=400, detail="Invalid hostname")

    # check if we have a cached certificate
    if hostname in CACHE:
        return CACHE[hostname]
    cert = ssl.get_server_certificate((hostname, 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    _cert = x509_to_certificate(x509)
    CACHE[hostname] = _cert
    return _cert
