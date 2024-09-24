// Assuming your JSON file is named 'Full_Database_Backend.json' and is in the same directory
document.addEventListener("DOMContentLoaded", function () {
    const loadingOverlay = document.getElementById('loading-overlay');
    const dataTableElement = document.getElementById('data-table');

    // Show the loading overlay
    loadingOverlay.style.display = 'flex';

    // Define the default visible columns
    const defaultVisibleColumns = [0, 1, 2, 3, 8, 9];

    // Function to fetch and load data
    function loadData() {
        fetch('/data/Full_Database_Backend.json')
            .then(response => response.json())
            .then(data => {
                // Extract headers from the data
                const headers = Object.keys(data[0]);

                // Create columns array with 'data', 'title', and 'visible'
                const columns = headers.map((header, index) => ({
                    data: header,
                    title: header.replace(/([A-Z])/g, ' $1').trim(),
                    visible: defaultVisibleColumns.includes(index) // Set visibility based on default
                }));

                // Initialize DataTables
                $(document).ready(function () {
                    var table = $('#data-table').DataTable({
                        data: data,
                        columns: columns,
                        dom: '<"top"Bf>rt<"bottom"lip><"clear">',
                        buttons: [
                            {
                                extend: 'colvis',
                                text: 'Select Columns',
                                columns: ':not(:first-child)'
                            },
                            {
                                text: 'Reset Columns',
                                action: function (e, dt, node, config) {
                                    // Clear the saved state in localStorage
                                    dt.state.clear();

                                    // Reset all columns to invisible
                                    dt.columns().visible(false);

                                    // Set default columns to visible
                                    defaultVisibleColumns.forEach(function (colIndex) {
                                        dt.column(colIndex).visible(true);
                                    });

                                    // Adjust column widths and redraw table
                                    dt.columns.adjust().draw(false);

                                    // Save the new state
                                    dt.state.save();
                                }
                            }
                        ],
                        "stateSave": true,
                        "stateDuration": -1,
                        "initComplete": function (settings, json) {
                            // Hide the loading overlay and show the table after DataTables initialization is complete
                            loadingOverlay.style.display = 'none';
                            dataTableElement.style.display = 'table';
                        },
                        "pagingType": "full_numbers",
                        "language": {
                            "search": "",
                            "searchPlaceholder": "Search records"
                        },
                        "pageLength": 100,
                        "lengthMenu": [
                            [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
                            [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
                        ],
                        "order": [[0, 'asc']],
                        "autoWidth": false // Disable automatic column width calculation
                    });

                    // Event listener to adjust columns when visibility changes
                    table.on('column-visibility.dt', function (e, settings, column, state) {
                        table.columns.adjust().draw(false);
                    });
                });
            })
            .catch(error => {
                console.error('Error loading the data:', error);
                // Hide the loading overlay even if there's an error
                loadingOverlay.style.display = 'none';
            });
    }

    // Load the data
    loadData();
});
