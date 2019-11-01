<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script type="text/javascript" src="http://code.highcharts.com/highcharts.js"></script>
<title>ハードオフ来店管理</title>
</head>
<body>
<div id="chart_area" style="width:900px; height:600px;"></div>
<?php
    //データベースに接続
    $db = new mysqli('localhost', 'iariro', 'abc123', 'iariro');
    if ($db->connect_error) {
        echo $db->connect_error;
        exit();
    } else {
        $db->set_charset("utf8");
    }

	$prefectures = '';
	$visited = '';
	$unvisited = '';
    $sql = "SELECT SUBSTRING(address,1, CASE WHEN locate('県',address)<>0 THEN locate('県',address) WHEN locate('府',address)<>0 THEN locate('府',address) WHEN locate('都',address)<>0 THEN locate('都',address) END) as prefecture, count(visit_date), count(*) FROM iariro.ho_store group by prefecture;";
    if ($result = $db->query($sql)) {
        while ($row = $result->fetch_assoc()) {
			if (strlen($prefectures) > 0)
			{
				$prefectures = $prefectures . ',';
			}
			$prefectures = $prefectures . "'" . $row["prefecture"] . "'";

			if (strlen($visited) > 0)
			{
				$visited = $visited . ',';
			}
			$visited = $visited . $row["count(visit_date)"];

			if (strlen($unvisited) > 0)
			{
				$unvisited = $unvisited . ',';
			}
			$unvisited = $unvisited . ($row["count(*)"] - $row["count(visit_date)"]);
        }
        $result->close();
	}
    $db->close();
?>
<script type="text/javascript">
function draw()
{
	new Highcharts.Chart(
	{
		chart: {renderTo: 'chart_area', type: 'column', zoomType:'xy', plotBackgroundColor: 'lightgray'},
		plotOptions: {column: {stacking: 'normal'}},
		title: {text: '都道府県別開拓店舗数'},
		xAxis: {title: '都道府県', categories: [ <?php echo $prefectures; ?> ]},
		yAxis: {title: {text:'店舗数'}},
		series: [
			{name:'来店済み', data:[ <?php echo $visited; ?> ], index:1},
			{name:'未来店', data:[ <?php echo $unvisited; ?> ], index:0}
		]
	});
};
document.body.onload = draw();
</script>
</body>
</html>
