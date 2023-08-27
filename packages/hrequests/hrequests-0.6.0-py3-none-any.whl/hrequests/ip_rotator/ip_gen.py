import csv
import ipaddress
import random


class IPGenerator:
    def __init__(self):
        with open('IP2LOCATION-LITE-DB1.CSV') as csvfile:
            reader = csv.reader(csvfile)
            self.ip_ranges: tuple = tuple(reader)

    def generate(self, country_code) -> str:
        filtered_ranges: tuple = self.by_country(self.ip_ranges, country_code)

        if not filtered_ranges:
            raise ValueError(f'No IP ranges found for country code: {country_code}')

        selected_range = random.choice(filtered_ranges)
        random_ip = random.randint(selected_range[0], selected_range[1])

        return ipaddress.IPv4Address._string_from_ip_int(random_ip)

    @staticmethod
    def by_country(ip_ranges, country_code: str) -> tuple:
        country_code = country_code.upper()
        return tuple(filter(lambda ip_range: ip_range[2] == country_code, ip_ranges))