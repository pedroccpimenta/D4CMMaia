<?php
// FLOW FROM THE SKY - DISTRIBUTION
// DATA PARSING AND JSON CREATOR

// API ACCESS AND HEADERS
// -------------------------------------------------------------------------------------------------------------
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

  if (isset($_SERVER['HTTP_ORIGIN'])) {
        // Decide if the origin in $_SERVER['HTTP_ORIGIN'] is one you want to allow, and if so:
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
        // HEADER ('CHARTSET', 'UTF-8');
        header('Content-type: application/json;charset=utf-8');
        date_default_timezone_set('Europe/Lisbon');
// -------------------------------------------------------------------------------------------------------------

// DATABASE CREDENTIALS STORED IN 'credentials_ef.php'
require 'credentials_ef.php';

// JSON START
echo '{"flow":{';

// CREATE CONNECTION TO THE DATABASE
$conn = new mysqli($servername, $username, $password, "BAZE");

// CHECK CONNECTION
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
  }

// IF THERE IS NO CHOSEN CAMERA, SHOW ALL
if(isset($_GET['C_G']))
{ $C_G = $_GET['C_G']; 
} 
else {	
    $sql = "SELECT DISTINCT(C_G) FROM Flow_Distribution ORDER BY C_G ASC";
    $result = mysqli_query($conn, $sql);

    $C_G = array();

    $i=1;
    while($row = mysqli_fetch_assoc($result)) 
        {   
            array_push($C_G, $row['C_G']);       
        }

    $n=count($C_G);
    $i=1;

    echo '"properties":{"C_G":[';
    foreach ( $C_G as $b) { echo '"'.$b.'"'; if ($i<$n)  { echo ", "; } $i++; }
 
    echo "]}".PHP_EOL; 
    echo "}".PHP_EOL; 

    exit("}");
}

// CURRENT TIME DEFINITION AND QUERY FORMAT
$agora = new \DateTime();
$format = "Y-m-d H:i:s";
$dataToday= new $agora;
$dataToday=$dataToday->format($format);

//$sql = "SELECT C_G, DATE(Start_datetime) as Start_datetime, DATE(End_datetime) AS End_datetime, Bicycle, Bus, Car, Heavy, Light, Motorcycle FROM BAZE.Flow_Distribution WHERE C_G = '".$C_G."' AND DATE(Start_datetime) >= '2022-07-01' and DATE(End_datetime) <= '$dataToday' order by End_datetime desc;";
$sql = "SELECT C_G, DATE(Start_datetime) 
     as Start_datetime, End_datetime, Bicycle, Bus, Car, Heavy, Light, Motorcycle 
     FROM BAZE.Flow_Distribution 
     WHERE C_G = '".$C_G."' AND DATE(Start_datetime) >= '2022-07-01' and DATE(End_datetime) <= '$dataToday' 
     order by End_datetime desc;";

//echo $sql;

$result = mysqli_query($conn, $sql);
$n = mysqli_num_rows($result); # Conta o nº de resultados
$ul=mysqli_fetch_assoc($result); # Pega no 1º resultado do local

echo '"properties":{ "CAMERA_GATE":"'.$C_G.'", '.PHP_EOL;

mysqli_data_seek($result, 0); # Volta a iniciar a pilha

// CREATE EMPTY ARRAYS
$pC_G=array();
$pStart_datetime=array();
$pEnd_datetime=array();
$pBicycle=array();
$pBus=array();
$pCar=array();
$pHeavy=array();
$pLight=array();
$pMotorcycle=array();

// INSERT DATA INTO THE EMPTY ARRAYS 
$i=1;
while($row = mysqli_fetch_assoc($result)) 
{	
	array_push($pC_G, $row['C_G']);			
    array_push($pStart_datetime, $row['Start_datetime']);           
    array_push($pEnd_datetime, $row['End_datetime']);
    array_push($pBicycle, $row['Bicycle']);
    array_push($pBus, $row['Bus']);
    array_push($pCar, $row['Car']);           
    array_push($pHeavy, $row['Heavy']);           
    array_push($pLight, $row['Light']);           
    array_push($pMotorcycle, $row['Motorcycle']);         	

}

// JSON BUILDING
$i=1;
echo '"C_G":[';
foreach ( $pC_G as $b) { echo '"'.$b.'"'; if ($i<$n)  { echo ", "; } $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Start_datetime":[';
foreach ( $pStart_datetime as $b) { echo '"'.$b.'"'; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"End_datetime":[';
foreach ( $pEnd_datetime as $b) { echo '"'.$b.'"'; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Bicycle":[';
foreach ( $pBicycle as $b) { echo ''.$b.''; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Bus":[';
foreach ( $pBus as $b) { echo ''.$b.''; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Car":[';
foreach ( $pCar as $b) { echo ''.$b.''; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Heavy":[';
foreach ( $pHeavy as $b) { echo ''.$b.''; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Light":[';
foreach ( $pLight as $b) { echo ''.$b.''; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Motorcycle":[';
foreach ( $pMotorcycle as $b) { echo ''.$b.''; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "]".PHP_EOL;

echo "}}".PHP_EOL; 

$w=mysqli_close($conn);

exit("}");

?>