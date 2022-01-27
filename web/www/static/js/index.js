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
	var data = [
		{
			"x": "IT",
			"value": 590000000,
			category: "Sino-Tibetan"
		},
		{
			"x": "Python",
			"value": 283000000,
			category: "Indo-European"
		},
		{
			"x": "소프트웨어",
			"value": 544000000,
			category: "Indo-European"
		},
		{
			"x": "JAVA",
			"value": 527000000,
			category: "Indo-European"
		},
		{
			"x": "C++",
			"value": 422000000,
			category: "Afro-Asiatic"
		},
		{
			"x": "HTML",
			"value": 620000000,
			category: "Afro-Asiatic"
		}
	];
	var chart = anychart.tagCloud(data);
	chart.angles([0]);
	chart.container("grid-wordcloud");
	// chart.getCredits().setEnabled(false);
	chart.draw();
});
