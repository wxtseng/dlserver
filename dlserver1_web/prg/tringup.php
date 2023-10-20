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
$folderPath = '../python/model';
$folderHandle = opendir($folderPath);
$latestTime = 0;
$latestFileName = "";

// 遍歷資料夾中的文件
while (false !== ($entry = readdir($folderHandle))) {
    $filePath = $folderPath . '/' . $entry;
    
    // 排除特殊檔案（目前目錄和上級目錄）
    if ($entry == "." || $entry == "..") {
        continue;
    }
    
    // 檢查檔案副檔名是否為 .txt
    if (pathinfo($filePath, PATHINFO_EXTENSION) == "txt") {
        // 获取文件的修改时间
        $fileTime = filemtime($filePath);
        
        // 比較修改時間，找到最新的文件
        if ($fileTime > $latestTime) {
            $latestTime = $fileTime;
            $latestFileName = $entry;
        }
    }
}

// 關閉資料夾
closedir($folderHandle);

// 打印最新 .txt 文件的檔名和修改時間
//echo "最新 .txt 文件: " . $latestFileName . "\n";
$newestFilePath = $folderPath . DIRECTORY_SEPARATOR . $latestFileName;
//echo "最新 2322文件: ".$newestFilePath."\n"; 
$fileopen = fopen($newestFilePath, "r");
$jsonData = fgets($fileopen);  // 讀取文件内容
fclose($fileopen);

$arr = json_decode($jsonData, true);  // 解碼 JSON 資料為關聯數組

if ($arr !== null) {  // 確保解碼成功
    for ($i = 0; $i < count($arr); $i++) {
    $modeltraining = $arr[$i]["modeltraining"];
    $epoch = $arr[$i]["epoch"];
    $model = $arr[$i]["model"];
    $time = $arr[$i]["time"];
    $duration = $arr[$i]["duration"];
    

    $imglocalArray = array();
        $entry = array(
            "modeltraining" => $modeltraining,
            "epoch" => $epoch,
            "model" => $model,
            "time" => $time,
            "duration" => $duration 
        );
    
        array_push($resultArray, $entry);
}
	 
	
    echo json_encode($resultArray); // 输出 JSON 資料到瀏覽器
} else {
    echo "JSON 失敗或數據為空。";
}
?>
 