#Sadly no pralelisation for now :( simple for cycle

import cdsapi
import multiprocessing

client = cdsapi.Client(timeout=300)

def cdsapi_worker(dataset):
  result = client.retrieve("reanalysis-era5-pressure-levels", dataset)
  result.download(dataset['file_name'])

def download_era_radiosounde(year,month,day,lat,lon,folder):
    delta = 0.005
    request = {
        "product_type": ["reanalysis"],
        "variable": [
            "relative_humidity",
            "temperature",
            "u_component_of_wind",
            "v_component_of_wind"
        ],
        "year": [str(year)],
        "month": [str(month)],
        "day": [str(day)],
        "time": [
        "00:00", "01:00", "02:00",
        "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00",
        "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00",
        "21:00", "22:00", "23:00"
        ],
        "pressure_level": [
            "1", "2", "3",
            "5", "7", "10",
            "20", "30", "50",
            "70", "100", "125",
            "150", "175", "200",
            "225", "250", "300",
            "350", "400", "450",
            "500", "550", "600",
            "650", "700", "750",
            "775", "800", "825",
            "850", "875", "900",
            "925", "950", "975",
            "1000"
        ],
        "data_format": "netcdf",
        "download_format": "unarchived",
        "area": [lat+delta, lon-delta, lat-delta, lon+delta],
    }
    client = cdsapi.Client()
    client.retrieve("reanalysis-era5-pressure-levels", request).download(f"{folder}/Radiosonde_ERA5_{year}{month}{day}.nc")
    
for month in [
        "05", "06",
        "07", "08", "09",
        "10", "11", "12"]:
    
    for day in [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12",
        "13", "14", "15",
        "16", "17", "18",
        "19", "20", "21",
        "22", "23", "24",
        "25", "26", "27",
        "28", "29", "30",
        "31"]:
        if day == "29" or day == "30" or day == "31" and month== "02":
            pass
        if day == "31" and int(month)%2==0:
            pass
        download_era_radiosounde(2014, month, day, 42.69, 23.41,"Radiosonde")