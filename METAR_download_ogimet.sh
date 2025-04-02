#!/bin/bash

# Set parameters for Ogimet query
station=$1     # ICAO station code

# Construct the URL
base_url=http://www.ogimet.com/cgi-bin/getmetar?icao=LBSF
url="http://www.ogimet.com/cgi-bin/getmetar?icao=${station}"

# Timespan
start_date=$2
end_date=$3

# Output file
output_file="metar_${station}_${start_date}_${end_date}.txt"
if [ -e "$output_file" ]; then
    rm "$output_file"
fi
# Time increment in days
increment="10 days"  # 10 day increments, ogimet doesn't allow longer :( 

date

# Loop through each timestamp in the range
current_epoch=$(date -d "$start_date" +"%Y-%m-%d")
end_date=$(date -d "$end_date" +"%Y-%m-%d")
while [[ "$current_epoch" < "$end_date" ]]; do
    # Getting the year, month and day from the current epoch
    start=$(date -d "$current_epoch" +%Y%m%d)

    # Getting the year, month and day from the next epoch and increment the current epoch
    current_epoch=$(date -I -d "$current_epoch + $increment")
    end=$(date -d "$current_epoch" +%Y%m%d)

    # Some logic to fill in the last 10 days of the download 
    if [[ "$current_epoch" > "$end_date" ]]; then
        # Getting bach to the last valid date
        current_epoch=$(date -I -d "$current_epoch - $increment")
        start=$(date -d "$current_epoch" +%Y%m%d)
        # Getting the difference in days between the date and the end date
        # Convert to seconds since epoch
        seconds_end=$(date -d "$end_date" +%s)
        seconds_date=$(date -d "$current_epoch" +%s)
        # Subtract and convert to days
        increment="$(( ($seconds_end - $seconds_date)/86400 )) days"

        # Getting the year, month and day from the next epoch and increment the current epoch
        current_epoch=$(date -I -d "$current_epoch + $increment")
        end=$(date -d "$current_epoch" +%Y%m%d)

        if [[ "$current_epoch" > "$end_date" ]]; then
            break
        fi

        # Construct the url with date
        url_time="${url}&begin=${start}0001&end=${end}0000"
        
        # Use curl to download the data                                                                                                                                                                                                            
        echo "Downloading data from Ogimet for station ${station} from $start to $end"
        wget -q -O - ${url_time} >> ${output_file}
        break
    fi

    # Construct the url with date
    url_time="${url}&begin=${start}0001&end=${end}0000"
    
    # Use curl to download the data                                                                                                                                                                                                            
    echo "Downloading data from Ogimet for station ${station} from $start to $end"
    wget -q -O - ${url_time} >> ${output_file}
    
    # Check if the download was successful                                                                                                                                                                                                     
    if [ $? -eq 0 ]; then
	echo "Data successfully downloaded to ${output_file}."
    else
	echo "Failed to download data. Please check the URL and parameters."
    fi    
    #Ogimet has policy for 1 request from an ip every 20s. The request may be up to 10-12 days long (even though that's much less than the 200 000 reports they claim)
    sleep 20
done

date
