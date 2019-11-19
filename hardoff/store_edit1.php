<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<meta name="viewport" content="width=device-width">
<title>ハードオフ来店管理</title>
</head>
<body>
<form action='store_edit2.php' method='get'>
<?php
echo sprintf("<input type='hidden' name='store_id' value='%d'><br>", $_GET['store_id']);
echo sprintf("店舗名：<input type='text' name='name' value='%s'><br>", $_GET['name']);
echo sprintf("住所：<input type='text' name='address' value='%s' size='50'><br>", $_GET['address']);
echo sprintf("最寄り駅：<input type='text' name='near_station' value='%s'><br>", $_GET['near_station']);
echo sprintf("徒歩：<input type='text' name='minutes_from_near_station' value='%s'><br>", $_GET['minutes_from_near_station']);
echo sprintf("来店日：<input type='text' name='visit_date' value='%s'><br>", $_GET['visit_date']);
echo sprintf("ターゲット：<input type='checkbox' name='targeting' value='target' %s><br>", $_GET['targeting'] == 'target' ? 'checked=checked' : '');
?>
<input type='submit' value='確定'>
</form>
<form action='store_visit_today.php' method='get'>
<?php
echo sprintf("<input type='hidden' name='store_id' value='%d'><br>", $_GET['store_id']);
?>
<input type='submit' value='本日来店'>
</form>
</body>
</html>
