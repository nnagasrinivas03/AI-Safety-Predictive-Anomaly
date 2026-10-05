let socket;

let anomalyCount = 0;


/* -------------------------------
   GET HTML ELEMENTS
-------------------------------- */

const liveDot =
    document.getElementById(
        "liveDot"
    );

const liveText =
    document.getElementById(
        "liveText"
    );

const systemStatus =
    document.getElementById(
        "systemStatus"
    );

const anomalyScore =
    document.getElementById(
        "anomalyScore"
    );

const lastUpdate =
    document.getElementById(
        "lastUpdate"
    );

const airTemperature =
    document.getElementById(
        "airTemperature"
    );

const processTemperature =
    document.getElementById(
        "processTemperature"
    );

const rotationalSpeed =
    document.getElementById(
        "rotationalSpeed"
    );

const torque =
    document.getElementById(
        "torque"
    );

const toolWear =
    document.getElementById(
        "toolWear"
    );

const prediction =
    document.getElementById(
        "prediction"
    );

const alertBox =
    document.getElementById(
        "alertBox"
    );

const alertMessage =
    document.getElementById(
        "alertMessage"
    );


/* -------------------------------
   CHART
-------------------------------- */

const chartContext =
    document
        .getElementById(
            "sensorChart"
        )
        .getContext("2d");


const sensorChart =
    new Chart(
        chartContext,
        {

            type: "line",

            data: {

                labels: [],

                datasets: [

                    {
                        label:
                            "Air Temperature",

                        data: [],

                        borderWidth: 2,

                        tension: 0.3
                    },

                    {
                        label:
                            "Process Temperature",

                        data: [],

                        borderWidth: 2,

                        tension: 0.3
                    },

                    {
                        label:
                            "Torque",

                        data: [],

                        borderWidth: 2,

                        tension: 0.3
                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: false,

                scales: {

                    x: {

                        ticks: {

                            color:
                                "#8498b1"

                        }

                    },

                    y: {

                        ticks: {

                            color:
                                "#8498b1"

                        }

                    }

                },

                plugins: {

                    legend: {

                        labels: {

                            color: "white"

                        }

                    }

                }

            }

        }
    );


/* -------------------------------
   CONNECT WEBSOCKET
-------------------------------- */

function connectWebSocket() {

    const protocol =
        window.location.protocol === "https:"
            ? "wss:"
            : "ws:";


    socket =
        new WebSocket(
            `${protocol}//${window.location.host}/ws`
        );


    /* CONNECTED */

    socket.onopen = function () {

        liveDot.style.background =
            "#22c55e";

        liveText.innerText =
            "LIVE";

    };


    /* DATA RECEIVED */

    socket.onmessage =
        function(event) {

            const data =
                JSON.parse(
                    event.data
                );


            updateDashboard(
                data
            );

        };


    /* DISCONNECTED */

    socket.onclose =
        function() {

            liveDot.style.background =
                "#ef4444";

            liveText.innerText =
                "DISCONNECTED";


            setTimeout(
                connectWebSocket,
                2000
            );

        };


    /* ERROR */

    socket.onerror =
        function() {

            liveDot.style.background =
                "#ef4444";

            liveText.innerText =
                "CONNECTION ERROR";

        };

}


/* -------------------------------
   UPDATE DASHBOARD
-------------------------------- */

function updateDashboard(data) {


    airTemperature.innerText =
        data.air_temperature;


    processTemperature.innerText =
        data.process_temperature;


    rotationalSpeed.innerText =
        data.rotational_speed;


    torque.innerText =
        data.torque;


    toolWear.innerText =
        data.tool_wear;


    anomalyScore.innerText =
        data.anomaly_score;


    lastUpdate.innerText =
        data.timestamp;


    prediction.innerText =
        data.status;


    /* ---------------------------
       NORMAL
    ---------------------------- */

    if (
        data.status ===
        "NORMAL"
    ) {

        systemStatus.innerText =
            "✓ NORMAL";

        systemStatus.style.color =
            "#22c55e";

        prediction.style.color =
            "#22c55e";

        alertBox.className =
            "alert normal-alert";

        alertMessage.innerText =
            "Machine operating within normal conditions.";

    }


    /* ---------------------------
       ANOMALY
    ---------------------------- */

    else {

        anomalyCount++;

        systemStatus.innerText =
            "⚠ ANOMALY DETECTED";

        systemStatus.style.color =
            "#ef4444";

        prediction.style.color =
            "#ef4444";

        alertBox.className =
            "alert anomaly-alert";

        alertMessage.innerText =
            "AI detected an abnormal machine condition.";

    }


    /* ---------------------------
       UPDATE CHART
    ---------------------------- */

    sensorChart.data.labels.push(
        data.timestamp.split(" ")[1]
    );


    sensorChart.data.datasets[0]
        .data.push(
            data.air_temperature
        );


    sensorChart.data.datasets[1]
        .data.push(
            data.process_temperature
        );


    sensorChart.data.datasets[2]
        .data.push(
            data.torque
        );


    /* Keep last 30 readings */

    if (
        sensorChart.data.labels.length
        > 30
    ) {

        sensorChart.data.labels.shift();

        sensorChart.data.datasets
            .forEach(
                dataset =>
                    dataset.data.shift()
            );

    }


    sensorChart.update();

}


/* -------------------------------
   START
-------------------------------- */

connectWebSocket();