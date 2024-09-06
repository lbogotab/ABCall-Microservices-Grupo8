#!/bin/bash
mkdir -p logs

export TZ=UTC  

# Array of service names
services=("realizar-factura" "log-factura" "consulta-factura" "download-file")

log_filename=$(date '+logs/service_restart_%Y%m%d_%H%M%S.log')

# Function to log timestamps
log_timestamp() {
    local service=$1
    local action=$2
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ${service} - ${action}" >> "${log_filename}"
}

# Infinite loop to randomly kill and restart services
while true; do
    # Select a random service
    service=${services[$RANDOM % ${#services[@]}]}

    # Kill the selected service
    echo "$(date '+%Y-%m-%d %H:%M:%S') Killing service: ${service}"
    docker-compose stop ${service}
    log_timestamp ${service} "stopped"

    # Wait for 20 seconds
    sleep 20

    # Restart the selected service
    echo "Restarting service: ${service}"
    docker-compose start ${service}
    log_timestamp ${service} "started"

    # Wait for before the next iteration
    sleep 5
done