<?php
header("Access-Control-Allow-Origin: *");
require './vendor/autoload.php';
use Medoo\Medoo;

$database = new Medoo([	
	'type' => 'mysql',
	'host' => 'localhost',
	'database' => 'dlserver1',
	'username' => 'dlserver1',
	'password' => '2050014',
    'charset' => 'utf8'
]);

$data=$database->query("SELECT * FROM `photoinput1` ORDER BY `id` desc")->fetchAll();
//$data = $database ->select("gewawa_orderlist","*",["login" => $login]);
//echo $database->last(); //顯示最後一個sql指令
echo json_encode($data);
?>
 