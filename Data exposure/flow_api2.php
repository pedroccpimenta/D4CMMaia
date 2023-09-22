<?php
// FLOW FROM THE SKY - CATEGORIES
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
    $sql = "SELECT DISTINCT(C_G) FROM Flow_Categories ORDER BY C_G ASC";
    $result = mysqli_query($conn, $sql);

    $C_G = array();
    $Category = array();

    $i=1;
    while($row = mysqli_fetch_assoc($result)) 
        {   
            array_push($C_G, $row['C_G']);   
        }

    $n=count($C_G);
    $n2=count($Category);
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

// $sql = "SELECT C_G, DATE(Start_datetime) as Start_datetime, DATE(End_datetime) AS End_datetime, Bicycle, Bus, Car, Heavy, Light, Motorcycle FROM BAZE.Flow_Distribution WHERE C_G = '".$C_G."' AND DATE(Start_datetime) >= '2022-07-01' and DATE(End_datetime) <= '$dataToday' order by End_datetime desc;";
$sql = "SELECT C_G, Category, DATE(Trajectory_start_datetime) AS Trajectory_start_datetime, Trajectory_end_datetime, Average_speed_kpxh, Duration_of_occurrence_s, Stationary_duration_s FROM BAZE.Flow_Categories WHERE C_G = '".$C_G."' AND DATE(Trajectory_start_datetime) >= '2022-10-08' AND DATE(Trajectory_end_datetime) <= '2022-10-25' <= '$dataToday' ORDER BY Trajectory_end_datetime DESC;";

//echo $sql;

$result = mysqli_query($conn, $sql);
$n = mysqli_num_rows($result); # Conta o nº de resultados
$ul = mysqli_fetch_assoc($result); # Pega no 1º resultado do local

echo '"properties":{ "CAMERA_GATE":"'.$C_G.'", '.PHP_EOL;

mysqli_data_seek($result, 0); # Volta a iniciar a pilha

// CREATE EMPTY ARRAYS
$pC_G=array();
$pCategory=array();
$pTrajectory_start_datetime=array();
$pTrajectory_end_datetime=array();
$pAverage_speed_kpxh=array();
$pDuration_of_occurrence_s=array();
$pStationary_duration_s=array();

// INSERT DATA INTO THE EMPTY ARRAYS 
$i=1;
while($row = mysqli_fetch_assoc($result)) 
{	
	array_push($pC_G, $row['C_G']);		
    array_push($pCategory, $row['Category']);	
    array_push($pTrajectory_start_datetime, $row['Trajectory_start_datetime']);           
    array_push($pTrajectory_end_datetime, $row['Trajectory_end_datetime']);
    array_push($pAverage_speed_kpxh, $row['Average_speed_kpxh']);
    array_push($pDuration_of_occurrence_s, $row['Duration_of_occurrence_s']);  
    array_push($pStationary_duration_s, $row['Stationary_duration_s']);    	
}

// JSON BUILDING
$i=1;
echo '"C_G":[';
foreach ( $pC_G as $b) { echo '"'.$b.'"'; if ($i<$n)  { echo ", "; } $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Category":[';
foreach ( $pCategory as $b) { echo '"'.$b.'"'; if ($i<$n)  { echo ", "; } $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Trajectory_start_datetime":[';
foreach ( $pTrajectory_start_datetime as $b) { echo '"'.$b.'"'; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Trajectory_end_datetime":[';
foreach ( $pTrajectory_end_datetime as $b) { echo '"'.$b.'"'; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Average_speed_kpxh":[';
foreach ( $pAverage_speed_kpxh as $b) { echo ''.$b.''; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Duration_of_occurrence_s":[';
foreach ( $pDuration_of_occurrence_s as $b) { echo ''.$b.''; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Stationary_duration_s":[';
foreach ( $pStationary_duration_s as $b) { echo ''.$b.''; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "]".PHP_EOL;

echo "}}".PHP_EOL; 

$w=mysqli_close($conn);

exit("}");

?>