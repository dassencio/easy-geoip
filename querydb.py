#!/usr/bin/env python3

"""Tools for querying a generated IP geolocation database."""

import ipfunctions
import json
import pickle


class IPInfo:

    """Holds geolocation data for an IP address."""

    def __init__(self, ip_address):
        """Initializes an IPInfo object with an IP address."""

        (self.ip_address,
         self.geoid,
         self.locale_code,
         self.continent_code,
         self.continent_name,
         self.country_iso_code,
         self.country_name,
         self.subdiv1_iso_code,
         self.subdiv1_name,
         self.subdiv2_iso_code,
         self.subdiv2_name,
         self.city_name,
         self.metro_code,
         self.time_zone,
         self.is_in_european_union) = [ip_address, None] + (["Unknown"] * 13)

    def set_values(self, row):
        """Extracts geolocation data for an IP address from an array."""

        (self.geoid,
         self.locale_code,
         self.continent_code,
         self.continent_name,
         self.country_iso_code,
         self.country_name,
         self.subdiv1_iso_code,
         self.subdiv1_name,
         self.subdiv2_iso_code,
         self.subdiv2_name,
         self.city_name,
         self.metro_code,
         self.time_zone,
         self.is_in_european_union) = ["Unknown" if field == "" else field for field in row]

    def to_string(self):
        """Returns all geolocation data as a multi-line string."""

        result = "IP address: %s\n" % self.ip_address
        result += "Locale code: %s\n" % self.locale_code
        result += "Continent: %s (%s)\n" % (
            self.continent_name, self.continent_code)
        result += "Country: %s (%s)\n" % (
            self.country_name, self.country_iso_code)
        result += "Subdivision 1: %s (%s)\n" % (
            self.subdiv1_name, self.subdiv1_iso_code)
        result += "Subdivision 2: %s (%s)\n" % (
            self.subdiv2_name, self.subdiv2_iso_code)
        result += "City: %s\n" % self.city_name
        result += "Metro code: %s\n" % self.metro_code
        result += "Time zone: %s\n" % self.time_zone
        result += "Is in European Union: %s" % self.is_in_european_union

        return result

    def to_json(self):
        """Returns all geolocation data as a JSON string."""

        result = {
            "ip_address": self.ip_address,
            "locale_code": self.locale_code,
            "continent": {
                "name": self.continent_name,
                "code": self.continent_code
            },
            "country": {
                "name": self.country_name,
                "code": self.country_iso_code
            },
            "subdivision1": {
                "name": self.subdiv1_name,
                "code": self.subdiv1_iso_code
            },
            "subdivision2": {
                "name": self.subdiv2_name,
                "code": self.subdiv2_iso_code
            },
            "city": self.city_name,
            "metro_code": self.metro_code,
            "time_zone": self.time_zone,
            "is_in_european_union": self.is_in_european_union
        }

        return json.dumps(result, indent=2, sort_keys=True)


def query_database(ip_address):
    """
    Returns geolocation data for an IP address (represented as a string
    such as "1.2.3.4") as an IPInfo object.
    """

    # convert the IP address into an integer and get its version
    try:
        (ip_integer, version) = ipfunctions.ip_to_integer(ip_address)
    except:
        raise ValueError("invalid IP address (%s)" % ip_address)

    ip_info = IPInfo(ip_address)

    # obtain the name of the segment file in which the geoname ID for the
    # given IP address is stored
    geoid_segment = None
    try:
        index_filename = "database/index-geoid-ip%d" % version
        with open(index_filename, "rb") as index_file:
            segment_num = 0
            while True:
                try:
                    row = pickle.load(index_file)
                    if row[0] <= ip_integer <= row[1]:
                        geoid_segment = segment_num
                        break
                    segment_num += 1
                # if the IP address is not in any listed subnetwork
                except EOFError:
                    return ip_info
    except:
        raise Exception("geoname ID index file was not found on database")

    # get the geoname ID for the given IP address
    geoid = None
    try:
        segment_filename = "database/geoid-ip%d-%d" % (version, geoid_segment)
        with open(segment_filename, "rb") as segment_file:
            while True:
                try:
                    row = pickle.load(segment_file)
                    if row[0] <= ip_integer <= row[1]:
                        geoid = row[2]
                        break
                # if the IP address is not in any listed subnetwork
                except EOFError:
                    return ip_info
    except IOError:
        raise Exception("geoname ID segment file was not found on database")

    # obtain the name of the segment file in which the geolocation data for
    # the given IP address is stored
    location_segment = None
    try:
        index_filename = "database/index-location"
        with open(index_filename, "rb") as index_file:
            segment_num = 0
            # since we got a geoname ID, this loop MUST succeed
            while True:
                row = pickle.load(index_file)
                if row[0] <= geoid <= row[1]:
                    location_segment = segment_num
                    break
                segment_num += 1
    except:
        raise Exception("location index file was not found on database")

    # get the geolocation data for the given IP address
    try:
        segment_filename = "database/location-%d" % location_segment
        with open(segment_filename, "rb") as segment_file:
            # since we got a geoname ID, this loop MUST succeed
            while True:
                row = pickle.load(segment_file)
                if row[0] == geoid:
                    ip_info.set_values(row)
                    break
    except:
        raise Exception("location segment file was not found on database")

    return ip_info
