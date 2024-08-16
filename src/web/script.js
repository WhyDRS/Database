// Assuming your JSON file is named 'Full_Database_Backend.json' and is in the same directory
document.addEventListener("DOMContentLoaded", function() {
    const loadingBar = document.getElementById('loading-bar');
    const dataTable = document.getElementById('data-table');

    // Show the loading bar
    loadingBar.style.display = 'block';

    // Function to fetch and load data
    function loadData() {
        fetch('/data/Full_Database_Backend.json') // Asynchronously fetches the JSON file
            .then(response => response.json()) // Parses the JSON file
            .then(data => {
                const table = document.getElementById('data-table'); // Gets the table element by its ID
                
                // Clear previous table body
                table.tBodies[0].innerHTML = ''; // Clears the existing table body content

                // Create table headers from the keys of the first JSON object
                const headers = Object.keys(data[0]); // Extracts keys to use as table headers
                const headerRow = document.createElement('tr'); // Creates a table row for headers
                headers.forEach(headerText => {
                    const header = document.createElement('th'); // Creates a table header cell
                    header.textContent = headerText.replace(/([A-Z])/g, ' $1').trim(); // Formats header text to include spaces before capital letters
                    headerRow.appendChild(header); // Appends the header cell to the header row
                });
                table.tHead.innerHTML = '';  // Clears any existing headers
                table.tHead.appendChild(headerRow); // Appends the new header row to the table header

                // Create the table body rows
                data.forEach(rowData => {
                    const row = document.createElement('tr'); // Creates a table row
                    Object.values(rowData).forEach(cellData => {
                        const cell = document.createElement('td'); // Creates a table cell
                        cell.textContent = cellData; // Sets the text content of the cell
                        row.appendChild(cell); // Appends the cell to the row
                    });
                    table.tBodies[0].appendChild(row); // Appends the row to the table body
                });

                // Initialize DataTables
                $(document).ready(function() {
                    $('#data-table').DataTable({
                        "initComplete": function(settings, json) {
                            // Hide the loading bar and show the table after DataTables initialization is complete
                            loadingBar.style.display = 'none';
                            dataTable.style.display = 'table';
                        }
                    });
                });
            })
            .catch(error => {
                console.error('Error loading the data:', error); // Logs any errors to the console

                // Hide the loading bar even if there's an error
                loadingBar.style.display = 'none';
            });
    }

    // Load the data
    loadData();
});