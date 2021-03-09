async function getAvailableRoom() {
    var formData = $('#roomSearchForm').serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
    $.ajax({
        method: 'GET',
        url: '/room-search',
        data: {
            cmd: 'room_booking.www.room-search.index.get_available_rooms',
            from_date: formData.fromDate,
            to_date: formData.toDate,
            capacity: formData.capacity
        },
        dataType: 'json',
        success: function(response) {
            console.log(response);
        }
    })
}