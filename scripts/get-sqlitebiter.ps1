$package = "sqlitebiter"
$latest_release = Invoke-WebRequest https://github.com/thombashi/$package/releases/latest -Headers @{"Accept"="application/json"} | ConvertFrom-Json
$version = $latest_release.tag_name
$archive = "sqlitebiter_win_x64.zip"

wget https://github.com/thombashi/$package/releases/download/$version/$archive -OutFile $archive
Expand-Archive -Path $archive -DestinationPath .
Remove-Item $archive
