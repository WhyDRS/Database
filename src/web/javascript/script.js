// Constants for configuration
const CONFIG = {
    dataUrl: '/data/Issuers/Full_Database_Backend.json',
    defaultVisibleColumns: [0, 1, 2, 3, 8, 9],
    pageLength: 100,
    lengthMenu: [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
};

// Wait for the DOM to be fully loaded before executing the script
document.addEventListener("DOMContentLoaded", function () {
    const elements = {
        loadingOverlay: document.getElementById('loading-overlay'),
        dataTable: document.getElementById('data-table')
    };

    // Function to show error message to user
    function showError(message) {
        elements.loadingOverlay.innerHTML = `
            <div class="error-message">
                <p>Error: ${message}</p>
                <button onclick="window.location.reload()">Retry</button>
            </div>
        `;
    }

    // Function to initialize DataTable with the provided data
    function initializeDataTable(data, headers) {
        const columns = headers.map((header, index) => ({
            data: header,
            title: header.replace(/_/g, ' '),
            visible: CONFIG.defaultVisibleColumns.includes(index)
        }));

        const table = $('#data-table').DataTable({
            data,
            columns,
            dom: '<"top"Bf>rt<"bottom"lip><"clear">',
            buttons: [
                {
                    extend: 'colvis',
                    text: 'Select Columns',
                    columns: ':not(:first-child)'
                },
                {
                    text: 'Reset Columns',
                    action: function (e, dt) {
                        dt.state.clear();
                        dt.columns().visible(false);
                        CONFIG.defaultVisibleColumns.forEach(colIndex => {
                            dt.column(colIndex).visible(true);
                        });
                        dt.columns.adjust().draw(false);
                        dt.state.save();
                    }
                }
            ],
            stateSave: true,
            stateDuration: -1,
            initComplete: function () {
                elements.loadingOverlay.classList.add('hidden');
                elements.dataTable.classList.remove('hidden');
            },
            pagingType: "full_numbers",
            language: {
                search: "",
                searchPlaceholder: "Search records"
            },
            pageLength: CONFIG.pageLength,
            lengthMenu: [CONFIG.lengthMenu, CONFIG.lengthMenu],
            order: [[0, 'asc']],
            autoWidth: false,
            deferRender: true,
            processing: true
        });

        // Optimize column visibility changes
        table.on('column-visibility.dt', function (e, settings, column, state) {
            requestAnimationFrame(() => {
                table.columns.adjust().draw(false);
            });
        });

        // Add responsive window resize handler
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                table.columns.adjust();
            }, 250);
        });
    }

    // Function to load and process data
    async function loadData() {
        try {
            const response = await fetch(CONFIG.dataUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            if (!data || !data.length) {
                throw new Error('No data received from the server');
            }

            const headers = Object.keys(data[0]);
            $(document).ready(() => initializeDataTable(data, headers));
        } catch (error) {
            console.error('Error loading the data:', error);
            showError(error.message || 'Failed to load data. Please try again later.');
            elements.loadingOverlay.classList.add('error');
        }
    }

    // Start loading data
    loadData();
});
