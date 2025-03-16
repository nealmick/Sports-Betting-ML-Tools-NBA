// === Welcome popup ===
document.addEventListener("DOMContentLoaded", function() {
    if (!localStorage.getItem('welcomeShownArb')) {
        // document.getElementById("welcomePopup").style.display = "flex";
        // document.getElementById("mainContent").classList.add("blur");
    }

    document.getElementById("closePopup").addEventListener("click", function() {
    });
});

function welcome(){
    document.getElementById("welcomePopup").style.display = "none";
    localStorage.setItem('welcomeShownArb', 'true');
}

// === Region selection storage ===
document.addEventListener('DOMContentLoaded', function () {
    const regionSelect = document.getElementById('region');
    const storedRegion = localStorage.getItem('selectedRegion');
    if (storedRegion) {
        regionSelect.value = storedRegion;
    }
    regionSelect.addEventListener('change', function () {
        localStorage.setItem('selectedRegion', this.value);
    });
});

// === Refresh button with region ===
document.addEventListener('DOMContentLoaded', function () {
    const refreshButton = document.getElementById('refreshButton');
    const regionSelect = document.getElementById('region');
    const spinner = document.getElementById('spinner');

    refreshButton.addEventListener('click', function (event) {
        event.preventDefault();
        const selectedRegion = regionSelect.value;
        const baseUrl = ARB_ACTIVE ? '/predict/arb/refresh/' : '/autoshop/';
        const newUrl = ARB_ACTIVE ? baseUrl + selectedRegion : baseUrl;
        spinner.style.display = 'flex';
        window.location.href = newUrl;
    });
});

// === Bookmaker list display by region ===
document.addEventListener('DOMContentLoaded', function() {
    const regionSelect = document.getElementById('region');

    function displayCorrectBookmakers(region) {
        const bookmakerLists = document.querySelectorAll('.bookmakers-list');
        bookmakerLists.forEach(list => list.classList.add('d-none'));
        const activeList = document.getElementById(region + '-books');
        if (activeList) {
            activeList.classList.remove('d-none');
        }
    }

    const storedRegion = localStorage.getItem('selectedRegion') || 'us';
    regionSelect.value = storedRegion;
    displayCorrectBookmakers(storedRegion);

    regionSelect.addEventListener('change', function() {
        localStorage.setItem('selectedRegion', this.value);
        displayCorrectBookmakers(this.value);
    });
});

// === Chart.js bookies bar chart ===
(function() {
    const labels = ['USA', 'EU', 'UK', 'AU'];
    const chartData = {
        labels: labels,
        datasets: [
            {
                label: 'Bookies',
                data: [15, 18, 18, 11],
                backgroundColor: 'rgba(252, 134, 30, 0.5)',
                borderColor: "#fc861e",
                borderWidth: 2,
                borderRadius: Number.MAX_VALUE,
                borderSkipped: false,
                barPercentage: 0.5,
                categoryPercentage: 0.5,
            }
        ]
    };

    const config = {
        type: 'bar',
        data: chartData,
        options: {
            indexAxis: 'x',
            scales: {
                y: {
                    beginAtZero: true,
                }
            },
            plugins: {
                legend: {
                    display: false,
                }
            }
        },
    };

    var myChart = new Chart(document.getElementById('myChart'), config);
})();

// === Arbitrage calculator ===
function calculateArbitrage() {
    let wager1Amount = parseFloat(document.getElementById('wager1Amount').value) || 0;
    let odds1 = parseFloat(document.getElementById('wager1Odds').value);
    let odds2 = parseFloat(document.getElementById('wager2Odds').value);

    const decimalOdds1 = odds1 > 0 ? odds1 / 100 + 1 : -100 / odds1 + 1;
    const decimalOdds2 = odds2 > 0 ? odds2 / 100 + 1 : -100 / odds2 + 1;

    let wager2Amount = (wager1Amount * decimalOdds1) / decimalOdds2;

    if (wager1Amount < 0 || wager2Amount < 0) {
        alert("Wager amounts cannot be negative.");
        return;
    }

    let totalWager = wager1Amount + wager2Amount;
    let payout = wager1Amount * decimalOdds1;
    let profit = payout - totalWager;

    document.getElementById('wager2Amount').textContent = '$' + wager2Amount.toFixed(2);
    document.getElementById('totalWager').textContent = '$' + totalWager.toFixed(2);
    document.getElementById('profit').textContent = '$' + profit.toFixed(2);
    document.getElementById('percentReturn').textContent = ((profit / totalWager) * 100).toFixed(2) + '%';
}

// === Bookmaker filtering ===
var usBooks = (function() {
    var el = document.getElementById('arb-books-us');
    return el ? JSON.parse(el.textContent) : [];
})();
var auBooks = (function() {
    var el = document.getElementById('arb-books-au');
    return el ? JSON.parse(el.textContent) : [];
})();
var euBooks = (function() {
    var el = document.getElementById('arb-books-eu');
    return el ? JSON.parse(el.textContent) : [];
})();
var ukBooks = (function() {
    var el = document.getElementById('arb-books-uk');
    return el ? JSON.parse(el.textContent) : [];
})();

function normalizeBookmakerName(name) {
    var selectedRegion = document.getElementById('region').value;
    if (name === 'Unibet' && selectedRegion === 'us') {
        name = 'unibet_us';
    }
    if (name === 'LowVig.ag') {
        name = 'lowvig';
    }
    return name.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
}

function filterArbitrage() {
    var uncheckedBookmakers = new Set();
    var selectedRegion = document.getElementById('region').value;
    document.querySelectorAll('#' + selectedRegion + '-books input[name="bookmakers"]:not(:checked)').forEach(function(checkbox) {
        uncheckedBookmakers.add(normalizeBookmakerName(checkbox.value));
    });

    document.querySelectorAll('.col-lg-4').forEach(function(colDiv) {
        var cardBookmakers = Array.from(colDiv.querySelectorAll('.line-book')).map(element => normalizeBookmakerName(element.textContent.trim()));
        var isHidden = cardBookmakers.some(bookmaker => uncheckedBookmakers.has(bookmaker));
        colDiv.style.display = isHidden ? 'none' : '';
    });
}

function saveFilters() {
    var selectedRegion = document.getElementById('region').value;
    var selectedBookmakers = {};
    selectedBookmakers[selectedRegion] = [];

    var regionBookmakers = [];
    if (selectedRegion === 'au') {
        regionBookmakers = auBooks;
    } else if (selectedRegion === 'eu') {
        regionBookmakers = euBooks;
    } else if (selectedRegion === 'uk') {
        regionBookmakers = ukBooks;
    } else if (selectedRegion === 'us') {
        regionBookmakers = usBooks;
    }
    regionBookmakers.forEach(bookmaker => {
        var checkboxId = 'bookmaker-' + selectedRegion + '-' + bookmaker;
        var checkbox = document.getElementById(checkboxId);
        if (checkbox && checkbox.checked) {
            selectedBookmakers[selectedRegion].push(bookmaker);
        }
    });

    localStorage.setItem('selectedBookmakers', JSON.stringify(selectedBookmakers));
    filterArbitrage();
}

document.addEventListener('DOMContentLoaded', function() {
    var selectedRegion = document.getElementById('region').value;
    var savedBookmakers = JSON.parse(localStorage.getItem('selectedBookmakers')) || {};
    var checkboxes = document.querySelectorAll('#' + selectedRegion + '-books input[name="bookmakers"]');
    if (savedBookmakers[selectedRegion]) {
        checkboxes.forEach(function(checkbox) {
            checkbox.checked = savedBookmakers[selectedRegion].includes(checkbox.value);
        });
    } else {
        checkboxes.forEach(function(checkbox) {
            checkbox.checked = true;
        });
    }
    filterArbitrage();
});

document.querySelectorAll('input[name="bookmakers"]').forEach(function(checkbox) {
    checkbox.addEventListener('change', saveFilters);
});

// === Latest odds tracking ===
var latestOddsMap = {};

function initializeLatestOdds(counter, odds1, odds2) {
    latestOddsMap[counter] = {
        odds1: odds1,
        odds2: odds2
    };
}

// Initialize from injected data
if (window.ARB_OPPORTUNITIES_DATA) {
    window.ARB_OPPORTUNITIES_DATA.forEach(function(opp) {
        initializeLatestOdds(opp.counter, opp.odds1, opp.odds2);
    });
}

// === Chart rendering for arbitrage history ===
function fetchAndRenderChart(eventId, sportKey, modalCounter) {
    if (!ARB_ACTIVE) {
        if (modalCounter >= 0) {
            window.location.href = '/autoshop/';
        }
    } else {
        fetch('/predict/history-arb/?event_id=' + eventId + '&sport_key=' + sportKey)
            .then(function(response) { return response.json(); })
            .then(function(data) {
                renderChart(data, modalCounter);
            })
            .catch(function(error) { console.error('Error:', error); });
    }
}

function renderChart(chartData, modalCounter) {
    chartData.labels.reverse();
    chartData.datasets.forEach(function(dataset) {
        dataset.data.reverse();
    });

    var ctx = document.getElementById('chartCanvas' + modalCounter).getContext('2d');
    var hideXAxisLabels = window.innerWidth < 750;

    new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            elements: {
                line: {
                    tension: 0.4
                }
            },
            scales: {
                x: {
                    display: !hideXAxisLabels
                }
            },
            plugins: {}
        }
    });
}

function refreshOdds(eventId, bookmakers, counter) {
    fetch('/predict/update-arb/?event_id=' + eventId + '&bookmakers[]=' + bookmakers.join('&bookmakers[]='))
    .then(function(response) { return response.json(); })
    .then(function(data) {
        var updatedOdds = data[eventId];
        if (updatedOdds && updatedOdds.odds) {
            var newOdds1, newOdds2;
            var index = 1;
            for (const [bookmakerKey, markets] of Object.entries(updatedOdds.odds)) {
                var h2hMarket = markets.find(function(market) { return market.key === 'h2h'; });
                if (h2hMarket) {
                    h2hMarket.outcomes.forEach(function(outcome) {
                        if (index === 1) {
                            newOdds1 = outcome.price;
                        } else if (index === 2) {
                            newOdds2 = outcome.price;
                        }
                        if (index === 1) {
                            latestOddsMap[counter].odds1 = outcome.price;
                        } else if (index === 2) {
                            latestOddsMap[counter].odds2 = outcome.price;
                        }
                        var oddsElementId = 'odds-display-' + counter + '-' + index;
                        console.log(oddsElementId)
                        var oddsElement = document.getElementById(oddsElementId);
                        if (oddsElement) {
                            oddsElement.innerHTML = 'Updated Odds: ' + outcome.price;
                        }
                        index++;
                    });
                }
            }
            if (newOdds1 !== undefined && newOdds2 !== undefined) {
                updateBankroll(counter, newOdds1, newOdds2);
            }
        }
    })
    .catch(function(error) { console.error('Error:', error); });
}

function updateBankroll(counter, odds1, odds2) {
    var slider = document.getElementById('bankroll-input' + counter);
    var bankrollDisplay = document.getElementById('bankroll-display' + counter);
    var otherSplitDisplay = document.getElementById('other-split' + counter);
    var newProfitOutcome1Display = document.getElementById('newProfitOutcome1' + counter);
    var newProfitOutcome2Display = document.getElementById('newProfitOutcome2' + counter);

    var totalBankroll = 100;
    var bankrollPercentage = parseFloat(slider.value);
    var otherSplitPercentage = 100 - bankrollPercentage;

    bankrollDisplay.innerHTML = 'Bankroll: ' + bankrollPercentage.toFixed(1) + '%';
    otherSplitDisplay.innerHTML = 'Bankroll: ' + otherSplitPercentage.toFixed(1) + '%';

    var stake1 = totalBankroll * (bankrollPercentage / 100);
    var stake2 = totalBankroll - stake1;

    var profitIfOutcome1 = (stake1 * odds1) - totalBankroll;
    var profitIfOutcome2 = (stake2 * odds2) - totalBankroll;

    newProfitOutcome1Display.innerHTML = 'Profit: ' + profitIfOutcome1.toFixed(2) + '%';
    newProfitOutcome2Display.innerHTML = 'Profit: ' + profitIfOutcome2.toFixed(2) + '%';
}

// === Team name shortening ===
document.addEventListener('DOMContentLoaded', function(event) {
    const teamElements = document.querySelectorAll('.team-name');
    teamElements.forEach(function(element) {
        let fullTeamName = element.textContent || element.innerText;
        let teamNameParts = fullTeamName.trim().split(' ');
        let lastWord = teamNameParts[teamNameParts.length - 1];
        let shortenedWord = lastWord.substring(0, 8);
        element.textContent = shortenedWord;
    });
});

// === API key from localStorage ===
document.addEventListener('DOMContentLoaded', function() {
    var apiKey = localStorage.getItem('apiKey');
    if (apiKey) {
        var msgInput = document.getElementById('message-input');
        if (msgInput) {
            msgInput.value = apiKey;
        }
    }
});
