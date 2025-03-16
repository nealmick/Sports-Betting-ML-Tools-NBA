let currentLine = 0;
let modelNumber = document.getElementById("model-slot").value;
let isModalOpen = true;
function retrainLogs(modelNumber) {
    let url = `/predict/retrain-logs/${modelNumber}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                let modalContent = document.querySelector("#retrainModal .modal-body");
                modalContent.innerHTML = 'Model slot has no history... Click Train Model.';
                throw new Error('No Logs Found..');
            }
            return response.json();
        })
        .then(data => {
            let modalContent = document.querySelector("#retrainModal .modal-body");
            modalContent.innerHTML = '';

            if (data.lines && data.lines.length > 0) {
                data.lines.forEach((entry, index) => {
                    let logLine = document.createElement("p");
                    logLine.classList.add("log-entry", entry.type);

                    let formattedDate = timeSince(new Date(entry.date_posted));
                    let text = `${entry.type.charAt(0).toUpperCase() + entry.type.slice(1)} Model: ${formattedDate} `;
                    if (entry.type === 'retrain') {
                        text += `Game: ${entry.game} `;
                        logLine.onclick = () => window.location.href = `/predict/edit/${entry.game}`;
                    }

                    logLine.textContent = text;
                    modalContent.appendChild(logLine);

                    if (index < data.lines.length - 1) {
                        let separator = document.createElement("hr");
                        modalContent.appendChild(separator);
                    }
                });
            } else {
                let noDataMsg = document.createElement("p");
                noDataMsg.textContent = 'No retrain logs found for model.';
                modalContent.appendChild(noDataMsg);
            }

            $('#retrainModal').modal('show');
        })
        .catch(error => {
            console.error('Error fetching all model logs:', error);
            let modalContent = document.querySelector("#retrainModal .modal-body");
            modalContent.innerHTML = '';

            let errorMsg = document.createElement("p");
            errorMsg.textContent = 'Error fetching logs: '
            modalContent.appendChild(errorMsg);
            let errorMsgTxt = document.createElement("p");
            errorMsgTxt.textContent = error.message;
            modalContent.appendChild(errorMsgTxt);
        });
}

function timeSince(date) {
    const now = new Date();
    const secondsPast = (now.getTime() - date.getTime()) / 1000;

    if (secondsPast < 60) {
        return `${parseInt(secondsPast)} seconds ago`;
    }
    if (secondsPast < 3600) {
        return `${parseInt(secondsPast / 60)} minutes ago`;
    }
    if (secondsPast <= 86400) {
        return `${parseInt(secondsPast / 3600)} hours ago`;
    }
    if (secondsPast <= 2592000) {
        return `${parseInt(secondsPast / 86400)} days ago`;
    }
    if (secondsPast <= 31536000) {
        return `${parseInt(secondsPast / 2592000)} months ago`;
    }
    return `${parseInt(secondsPast / 31536000)} years ago`;
}

function viewOldLogs(modelNumber) {
    let url = `/predict/all-model-logs/${modelNumber}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('No Logs Found.  Make sure you have a custom model trained.  The default model does not display logs.');
            }
            return response.json();
        })
        .then(data => {
            let modalContent = document.querySelector("#oldLogsModal .modal-body");
            modalContent.innerHTML = '';

            if (data.lines && data.lines.length > 0) {
                data.lines.forEach(line => {
                    let logLine = document.createElement("p");
                    logLine.textContent = line;
                    modalContent.appendChild(logLine);
                });
            } else {
                let noDataMsg = document.createElement("p");
                noDataMsg.textContent = 'No logs found for this model.';
                modalContent.appendChild(noDataMsg);
            }

            $('#oldLogsModal').modal('show');
        })
        .catch(error => {
            console.error('Error fetching all model logs:', error);
            let modalContent = document.querySelector("#oldLogsModal .modal-body");
            modalContent.innerHTML = '';

            let errorMsg = document.createElement("p");
            errorMsg.textContent = 'Error fetching logs: '
            modalContent.appendChild(errorMsg);
            let errorMsgTxt = document.createElement("p");
            errorMsgTxt.textContent = error.message;
            modalContent.appendChild(errorMsgTxt);
        });
}

function fetchModelLogs() {
    if (!isModalOpen) {
        return;
    }

    let url = `/predict/model-logs/${modelNumber}/${currentLine}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.line) {
                let modalContent = document.querySelector("#trainModal .modal-body");
                let newLine = document.createElement("p");
                newLine.textContent = data.line;
                modalContent.appendChild(newLine);
                modalContent.scrollTop = modalContent.scrollHeight;

                currentLine++;
            }

            setTimeout(fetchModelLogs, 25);
        })
        .catch(error => console.error('Error fetching model logs:', error));
}

$(document).ready(function() {
    $('#trainModal').on('shown.bs.modal', function() {
        currentLine = 0;
        isModalOpen = true;
        modelNumber = document.getElementById("model-slot").value;
        fetchModelLogs();
    });

    $('#trainModal').on('hidden.bs.modal', function() {
        isModalOpen = false;
    });

    $('#oldLogsModal').on('shown.bs.modal', function() {
        modelNumber = document.getElementById("model-slot").value;
        viewOldLogs(modelNumber);
    });
    $('#retrainModal').on('shown.bs.modal', function() {
        modelNumber = document.getElementById("model-slot").value;
        retrainLogs(modelNumber);
    });
});

document.getElementById("players").addEventListener("input", () => {
    document.getElementById("players-display").innerHTML = document.getElementById("players").value;
});

document.getElementById("epochs-input").addEventListener("input", () => {
    document.getElementById("epochs-display").innerHTML = document.getElementById("epochs-input").value;
});

document.getElementById("batch-size").addEventListener("input", () => {
    document.getElementById("batch-display").innerHTML = document.getElementById("batch-size").value;
});
document.getElementById("layer1-count").addEventListener("input", () => {
    document.getElementById("1count-display").innerHTML = document.getElementById("layer1-count").value;
});
document.getElementById("layer2-count").addEventListener("input", () => {
    document.getElementById("2count-display").innerHTML = document.getElementById("layer2-count").value;
});
document.getElementById("model-slot").addEventListener("input", () => {
    model = document.getElementById("model-slot").value
    window.location.href = TRAIN_BASE_URL + 'train/' + model
});

function makeDataset(){
    seasons = document.getElementById("seasons-input").value
    numgames = document.getElementById("testGame-input").value
    window.location.href = MAKE_DATASET_URL + '/' + seasons + '/' + numgames
}

function trainModel(){
    epochs = document.getElementById("epochs-input").value
    batchSize = document.getElementById("batch-size").value
    layer1Count = document.getElementById("layer1-count").value
    layer1Activation = document.getElementById("layer1-activation").value
    layer2Count = document.getElementById("layer2-count").value
    layer2Activation = document.getElementById("layer2-activation").value
    es = document.getElementById("es").checked
    rmw = document.getElementById("rmw").checked
    kr = document.getElementById("kr").checked

    streaks = document.getElementById("streaks").checked
    wl = document.getElementById("wl").checked
    gp = document.getElementById("gp").checked
    ps = document.getElementById("ps").checked

    optimizer = document.getElementById("optimizer").value
    optimizers = ['adam','adamax','RMSprop','adagrad','nadam','SGD']
    activations = ['relu','LeakyReLU','swish','elu','gelu','selu']
    document.getElementById("loading-div").style.opacity = 1

    model = document.getElementById("model-slot").value
    players = document.getElementById("players").value

    ast = document.getElementById("ast").checked
    blk = document.getElementById("blk").checked
    reb = document.getElementById("reb").checked
    fg3 = document.getElementById("fg3").checked
    fg = document.getElementById("fg").checked
    ft = document.getElementById("ft").checked
    pf = document.getElementById("pf").checked
    pts = document.getElementById("pts").checked
    stl = document.getElementById("stl").checked
    turnover = document.getElementById("turnover").checked

    console.log(optimizers[optimizer])

    window.location.href = TRAIN_BASE_URL + 'trainmodel/' + model + '/' + epochs + '/' + batchSize + '/' + layer1Count + '/' + activations[layer1Activation] + '/' + layer2Count + '/' + activations[layer2Activation] + '/' + optimizers[optimizer] + '/' + es + '/' + rmw + '/' + kr + '/' + streaks + '/' + wl + '/' + gp + '/' + ps + '/' + players +
    '/' + ast + '/' + blk + '/' + reb + '/' + fg3 + '/' + fg + '/' + ft + '/' + pf + '/' + pts + '/' + stl + '/' + turnover + '/' + 'false'
}

function updateURL() {
    let modelNumber = document.getElementById("model-slot").value;
    let newURL = '/predict/train/' + modelNumber;

    window.history.pushState({}, '', window.location.origin + newURL);
}

updateURL();
