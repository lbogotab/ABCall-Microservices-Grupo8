import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# Funcion para parsear archivo de logs service_restart.log
def parse_service_restart_log(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            timestamp_str, service, action = line.strip().split(' - ')
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            data.append({'timestamp': timestamp, 'service': service, 'action': action})
    return pd.DataFrame(data)


# Funcion para parsear archivo de logs service monitor.log
def parse_service_monitor_log(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            timestamp_str, _, service, status = line.strip().split(' - ')
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
            status = 'OK' if 'OK' in status else 'FAIL'
            data.append({'timestamp': timestamp, 'service': service, 'status': status})
    return pd.DataFrame(data)


# Parsear logs
service_restart_df = parse_service_restart_log('service_restart.log')
service_monitor_df = parse_service_monitor_log('service_monitor.log')

services = service_restart_df['service'].unique()

# Marcadores distintos para identificar detención y arranque simulados de los servicios
action_markers = {'stopped': ('x', 'red'), 'started': ('o', 'green')}

fig, axes = plt.subplots(len(services), 1, figsize=(15, 5 * len(services)), sharex=True)

# Plot data for each service
for i, service in enumerate(services):
    ax = axes[i] if len(services) > 1 else axes
    service_restart_data = service_restart_df[service_restart_df['service'] == service]
    service_monitor_data = service_monitor_df[service_monitor_df['service'] == service]

    # Plot service monitor status
    ax.plot(
        service_monitor_data['timestamp'],
        service_monitor_data['status'],
        label=f'{service} status',
        color='blue',
    )


    # Plot service restart events with different markers for each action
    for action, marker in action_markers.items():
        action_data = service_restart_data[service_restart_data['action'] == action]
        ax.scatter(
            action_data['timestamp'],
            action_data['action'],
            label=f'{service} {action}',
            marker=marker[0],
            color=marker[1],
        )

    # Formatting the subplot
    ax.set_title(f'Service: {service}')
    ax.set_ylabel('Status/Action')
    ax.legend()

# Formatting the plot
plt.xlabel('Timestamp')
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
