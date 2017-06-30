!(function(window, $) {
    "use strict";
    var orderObject,
        apiRoot = '/en/api/v1',
        createAccEndpoint =  '/en/accounts/authenticate/',
        menuEndpoint = apiRoot + '/menu',
        breadcrumbsEndpoint = apiRoot + '/breadcrumbs',
        validatePhoneEndpoint = '/en/accounts/verify_user/';


    function lockoutResponse (data) {
        toastr.error(window.getLockOutText(data));
    }

    function failureResponse (data, defaultMsg) {
        var _defaultMsg = gettext(defaultMsg),
            message = data.responseJSON.message || _defaultMsg;
        toastr.error(message);

    }

    function canProceedtoRegister(objectName) {
        var payMeth = $('#payment_method_id').val(),
            userAcc = $('#user_address_id').val(),
            userAccId = $('#new_user_account').val();
        if (!((objectName == 'menu2' || objectName == 'btn-register') &&
            payMeth === '' &&
            userAcc === '' &&
            userAccId === '')) {
            return true;
        }
        return false;
    }

    function seemlessRegistration (payload) {
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: createAccEndpoint,
            data: payload,
            statusCode: {
                200: function (data) {
                    if ($('#login-form').is(':visible')) {
                        $('.login-otp').removeClass('hidden');
                        $('.resend-otp').removeClass('hidden');
                        $('#submit').addClass('hidden');
                        $('#submit').addClass('disabled');
                        $('#id_password').val('');
                        $('#id_password').attr(
                            'placeholder', gettext('SMS Token'));
                        $('#id_password').attr(
                            'type', 'text');
                        $('label[for="id_password"]').text(
                            gettext('One Time Password')
                        );
                        $('.send-otp').addClass('hidden');
                        $('#id_username').attr('readonly', true);
                    } else {
                        $('.register .step2').removeClass('hidden');
                        $('.verify-acc').removeClass('hidden');
                        $('.create-acc').addClass('hidden');
                        $('.create-acc.resend').removeClass('hidden');
                    }
                },
                400: function (data) {
                    return failureResponse(
                        data,
                        gettext('Invalid phone number')
                    );
                },
                503: function (data) {
                    return failureResponse(
                        data,
                        gettext('Service provider error')
                    );
                },
                403: lockoutResponse,
                428: function (data) {
                    return failureResponse(
                        data,
                        gettext('Invalid phone number')
                    );
                }
            }
        });
    }

    function verifyAccount (payload) {
        if ($('#login-form').is(':visible')) {
            $('.login-otp').addClass('disabled');
        }
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: validatePhoneEndpoint,
            data: payload,
            statusCode: {
                201: function(data) {
                    if ($('#login-form').is(':visible')) {
                        window.location.href = '/';
                    } else {
                        orderObject = require('./orders.js');
                        orderObject.reloadRoleRelatedElements(menuEndpoint, breadcrumbsEndpoint);
                        orderObject.changeState(null, 'next');
                    }
                },
                400: function (data) {
                    if ($('#login-form').is(':visible')) {
                        $('.login-otp').removeClass('disabled');
                    }
                    failureResponse(
                        data,
                        'Incorrect code'
                    );
                },
                410: function (data) {
                    if ($('#login-form').is(':visible')) {
                        $('.login-otp').removeClass('disabled');
                    }
                    return failureResponse(
                        data,
                        'Your token has expired, please request a new token'
                    );
                },
                403: lockoutResponse
            }
        });

    }

    module.exports = {
        canProceedtoRegister: canProceedtoRegister,
        seemlessRegistration: seemlessRegistration,
        verifyAccount: verifyAccount,
    };
}(window, window.jQuery)); //jshint ignore:line