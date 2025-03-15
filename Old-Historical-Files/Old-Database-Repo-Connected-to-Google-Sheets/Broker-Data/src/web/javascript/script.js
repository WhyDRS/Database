document.addEventListener("DOMContentLoaded", function () {
    const loadingOverlay = document.getElementById('loading-overlay');
    const dataTableElement = document.getElementById('data-table');

    function loadData() {
        fetch('Broker-Data/data/DRSGME_Broker_Guides.json')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(jsonData => {
                console.log('JSON Data:', jsonData);
                if (!jsonData.fields || !jsonData.data || !Array.isArray(jsonData.data) || jsonData.data.length === 0) {
                    throw new Error('Data is empty or not in the expected format');
                }
                const columns = jsonData.fields.map(field => ({
                    data: null,
                    title: field,
                    render: function (data, type, row, meta) {
                        return row[meta.col];
                    }
                }));
                $(document).ready(function () {
                    var table = $('#data-table').DataTable({
                        data: jsonData.data,
                        columns: columns,
                        dom: '<"top"Bf>rt<"bottom"lip><"clear">',
                        buttons: ['colvis'],
                        stateSave: true,
                        autoWidth: false
                    });
                    loadingOverlay.classList.add('hidden');
                    dataTableElement.classList.remove('hidden');
                });
            })
            .catch(error => {
                console.error('Error loading the data:', error.message);
                loadingOverlay.classList.add('hidden');
                dataTableElement.textContent = 'Failed to load data. Please try again later.';
                dataTableElement.classList.remove('hidden');
            });
    }
    loadData();
});
