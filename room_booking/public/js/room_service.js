async function deserializeFormData(formSelector) {
    return $(formSelector).serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
}

async function bookRoom() {
    var formData = $("#roomBookingForm").serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});;
    var bookingDetails = {
        first_name: formData["guestFirstName"],
        middle_name: formData["guestMiddleName"],
        last_name: formData["guestLastName"],
        email: formData["guestEmail"],
        phone_number: formData["guestPhoneNumber"],
        address: {
            address_line: formData["guestAddressLine"],
            city: formData["guestCity"],
            state: formData["guestState"]
        },
        booking_detail: {
            check_in: formData["checkin"],
            check_out: formData["checkout"],
            room: ""
        }
    }
    $.ajax({
        method: 'POST',
        url: 'api/method/room_booking.www.room-booking.index.book_room',
        data: JSON.stringify(bookingDetails),
        headers: {
            'X-Frappe-CSRF-Token': formData._token
        },
        dataType: 'json',
        success: function(response) {
            console.log(response);
        }
    });
}