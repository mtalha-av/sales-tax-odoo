from typing import List


class Output:
    class Product:
        date: str
        record_number: str
        seller_id: str
        seller_location_id: str
        seller_state: str
        delivery_method: str
        customer_entity_code: str
        order_received_address: str
        order_received_suite: str
        order_received_city: str
        order_received_county: str
        order_received_state: str
        order_received_zip_code: str
        order_received_zip_plus: str
        ship_to_address: str
        ship_to_suite: str
        ship_to_city: str
        ship_to_county: str
        ship_to_state: str
        ship_to_zip_code: str
        ship_to_zip_plus: str
        sku: str
        amount_of_sale: str
        resulttype: str
        taxability_code: str
        taxes: List["Output.Tax"]

        def __init__(self, data, taxes=None):
            taxes = taxes or []
            self.date = data["date"]
            self.record_number = data["record number"]
            self.seller_id = data["seller id"]
            self.seller_location_id = data["seller location id"]
            self.seller_state = data["seller state"]
            self.delivery_method = data["delivery method"]
            self.customer_entity_code = data["customer entity code"]
            self.ship_to_address = data["ship to address"]
            self.ship_to_suite = data["ship to suite"]
            self.ship_to_city = data["ship to city"]
            self.ship_to_county = data["ship to county"]
            self.ship_to_state = data["ship to state"]
            self.ship_to_zip_code = data["ship to zip code"]
            self.ship_to_zip_plus = data["ship to zip plus"]
            self.order_received_address = data["order received address"]
            self.order_received_suite = data["order received suite"]
            self.order_received_city = data["order received city"]
            self.order_received_county = data["order received county"]
            self.order_received_state = data["order received state"]
            self.order_received_zip_code = data["order received zip code"]
            self.order_received_zip_plus = data["order received zip plus"]
            self.sku = data["sku"]
            self.amount_of_sale = data["amount of sale"]
            self.resulttype = data["resulttype"]
            self.taxability_code = data["taxability code"]
            self.taxes = taxes

        def add_taxes(self, taxes: List["Output.Tax"]):
            self.taxes = taxes

        @property
        def tax_amount(self):
            return sum(float(t.fips_tax_amount) for t in self.taxes)

    class Tax:
        fips_jurisdiction_code: str
        fips_tax_rate: str
        fips_tax_amount: str

        def __init__(self, data):
            self.fips_jurisdiction_code = data["fips_jurisdiction_code"]
            self.fips_tax_rate = data["fips_tax_rate"]
            self.fips_tax_amount = data["fips_tax_amount"]
