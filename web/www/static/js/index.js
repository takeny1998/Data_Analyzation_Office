$(document).ready(function() {

	var today = get_fmtted_date(new Date());
	
	new dateDropper({
		selector: '#date-picker',
		minDate: "2021-12-17",
		lang: 'ko',
		maxDate: today,
		expandedOnly: true,
		onChange: function (res) {
			selected_day = res.output.y + "-" + res.output.mm + "-" + res.output.dd;
			console.log(selected_day)
		}
	});

	selected_day = today;

	$('#date-picker').val(today);
	
	// navbar 색상 변경 스크립트
	$('.site-link').hover(
		// 마우스 올라왔을때
		function() {
			$('#navbar').css('background-color', 'white')
			// navbar 링크 색상 변경
			$('.site-link').children().css('color', 'black')
			// 로고 이미지 변경
			$('#site-logo').attr('src', '/static/images/logo-black.png')
		},
		// 마우스 떠났을때
		function() {
			$('#navbar').css('background-color', '')
			// navbar 링크 색상 변경
			$('.site-link').children().css('color', 'white')
			// 로고 이미지 변경
			$('#site-logo').attr('src', '/static/images/logo.png')
		}
	)
	
	// 카운트다운
	refresh_data();

	new Pageable("#wrap", {
		animation: 500,
		pip: true,
	});
})


function get_fmtted_date(dt) {
	return dt.getFullYear() + '-' + (dt.getMonth()+1).toString().padStart(2, '0') + '-'+ (dt.getDate()).toString().padStart(2, '0');
}


// chart
anychart.onDocumentReady(function() {
	var chart = anychart.tagCloud(data['C']);
	chart.angles([0]);
	chart.container("grid-wordcloud");
	// create and configure a color scale.
	var customColorScale = anychart.scales.linearColor();
	customColorScale.colors(["#00467F", "#A5CC82"]);

	// set the color scale as the color scale of the chart
	chart.colorScale(customColorScale);
	chart.background().fill("rgb(56, 56, 56)");
	chart.fontFamily('score-bold')
	// add and configure a color range
	chart.colorRange().enabled(true);
	chart.colorRange().length("90%");
	// chart.getCredits().setEnabled(false);
	chart.draw();
});