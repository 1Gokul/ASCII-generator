
$(document).ready(function () {

    var conversionType;
    var errors;
    window.convert_image = function (imglink) { };
    window.send_file_to_upload = function (imgData) { };
    window.display_converted_image = function (imglink) { };
    window.display_converted_text = function (imglink) { };

    $(document).on('click', '#submitbutton', function () {

        conversionType = $("#type").val();
        // Get the file from the form
        var $file = $("#inputform-file").prop('files')[0];

        if ($file) {

            var fileType = $file["type"];

            // If the file's type is not supported
            var validImageTypes = ["image/gif", "image/jpeg", "image/png"];
            if ($.inArray(fileType, validImageTypes) < 0) {
                send_error("Select a <b>valid</b> image file.");
            }

            // Else if file is larger than 20MB(Imgur's upload size limit)
            else if ($file.size > parseInt(maxFileSize) * 1024 * 1024) {
                send_error("The file was bigger than the 20MB limit! Select a smaller one.");
                return false;
            }
            // Else if the file is good to go
            else {
                if ($('#error').length) {
                    send_error("Nice!");
                }

                // Disable the submit button to prevent repeated submissions.
                $(this).css('background', '#d44444');
                $(this).val('Uploading...')
                    .attr('disabled', 'disabled');


                console.log("uploading submitted file...");
                send_file_to_upload($file, "convert_image");
            }


        }
        // If no file was selected at all
        else {
            send_error("Select a file first, goofball.");
        }
    });

    function get_status(taskID, funcToCall) {
        $.ajax({
            method: 'GET',
            url: `tasks/${taskID}`
        })
            .done((response) => {
                const taskStatus = response.data.taskStatus;

                if (taskStatus === 'failed') {
                    console.log(response);
                    return false;
                }
                else if (taskStatus == 'finished') {
                    // Parse the returned JSON and return the link to the image.
                    console.log(response);

                    window[funcToCall](response.data.taskResult.result, response.data.taskResult.errors);
                    return false;
                }

                // If the task hasn't been finished, try again in 1 second.
                setTimeout(function () {
                    get_status(response.data.taskID, funcToCall);
                }, 1000);
            })
            .fail((error) => {
                console.log(error);
            });
    }

    // Send an Ajax POST request to Imgur's API to upload a file.
    function upload_to_imgur(fileToUpload) {

        // The image's data
        var formData = new FormData();
        formData.append('image', fileToUpload);

        // Taken from: https://apidocs.imgur.com/#c85c9dfc-7487-4de2-9ecd-66f727cf3139
        var settings = {
            "url": "https://api.imgur.com/3/image",
            "method": "POST",
            "timeout": 0,
            "headers": {
                "Authorization": "Client-ID "
            },
            "processData": false,
            "mimeType": "multipart/form-data",
            "contentType": false,
            "data": formData
        };

        // Upload the file to Imgur.
        var parsedResponse;

        $.ajax(settings).done(function (response) {

            // Parse the returned JSON and return the link to the image.
            parsedResponse = $.parseJSON(response);

            return parsedResponse.data.link;
        });
    }

    window.convert_image = function (submittedImageData) {
        $('#submitbutton').css('background', '#d9bf00');
        $('#submitbutton').val('Converting...');

        var imglink = submittedImageData.mainResult;

        // Data to be passed to the convert_image() function in the server.
        var formData = new FormData();
        formData.append('imglink', imglink);
        formData.append('type', $("#type").val());
        formData.append('mode', $("#mode").val());
        formData.append('num_cols', $("#num_cols").val());
        formData.append('scale', $("#scale").val());
        formData.append('bg', $("#bg").val());

        $.ajax({
            "type": 'POST',
            "url": Flask.url_for('convert_file'),
            "data": formData,
            "processData": false,
            "contentType": false
        })
            .done((response) => {


                /* Once the image conversion has started, call get_status while passing in the function to display the result.*/
                if (conversionType == 'img') {

                    get_status(response.data.taskID, "display_converted_image");
                }
                else if (conversionType == 'txt') {
                    get_status(response.data.taskID, "display_converted_text");
                }
            })
            .fail((error) => {
                console.log("Error during file convert: " + error);
            });

    }


    function send_error(error) {
        $("#error").remove();
        $("<div id=" + "error" + " class=" + "error" + ">" + error + "</p>").insertAfter("#subtitle");
    }

    window.send_file_to_upload = function ($file, funcToCallOnceCompleted) {
        // Would be accessed as a form in the API
        var formData = new FormData();
        formData.append('file', $file);

        // Ajax POST request to upload_file() in the API
        $.ajax({
            type: 'POST',
            url: Flask.url_for('upload_file'),
            data: formData,
            cache: false,
            processData: false,
            contentType: false
        })
            // If done, get the status of the background job that was started for this file's upload.
            .done((response) => {
                get_status(response.data.taskID, funcToCallOnceCompleted);
            })

            .fail((error) => {
                console.log("Error during file upload: " + error);
            });
    }

    window.display_converted_image = function (conversionResult, errors) {
        before_displaying_result();
        var html = "";
        html += '<p class="result-title"">Your converted image</p>';
        html += '<div class="column left"><img src=' + conversionResult.mainResult + '></div>';
        if (errors != "none") {
            html += '<div class="column right"><div class="error" style="padding:15px;"><p style="color: white;">Errors faced while processing:</p>' + errors + '</div></div>';
        }
        html += '<div class="column right"><a class="downloadlink" href=' + conversionResult.dl + '>Download image</a></div>';

        $('#result-box').html(html);



    }

    window.display_converted_text = function (conversionResult, errors) {
        before_displaying_result();

        var html = "";
        html += '<p class="result-title">Your converted text</p>';
        html += '<div class="column left"><pre><div class="data" style="font-size: 1;">' + conversionResult.mainResult + '/div></pre></div>';
        if (errors != "none") {
            html += '<div class="column right"><div class="error" style="padding:15px;"><p style="color: white;">Errors faced while processing:</p>' + errors + '</div></div>';
        }
        html += '<div class="column right"><div class="downloadlink"><a href=' + conversionResult.dl + '>Download .txt file</a></div></div>';
        html += '<div class="column right"><div class="downloadlink"><a href=' + conversionResult.raw + '>View raw text</a></div></div>';

        $('#result-box').html(html);
    }

});

function before_displaying_result() {
    $('#result-box').css('min-height', 500);
    $(document.body).animate({
        scrollTop: document.body.scrollHeight
    }, 500);
    $('#submitbutton').css('background', '#02d16d');
    $('#submitbutton').val('Scroll down! :D');
}
