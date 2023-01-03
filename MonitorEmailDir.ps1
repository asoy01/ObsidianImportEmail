# Read the setting file
$setting_file = ".\Settings.json"
$json = ConvertFrom-Json -InputObject (Get-Content $setting_file -Raw)

# Set up a filesystem watcher
$watcher = New-Object System.IO.FileSystemWatcher 
$watcher.Path =  $json.WatchDir 
$watcher.Filter = "*.eml" 
$watcher.IncludeSubdirectories = $false 
$watcher.EnableRaisingEvents = $true

# Construct an action to be executed when a new file is created
$action_command_line = $json.Python.Command + " " + $json.Python.Script + " -f " + $path
$action = { $path = $Event.SourceEventArgs.FullPath
Invoke-Expression $action_command_line
}

# Register the action to the watcher
Register-ObjectEvent $watcher "Created" -Action $action
while ($true) { sleep 1 }