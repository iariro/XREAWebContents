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
    $db = new mysqli('localhost', 'iariro', 'abc123', 'iariro');
    if ($db->connect_error) {
        echo $db->connect_error;
        exit();
    } else {
        $db->set_charset("utf8");
    }

    echo "<table id='sorter' class='tablesorter'>";
    echo "<thead><tr><th>店舗名</th><th>住所</th><th>最寄り駅</th><th>徒歩</th><th>来店日</th><th>編集</th></tr></thead><tbody>";
    //SQL文でデータを取得
    $sql = "SELECT * FROM ho_store;";
    if ($result = $db->query($sql)) {
        //連想配列を取得
        while ($row = $result->fetch_assoc()) {
            if (strlen($row["visit_date"]) > 0)
				echo "<tr style='background-color:powderblue;'>";
			else
				echo "<tr>";
            echo "<td>" . $row["name"] . "</td>";
            echo "<td>" . $row["address"] . "</td>";
            echo "<td>" . $row["near_station"] . "</td>";
            echo "<td>" . $row["minutes_from_near_station"] . "</td>";
            echo "<td>" . $row["visit_date"] . "</td>";
            echo "<td>";
            echo "<form action='store_edit1.php' method='get'>";
            echo "<input type='hidden' name='store_id' value='" . $row["store_id"] . "'>";
            echo "<input type='hidden' name='name' value='" . $row["name"] . "'>";
            echo "<input type='hidden' name='address' value='" . $row["address"] . "'>";
            echo "<input type='hidden' name='near_station' value='" . $row["near_station"] . "'>";
            echo "<input type='hidden' name='minutes_from_near_station' value='" . $row["minutes_from_near_station"] . "'>";
            echo "<input type='hidden' name='visit_date' value='" . $row["visit_date"] . "'>";
            echo "<input type='submit' value='編集'></form></td>";
            echo "</tr>";
        }
        //結果を閉じる
        $result->close();
    }
    echo "</tbody></table>";
 
    //データベース切断
    $db->close();
?>
</div>
</div>
</div>
</body>
</html>
