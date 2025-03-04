export default `
<div class="modal" id="myModal">
    <div class="modal-dialog modal-fullscreen">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">{{ title }}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body" id="modalBodyDiv" style="padding-bottom: 0rem">
                <div class="text-center mb-3"></div>
                <div id="consoleDiv">
                    <pre style="margin-bottom: 0rem" id="console">
                        <div class="d-flex justify-content-center" id="loadPreviousDiv">
                            <button class="btn btn-success" id="loadPreviousButton" style="display: none;" @click="loadPrevious">Load Previous</button>
                        </div>
                    </pre>
                </div>
            </div>
            <div class="modal-footer">
                <div class="container">
                    <div class="row">
                        <div class="col-sm">
                            <span>&nbsp</span>
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" role="switch" id="darkModeToggle" v-model="darkMode">
                                <label class="form-check-label" for="darkModeToggle">Dark Mode</label>
                            </div>
                        </div>
                        <div class="col-sm d-md-flex justify-content-md-end">
                            <button class="btn btn-warning" id="downloadButton" :disabled="!isDownloadEnabled" @click="downloadResult">Download Result</button>
                            &nbsp;
                            <button class="btn btn-secondary" id="clearButton" @click="clearLog">Clear Log</button>
                            &nbsp;
                            <button class="btn btn-primary" id="saveButton" @click="saveLog">Save Execution Log</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

`;