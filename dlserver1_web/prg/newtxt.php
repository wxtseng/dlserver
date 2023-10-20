<?php
$folder_path = '../python/model';  // 文件夹的路径
$latest_file = null;
$latest_file_time = 0;

foreach (glob($folder_path . '/*.txt') as $filename) {
    $file_time = filemtime($filename);

    if ($file_time > $latest_file_time) {
        $latest_file = basename($filename);
        $latest_file_time = $file_time;
    }
}

$response_data = ['latest_file' => $latest_file];

// 设置响应头以返回JSON数据
header('Content-Type: application/json');
echo json_encode($response_data);
?>
