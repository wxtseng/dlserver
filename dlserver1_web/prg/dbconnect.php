<?php
header("Access-Control-Allow-Origin: *");
require './vendor/autoload.php';
use Medoo\Medoo;

//連線
$$database = new Medoo([	
	'type' => 'mysql',
	'host' => 'localhost',
	'database' => 'dlserver1',
	'username' => 'dlserver1',
	'password' => '2050014',
    'charset' => 'utf8'
]);

?>