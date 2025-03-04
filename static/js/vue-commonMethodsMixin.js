// Common methods mixin: loadPrevious, clearLog, saveLog, downloadResult
var commonLogMethodsMixin = {
    methods: {
        loadPrevious() {
            if (window.removedData && window.removedData.length > 0) {
                let previousData = window.removedData.pop();
                let newDiv = $("<code>");
                newDiv.text(previousData + "\n");
                newDiv.insertBefore($("#console code:first"));
                newDiv.addClass("shellsession");

                if (this.darkMode) {
                    hljs.highlightElement(newDiv[0]);
                }

                if (window.removedData.length === 0) {
                    $("#loadPreviousButton").hide();
                }
            }
        },
        clearLog() {
            $("#console").children().not("#loadPreviousDiv").remove();
            window.removedData = [];
        },
        saveLog() {
            let removedLogContent = window.removedData.join('\n') + '\n';
            let codeElement = document.getElementById('console');
            let codeElementCopy = codeElement.cloneNode(true);
            let divToRemove = codeElementCopy.querySelector("#loadPreviousDiv");
            if (divToRemove) {
                codeElementCopy.removeChild(divToRemove);
            }
            let innerText = (removedLogContent + codeElementCopy.innerText)
                .replaceAll("                ", "")
                .replace("                    [", "[")
                .replaceAll("<", "&lt;")
                .replaceAll(">", "&gt;");
            let downloadLink = document.createElement('a');
            downloadLink.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(innerText);
            downloadLink.download = 'log.txt';
            downloadLink.style.display = 'none';
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        },
        downloadResult() {
            let roomName = sessionStorage.getItem('roomName');
            window.open(HOST_URL + 'download/' + roomName, '_blank');
        }
    }
};
