<?php
//header('Access-Control-Allow-Origin: *');
//Response.AddHeader("Access-Control-Allow-Origin", "*"); 
//header("Access-Control-Allow-Origin: '*'");
header("Access-Control-Allow-Origin: *");
header('Access-Control-Allow-Methods: GET, POST');

//header("Content-type: text/html; charset=utf-8");
header('Content-type: application/json;charset=utf-8');

if (isset($_SERVER['HTTP_ORIGIN'])) 
{
  // Decide if the origin in $_SERVER['HTTP_ORIGIN'] is one you want to allow, and if so:
  header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
  header('Access-Control-Allow-Credentials: true');
  //        header('Access-Control-Max-Age: 86400');    // cache for 1 day
}


// Access-Control headers are received during OPTIONS requests
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') 
{
  if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD']))
            header("Access-Control-Allow-Methods: GET, POST, OPTIONS");         

  if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']))
            header("Access-Control-Allow-Headers: {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");

  exit(0);
}

require 'credentials.php';


// Create connection
$conn = new mysqli($servername, $username, $password, "BAZE");
$conn->set_charset("utf8");

// Check connection
if ($conn->connect_error) 
{
    die("'r':'".  $conn->connect_error . "'");
}

if(isset($_GET['cpe'])){
    $cpe=$_GET['cpe'];
}
else
{   $cpe="PT0002000033026194LZ";
}

if(isset($_GET['ag'])){
    $ag=$_GET['ag'];
}
else
{   $ag="mes";
}

if(isset($_GET['tstart'])){
    $ts=$_GET['tstart'];
}
else
{   $ts="";
}

if(isset($_GET['tend'])){
    $te=$_GET['tend'];
}
else
{   $te="";
}




//echo "cpe:".$cpe."agf: ".$ag.PHP_EOL;

switch ($ag) {
    case 'mes':
        $factor="100000000"; // por mês
        $limite="200";
        break;
    case 'dia':   
        $factor="1000000"; // por dia
        $limite=200;
        break;
    case "hora":
        $factor="10000"; // por hora
        $limite=300;
        break;
    default:
        $factor=100;
        $limite=200;
}


switch ($cpe) {
  case 'PT0002000077348081AG':
  case 'PT0002000081997398TD':
  case "PT0002000073573036KH":
  case "PT0002000078441876HB":
  case "PT0002000082549706RH":
  case "PT0002000068859325FL":
  case "PT0002000079469719HF":
  case "PT0002000110090564GD":
  case "PT0002000201212633ZB":
  case "PT0002000068856826ZG":
  case "PT0002000068856781NM":
  case "PT0002000115673389QK":
  case "PT0002000115673471CB":
  
    $sql="select id, hora , floor(hora/".$factor.") as t, sum(PotActiva+PotReactIndut+PotReactCapac) as v from Consumo15m where cpe='".$cpe."' and floor(hora/".$factor.") in ( select distinct floor(hora/".$factor.") from Consumo15m ) group by floor(hora/".$factor.") order by hora desc limit ".$limite.";";

    if ($te!="" and $ts !="")
    {
        $sql="select id, hora , floor(hora/".$factor.") as t, sum(PotActiva+PotReactIndut+PotReactCapac) as v from Consumo15m where cpe='".$cpe."' and hora < date(".$te.") and hora > date(".$ts.") and floor(hora/".$factor.") in ( select distinct floor(hora/".$factor.") from Consumo15m ) group by floor(hora/".$factor.") order by hora limit ".$limite.";";

    }    

# code...
    break;
  
  default:
    $sql="select id, hora , floor(hora/".$factor.") as t, sum(DadosdeConsumo) as v from Consumo15m where cpe='".$cpe."' and floor(hora/".$factor.") in ( select distinct floor(hora/".$factor.") from Consumo15m ) group by floor(hora/".$factor.") order by hora desc limit ".$limite.";";
    # code...

    if ($te!="" and $ts !="")
    {
         $sql="select id, hora , floor(hora/".$factor.") as t, sum(DadosdeConsumo) as v from Consumo15m where cpe='".$cpe."'  and hora < date(".$te.") and hora > date(".$ts.")  and floor(hora/".$factor.") in ( select distinct floor(hora/".$factor.") from Consumo15m ) group by floor(hora/".$factor.") order by hora limit ".$limite.";";
   
    }    
    break;
}

$sql2="select * from LocaisDeConsumo where CPE='".$cpe."'";
//echo $sql2;
$r2= mysqli_query($conn,$sql2);
//echo "====".var_dump($r2);
$n2 = mysqli_num_rows($r2);

//echo $n2;
if ($n2==1)//echo $n2; 
    $d2 = mysqli_fetch_assoc($r2);
else
{
    $d2=["morada"=>"Verifique o CPE na tabela LocaisDeConsumo!!",
        "tipo"=>"***",
        "Freguesia"=>"***",
        "Tipo"=>"***",
        "Instalação"=>"***",
        "Tensão"=>"***",
        "Latitude"=>"null",
        "Longitude"=>"null",

      ];
}
//echo $sql;
//flush(); exit(2);

$result= mysqli_query($conn,$sql);
$n = mysqli_num_rows($result);
//echo "Número de registos recebidos:".$n.PHP_EOL;
//flush(); exit(2);

echo '{"cpe":"'.$cpe.'", '.PHP_EOL;
echo '"ag":"'.$ag.'", '.PHP_EOL;
echo '"ts":"'.$ts.'", '.PHP_EOL;
echo '"te":"'.$te.'", '.PHP_EOL;
echo '"sql":"'.$sql.'", '.PHP_EOL;
    
$t=array();
$v=array();

while($row = mysqli_fetch_assoc($result)) 
{ array_push($t, $row["t"]);
  array_push($v, $row["v"]);
}   

echo ('"t": '.json_encode($t)).",".PHP_EOL;
echo ('"v": '.json_encode($v, JSON_NUMERIC_CHECK)).",".PHP_EOL;

$dt = new DateTime("now", new DateTimeZone('Europe/Lisbon'));

echo '"metadata":{"consultado em":"'.$dt->format("d-m-Y H:i:s").'", "editor":"PCP (ppimenta@cm-maia.pt), Francisco Mesquita", "morada":"'.$d2['morada'].'", "Freguesia":"'.$d2['Freguesia'].'", "tipo":"'.$d2['tipo'].'", "Instalação":"'.$d2['Instalação'].'","Tensão":"'.$d2['Tensão'].'","Lat":'.$d2['Latitude'].', "Lon":'.$d2['Longitude'].', "outros":"(...)"}';

echo "}";
flush();
mysqli_close($conn);

?>