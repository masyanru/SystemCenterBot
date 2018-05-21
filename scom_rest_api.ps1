$scomHeaders = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$scomHeaders.Add('Content-Type','application/json; charset=utf-8')

$bodyraw = "Windows"
$Bytes = [System.Text.Encoding]::UTF8.GetBytes($bodyraw)
$EncodedText =[Convert]::ToBase64String($Bytes)
$jsonbody = $EncodedText | ConvertTo-Json

$uriBase = "http://srv-scom-01/OperationsManager/authenticate"

$auth = Invoke-RestMethod -Method POST -Uri $uriBase -Headers $scomheaders -body $jsonbody -UseDefaultCredentials -SessionVariable websession

$query = @(@{ 
        "classid" = "58778b00-7b4b-6c79-6365-2a32e982d4a3"
        "criteria" =""
        "displayColumns" = "name", "age", "repeatcount"
        
        })

$jsonquery = $query | ConvertTo-Json
$Response = Invoke-WebRequest -Uri "http://srv-scom-01/OperationsManager/data/alert" -Method Post -Body $jsonquery -ContentType "application/json" -UseDefaultCredentials -WebSession $websession
$alerts = ConvertFrom-Json -InputObject $Response.Content
$alerts.rows | select -First 5
