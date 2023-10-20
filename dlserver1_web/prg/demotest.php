<?php
header("Access-Control-Allow-Origin: *");
require 'vendor/autoload.php';
use Medoo\Medoo;

// set_time_limit(300);
$database = new Medoo([	
	'type' => 'mysql',
	'host' => 'localhost',
	'database' => 'dlserver1',
	'username' => 'dlserver1',
	'password' => '2050014',
    'charset' => 'utf8'
]);
$categoriesJSON = $_POST['categories'];
// 建立SSH连接
$connection = ssh2_connect('120.114.140.5', 115);
ssh2_auth_password($connection, 'dlserver1', '2050014');
$uptime = date("Y-m-d H:i:s");
if (isset($_FILES)) {
    // // 删除目录及其内容
    $strrm = ssh2_exec($connection,"rm -rf /home/dlserver1/dlserver1_web/all/");
    //////刪除目錄
    function rrmdir($dir) {
        if (is_dir($dir)) {
            $objects = scandir($dir);
            foreach ($objects as $object) {
                if ($object != "." && $object != "..") {
                    if (is_dir($dir . DIRECTORY_SEPARATOR . $object)) {
                        rrmdir($dir . DIRECTORY_SEPARATOR . $object);
                    } else {
                        unlink($dir . DIRECTORY_SEPARATOR . $object);
                    }
                }
            }
            rmdir($dir);
        }
    }
    $dir_to_delete1 = '../imagetrain/readypic/';
    rrmdir($dir_to_delete1);    
    //////////
    foreach ($_FILES as $categoryName => $fileData) {
        // 确定文件保存目录
        $uploadDirectory = '../imagetrain/readypic/' . $categoryName . '/';
        // 确保目标文件夹存在，如果不存在则创建它
        if (!file_exists($uploadDirectory)) {
            mkdir($uploadDirectory, 0775, true);
        }
        // 处理每个文件
        for ($i = 0; $i < count($fileData['name']); $i++) {
            $fileName = $fileData['name'][$i];
            $tmpFileName = $fileData['tmp_name'][$i];
            // 构建上传文件的完整路径
            $uploadPath = $uploadDirectory . $fileName;
            // 将文件从临时位置移动到目标位置
            if (move_uploaded_file($tmpFileName, $uploadPath)) {
                $database->insert('uploadclassimg',[ //要新增的資料表名子
                    'imgclass' => $categoriesJSON,
                    'uptime'   => $uptime
                     //依欄位填入
                ]);
                // 文件成功上传
                $stream1 = ssh2_exec($connection, "sh /home/dlserver1/dlserver1_web/prg/pythonbash.sh");
                //$stream2 = ssh2_exec($connection, "python3 /home/aireco/aireco_web/python/imgdata.py /home/aireco/aireco_web/python/comp.png");
                ssh2_disconnect($connection);
            }
        }
    }
}
    // 返回成功响应（可选）
    echo json_encode(['message' => 'success']);
// }

    
?>