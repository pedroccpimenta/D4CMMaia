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
{ $nome=null;
}

if(isset($_GET['formato'])){
    $formato = utf8_encode($_GET['formato']);
}
else
{ $formato="JSON";
}


//$sql="select * from fonte where nome='".$nome."'";
    // echo $sql;
//$result= mysqli_query($conn,$sql);
//    echo "Resul".$result.FLINHA;
//  echo $result;

//flush();

//if (mysqli_num_rows($result) > 0 and $nome!=false) {

if (5==5)
{
// echo "TEMOS VALOR";
  $sql="select * from datalakesize where discousado is null order by id desc limit 600;";  
  $resultp2= mysqli_query($conn,$sql);
  $st1="[";
  $sp1="[";
  $sp2="[";
  $sp3="[";
  $sp4="[";
  $sp5="[";
  $sp6="[";
  $nsd=mysqli_num_rows($resultp2);
  $si=0;
  while($row = mysqli_fetch_assoc($resultp2)) 
  {   $st1=$st1.'"'.$row["data"].'"';
      $sp1=$sp1.$row["puser"];
      $sp2=$sp2.$row["pnice"];
      $sp3=$sp3.$row["psystem"];
      $sp4=$sp4.$row["piowait"];
      $sp5=$sp5.$row["pidle"];
      $sp6=$sp6.$row["psteal"];
      $si++;
      if ($si<$nsd)
      {  $st1=$st1.", "; 
         $sp1=$sp1.", ";
         $sp2=$sp2.", ";
         $sp3=$sp3.", ";
         $sp4=$sp4.", ";
         $sp5=$sp5.", ";
         $sp6=$sp6.", ";
      }
  }   
  $st1=$st1."]"; 
  $sp1=$sp1."]"; 
  $sp2=$sp2."]"; 
  $sp3=$sp3."]"; 
  $sp4=$sp4."]"; 
  $sp5=$sp5."]"; 
  $sp6=$sp6."]"; 
 
 
  //$sql="select ano, ".$nome." from baze21RA order by ano";  
  $sql="select data, datafile, discousado from datalakesize where discousado is not null order by id desc limit 120;";  
  
  $result2= mysqli_query($conn,$sql);
  $s1="[";
  $s2="[";
  $s3="[";
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
  {   $s1=$s1.'"'.$row["data"].'"';
      $s2=$s2.'"'.$row["datafile"].'"';
      $s3=$s3.$row["discousado"];
      $si++;
      if ($si<$nsd)
      {  $s1=$s1.", "; 
         $s2=$s2.", ";
         $s3=$s3.", ";
      }
  }   
  $s1=$s1."]"; 
  $s2=$s2."]"; 
  $s3=$s3."]"; 

    echo '{"s1":'.$s1.",".PHP_EOL;
    echo ' "s2":'.$s2.",".PHP_EOL;
    echo ' "s3":'.$s3.",".PHP_EOL;

    echo ' "st1":'.$st1.",".PHP_EOL;
    echo ' "sp1":'.$sp1.",".PHP_EOL;
    echo ' "sp2":'.$sp2.",".PHP_EOL;
    echo ' "sp3":'.$sp3.",".PHP_EOL;
    echo ' "sp4":'.$sp4.",".PHP_EOL;
    echo ' "sp5":'.$sp5.",".PHP_EOL;
    echo ' "sp6":'.$sp6.PHP_EOL;


}

if (9==5)
{

$row = mysqli_fetch_assoc($result);
    $nome=utf8_encode($row['nome']);
      $desc=utf8_encode( $row['descri']);
      $comm=utf8_encode( $row['comm']);
      $dato=utf8_encode( $row['RegDate']);
      $editor =utf8_encode( $row['editor']);
      $fonte =utf8_encode( $row['fonte']);


echo '    "metadata":{'.PHP_EOL;
echo '          "nome":"'.$nome.'", '.PHP_EOL;      
echo '          "descrição":"'.$desc.'", '.PHP_EOL;     
echo '          "editor":"'.$editor.'", '.PHP_EOL;      
echo '          "fonte":"'.$fonte.'", '.PHP_EOL;      
echo '          "comentário":"'.$comm.'" '.PHP_EOL;     
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
      $comm=utf8_encode( $row['comm']);
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

    //    printf(PHP_EOL.".".$desc.".".PHP_EOL);

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
