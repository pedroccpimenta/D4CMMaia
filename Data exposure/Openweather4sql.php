<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

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


// header('CharSet', 'UTF-8');

header('Content-type: application/json;charset=utf-8');
date_default_timezone_set('Europe/Lisbon');

echo '{"type":"FeatureCollection", "features":[';
// echo "{";
// echo "{'agora':'".date('d/m/Y')." ".date('H.i.sa')."'";

if (!function_exists('mysqli_init') && !extension_loaded('mysqli')) {
    //echo ", 'ax':false";
} else {
    //echo ", 'ax':true";
}

 

// The variables $servername, $username and $password (to access the database)
// are stored in the file "credentials.php"
require 'credentials.php';
// Create connection
$conn = new mysqli($servername, $username, $password, "BAZE");


// Check connection
if ($conn->connect_error) 
	{
    die("'r':'".  $conn->connect_error . "'");
	}
	else{
	//echo "... r so far so good...";
}
	
// Senão tiver local -> Por Default mostra todos os locais
if(isset($_GET['ponto'])){ $ponto = $_GET['ponto']; } 
else {
	$sql = "SELECT distinct(local) FROM baze21r where fonte = 'OpenWeatherMap'";
    $result = mysqli_query($conn, $sql);
    $n = mysqli_num_rows($result); # Conta o nº de resultados

    $plocal=array();

    $i=1;
    while($row = mysqli_fetch_assoc($result)) 
        {   
            array_push($plocal, $row['local']);           
               
        }

    $n =count($plocal);
    $i=1;

    echo '{"local":[';
    foreach ( $plocal as $b) { echo '"'.$b.'"'; if ($i<$n)  { echo ", "; } $i++; }
 
    echo "]".PHP_EOL; 
    echo "}]".PHP_EOL; 

    exit("}");


}

$agora = new \DateTime();
$format = "Y-m-d H:i:s";
$datainic= new $agora;
$datainic->modify('-3 days');

$sql = "SELECT * FROM  baze21r where fonte='OpenWeatherMap' and local='".$ponto."' and data > '".$datainic->format($format)."'  ORDER BY regdata desc;";

$result = mysqli_query($conn, $sql);
$n = mysqli_num_rows($result); # Conta o nº de resultados

$ul=mysqli_fetch_assoc($result); # Pega no 1º resultado do local

echo '{"type":"Feature","geometry":{"type":"Point","coordinates":['.number_format($ul['lon'],6).','.number_format($ul['lat'],6).']}';
echo ',"properties":{ "popupContent":"'.$ponto.'", '.PHP_EOL;


 mysqli_data_seek($result, 0); # Volta a iniciar a pilha

$pdata=array();
$pTemp=array();

$ppressao=array();
$phumidade=array();
$pnebulosidade=array();
$pvento=array();
$pventodir=array();
$pvis=array();

$i=1;
while($row = mysqli_fetch_assoc($result)) 
{	//echo '"aspas duplas"';
	array_push($pdata, $row['data']);			
    array_push($pTemp, $row['temp']);           
    array_push($ppressao, $row['pressao']);
    array_push($phumidade, $row['humidade']);
    array_push($pnebulosidade, $row['nebulosidade']);           
    array_push($pvento, $row['vento']);           
    array_push($pventodir, $row['ventodir']);           
    array_push($pvis, $row['vis']);         		
}

$n =count($pdata);
$i=1;

echo '"data":[';
foreach ( $pdata as $b) { echo '"'.$b.'"'; if ($i<$n)  { echo ", "; } $i++; }
echo "],".PHP_EOL;

$n =count($pTemp);
$i=1;
echo '"Temp":[';
foreach ( $pTemp as $b) { echo $b; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Pressao":[';
foreach ( $ppressao as $b) { echo $b; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Humidade":[';
foreach ( $phumidade as $b) { echo $b; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Nebulosidade":[';
foreach ( $pnebulosidade as $b) { echo $b; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Vento":[';
foreach ( $pvento as $b) { echo $b; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Ventodir":[';
foreach ( $pventodir as $b) { echo $b; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "],".PHP_EOL;

$i=1;
echo '"Vis":[';
foreach ( $pvis as $b) { echo $b; if ($i<$n) { echo ", "; } else if (is_null($b)) {echo "null";} $i++; }
echo "]".PHP_EOL;

echo "}}]".PHP_EOL; 

$w=mysqli_close($conn);

if(isset($_GET['debug']))
{
    echo "Debug: ".$k." pontos.";
}

exit("}");

?>