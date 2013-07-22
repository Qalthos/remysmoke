$(function() {
    $('input#nosmoke').click(function() {
        $('input#justification').prop('disabled', $(this).checked);
    });
});
