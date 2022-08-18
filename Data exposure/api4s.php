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


function add($a, $b)
{
  return $a + $b;
}

function pac($str, $t)
{     
    // $s2 = mb_strlen($str) <= $t ? $str : substr($str, 0, $t-8)."(...)";
    $s2 = strlen($str) <= $t-2 ? $str : substr($str, 0, $t-6)."(..)";
    $s3='"'.$s2.'"';
    for ($y=mb_strlen($s3);$y<$t;$y++) $s3=$s3." ";
    return $s3;
}

// Create connection
$conn = new mysqli($servername, $username, $password, "BAZE");
$conn->set_charset("utf8");

// Check connection
if ($conn->connect_error) 
{ die("'r':'".  $conn->connect_error . "'");
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

//echo $formato;
$sql="select * from fonte where nome='".$nome."'";
// echo $sql;
$result= mysqli_query($conn,$sql);


flush(); 

if (mysqli_num_rows($result) > 0 and $nome!=false) {
  $sql="select ano, `C".$nome."` from baze21RA order by ano";  

//  echo ($sql);
  $result2= mysqli_query($conn,$sql);
 
  $data="[";
  $valor="[";
  $nsd=mysqli_num_rows($result2);

if ($formato=="CSV" or $formato=="csv")
{   
  echo "Ano, ".$nome.PHP_EOL;
  while($row = mysqli_fetch_assoc($result2)) 
  { $tv=$row['C'.$nome]===NULL ? "null" : $row['C'.$nome];
    echo $row['ano'].", ".$tv.PHP_EOL;
  }  
}
else
{
  $si=0;
  $anv=false;
  while($row = mysqli_fetch_assoc($result2)) 
  {
    $si++;
    if ($row['C'.$nome]===NULL && $anv==false)
    {}
    else  
    { $anv=true;
     $data=$data.$row["ano"];

      $tv=$row['C'.$nome]===NULL ? "null" : $row['C'.$nome];
      $valor=$valor.$tv;
    
      if ($si<$nsd) 
      {  $data=$data.", "; 
         $valor=$valor.", ";
      }
    }
  }   
  $data=$data."],"; 
  $valor=$valor."]";

    echo '{"t":'.$data.PHP_EOL;
    echo ' "v":'.$valor.",".PHP_EOL;
}



$row = mysqli_fetch_assoc($result);
    $nome=utf8_encode($row['nome']);
      $desc=utf8_encode( $row['descri']);
      $desc=$row['descri'];
      
      $comm=utf8_encode( $row['Comm']);
      $dato=utf8_encode( $row['RegDate']);
      $editor =utf8_encode( $row['editor']);
      $fonte =utf8_encode( $row['origem']);


echo '    "metadata":{'.PHP_EOL;
echo '          "nome":"'.$nome.'", '.PHP_EOL;			
echo '          "descrição":"'.$desc.'", '.PHP_EOL;			
echo '          "descri+":"'.$row['DescriPlus'].'", '.PHP_EOL;      
echo '          "fonte":"'.$fonte.'", '.PHP_EOL;      
echo '          "MetaInfUrl":"'.$row["MetaInfUrl"].'", '.PHP_EOL;      
echo '          "UltimoPref":"'.$row["UltimoPref"].'", '.PHP_EOL;			
echo '          "DataUltimaActual":"'.$row["DataUltimaActual"].'", '.PHP_EOL;      
echo '          "DataUltimaActuaLocal":"'.$row["DataUltimaActuaLocal"].'", '.PHP_EOL;      
echo '          "DataUltimaVerifica":"'.$row["DataUltimaVerifica"].'", '.PHP_EOL;      

echo '          "Editor":"'.$editor.'", '.PHP_EOL;      
echo '          "comm":"'.$comm.'" '.PHP_EOL;			
echo '               },'.PHP_EOL;
echo '    "source":{'.PHP_EOL; 
echo '       "api url": "http://baze.cm-maia.pt/BaZe/api/api4s.php",'.PHP_EOL;
echo '       "exemplo": "http://baze.cm-maia.pt/BaZe/api/api4s.php?nome=nhabit",'.PHP_EOL;
echo '       "JSON validado em": ["https://www.itb.ec.europa.eu/json/any/upload","https://jsonlint.com/"]'.PHP_EOL;
echo '     }'.PHP_EOL;




    echo "}";  

}     /// Se não encontrámos a série pedida...
else
{
  echo '{'.PHP_EOL.'    "título": "BaZe datalake  - Séries disponíveis (relativas ao Concelho da Maia)",'.PHP_EOL;
  echo '    "o": ['.PHP_EOL;
  
  printf( '         ['.pac('Código', 14));

  print(', '.pac('Descrição', 40));
  print(', '.pac('Fonte', 9));
  print(', '.pac('Últ. ano', 11));
  print(', '.pac('Data act. fonte', 17));
  print(', '.pac('Data act. local', 21));
  print(', '.pac('Data ult. sinc.', 21));

  print('],'.PHP_EOL);  
  $sql="select * from fonte  where status not like 'indisp%' order by nome" ;
  $sql="select * from fonte  where status like 'disp%' order by nome" ;

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
      $descri=utf8_encode( $row['descri']);
      $descri= $row['descri'];
      $descriplus=utf8_encode( $row['DescriPlus']);
      $MetaInfoUrl=utf8_encode( $row['MetaInfUrl']);
      $DataUltimaActual=utf8_encode( $row['DataUltimaActual']);
      $DataUltimaActuaLocal=utf8_encode( $row['DataUltimaActuaLocal']);
      $DataUltimaVerifica=utf8_encode( $row['DataUltimaVerifica']);
      $UltimoPref=utf8_encode( $row['UltimoPref']);
      $comm=utf8_encode( $row['Comm']);
      $editor =utf8_encode( $row['editor']);

      $fonte =utf8_encode( $row['fonte']);  // deprecated
      $origem =utf8_encode( $row['origem']);

      $dato=utf8_encode( $row['RegDate']);  // just for internal checking
      

      if ($fonte=="")      {$fonte="N/A";}
      if ($dato=="")      {$dato="N/A";}
      if ($editor=="")      {$editor="N/A";}
      if ($comm=="")      {$comm="N/A";}
    
      printf ('         ['.pac($nome, 14).', ');
      printf (pac($descri, 40).', ');
      printf (pac($origem, 9).', ');
      printf (pac($UltimoPref, 11).', ');

      printf (pac($DataUltimaActual, 17).', ');
      printf (pac($DataUltimaActuaLocal, 21).', ');
      printf (pac($DataUltimaVerifica, 21));

      print ("]");  

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
 }

 echo "}";

}



mysqli_close($conn);

?>
