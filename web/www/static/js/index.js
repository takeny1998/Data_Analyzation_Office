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

	
    $('.topic-card').on('click', function() {
        $('.topic-card').addClass('topic-fold')
        $(this).addClass('topic-selected')

        fold_card()
		get_crawling_data()
    })
	
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

function get_crawling_data() {
	$.ajax({
		type: 'POST',
		url: url_get_data,
		data: JSON.stringify({
		'date':'2022-01-28',
		'type':'C'
	}),
		dataType : 'JSON',
		contentType: "application/json",
		success: function(data){

			show_tagcloud(data.tag)
			show_barchart(data.bar)
		},
		error: function(request, status, error){
			alert('ajax 통신 실패')
			alert(error);
		}
	})
}


function show_tagcloud(data) {
	// chart
	var chart = anychart.tagCloud(data);
	chart.angles([0]);
	chart.container("grid-wordcloud");

	// create and configure a color scale.
	var customColorScale = anychart.scales.linearColor();
	chart.hover({
		fill: '#ffffff'
	});

	customColorScale.colors(["#7c7c7c", "#FFFFFF"]);
	chart.selected({
		fill: '#ffffff',
		fontWeight: 'bold'
	});
	
	// set the color scale as the color scale of the chart
	chart.colorScale(customColorScale);
	chart.background().fill("rgb(56, 56, 56)");
	chart.fontFamily('score-bold');
	
	// add and configure a color range
	chart.colorRange().enabled(true);
	chart.colorRange().length("90%");
	chart.draw();

}

function show_barchart(data) {
	var chart = anychart.bar();
	var series = chart.bar(data);

	chart.container("grid-bar");
	chart.background().fill("rgb(56, 56, 56)");

	series.normal().fill("#d4d4d4");
	series.normal().stroke(null);

	series.labels().fontFamily("score");
	series.labels().fontColor("#d4d4d4");
	series.labels(true);
	

	chart.title('상위 15개 검색단어');
	chart.title().fontFamily('score-bold');
	chart.title().fontColor('#d4d4d4');
	chart.title().fontSize(18);

	chart.xAxis().labels().fontFamily('score');
	chart.xAxis().labels().fontColor('#d4d4d4');

	chart.yAxis().labels().fontFamily('score');
	chart.yAxis().labels().fontColor('#d4d4d4');
	chart.draw();
}
