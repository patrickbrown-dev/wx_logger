import sys
import os
import json
import csv
import logging
import datetime
import http.client


SECRET_KEY  = os.environ['DARK_SKY_SECRET_KEY']
CSV_HEADERS = [
    "time",
    "summary",
    "icon",
    "nearestStormDistance",
    "nearestStormBearing",
    "precipIntensity",
    "precipIntensityError",
    "precipProbability",
    "precipType",
    "temperature",
    "apparentTemperature",
    "dewPoint",
    "humidity",
    "pressure",
    "windSpeed",
    "windGust",
    "windBearing",
    "cloudCover",
    "uvIndex",
    "visibility",
    "ozone"
]


def main(latitude, longitude):
    log_filename = datetime.date.today().strftime("wx%Y%m%d.log")
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        filename=log_filename,
        level=logging.INFO
    )
    logging.info("Requesting weather data from Dark Sky")
    row = get_weather_http(latitude, longitude)
    logging.info("Writing data to CSV")
    write_csv(row)
    logging.info("Done.")


def get_weather_http(latitude, longitude):
    url = "/forecast/{}/{},{}".format(SECRET_KEY, latitude, longitude)
    conn = http.client.HTTPSConnection("api.darksky.net")
    conn.request("GET", url)
    resp = conn.getresponse()

    if resp.code != 200:
        logging.error("Bad response from Dark Sky")
        logging.error("Code: {}, Mesg: {}".format(resp.code, resp.reason)) 
        exit(1)
    
    resp_body = resp.read()
    resp_object = json.loads(resp_body)
    conn.close()

    return resp_object['currently']


def write_csv(row):
    csv_filename = datetime.date.today().strftime("wx%Y%m%d.csv")
    write_headers = True
    if os.path.exists(csv_filename):
        write_headers = False

    with open(csv_filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        if write_headers:
            writer.writeheader()
        writer.writerow(row)


if __name__ == '__main__':
    latitude  = 37.8321
    longitude = -122.2626
    main(latitude, longitude)