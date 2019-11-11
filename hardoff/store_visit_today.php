<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<meta name="viewport" content="width=device-width">
<title>ハードオフ来店管理</title>
</head>
<body>
<?php
    //データベースに接続
    $db = new mysqli('localhost', 'iariro', 'abc123', 'iariro');
    if ($db->connect_error) {
        echo $db->connect_error;
        exit();
    } else {
        $db->set_charset("utf8");
    }

	$values = [];
	$values[] = sprintf("visit_date='%s'", date('Y/m/d', time()));

	$sql = sprintf("update ho_store set %s where store_id=%d;",  join(',', $values),  $_GET['store_id']);
    if ($result = $db->query($sql)) {
        //結果を閉じる
		echo '更新しました';
        $result->close();
    }
	else
	{
		echo $sql . 'に失敗しました';
	}

    //データベース切断
    $db->close();

?>
</form>
</body>
</html>
