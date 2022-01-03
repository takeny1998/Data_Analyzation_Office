$(document).ready(function() {

	var is_expanded = get_is_expanded();

	if(is_expanded == 'true') {
		expand()
	} else{
		fold()
	}
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
	
	$('#btn-expand').click(function() {
		
		set_is_expanded('false')
		expand();
	})
	// 카운트다운
	refresh_data();
})
