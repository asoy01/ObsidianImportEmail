# Read the setting file
$setting_file = ".\Settings.json"
$json = ConvertFrom-Json -InputObject (Get-Content $setting_file -Raw)

$argument = "-File " + $json.MonitorScript
Start-Process -WindowStyle Hidden -FilePath powershell.exe -ArgumentList $argument