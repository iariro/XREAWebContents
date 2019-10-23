<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<title>PHP & MySQL Test</title>
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
 
    echo "<table border>";
    //SQL文でデータを取得
    $sql = "SELECT * FROM wp_posts where post_status='publish' and id not in (1,2);";
    if ($result = $db->query($sql)) {
        //連想配列を取得
        while ($row = $result->fetch_assoc()) {
            echo "<tr><td>" . $row["post_date"] . "</td><td>" . $row["post_title"] . "</td><td>" . $row["post_content"] . "</td></tr>";
        }
        //結果を閉じる
        $result->close();
    }
    echo "</table>";
 
    //データベース切断
    $db->close();
?>
</body>
</html>
