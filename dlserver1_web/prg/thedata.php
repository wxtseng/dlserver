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
$resultArray = array();
//$files=$_POST["json"];
$file = fopen("../python/output.txt", "r");
$jsonData = fgets($file);  // 读取文件内容
fclose($file);

$arr = json_decode($jsonData, true);  // 解码 JSON 数据为关联数组

if ($arr !== null) {  // 确保解码成功
    for ($i = 0; $i < count($arr); $i++) {
    $rank = $arr[$i]["rank"];
    $itype = $arr[$i]["itype"];
    $Similarity = $arr[$i]["Similarity"];
    $itypedata = $database->query("SELECT `imglocal` FROM `compare` WHERE `oimgtype` = '$itype' ")->fetchAll();
    
    $imglocal = "";
    if (!empty($itypedata)) {
        $imglocal = $itypedata[0]['imglocal'];
    }
    $imglocalArray = array();
	if (!empty($imglocal)) {
		$imglocalArray = $imglocal;
	}
    // 检查 itypedata 是否为空，如果不为空，才将其添加到 resultArray 中
        $entry = array(
            "rank" => $rank,
            "itype" => $itype,
            "Similarity" => $Similarity,
            "itypedata" => $imglocalArray // 构建 itypedata 数组
        );
    
        array_push($resultArray, $entry);
    // 在这里可以使用 $itype 和 $Similarity 进行操作
    //echo "类型: $itype, 相似度: $Similarity<br>";
}
	 
	
    echo json_encode($resultArray); // 输出 JSON 数据到浏览器
} else {
    echo "JSON 解码失败或数据为空。";
}
?>
 