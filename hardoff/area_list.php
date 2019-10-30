<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<meta http-equiv=Content-Style-Type content=text/css>
<title>ハードオフ来店管理</title>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js"></script>
<script src="jquery/jquery.tablesorter.min.js"></script>
<script>
$(function() { $('#sorter').tablesorter({sortInitialOrder:"desc",headers:{5:{sorter:false}}}); });
</script>
<link rel="stylesheet" type="text/css" href="jquery/style.css">
<link rel="stylesheet" type="text/css" href="hatena.css">
</head>
<body>
<div class=hatena-body>
<div class=main>
<div class=day>
<?php
 
    //データベースに接続
    $db = new mysqli('localhost', 'iariro', '3ViewsOf4', 'iariro');
    if ($db->connect_error) {
        echo $db->connect_error;
        exit();
    } else {
        $db->set_charset("utf8");
    }

    $sql = "SELECT SUBSTRING(address,1, CASE WHEN locate('県',address)<>0 THEN locate('県',address) WHEN locate('府',address)<>0 THEN locate('府',address) WHEN locate('都',address)<>0 THEN locate('都',address) END) as prefecture, count(visit_date), count(*) FROM iariro.ho_store group by prefecture;";
    echo "<table>";
    echo "<tr><th>都道府県</th><th>来店数</th><th>全店舗数</th><th>コンプリート率</th></tr>";
    if ($result = $db->query($sql)) {
        while ($row = $result->fetch_assoc()) {
            echo "<tr>";
            echo "<td>" . $row["prefecture"] . "</td>";
            echo "<td align='right'>" . $row["count(visit_date)"] . "</td>";
            echo "<td align='right'>" . $row["count(*)"] . "</td>";
            echo "<td align='right'>" . floor($row["count(visit_date)"] * 100 / $row["count(*)"]) . "%</td>";
            echo "</tr>";
        }
        //結果を閉じる
        $result->close();
	}
    echo "</table>";
 
    //データベース切断
    $db->close();
?>
</div>
</div>
</div>
</body>
</html>
