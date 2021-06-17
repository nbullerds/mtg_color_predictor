var tableData = data;

//Update table on site with currently filtered table data
function updateTable(data) {
    console.log("I'm running!");
    console.log(data);
    var tbody = d3.select("tbody");
    tbody.html("");
    data.forEach(ufoSighting => {
        //Create a row for each instance of data in data.js
        var row = tbody.append("tr");

        //For each data element appened table data to the current table row
        Object.entries(ufoSighting).forEach(([key, value]) => {
            var cell = row.append("td");
            cell.text(value);
        });
    });
}

//Updates datalists for search suggestions from possible data values
function updateDatalists(data) {
    
    //update for cities
    var cities = d3.map(data, function(d){
        return(d.city)
    }).keys()
    var citylist = d3.select("#citylist");
    cities.forEach(d => {
        var option = citylist.append("option").text(d);
    })

    //update for state
    var states = d3.map(data, function(d){
        return(d.state)
    }).keys()
    var statelist = d3.select("#statelist");
    states.forEach(d => {
        var option = statelist.append("option").text(d);
    })

    //update for country
    var countries = d3.map(data, function(d){
        return(d.country)
    }).keys()
    var countrylist = d3.select("#countrylist");
    countries.forEach(d => {
        var option = countrylist.append("option").text(d);
    })

    //update for shape
    var shapes = d3.map(data, function(d){
        return(d.shape)
    }).keys()
    var shapelist = d3.select("#shapelist");
    shapes.forEach(d => {
        var option = shapelist.append("option").text(d);
    })
}

function filterSightings() {
    
    var filteredData;

    // Prevent the page from refreshing
    d3.event.preventDefault();

    // Select the date input element and get the raw HTML node
    var inputElement = d3.select("#datetime");
    var dateValue = inputElement.property("value");
    // Filter the table based on date.  Else statement solves all null values being input
    if (dateValue != ""){
        filteredData = tableData.filter(tableData => tableData.datetime === dateValue);
    } else {
        filteredData = tableData;
    }

    // Select the city input element and get the raw HTML node
    inputElement = d3.select("#city");
    var cityValue = inputElement.property("value");
    // Filter the table based on city
    if (cityValue != ""){
        filteredData = filteredData.filter(tableData => tableData.city === cityValue);
    } 

    // Select the state input element and get the raw HTML node
    inputElement = d3.select("#state");
    var stateValue = inputElement.property("value");
    // Filter the table based on state
    if (stateValue != ""){
        filteredData = filteredData.filter(tableData => tableData.state === stateValue);
    } 

    // Select the country input element and get the raw HTML node
    inputElement = d3.select("#country");
    var countryValue = inputElement.property("value");
    // Filter the table based on country
    if (countryValue != ""){
        filteredData = filteredData.filter(tableData => tableData.country === countryValue);
    } 

    // Select the shape input element and get the raw HTML node
    inputElement = d3.select("#shape");
    var shapeValue = inputElement.property("value");
    // Filter the table based on shape
    if (shapeValue != ""){
        filteredData = filteredData.filter(tableData => tableData.shape === shapeValue);
    } 

    updateTable(filteredData);
}

function resetTable() {
    location.reload();
}
updateDatalists(tableData);
updateTable(tableData);
d3.select("#filter-btn").on("click", filterSightings);
d3.select("#reset-btn").on("click", resetTable);