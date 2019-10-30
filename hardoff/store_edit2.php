<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<title>ハードオフ来店管理</title>
</head>
<body>
<?php
    //データベースに接続
    $db = new mysqli('localhost', 'iariro', '3ViewsOf4', 'iariro');
    if ($db->connect_error) {
        echo $db->connect_error;
        exit();
    } else {
        $db->set_charset("utf8");
    }

	$sql = "";
	if (strlen($_GET['near_station']) > 0 && strlen($_GET['minutes_from_near_station']) > 0)
	{
		$sql = $sql . "near_station='" .  $_GET['near_station'] . "', minutes_from_near_station=" . $_GET['minutes_from_near_station'];
	}
	if (strlen($_GET['visit_date']) > 0)
	{
		if (strlen($sql) > 0)
		{
			$sql = $sql . ",";
		}
		$sql = $sql . "visit_date='" . $_GET['visit_date'] . "'";
	}
	$sql = "update ho_store set " . $sql . " where store_id=" .  $_GET['store_id'] . ";";
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
