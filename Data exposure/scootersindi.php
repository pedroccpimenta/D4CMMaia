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


require 'credentials.php';

echo '{';



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
	

$sql = "SELECT * FROM scooterindi1 order by regdata desc limit 680";
$result = mysqli_query($conn, $sql);
$n = mysqli_num_rows($result);

$i=1;
$tt="";
$nbikes="";
$kmsdisp="";
$dispercent="";

while($row = mysqli_fetch_assoc($result)) 
{	//echo '"aspas duplas"';
    $tt=$tt.'"'.$row['regdata'].'"';
    $nbikes=$nbikes.$row['nbikes'];
    $kmsdisp=$kmsdisp.$row['kmsdisp'];

    if ($i<$n)
    {   $tt=$tt.", ";
        $nbikes=$nbikes.", ";
        $kmsdisp=$kmsdisp.", ";
    }
    $i++;

}
echo PHP_EOL.'"t":['.$tt.'], '.PHP_EOL.PHP_EOL;
echo '"nbikes":['.$nbikes.'], '.PHP_EOL.PHP_EOL;
echo '"kmsdisp":['.$kmsdisp.'] '.PHP_EOL;
//echo "---".$row.gettype($row);

 

$w=mysqli_close($conn);
//echo ", 'w':'".$w."'";

//echo date('h:i:sa');

if(isset($_GET['debug']))
{
    echo "Debug: ".$k." pontos.";
}

exit("}");

?>
