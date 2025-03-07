from recorder.malina_raw_recorder import record_radio_with_backup, shutdown_computer

# Proměnné pro nahrávání
radio_url = "https://stream.rcs.revma.com/asn0cmvb938uv"
interval_duration = 900  # Výchozí interval 15 minut
total_duration = 9000  # Výchozí celková doba 2.5 hodiny
temp_file_prefix = "temp_stream"
output_file_prefix = "recorded_radio"

def start_recording(url, interval, total, temp_prefix, output_prefix):
    record_radio_with_backup(url, interval, total, temp_prefix, output_prefix)
    shutdown_computer()
