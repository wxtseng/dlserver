<?php    
header("Access-Control-Allow-Origin: *");
header('Access-Control-Allow-Methods: POST,GET,OPTIONS');
header('Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept');

$fname=$_REQUEST['fname'];
$fname=$_POST['bdata'];


if ( $_FILES['bdata']['error']>0 ) {
    echo 'Error: ' . $_FILES['bdata']['error'] . '<br>';
}
else {

move_uploaded_file($_FILES['bdata']['tmp_name'], './backupimg/' .$fname . '.png');

//var_dump($output);
//var_dump($value);
var_dump($cmd);
exit;


}

?>