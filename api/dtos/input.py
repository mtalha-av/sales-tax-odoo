class Input:
    class Product:
        def init(
            self,
            date: str,
            record_number: str,
            seller_id: str,
            seller_location_id: str,
            seller_state: str,
            delivery_method: str,
            customer_entity_code: str,
            ship_to_address: str,
            ship_to_suite: str,
            ship_to_city: str,
            ship_to_county: str,
            ship_to_state: str,
            ship_to_zip_code: str,
            ship_to_zip_plus: str,
            sku: str,
            amount_of_sale: str,
        ):
            self.date = date
            self.record_number = record_number
            self.seller_id = seller_id
            self.seller_location_id = seller_location_id
            self.seller_state = seller_state
            self.delivery_method = delivery_method
            self.customer_entity_code = customer_entity_code
            self.ship_to_address = ship_to_address
            self.ship_to_suite = ship_to_suite
            self.ship_to_city = ship_to_city
            self.ship_to_county = ship_to_county
            self.ship_to_state = ship_to_state
            self.ship_to_zip_code = ship_to_zip_code
            self.ship_to_zip_plus = ship_to_zip_plus
            self.sku = sku
            self.amount_of_sale = amount_of_sale

        def asdict(self):
            return {
                "date": self.date,
                "record number": self.record_number,
                "seller id": self.seller_id,
                "seller location id": self.seller_location_id,
                "seller state": self.seller_state,
                "delivery method": self.delivery_method,
                "customer entity code": self.customer_entity_code,
                "ship to address": self.ship_to_address,
                "ship to suite": self.ship_to_suite,
                "ship to city": self.ship_to_city,
                "ship to county": self.ship_to_county,
                "ship to state": self.ship_to_state,
                "ship to zip code": self.ship_to_zip_code,
                "ship to zip plus": self.ship_to_zip_plus,
                "sku": self.sku,
                "amount of sale": self.amount_of_sale,
            }
