<?php
header("Access-Control-Allow-Origin: *");
require 'vendor/autoload.php';
use Medoo\Medoo;
$database = new Medoo([	
	'type' => 'mysql',
	'host' => 'localhost',
	'database' => 'dlserver1',
	'username' => 'dlserver1',
	'password' => '2050014',
  'charset' => 'utf8'
]);
$today = date("YmdHis");
$savetime = date("Y-m-d H:i:s");
$uploaddir = "../backupimg/";
$files=$_POST["imgfn"];
$uploadfile = $uploaddir.basename($today.".png");
$msg=array();
if(move_uploaded_file($_FILES["imgfn"]["tmp_name"],$uploadfile )){
	$database->insert('photoinput1',[ //要新增的資料表名子
	'picname' => $today, //依欄位填入
	'picurl' => "./backupimg/$today.png" ,//依欄位填入
	'savetime' => $savetime,//依欄位填入
	]);
		$connection = ssh2_connect('120.114.140.5', 115);
		ssh2_auth_password($connection, 'dlserver1', '2050014');
		$stream1 = ssh2_exec($connection, "python3 /home/dlserver1/dlserver1_web/python/cutphoto.py /home/dlserver1/dlserver1_web/backupimg/$today.png");
		stream_set_blocking($stream1, true);
		$output1 = stream_get_contents($stream1);
		$stream2 = ssh2_exec($connection, "python3 /home/dlserver1/dlserver1_web/python/imgdata.py /home/dlserver1/dlserver1_web/python/compcut.png");
		stream_set_blocking($stream2, true);
		$output2 = stream_get_contents($stream2);
		ssh2_disconnect($connection);
		array_push($msg, true, "上傳成功");				
		echo json_encode($msg);
}
else {
	array_push($msg,false,"上傳失敗1");
  echo json_encode($msg);
}
?>