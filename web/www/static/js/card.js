$(document).ready(function() {
    $('.topic-card').on('click', function() {
        $(this).addClass('fold')
        fold_card()
    })
})

function fold_card() {
    $('.topic-cards').animate({
        height: '75px',
        width: '750px',
        marginTop: '10px',
        marginBottom: '60px'
    });
    


    $('.card-body').animate({
        top: '60%'
    })

    $('.card-body').children('hr').animate({
        opacity: '0'
    })
    $('.card-overlay').animate({
        opacity: '0.6'
    })

    $('.site-text').animate({
        fontSize: '0px'
    })

    $('.headline').animate({
        fontSize: '0px'
    })

    $('.card-title').animate({
        fontSize: '18px'
    })

    $('#gap-expand').animate({
        height: '10vh'
    })

    $('#expand-body').css('flex', '1')
}

