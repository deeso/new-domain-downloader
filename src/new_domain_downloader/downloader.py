from datetime import timedelta, datetime
import base64
import requests

import io
import zipfile



class Downloader(object):
    URL_FORMAT = 'https://whoisds.com//whois-database/newly-registered-domains/{}/nrd'
    NRD_FORMAT = "{}-{}-{}.zip"

    @classmethod
    def get_nrd(cls, month, day, year):
        return cls.NRD_FORMAT.format(year, month, day)

    @classmethod
    def get_nrd_b64(cls, month, day, year):
        return base64.encodebytes(cls.get_nrd(month, day, year).encode('ascii')).decode('ascii').strip()

    @classmethod
    def get_nrd_url(cls, month, day, year):
        nrd_b64 = cls.get_nrd_b64(month, day, year)
        return cls.URL_FORMAT.format(nrd_b64)

    @classmethod
    def nrd_url_yesterday(cls):
        return cls.nrd_url_back_ndays(1)

    @classmethod
    def nrd_file_yesterday(cls):
        return cls.nrd_file_back_ndays(1)

    @classmethod
    def nrd_url_today(cls):
        return cls.nrd_url_back_ndays(0)

    @classmethod
    def nrd_file_today(cls):
        return cls.nrd_file_back_ndays(0)

    @classmethod
    def nrd_url_back_ndays(cls, days=1):
        now = datetime.now()
        dt = now - timedelta(days=days)
        return cls.get_nrd_url(dt.month, dt.day, dt.year)

    @classmethod
    def nrd_file_back_ndays(cls, days=1):
        now = datetime.now()
        dt = now - timedelta(days=days)
        return cls.get_nrd(dt.month, dt.day, dt.year)

    @classmethod
    def nrd_download_yesterday(cls):
        return cls.nrd_download_back_ndays()

    @classmethod
    def nrd_download_today(cls):
        return cls.nrd_download_back_ndays(0)

    @classmethod
    def nrd_download(cls, month, day, year):
        url = cls.get_nrd_url(month, day, year)
        rsp = requests.get(url)
        if rsp.status_code == 200:
            zip_data = rsp.content
            return {'filename': cls.get_nrd(month, day, year),
                    'data': zip_data,
                    'format': 'zip'}
        else:
            return {'filename': cls.get_nrd(month, day, year),
                    'data': None,
                    'format': None}

    @classmethod
    def nrd_extract_yesterday(cls):
        return cls.nrd_extract_back_ndays()

    @classmethod
    def nrd_extract_today(cls):
        return cls.nrd_extract_back_ndays(0)

    @classmethod
    def nrd_extract(cls, month, day, year):
        results = cls.nrd_download(month, day, year)
        if results['data'] is None:
            return results
        in_memory_zip = io.BytesIO()
        in_memory_zip.write(results['data'])
        in_memory_zip.seek(0, io.SEEK_SET)

        zf = zipfile.ZipFile(in_memory_zip)
        results['filename'] = zf.namelist()[0]
        domain_string = zf.read(results['filename'])
        results['data'] = domain_string
        results['format'] = 'text'
        return results

    @classmethod
    def nrd_list(cls, month, day, year):
        results = cls.nrd_extract(month, day, year)
        if results['data'] is None:
            return results

        dl = results['data']
        if isinstance(dl, str):
            pass
        elif isinstance(dl, bytes):
            dl = dl.decode('utf8')
        else:
            return results

        domains = [i.strip() for i in dl.splitlines()]
        results['data'] = domains
        results['format'] = 'list'
        return results

    @classmethod
    def nrd_download_back_ndays(cls, days=1):
        url = cls.nrd_url_back_ndays(days)
        rsp = requests.get(url)
        if rsp.status_code == 200:
            zip_data = rsp.content
            return {'filename': cls.nrd_file_back_ndays(days),
                    'data': zip_data,
                    'format': 'zip'}
        else:
            return {'filename': cls.nrd_file_back_ndays(days),
                    'data': None,
                    'format': None}


    @classmethod
    def nrd_extract_back_ndays(cls, days=1):
        results = cls.nrd_download_back_ndays(days)
        if results['data'] is None:
            return results
        in_memory_zip = io.BytesIO()
        in_memory_zip.write(results['data'])
        in_memory_zip.seek(0, io.SEEK_SET)

        zf = zipfile.ZipFile(in_memory_zip)
        results['filename'] = zf.namelist()[0]
        domain_string = zf.read(results['filename'])
        results['data'] = domain_string
        results['format'] = 'text'
        return results

    @classmethod
    def nrd_list_back_ndays(cls, days=1):
        results = cls.nrd_extract_back_ndays(days)
        if results['data'] is None:
            return results

        dl = results['data']
        if isinstance(dl, str):
            pass
        elif isinstance(dl, bytes):
            dl = dl.decode('utf8')
        else:
            return results

        domains = [i.strip() for i in dl.splitlines()]
        results['data'] = domains
        results['format'] = 'list'
        return results

