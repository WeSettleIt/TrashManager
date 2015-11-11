(function ($) {
    $(function () {

        $('.button-collapse').sideNav();
        $('select').material_select();

        $('#list #customer-id').change(function () {
            this.form.submit();
        });

        toastr.options.closeButton = false;
        toastr.options.timeOut = 30000;
        toastr.options.extendedTimeOut = 600000;
        toastr.options.progressBar = true;
        toastr.options.positionClass = "toast-bottom-full-width";
    }); // end of document ready
})(jQuery); // end of jQuery name space