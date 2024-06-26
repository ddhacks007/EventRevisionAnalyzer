function addOptions(selectElementId, options) {
    const selectElement = document.getElementById(selectElementId);
    options.forEach(optionValue => {
        let option = new Option(optionValue, optionValue);
        selectElement.add(option);
    });
}

function roundNumber(pf) {
    pf = pf * 100;
    value = parseFloat(pf.toFixed(1));
    if (Number.isInteger(value)) {
        console.log(value)
        return parseInt(value);
    } else {
        console.log(value)
        return value;
    }
}

function updateQueryParams(triggeringElement) {
    const value = triggeringElement.value;
    const queryParams = new URLSearchParams(window.location.search);
    queryParams.set(triggeringElement.id, value);
    window.location.search = queryParams.toString();
}

function setDefaultValues() {
    const queryParams = new URLSearchParams(window.location.search);

    const selectIds = ['timeperiod', 'tag', 'title', 'event'];

    selectIds.forEach(id => {
        if (queryParams.has(id)) {
            const value = queryParams.get(id);
            const selectElement = document.getElementById(id);
            const optionToSelect = [...selectElement.options].find(option => option.value === value);
            if (optionToSelect) {
                optionToSelect.selected = true;
            }
        }
    });
}
