$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const commentID = button.data('source') // Extract info from data-* attributes
        const park = button.data('park') // Extract info from data-* attributes
        const rating = button.data('rating')
        const comments = button.data('comments')

        const modal = $(this)
        if (commentID === 'New Comments') {
            modal.find('.modal-title').text(commentID)
            $('#task-form-display').removeAttr('commentID')
        } else {
            modal.find('.modal-title').text('Edit Task ' + commentID)
            $('#task-form-display').attr('commentID', commentID)
        }

        if (park) {
            modal.find('.form-control1').val(park);
        } else {
            modal.find('.form-control1').val('');
        }
        if (rating) {
            modal.find('.form-control2').val(rating);
        } else {
            modal.find('.form-control2').val('');
        }
        if (comments) {
            modal.find('.form-control3').val(comments);
        } else {
            modal.find('.form-control3').val('');
        }
    })


    $('#submit-task').click(function () {
        const cID = $('#task-form-display').attr('commentID');
        // console.log($('#task-modal').find('.form-control1').val())
        // console.log($('#task-modal').find('.form-control2').val())
        // console.log($('#task-modal').find('.form-control3').val())
        $.ajax({
            type: 'POST',
            url: cID ? '/edit/'+cID : '/insert',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                 'park_name':$('#task-modal').find('.form-control1').val(),
                'rating': $('#task-modal').find('.form-control2').val(),
                'comments': $('#task-modal').find('.form-control3').val(),
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.state').click(function () {
        const state = $(this)
        const tID = state.data('source')

        $.ajax({
            type: 'POST',
            url: '/edit/' + tID,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'park_name':$('#task-modal').find('.form-control1').val(),
                'rating': $('#task-modal').find('.form-control2').val(),
                'comments': $('#task-modal').find('.form-control3').val(),
            }),
            success: function (res) {
                console.log(res)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

});