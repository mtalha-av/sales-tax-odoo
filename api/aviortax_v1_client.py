import requests

from .dtos import Output


def build_tax(product_dict: dict, count: int):
    data = {
        "fips_jurisdiction_code": product_dict[f"fips jurisdiction code {count}"],
        "fips_tax_rate": product_dict[f"fips tax rate {count}"],
        "fips_tax_amount": product_dict[f"fips tax amount {count}"],
    }
    tax = Output.Tax(data)
    return tax


def build_tax_from_product(product_dict: dict):
    count = 1
    taxes = []
    while product_dict[f"fips jurisdiction code {count}"]:
        taxes.append(build_tax(product_dict, count))
        count += 1
    return taxes


def build_product(product_dict: dict):
    product = Output.Product(product_dict)
    product.taxes = build_tax_from_product(product_dict)
    return product


class AviortaxV1Client:
    def __init__(self, service_url, auth_token):
        self.service_url = service_url
        self.auth_token = auth_token

    @staticmethod
    def login(service_url, username, password):
        response = requests.post(
            f"{service_url}/api/auth/token/login/",
            data={"username": username, "password": password},
        )
        if not response.ok:
            raise Exception("Login failed")
        data = response.json()
        return data["auth_token"]

    def get_tax(self, input_products=[]):
        response = requests.post(
            f"{self.service_url}/suttaxd/gettax/",
            data=input_products,
            headers={"Authorization": f"Token {self.auth_token}"},
        )
        if not response.ok:
            raise Exception("Get tax failed")
        data = response.json()
        return build_product(data)


__all__ = ["AviortaxV1Client"]
