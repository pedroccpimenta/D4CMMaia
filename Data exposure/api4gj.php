<?php
//header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Origin: *");
header('Access-Control-Allow-Methods: GET, POST');

  //Response.AddHeader("Access-Control-Allow-Origin", "*"); 

header('Content-type: application/json;charset=utf-8');

//header("Content-type: text/html; charset=utf-8");
//header("Access-Control-Allow-Origin: '*'");

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


//printf("Initial character set: %s\n", mysqli_character_set_name($conn));
//mysqli_set_charset($conn, "utf8mb4");

//printf("Current character set: %s\n", mysqli_character_set_name($conn));


$nome = false;

if(isset($_GET['nome'])){

    $nome = utf8_encode($_GET['nome']);

}
else
{	$nome=null;
}


switch (strtoupper($nome)) {
	case 'HIDRANTES':
	case  'HIDRANTE':

	$myfile = fopen("hidrantes-curto.geojson", "r") or die("{Unable to open file!}");
	echo fread($myfile,filesize("hidrantes-curto.geojson"));
	fclose($myfile);

	break;
/*    case "TPWAPI":
      header("Location: http://baze.cm-maia.pt/BaZe/api/testepontos.php?fonte=WeatherAPI"); 
    exit();
*/
	default:
		# code...

$sql="select * from GJSON where nome='".$nome."'";
    // echo $sql;
$result= mysqli_query($conn,$sql);
//    echo "Resul".$result.PHP_EOL;
//  echo $result;

flush();

if (mysqli_num_rows($result) > 0 and $nome!=false) {

// echo "TEMOS VALOR";
  while($row = mysqli_fetch_assoc($result)) 
  {// output data of each row
  //echo '<br>'.PHP_EOL.'"dados":[<br>';
  echo $row['valor'];
  }   
}
else {
  // code...
  //  echo "ci siamo";  
  echo '{'.PHP_EOL.'    "título": "Baze datalake  - Objectos GeoJSON disponíveis",'.PHP_EOL;
  echo '    "o": ['.PHP_EOL;
  echo '        ["Nome", "Descrição", "Fonte", "Data"],'.PHP_EOL;  
  $sql="select * from GJSON  where status not like 'indisp%' order by nome" ;

  $result= mysqli_query($conn,$sql);
  $nr=mysqli_num_rows($result);
//
  //echo PHP_EOL.$nr.PHP_EOL;
  //echo $A;
  $i=1;
  while($row = mysqli_fetch_assoc($result)) 
  {   // output data of each row
      //echo '<br>'.PHP_EOL.'"dados":[<br>';
      $nome=utf8_encode($row['nome']);
      $desc=utf8_encode( $row['Desc']);
      $fonte=utf8_encode( $row['fonte']);
      $dato=utf8_encode( $row['data']);

      if ($fonte=="")      {$fonte="N/A";}
      if ($dato=="")      {$dato="N/A";}

      echo '        ["'.trim($nome).'", "'.$desc.'", "'.$fonte.'", "'.$dato.'"]';
      if ($i < $nr)
      {   echo ',';
      }
      else
      {}
      $i++;
//      echo $i.PHP_EOL;

      echo PHP_EOL;
  }   


echo "    ],".PHP_EOL;
echo '    "api url": "http://baze.cm-maia.pt/BaZe/api/api4gj.php",'.PHP_EOL;
echo '    "exemplo": "http://baze.cm-maia.pt/BaZe/api/api4gj.php?nome=Aeroporto",'.PHP_EOL;
echo '    "JSON validado em": ["https://www.itb.ec.europa.eu/json/any/upload","https://jsonlint.com/", "https://jsonformatter.curiousconcept.com/"],'.PHP_EOL;
echo '    "GeoJSON validado em": ["https://www.itb.ec.europa.eu/json/geojson/upload", "https://geojsonlint.com/", "https://geojson.io/"]'.PHP_EOL;
echo "}";
}
}
mysqli_close($conn);

?>
