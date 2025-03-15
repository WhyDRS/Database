/**
 * Configuration object for DataTables.
 * Adjust these values to change behavior like data source,
 * default visible columns, and pagination settings.
 */
const CONFIG = {
    // URL where the JSON data is hosted
    dataUrl: '/data/Issuers/Main_Database.json',
  
    // By default, which columns should be visible? 
    // (indexing columns in the order they appear in the JSON keys array)
    defaultVisibleColumns: [0, 1, 2, 3, 8, 9],
  
    // Default number of rows shown per page
    pageLength: 100,
  
    // Array of page length options for the dropdown
    lengthMenu: [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
  };
  
  /**
   * Main script block: runs after the DOM has fully loaded.
   */
  document.addEventListener('DOMContentLoaded', function () {
    // Cache DOM elements for easy reference
    const elements = {
      loadingOverlay: document.getElementById('loading-overlay'),
      dataTable: document.getElementById('data-table'),
      stickyBottomBar: document.getElementById('sticky-bottom-bar')
    };
  
    // Add event listener for the close button
    if (elements.stickyBottomBar) {
        const closeButton = elements.stickyBottomBar.querySelector('.close-button');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                elements.stickyBottomBar.style.display = 'none';
            });
        }
    }
  
    /**
     * Displays an error message and provides a "Retry" button that reloads the page.
     * @param {string} message - The error message to display.
     */
    function showError(message) {
      elements.loadingOverlay.innerHTML = `
        <div class="error-message">
          <p>Error: ${message}</p>
          <button onclick="window.location.reload()">Retry</button>
        </div>
      `;
    }
  
    /**
     * Initialize the DataTable with the given data and column headers.
     * @param {Array} data - Array of data objects (rows).
     * @param {Array} headers - Array of header strings (column names).
     */
    function initializeDataTable(data, headers) {
      // Create column configurations for DataTables
      const columns = headers.map((header, index) => ({
        data: header, // which property of the row object to display in this column
        title: header.replace(/_/g, ' '), // convert underscores to spaces for readability
        visible: CONFIG.defaultVisibleColumns.includes(index) // whether the column is initially visible
      }));
  
      // Use jQuery to initialize the DataTable on the selected element (#data-table)
      const table = $('#data-table').DataTable({
        data: data,          // the row data
        columns: columns,    // the column definitions
        dom: '<"top"Bf>rt<"bottom"lip><"clear">', 
        /*
         * dom explanation:
         * <"top"Bf>: places Buttons and the filter ("f") in the top container
         * rt: the table ('r' = processing display element, 't' = table)
         * <"bottom"lip>: places length ("l"), info ("i"), and pagination ("p") in the bottom container
         * <"clear">: a clearing element
         */
  
        // Buttons to toggle column visibility and reset columns
        buttons: [
          {
            extend: 'colvis',
            text: 'Select Columns',
            columns: ':not(:first-child)' // allow toggling of all columns except the first, if desired
          },
          {
            text: 'Reset Columns',
            action: function (e, dt) {
              // Clear saved state and reset column visibility
              dt.state.clear();
              dt.columns().visible(false); // hide all columns
              // Show only the default columns
              CONFIG.defaultVisibleColumns.forEach((colIndex) => {
                dt.column(colIndex).visible(true);
              });
              dt.columns.adjust().draw(false); // redraw table
              dt.state.save(); // persist the state
            }
          }
        ],
        stateSave: true,       // ensures user preferences (column visibility, etc.) are remembered
        stateDuration: -1,     // -1 means state is saved indefinitely (until browser data is cleared)
        initComplete: function () {
          // Hide loading overlay and reveal table once initialization is done
          elements.loadingOverlay.classList.add('hidden');
          elements.dataTable.classList.remove('hidden');
        },
        pagingType: 'full_numbers', // displays first/last and previous/next buttons
        language: {
          search: '',
          searchPlaceholder: 'Search records' // placeholder text in the search input
        },
        pageLength: CONFIG.pageLength, // default page length
        lengthMenu: [CONFIG.lengthMenu, CONFIG.lengthMenu], // sets the same values for display
        order: [[0, 'asc']], // sorts by the first column ascending by default
        autoWidth: false,     // disables automatic column width calculation, so columns can shrink/grow
        deferRender: true,    // defer rendering for large datasets for performance
        processing: true      // show "processing" indicator if table is processing user input
      });
  
      // Handle column visibility changes, adjust the layout to fit new column widths
      table.on('column-visibility.dt', function () {
        requestAnimationFrame(() => {
          table.columns.adjust().draw(false);
        });
      });
  
      // Adjust columns on window resize to keep them responsive
      let resizeTimeout;
      window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
          table.columns.adjust();
        }, 250); // delay the adjustment for performance reasons
      });
    }
  
    /**
     * Fetch data from the configured URL, then initialize the table.
     */
    async function loadData() {
      try {
        // Send a GET request to the server for the JSON data
        const response = await fetch(CONFIG.dataUrl);
  
        // Throw an error if the HTTP status isn't 200-299
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
  
        // Parse JSON response
        const data = await response.json();
  
        // If data is empty or not an array, throw an error
        if (!data || !data.length) {
          throw new Error('No data received from the server');
        }
  
        // Extract table headers from the first object's keys (assuming uniform structure)
        const headers = Object.keys(data[0]);
  
        // Initialize DataTable with the data and headers once the DOM is ready
        $(document).ready(() => {
          initializeDataTable(data, headers);
        });
  
      } catch (error) {
        // Log the error for debugging and show the user an error message
        console.error('Error loading the data:', error);
        showError(error.message || 'Failed to load data. Please try again later.');
        elements.loadingOverlay.classList.add('error');
      }
    }
  
    // Start the data load process when the DOM is fully loaded
    loadData();
  });
  