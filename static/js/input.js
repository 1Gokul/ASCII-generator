
$(document).ready(function () {

    console.log("(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧");
    console.log("Hello there... I see you like to check the console!");
    console.log("Not much here though... except C̶͓̥̆́ͮU̔R̵̙̟ͥ́̄̾̀S̿È͇̻̹̬͑ͦ͗͒̕D̛̦ͬ̀ ͕̉ͧT̢̜̹͕͉̓̅E̸̥̓̋̒҉̑X͖̼̘̙ͨ͝T͇͖̂̚S̟̪̱ͯ͑ͩ̍̕҉̞  normal task logs!");
    console.log("┬┴┬┴┤ ͜ʖ ͡°) ├┬┴┬┴");


    var conversionType;
    var errors;
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
                // send_file_to_upload($file, "convert_image");

                upload_image($file);
            }


        }
        // If no file was selected at all
        else {
            send_error("Select a file first, goofball.");
        }
    });




    function send_error(error) {
        $("#error").remove();
        $("<div id=" + "error" + " class=" + "error" + ">" + error + "</p>").insertAfter("#subtitle");
    }


    display_converted_image = function (conversionResult, errors) {
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

    display_converted_text = function (conversionResult, errors) {
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

    function before_displaying_result() {
        window.scrollTo(0, $(".result-title").offset().top);
        $('#submitbutton').css('background', '#02d16d');
        $('#submitbutton').val('All done! :D');
    }


    function upload_image(file) {

        // Send an Ajax POST request to Imgur's API to upload a file.

        // The image's data
        var formData = new FormData();
        formData.append('image', file);

        // Taken from: https://apidocs.imgur.com/#c85c9dfc-7487-4de2-9ecd-66f727cf3139
        var settings = {
            "url": "https://api.imgur.com/3/image",
            "method": "POST",
            "timeout": 0,
            "headers": {
                "Authorization": "Client-ID " + apiKey
            },
            "processData": false,
            "mimeType": "multipart/form-data",
            "contentType": false,
            "data": formData
        };

        $.ajax(settings).done(function (response) {

            // Parse the returned JSON and return the link to the image.
            let parsedResponse = $.parseJSON(response);

            // Data to be passed to the convert_image() function in the API.
            var formData = new FormData();
            formData.append('imglink', parsedResponse.data.link);
            formData.append('type', $("#type").val());
            formData.append('mode', $("#mode").val());
            formData.append('num_cols', $("#num_cols").val());
            formData.append('scale', $("#scale").val());
            formData.append('bg', $("#bg").val());

            $('#submitbutton').css('background', '#d9bf00');
            $('#submitbutton').val('Converting...');

            console.log("upload complete.. now converting the file...")

            $.ajax({
                "type": 'POST',
                "url": Flask.url_for('convert_file'),
                "data": formData,
                "processData": false,
                "contentType": false
            })
                .done((response) => {

                    console.log("conversion completed successfully!");

                    /* Once the image conversion has started, call get_status while passing in the function to display the result.*/
                    if (conversionType == 'img') {

                        display_converted_image(response.result, response.errors);
                    }
                    else if (conversionType == 'txt') {
                        display_converted_text(response.result, response.errors);
                    }
                })
                .fail((error) => {
                    console.log("Error during file convert: " + error);
                });
        });




    }


});


