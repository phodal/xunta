var signInCallback = function(result) {
  if (result['error']) {
    alert('An error happened:', result['error']);
  } else {
    $('#code').attr('value', result['code']);
    $('#at').attr('value', result['access_token']);
  }
};

var modalDialog = function(modalId, modalLinkName, submitHandler) {
  var $modal;

  $modal = $(modalId).modal({
    show: false
  });

  $modal.on('click', '.btn-primary', submitHandler || function(event) {
    event.preventDefault();
    $modal.find('form').submit();
  });

  if (modalLinkName) {
    $('a[name="' + modalLinkName + '"]').on('click', function(event) {
      event.preventDefault();
      $modal.modal('toggle');
    });
  }

  return $modal;
};

$(function() {
  var $validationModal;

  modalDialog('#username-modal', 'username');

  modalDialog('#ajax-login-modal', 'ajax-login', function(event) {
    var $backend, $accessToken, $accessTokenSecret, $fields, $result;
    event.preventDefault();

    $modal = $(this).closest('.modal');
    $form = $modal.find('form');
    $backend = $modal.find('[name="backend"]');
    $accessToken = $modal.find('[name="access_token"]');
    $accessTokenSecret = $modal.find('[name="access_token_secret"]');
    $result = $modal.find('.login-result');

    $.get('/ajax-auth/' + $backend.val() + '/', {
      access_token: $accessToken.val(),
      access_token_secret: $accessTokenSecret.val(),
    }, function(data, xhr, response) {
      $result.find('.user-id').html(data.id);
      $result.find('.user-username').html(data.username);
      $form.hide();
      $result.show();
      setTimeout(function() {
        window.location = '/';
      }, 10000);
    }, 'json')
  });

  $('.disconnect-form').on('click', 'a.btn', function(event) {
    event.preventDefault();
    $(event.target).closest('form').submit();
  });
});