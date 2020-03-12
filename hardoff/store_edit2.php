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
	if (strlen($_GET['near_station']) > 0 && strlen($_GET['minutes_from_near_station']) > 0)
	{
		$values[] = sprintf("near_station='%s'",  $_GET['near_station']);
		$values[] = sprintf("minutes_from_near_station=%d", $_GET['minutes_from_near_station']);
	}

	if (strlen($_GET['visit_date']) > 0)
	{
		$values[] = sprintf("visit_date='%s'", $_GET['visit_date']);
	}
	else
	{
		$values[] = "visit_date=null";
	}

	if (strlen($_GET['address']) > 0)
	{
		$values[] = sprintf("address='%s'", $_GET['address']);
	}
	else
	{
		$values[] = "visit_date=null";
	}

	if (strlen($_GET['targeting']) > 0)
	{
		$values[] = "targeting='target'";
	}
	else
	{
		$values[] = "targeting=null";
	}
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
