 $(document).ready(function() {
        // إرسال رسالة عند الضغط على زر الإرسال
        $('#sendButton').click(function() {
            var message = $('#messageInput').val();
            if (message.trim() !== '') {
                var currentTime = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
                var messageHTML = `
                    <div class="message user">
                        <div class="text">${message}</div>
                        <div class="time">${currentTime}</div>
                    </div>
                `;
                $('#chatBox').append(messageHTML);
                $('#messageInput').val(''); // مسح المدخل بعد الإرسال
                $('#chatBox').scrollTop($('#chatBox')[0].scrollHeight); // التمرير لأسفل لإظهار الرسالة الجديدة
            }
        });

        // إرسال الرسالة عند الضغط على Enter
        $('#messageInput').keypress(function(event) {
            if (event.which === 13) {
                $('#sendButton').click();
            }
        });

        // إظهار نافذة الإعدادات
        $('#settingsButton').click(function() {
            $('#settingsModal').fadeIn();
        });

        // إغلاق نافذة الإعدادات
        $('#closeSettingsButton').click(function() {
            $('#settingsModal').fadeOut();
        });

        // حفظ الإعدادات وتطبيقها
        $('#saveSettingsButton').click(function() {
            var nickname = $('#nickname').val();
            var status = $('#status').val();
            var nameColor = $('#nameColor').val();
            var backgroundColor = $('#backgroundColor').val();
            var textColor = $('#textColor').val();
            var statusColor = $('#statusColor').val();
            var fontSize = $('#fontSize').val();
            var disableVisualNotifications = $('#disableVisualNotifications').is(':checked');
            var disableSoundNotifications = $('#disableSoundNotifications').is(':checked');
            var disablePrivateMessages = $('#disablePrivateMessages').is(':checked');
            var hideStar = $('#hideStar').is(':checked');
            var deleteProfilePic = $('#deleteProfilePic').is(':checked');
            var deleteBackgroundPic = $('#deleteBackgroundPic').is(':checked');

            // تطبيق الإعدادات
            if (nickname) {
                $('.custom-name').text(nickname);
            }
            if (status) {
                $('.custom-status').text(status);
            }

            // تغيير الألوان
            $('body').css({
                'color': textColor,
                'background-color': backgroundColor
            });

            $('.custom-name').css('color', nameColor);
            $('.custom-status').css('color', statusColor);

            // تغيير حجم الخط
            $('.message').css('font-size', fontSize + 'px');

            // إخفاء/إظهار الإشعارات
            if (disableVisualNotifications) {
                alert('تم تعطيل الإشعارات المرئية');
            }

            if (disableSoundNotifications) {
                alert('تم تعطيل الإشعارات الصوتية');
            }

            if (disablePrivateMessages) {
                alert('تم تعطيل استقبال رسائل الخاص');
            }

            if (hideStar) {
                alert('تم إخفاء النجمة');
            }

            // حذف الصور (إن تم تحديدها)
            if (deleteProfilePic) {
                alert('تم حذف صورة الرمزية');
            }
            if (deleteBackgroundPic) {
                alert('تم حذف صورة البطاقة');
            }

            $('#settingsModal').fadeOut(); // إغلاق نافذة الإعدادات
        });

        // إظهار التنبيه عند الضغط على زر التنبيهات
        $('#alertButton').click(function() {
            $('#alertMessage').toggle(); // إظهار/إخفاء التنبيه
        });
    });