# City to API mappings
city_api_map = {
    'amsterdam': 'https://oap.ind.nl/oap/api/desks/AM/slots/?productKey=BIO&persons=1',
    'the_hague': 'https://oap.ind.nl/oap/api/desks/DH/slots/?productKey=BIO&persons=1',
    'zwolle': 'https://oap.ind.nl/oap/api/desks/ZW/slots/?productKey=BIO&persons=1',
    'den_bosch': 'https://oap.ind.nl/oap/api/desks/ba60652efaf2be4de158be0367ee4763/slots/?productKey=BIO&persons=1',
    'haarlem': 'https://oap.ind.nl/oap/api/desks/6b425ff9f87de136a36b813cccf26e23/slots/?productKey=BIO&persons=1',
    'expat_center_wageningen': 'https://oap.ind.nl/oap/api/desks/b084907207cfeea941cd9698821fd894/slots/?productKey=BIO&persons=1',
    'expat_center_enschede': 'https://oap.ind.nl/oap/api/desks/3535aca0fb9a2e8e8015f768fb3fa69d/slots/?productKey=BIO&persons=1',
    'expat_center_utrecht': 'https://oap.ind.nl/oap/api/desks/fa24ccf0acbc76a7793765937eaee440/slots/?productKey=BIO&persons=1',
    'expat_center_nijmegen': 'https://oap.ind.nl/oap/api/desks/0d85a757c13105ba0c26c3d177a7a884/slots/?productKey=BIO&persons=1',
}

MAX_RETRIES = 5
SLEEP_TIME = 2  # Time to sleep between retries, in seconds
