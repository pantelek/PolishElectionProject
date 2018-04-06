google.charts.load('current', {'packages':['geochart']});

function drawRegionsMap() {

    var data = google.visualization.arrayToDataTable([
          ['voivodeship'],
          ['MAZOWIECKIE'],
          ['WARMIŃSKO-MAZURSKIE'],
          ['PODLASKIE'],
          ['KUJAWSKO-POMORSKIE'],
          ['ZACHODNIOPOMORSKIE'],
          ['MAŁOPOLSKIE'],
          ['WIELKOPOLSKIE'],
          ['OPOLSKIE'],
          ['POMORSKIE'],
          ['LUBELSKIE'],
          ['PODLASKIE'],
          ['ŁÓDZKIE'],
          ['DOLNOŚLĄSKIE'],
          ['LUBUSKIE'],
          ['PODKARPACKIE'],
          ['ŚLĄSKIE'],
          ['ŚWIĘTOKRZYSKIE']
        ]);

    var options = {
            region: 'PL',
            resolution: 'provinces',
            width: '90%'
        };

    var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));

    function myClickHandler(){
        var selection = chart.getSelection();
        var address = ''
        for (var i = 0; i < selection.length; i++) {
            var item = selection[i];
            if (item.row != null) {
                address = 'voivodeship/' + data.getValue(item.row, 0) + '.html'; }

        }
        window.location.href = address;
    }

google.visualization.events.addListener(chart, 'select', myClickHandler);
    chart.draw(data, options);

}

window.onload = function(){
    drawRegionsMap();
};
