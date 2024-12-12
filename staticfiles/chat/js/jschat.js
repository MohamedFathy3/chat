// فتح نافذة المحادثة مع اسم المستخدم
function openChatWindow(userName) {
    const chatWindow = document.getElementById('chatWindow');
    chatWindow.style.display = 'block';
    
    // تعيين اسم الشخص المتصل في العنوان
    setChatUserName(userName);
}

// تحديث اسم المستخدم في أعلى النافذة
function setChatUserName(userName) {
    document.getElementById('chatUserName').textContent = 'محادثة مع ' + userName;
}


// إغلاق نافذة المحادثة
function closeChatWindow() {
    const chatWindow = document.getElementById('chatWindow');
    chatWindow.style.display = 'none';
}

// إرسال رسالة
function sendMessage() {
    const messageInput = document.getElementById('messageInput1');
    const chatBody = document.getElementById('chatBody');

    // التأكد أن المستخدم كتب رسالة
    if (messageInput.value.trim() !== '') {
        // إضافة الرسالة إلى النافذة
        const newMessage = document.createElement('div');
        newMessage.classList.add('message', 'mb-2', 'p-2', 'bg-light', 'rounded');
        newMessage.innerHTML = messageInput.value; // استخدم innerHTML للسماح بإدخال النصوص المزخرفة
        chatBody.appendChild(newMessage);

        // تمرير النص إلى الأسفل بعد كل رسالة جديدة
        chatBody.scrollTop = chatBody.scrollHeight;

        // مسح النص المدخل
        messageInput.value = '';
    }
}

// تغيير مكان نافذة المحادثة حسب الخيار المحدد
function moveChatWindow(position) {
    const chatWindow = document.getElementById('chatWindow');
    
    // إزالة الفئات السابقة قبل إضافة الفئة الجديدة
    chatWindow.classList.remove('top-left', 'top-right', 'bottom-left', 'bottom-right');
    
    // إضافة الفئة الجديدة للموقع المحدد
    chatWindow.classList.add(position);
}

// التبديل بين إظهار واخفاء قائمة الإيموجي
function toggleEmojiPicker() {
    const emojiPicker1 = document.getElementById('emojiPicker1');
    emojiPicker1.style.display = (emojiPicker1.style.display === 'none' || emojiPicker1.style.display === '') ? 'block' : 'none';
}

// التبديل بين إظهار واخفاء قائمة النصوص المزخرفة
function toggleTextStylePicker() {
    const textStylePicker = document.getElementById('textStylePicker');
    textStylePicker.style.display = (textStylePicker.style.display === 'none' || textStylePicker.style.display === '') ? 'block' : 'none';
}

// إضافة الإيموجي إلى حقل الرسالة
function addEmoji(emoji) {
    const messageInput = document.getElementById('messageInput1');
    messageInput.value += emoji;
    toggleEmojiPicker();  // إغلاق قائمة الإيموجي بعد تحديد الإيموجي
}

// إضافة نص مزخرف إلى حقل الرسالة
function addDecorativeText(text) {
    const messageInput = document.getElementById('messageInput1');
    messageInput.value += text;
    toggleTextStylePicker();  // إغلاق قائمة النصوص المزخرفة بعد تحديد النص
}
