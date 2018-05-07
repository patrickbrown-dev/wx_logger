"""
uploader.py - Uploads previous day's Wx logs.

Copyright (c) 2018 Patrick Brown

All previously recorded Wx logs are freely and publicly available at
https://kineticdial.nyc3.digitaloceanspaces.com/Wx/wxYYYYMMDD.csv
"""

import os
import datetime

import boto3


def main():
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    filename = yesterday.strftime("wx%Y%m%d.csv")
    client = get_client()
    client.upload_file(
        filename,
        'kineticdial',
        "Wx/{}".format(filename),
        ExtraArgs={'ACL':'public-read'}
    )
    exit(0)


def get_client():
    return boto3.client(
        's3',
        region_name='nyc3',
        endpoint_url='https://nyc3.digitaloceanspaces.com',
        aws_access_key_id=os.getenv('DO_SPACES_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('DO_SPACES_SECRET_KEY'),
    )


if __name__ == '__main__':
    main()