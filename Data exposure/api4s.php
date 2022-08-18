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

if(isset($_GET['formato'])){
    $formato = utf8_encode($_GET['formato']);
}
else
{ $formato="JSON";
}


$sql="select * from fonte where nome='".$nome."'";
    // echo $sql;
$result= mysqli_query($conn,$sql);
//    echo "Resul".$result.FLINHA;
//  echo $result;

flush();

if (mysqli_num_rows($result) > 0 and $nome!=false) {


// echo "TEMOS VALOR";
 
  $sql="select ano, ".$nome." from baze21RA order by ano";  
  $result2= mysqli_query($conn,$sql);
  $data="[";
  $valor="[";
  $nsd=mysqli_num_rows($result2);

if ($formato=="CSV")
{   
  echo "Ano, ".$nome.PHP_EOL;
  while($row = mysqli_fetch_assoc($result2)) 
  { $tv=$row[$nome]===NULL ? "null" : $row[$nome];
    echo $row['ano'].", ".$tv.PHP_EOL;
  }  
}
else
{
  $si=0;
  while($row = mysqli_fetch_assoc($result2)) 
  {   $data=$data.$row["ano"];
      $tv=$row[$nome]===NULL ? "null" : $row[$nome];
      $valor=$valor.$tv;
      $si++;
      if ($si<$nsd)
      {  $data=$data.", "; 
         $valor=$valor.", ";
      }
  }   
  $data=$data."],"; 
  $valor=$valor."]";

    echo '{"t":'.$data.PHP_EOL;
    echo ' "v":'.$valor.",".PHP_EOL;
}

if (9==9)
{

$row = mysqli_fetch_assoc($result);
    $nome=utf8_encode($row['nome']);
      $desc=utf8_encode( $row['descri']);
      $comm=utf8_encode( $row['Comm']);
      $dato=utf8_encode( $row['RegDate']);
      $editor =utf8_encode( $row['editor']);
      $fonte =utf8_encode( $row['fonte']);


echo '    "metadata":{'.PHP_EOL;
echo '          "nome":"'.$nome.'", '.PHP_EOL;			
echo '          "descrição":"'.$desc.'", '.PHP_EOL;			
echo '          "Editor":"'.$editor.'", '.PHP_EOL;			
echo '          "fonte":"'.$fonte.'", '.PHP_EOL;			
echo '          "comm":"'.$comm.'" '.PHP_EOL;			
echo '               },'.PHP_EOL;
echo '    "source":{'.PHP_EOL; 
echo '       "api url": "http://baze.cm-maia.pt/BaZe/api/api4s.php",'.PHP_EOL;
echo '       "exemplo": "http://baze.cm-maia.pt/BaZe/api/api4s.php?nome=nhabit",'.PHP_EOL;
echo '       "JSON validado em": ["https://www.itb.ec.europa.eu/json/any/upload","https://jsonlint.com/"]'.PHP_EOL;
echo '     }'.PHP_EOL;


 }

    echo "}";  

}
else
{
  $formatolinha='         ["%`»15.15s", "%30.30s", "%12.12s", "%30s", "%30s"], ';
  // code...
  //  echo "ci siamo";  
  echo '{'.PHP_EOL.'    "título": "BaZe datalake  - Séries disponíveis",'.PHP_EOL;
  echo '    "o": ['.PHP_EOL;
  
  //printf($formatolinha.PHP_EOL, "Nome", "Descrição", "Fonte", "Data edição", "Editor");
  printf( '         ["Nome"'.str_pad("", 15-strlen("Nome"), " "));
  print(', "Descrição"'.str_pad("", 43-mb_strlen("Descrição"), " "));
  print(', "Fonte"'.str_pad("", 25-strlen("Fonte"), " "));
 // print(', "Data"'.str_pad("", 18-strlen("Data"), " ")." ");
  print(', "Comentário"'.str_pad("", 19-mb_strlen("Comentário"), " "));
  print('],'.PHP_EOL);  
  $sql="select * from fonte  where status not like 'indisp%' order by nome" ;

  $result= mysqli_query($conn,$sql);
  $nr=mysqli_num_rows($result);
//
  //echo FLINHA.$nr.FLINHA;
  //echo $A;
  $i=1;
  while($row = mysqli_fetch_assoc($result)) 
  {   // output data of each row
      //echo '<br>'.FLINHA.'"dados":[<br>';
      $nome=utf8_encode($row['nome']);
      $desc=utf8_encode( $row['descri']);
      $comm=utf8_encode( $row['Comm']);
      $dato=utf8_encode( $row['RegDate']);
      $editor =utf8_encode( $row['editor']);
      $fonte =utf8_encode( $row['fonte']);


      if ($fonte=="")      {$fonte="N/A";}
      if ($dato=="")      {$dato="N/A";}
      if ($editor=="")      {$editor="N/A";}
      if ($comm=="")      {$comm="N/A";}


     // printf($formatolinha, $nome, $desc, $fonte, $dato, $editor);
     // echo strlen($nome).PHP_EOL;
      $n2p = mb_strlen($nome) < 15 ? $nome : substr($nome, 0, 10)."(...)";
      printf ('         ["'.$nome.'"'.str_pad("", 15-mb_strlen($nome)).', ');
      
      $d2p = mb_strlen($desc) <= 43 ? $desc."" : substr($desc, 0, 38)."(...)";
      printf ('"'.$d2p.'"'.str_pad("", 43-mb_strlen($d2p), " ").', ');
      
      $f2p = mb_strlen($fonte) <= 25 ? $fonte : substr($fonte, 0, 20)."(...)";
      printf ('"'.$f2p.'"'.str_pad(" ", 25-mb_strlen($f2p)).', ');
      
      $d2p = mb_strlen($dato) < 20 ? $dato : substr($dato, 0, 15)."(...)";
   //   printf ('"'.$d2p.'"'.str_pad("", 19-strlen($d2p)).', ');
      $c2p = mb_strlen($comm) <= 50 ? $comm : substr($comm, 0, 45)."(...)";
      printf ('"'.$c2p.'"'.str_pad(" ", 50-mb_strlen($c2p)).']');

    //  	printf(PHP_EOL.".".$desc.".".PHP_EOL);

      if ($i < $nr)
      {   echo ',';
      }
      else
      {}
      $i++;
//      echo $i.FLINHA;

      echo PHP_EOL;
  }   


if (9==9)
{echo "    ],".PHP_EOL;
echo '    "api url": "http://baze.cm-maia.pt/BaZe/api/api4s.php",'.PHP_EOL;
echo '    "exemplo": "http://baze.cm-maia.pt/BaZe/api/api4s.php?nome=nhabit",'.PHP_EOL;
echo '    "JSON validado em": ["https://www.itb.ec.europa.eu/json/any/upload","https://jsonlint.com/"]'.PHP_EOL;
//echo '    "GeoJSON validado em": ["https://www.itb.ec.europa.eu/json/geojson/upload", "https://geojsonlint.com/", "https://geojson.io/"]'.PHP_EOL;
 }

 echo "}";

}



mysqli_close($conn);

?>
