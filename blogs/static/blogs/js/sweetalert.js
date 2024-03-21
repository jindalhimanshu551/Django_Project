// Force reloading page when using browser back button
(function () {
  window.onpageshow = function(event) {
      if (event.persisted) {
          window.location.reload();
      }
  };
})();

function sweetAlertBlogDelete(id){
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire({
          title: "Deleted!",
          text: "Your blog has been deleted.",
          icon: "success"
          }).then(() => {
            window.location.href = "/blogs/delete_blog/" + id + "/";
          });
        }
      });
}

function sweetAlertCommentDelete(id){
    Swal.fire({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire({
          title: "Deleted!",
          text: "Your comment has been deleted.",
          icon: "success"
          }).then(() => {
            window.location.href = "/blogs/delete_comment/" + id + "/";
          });
        }
      });
}

function submitForm(id){
  var form = $("#myForm"+id)
  $.ajax({
    type: form.attr('method'),
    url: form.attr('action'),
    data: form.serialize(),
    success: function (data) {
      Swal.fire({
        title: "Success",
        text: data,
        icon: "success"
      });
    },
    error: function(data) {
      Swal.fire({
        title: "Success",
        text: data,
        icon: "success"
      });
    }
  });
}