// Wait for the DOM to be fully loaded before executing the script
document.addEventListener("DOMContentLoaded", function () {
    // Get references to the loading overlay and data table elements
    const loadingOverlay = document.getElementById('loading-overlay');
    const dataTableElement = document.getElementById('data-table');

    // The loading overlay is visible by default (set in CSS)
    // The data table is hidden by default (has 'hidden' class)

    // Define the default visible columns by their indices (zero-based)
    const defaultVisibleColumns = [0, 1, 2, 3, 8, 9];

    // Function to load data from the JSON file and initialize the DataTable
    function loadData() {
        // Fetch data from the JSON file located at '/data/Full_Database_Backend.json'
        fetch('/data/Issuers/Full_Database_Backend.json')
            .then(response => response.json()) // Parse the JSON response
            .then(data => {
                // Extract headers (keys) from the first data object to use as column names
                const headers = Object.keys(data[0]);

                // Map headers to DataTables column definitions
                const columns = headers.map((header, index) => ({
                    // Specify the data property for the column
                    data: header,
                    // Replace underscores with spaces instead of adding spaces before capitals
                    title: header.replace(/_/g, ' '),
                    // Set column visibility based on defaultVisibleColumns array
                    visible: defaultVisibleColumns.includes(index)
                }));

                // Initialize the DataTable once the document is ready
                $(document).ready(function () {
                    // Initialize the DataTable with the specified options
                    var table = $('#data-table').DataTable({
                        // Set the data source for the table
                        data: data,
                        // Define the columns configuration
                        columns: columns,
                        // Define the table control elements layout
                        dom: '<"top"Bf>rt<"bottom"lip><"clear">',
                        // Define the buttons to be displayed
                        buttons: [
                            {
                                // Add a column visibility control button
                                extend: 'colvis',
                                // Set the button text
                                text: 'Select Columns',
                                // Exclude the first column (index 0) from the column visibility list
                                columns: ':not(:first-child)'
                            },
                            {
                                // Add a custom button to reset column visibility
                                text: 'Reset Columns',
                                // Define the action to be performed when the button is clicked
                                action: function (e, dt, node, config) {
                                    // Clear any saved state to reset to default
                                    dt.state.clear();

                                    // Hide all columns
                                    dt.columns().visible(false);

                                    // Show only the default visible columns
                                    defaultVisibleColumns.forEach(function (colIndex) {
                                        dt.column(colIndex).visible(true);
                                    });

                                    // Adjust columns and redraw the table without changing the page
                                    dt.columns.adjust().draw(false);

                                    // Save the new state
                                    dt.state.save();
                                }
                            }
                        ],
                        // Enable state saving to remember column visibility and other settings
                        "stateSave": true,
                        // Save the state indefinitely (-1 means no expiration)
                        "stateDuration": -1,
                        // Callback function executed once the table initialization is complete
                        "initComplete": function (settings, json) {
                            // Hide the loading overlay
                            loadingOverlay.classList.add('hidden');

                            // Show the data table by removing the 'hidden' class
                            dataTableElement.classList.remove('hidden');
                        },
                        // Define the pagination control type
                        "pagingType": "full_numbers",
                        // Customize the language settings
                        "language": {
                            // Remove the default search label text
                            "search": "",
                            // Set a placeholder for the search input field
                            "searchPlaceholder": "Search records"
                        },
                        // Set the default number of rows per page
                        "pageLength": 100,
                        // Define the options for the number of rows per page
                        "lengthMenu": [
                            // Page length options
                            [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
                            // Labels for the options
                            [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
                        ],
                        // Set the default sorting order (by the first column ascending)
                        "order": [[0, 'asc']],
                        // Disable automatic column width calculation for better performance
                        "autoWidth": false
                    });

                    // Adjust table columns when column visibility changes
                    table.on('column-visibility.dt', function (e, settings, column, state) {
                        // Adjust the column sizes and redraw the table without changing the page
                        table.columns.adjust().draw(false);
                    });
                });
            })
            .catch(error => {
                // Log any errors to the console for debugging
                console.error('Error loading the data:', error);

                // Hide the loading overlay in case of error to prevent blocking the UI
                loadingOverlay.classList.add('hidden');
            });
    }

    // Call the loadData function to fetch data and initialize the table
    loadData();
});
