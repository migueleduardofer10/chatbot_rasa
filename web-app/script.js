jQuery(document).ready(function($) {
    
 // Código para cargar los datos de la tabla desde el CSV
 fetch('/data/indicadores_demograficos.csv')
 .then(response => {
     console.log('Response:', response);
     return response.text();
 })
 .then(data => {
     console.log('Data:', data);
     const rows = data.split('\n');
     const tableHead = document.querySelector('#data-table thead tr');
     const tableBody = document.querySelector('#data-table tbody');

     // Crear encabezados de tabla
     const headers = rows[0].split(',');
     headers.forEach(header => {
         const th = document.createElement('th');
         th.textContent = header;
         tableHead.appendChild(th);
     });

     // Crear filas de datos
     rows.slice(1).forEach((row, index) => {
         const cols = row.split(',');
         console.log(`Row ${index + 1} columns:`, cols);
         if (cols.length > 1) {
             const tr = document.createElement('tr');
             cols.forEach(col => {
                 const td = document.createElement('td');
                 td.textContent = col;
                 tr.appendChild(td);
             });
             tableBody.appendChild(tr);
         }
     });
 })
 .catch(error => console.error('Error loading the CSV file:', error));
 
    
    jQuery(document).on('click', '.iconInner', function(e) {
        jQuery(this).parents('.botIcon').addClass('showBotSubject');
        $("[name='msg']").focus();
    });

    jQuery(document).on('click', '.closeBtn, .chat_close_icon', function(e) {
        jQuery(this).parents('.botIcon').removeClass('showBotSubject');
        jQuery(this).parents('.botIcon').removeClass('showMessenger');
    });

    jQuery(document).on('submit', '#botSubject', function(e) {
        e.preventDefault();

        jQuery(this).parents('.botIcon').removeClass('showBotSubject');
        jQuery(this).parents('.botIcon').addClass('showMessenger');
    });
    
    /* Chatbot Code */
    $(document).on("submit", "#messenger", function(e) {
        e.preventDefault();

        var userMessage = $("[name=msg]").val();
        if (userMessage.trim() === "") {
            return;
        }

        appendUserMessage(userMessage);
        sendMessageToRasa(userMessage);
    });

    function appendUserMessage(message) {
        $('.Messages_list').append('<div class="msg user"><span class="avtr"><figure style="background-image: url(https://mrseankumar25.github.io/Sandeep-Kumar-Frontend-Developer-UI-Specialist/images/avatar.png)"></figure></span><span class="responsText">' + message + '</span></div>');
        $("[name='msg']").val("");
        scrollToBottom();
    }

    function appendBotMessage(message) {
        $('.Messages_list').append('<div class="msg"><span class="avtr"><figure style="background-image: url(https://mrseankumar25.github.io/Sandeep-Kumar-Frontend-Developer-UI-Specialist/images/avatar.png)"></figure></span><span class="responsText">' + message + '</span></div>');
        scrollToBottom();
    }

    function scrollToBottom() {
        var lastMsg = $('.Messages_list').find('.msg').last().offset().top;
        $('.Messages').animate({scrollTop: lastMsg}, 'slow');
    }

    function sendMessageToRasa(message) {
        fetch('http://localhost:5005/webhooks/rest/webhook', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                data.forEach(msg => {
                    appendBotMessage(msg.text);
                });
            } else {
                appendBotMessage("Sorry, I didn't understand that.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            appendBotMessage("Sorry, there was an error processing your request.");
        });
    }

    
});
