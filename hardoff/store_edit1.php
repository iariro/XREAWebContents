<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<title>ハードオフ来店管理</title>
</head>
<body>
<form action='store_edit2.php' method='get'>
<?php
echo "<input type='hidden' name='store_id' value='" . $_GET['store_id'] . "'><br>";
echo "店舗名：<input type='text' name='name' value='" . $_GET['name'] . "'><br>";
echo "住所：<input type='text' name='address' value='" . $_GET['address'] . "' size='50'><br>";
echo "最寄り駅：<input type='text' name='near_station' value='" . $_GET['near_station'] . "'><br>";
echo "徒歩：<input type='text' name='minutes_from_near_station' value='" . $_GET['minutes_from_near_station'] . "'><br>";
echo "来店日：<input type='text' name='visit_date' value='" . $_GET['visit_date'] . "'><br>";
?>
<input type='submit' value='確定'>
</form>
</body>
</html>
