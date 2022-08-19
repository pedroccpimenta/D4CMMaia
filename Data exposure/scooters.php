<?php
    // Allow from any origin
    if (isset($_SERVER['HTTP_ORIGIN'])) {
        // Decide if the origin in $_SERVER['HTTP_ORIGIN'] is one
        // you want to allow, and if so:
        header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
        header('Access-Control-Allow-Credentials: true');
        header('Access-Control-Max-Age: 86400');    // cache for 1 day
    }
    
    // Access-Control headers are received during OPTIONS requests
    if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
        
        if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD']))
            // may also be using PUT, PATCH, HEAD etc
            header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
        
        if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']))
            header("Access-Control-Allow-Headers: {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");
}    



header('Content-type: application/json;charset=utf-8');

echo '{"type":"FeatureCollection", "features":[';

if (!function_exists('mysqli_init') && !extension_loaded('mysqli')) 
{
    //echo ", 'ax':false";
} else {
    //echo ", 'ax':true";
}

require 'credentials.php';

// Create connection
$conn = new mysqli($servername, $username, $password, "BAZE");

// Check connection
if ($conn->connect_error) 
	{
    die("'r':'".  $conn->connect_error . "'");
	}
	else{
	// echo "... r so far so good...";
}
	

$sql = "SELECT * FROM lastScooters";
$result = mysqli_query($conn, $sql);
$n = mysqli_num_rows($result);

$i=1;
while($row = mysqli_fetch_assoc($result)) 
{	//echo '"aspas duplas"';
    $topop="";


   // echo PHP_EOL.($row['lon']+8.592366054654121).PHP_EOL.($row['lat']-41.192674496763246).PHP_EOL;
          
   // echo PHP_EOL.sqrt( ($row['lon']+8.592366054654121)**2  + ($row['lat']-41.192674496763246)**2 ).PHP_EOL;
    if(sqrt( ($row['lon']+8.592366054654121)**2  + ($row['lat']-41.192674496763246)**2 ) <.001)
    { $topop="Parked";
    }    
    else
    {      
    if ($row['is_disabled'])
    {   $topop="Disabled";

    }
    else
    {   if ($row['is_reserved'])
        {   $topop="Reserved";

        }
        else
        {   $topop="Not&nbsp;reserved";

        }
        $topop=$topop."<br>CRM:".number_format($row['current_range_meters']/100,1)."&nbsp;km";
        $topop=$topop."<br>LR:".$row['last_reported'];
    }
    }

	echo '{"type":"Feature","geometry":{"type":"Point","coordinates":['.number_format($row['lon'],6).','.number_format($row['lat'],6).']}';
	echo ',"properties":{ "bike_id":"'.$row['bike_id'].'", "is_reserved": '.$row['is_reserved'].', "is_disabled":'.$row['is_disabled'].', "last_reported":"'.$row['last_reported'].'", "CRM":'.$row['current_range_meters'].', "popupContent":"'.$topop.'"';

    echo '}}';	
 //   if gettype($row)=="NULL" {} else { echo "," };
	if ($i<$n)
	{echo ",";
	}
	echo PHP_EOL;	
	//echo "====".gettype($row);	
	$i++;
}
//echo "---".$row.gettype($row);
echo "]".PHP_EOL;	
 

$w=mysqli_close($conn);
//echo ", 'w':'".$w."'";

//echo date('h:i:sa');

if(isset($_GET['debug']))
{
    echo "Debug: ".$k." pontos.";
}

exit("}");

?>
