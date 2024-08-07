// Assuming your JSON file is named 'Full_Database_Backend.json' and is in the same directory
fetch('/data/Full_Database_Backend.json') // Asynchronously fetches the JSON file
    .then(response => response.json()) // Parses the JSON file
    .then(data => {
        const table = document.getElementById('data-table'); // Gets the table element by its ID
        const chunkSize = 100; // Number of rows to load at a time
        let currentIndex = 0;

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

        // Function to load a chunk of data
        function loadChunk() {
            const fragment = document.createDocumentFragment();
            for (let i = currentIndex; i < currentIndex + chunkSize && i < data.length; i++) {
                const rowData = data[i];
                const row = document.createElement('tr'); // Creates a table row
                Object.values(rowData).forEach(cellData => {
                    const cell = document.createElement('td'); // Creates a table cell
                    cell.textContent = cellData; // Sets the text content of the cell
                    row.appendChild(cell); // Appends the cell to the row
                });
                fragment.appendChild(row); // Appends the row to the fragment
            }
            table.tBodies[0].appendChild(fragment); // Appends the fragment to the table body
            currentIndex += chunkSize;

            // If there are more records to load, continue loading
            if (currentIndex < data.length) {
                setTimeout(loadChunk, 0); // Schedule the next chunk to be loaded
            } else {
                // Initialize DataTables after all data is loaded
                $(document).ready(function () {
                    $('#data-table').DataTable(); // Initializes the DataTables plugin on the table
                });
            }
        }

        // Load the initial chunk
        loadChunk();
    })
    .catch(error => {
        console.error('Error loading the data:', error); // Logs any errors to the console
    });
