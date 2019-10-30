<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv=Content-Style-Type content=text/css>
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script type="text/javascript" src="http://code.highcharts.com/highcharts.js"></script>
<title>ハードオフ来店管理 - コンプリート率推移</title>
</head>

<body>
<div id="chart_monthly" style="width:900px; height:600px; display:table;margin: 0 auto;"></div>
<?php
    $db = new mysqli('localhost', 'iariro', '3ViewsOf4', 'iariro');
    if ($db->connect_error) {
        echo $db->connect_error;
        exit();
    } else {
        $db->set_charset("utf8");
    }

    $sql = "SELECT * FROM ho_store where visit_date is not null;";
	$dates = [];
    if ($result = $db->query($sql)) {
        while ($row = $result->fetch_assoc()) {
			$dates[] = strtotime($row['visit_date']);
		}
	}
    $result->close();
    $db->close();

	$monthlycount = array();
	$monthlycount2 = array();
	$nowyear = date('Y', time());
	$d2 = NULL;
	for($year = 2018; $year <= $nowyear+1; $year++) {
		for($month = 1; $month <= 12; $month++) {
			if ($year == $nowyear+1 && $month>1)
				break;
			$d = strtotime($year . '/' . $month . '/' . '1');
			$count = 0;
			$count2 = 0;
			foreach ($dates as $date) {
				if ($date < $d) {
					$count2++;
					if ($date >= $d2) {
						$count++;
					}
				}
			}
			if (!is_null($d2)) {
				$monthlycount[$d2] = $count;
				$monthlycount2[$d2] = $count2;
			}
			$d2 = $d;
		}
	}

	$bardata = '';
	$linedata = '';
	foreach ($monthlycount as $month => $count)
	{
		$bardata = $bardata . '[' . ($month * 1000) . ',' . $count . '],';
	}
	foreach ($monthlycount2 as $month => $count)
	{
		$linedata = $linedata . '[' . ($month * 1000) . ',' . $count . '],';
	}
?>
<script type="text/javascript">
function draw()
{
	new Highcharts.Chart(
	{
		chart: {renderTo: 'chart_monthly', zoomType:'xy', plotBackgroundColor: 'lightgray'},
		title: {text: '開拓店舗数・コンプリート率'},
		xAxis: {title: '月', type: 'datetime'},
		yAxis: [{title: {text:'店舗数'}},{title: {text:'コンプリート率'}, opposite: true}],
		series: [
			{name:'店舗数', type:'column', data:[ <?php echo $bardata; ?> ], yAxis: 0},
			{name:'コンプリート率', data:[ <?php echo $linedata; ?> ], yAxis: 1}
		]
	});
};
document.body.onload = draw();
</script>
</body>
</html>
