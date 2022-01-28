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
			god = console.log(data)
			show_graph(data)
		},
		error: function(request, status, error){
			alert('ajax 통신 실패')
			alert(error);
		}
	})
}


function show_graph(data) {
	// word_cloud
	var word_cloud = anychart.tagCloud(data);
	word_cloud.angles([0]);
	word_cloud.container("grid-wordcloud");

	// create and configure a color scale.
	var customColorScale = anychart.scales.linearColor();
	word_cloud.hover({
		fill: '#ffffff'
	});

	customColorScale.colors(["#7c7c7c", "#FFFFFF"]);
	word_cloud.selected({
		fill: '#ffffff',
		fontWeight: 'bold'
	});
	
	// set the color scale as the color scale of the chart
	word_cloud.colorScale(customColorScale);
	word_cloud.background().fill("rgb(56, 56, 56)");
	word_cloud.fontFamily('score-bold');
	
	// add and configure a color range
	word_cloud.colorRange().enabled(true);
	word_cloud.colorRange().length("90%");
	word_cloud.draw();


	var anychart_bar = anychart.bar();
	var bar_graph = anychart_bar.bar(data.slice(0, 10));
	bar_graph.container("grid-bar");
}
