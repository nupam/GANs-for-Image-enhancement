var el = x => document.getElementById(x);

function showPicker(inputId) { el('file-input').click(); }

function showPicked(input) {
    el('upload-label').innerHTML = input.files[0].name;
    var reader = new FileReader();
    reader.onload = function (e) {
        el('image-picked').src = e.target.result;
        el('image-picked').className = '';
        //el('image-picked').height = '720';
    }
    reader.readAsDataURL(input.files[0]);
}


function analyze() {
    var uploadFiles = el('file-input').files;
    if (uploadFiles.length != 1) alert('Please select 1 file to analyze!');

    el('analyze-button').innerHTML = 'Analyzing...';
    var xhr = new XMLHttpRequest();
    var loc = window.location
    xhr.open('POST', `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`, true);
    xhr.onerror = function() {alert (xhr.responseText);}
    xhr.onload = function(e) {
        if (this.readyState === 4) {
            var response = JSON.parse(e.target.responseText);
            el('result-label').innerHTML = `Result = ${response['result']}`;
            var xhr2 = new XMLHttpRequest();
            var fname = response['result'];
            console.log(fname)
            xhr2.onreadystatechange = function() {
            if (xhr2.readyState==4 && xhr2.status==200) {
                var blob = new Blob([xhr2.response], {
                    type: xhr2.getResponseHeader("Content-Type")
                });
                var imgUrl = window.URL.createObjectURL(blob);
                document.getElementById("analysed_img").src = imgUrl;
              }
            }
          xhr2.responseType = "arraybuffer";
          xhr2.open("GET",'/images/enhanced/' + fname ,true);
          xhr2.send();
        
        }
        el('analyze-button').innerHTML = 'Analyze';
    }

    var fileData = new FormData();
    fileData.append('file', uploadFiles[0]);
    xhr.send(fileData);
}





