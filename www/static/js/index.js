$(document).ready(function() {

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

	var today = get_fmtted_date(new Date());
	
	new dateDropper({
		selector: '#date-picker',
		minDate: "2021-12-17",
		lang: 'ko',
		maxDate: today,
		expandedOnly: true
	});

	new Pageable("#wrap", {
		animation: 500
	});
})


function get_fmtted_date(dt) {
	return dt.getFullYear() + '/' + (dt.getMonth()+1) + '/'+ dt.getDate();
}
