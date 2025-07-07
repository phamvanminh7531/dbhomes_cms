// static/js/custom_slug.js
(function() {
    'use strict';
    
    // Bản đồ chuyển đổi ký tự tiếng Việt
    const vietnameseMap = {
        'à': 'a', 'á': 'a', 'ạ': 'a', 'ả': 'a', 'ã': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ậ': 'a', 'ẩ': 'a', 'ẫ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ặ': 'a', 'ẳ': 'a', 'ẵ': 'a',
        'è': 'e', 'é': 'e', 'ẹ': 'e', 'ẻ': 'e', 'ẽ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ệ': 'e', 'ể': 'e', 'ễ': 'e',
        'ì': 'i', 'í': 'i', 'ị': 'i', 'ỉ': 'i', 'ĩ': 'i',
        'ò': 'o', 'ó': 'o', 'ọ': 'o', 'ỏ': 'o', 'õ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ộ': 'o', 'ổ': 'o', 'ỗ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ợ': 'o', 'ở': 'o', 'ỡ': 'o',
        'ù': 'u', 'ú': 'u', 'ụ': 'u', 'ủ': 'u', 'ũ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ự': 'u', 'ử': 'u', 'ữ': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỵ': 'y', 'ỷ': 'y', 'ỹ': 'y',
        'đ': 'd',
        // Uppercase
        'À': 'A', 'Á': 'A', 'Ạ': 'A', 'Ả': 'A', 'Ã': 'A',
        'Â': 'A', 'Ầ': 'A', 'Ấ': 'A', 'Ậ': 'A', 'Ẩ': 'A', 'Ẫ': 'A',
        'Ă': 'A', 'Ằ': 'A', 'Ắ': 'A', 'Ặ': 'A', 'Ẳ': 'A', 'Ẵ': 'A',
        'È': 'E', 'É': 'E', 'Ẹ': 'E', 'Ẻ': 'E', 'Ẽ': 'E',
        'Ê': 'E', 'Ề': 'E', 'Ế': 'E', 'Ệ': 'E', 'Ể': 'E', 'Ễ': 'E',
        'Ì': 'I', 'Í': 'I', 'Ị': 'I', 'Ỉ': 'I', 'Ĩ': 'I',
        'Ò': 'O', 'Ó': 'O', 'Ọ': 'O', 'Ỏ': 'O', 'Õ': 'O',
        'Ô': 'O', 'Ồ': 'O', 'Ố': 'O', 'Ộ': 'O', 'Ổ': 'O', 'Ỗ': 'O',
        'Ơ': 'O', 'Ờ': 'O', 'Ớ': 'O', 'Ợ': 'O', 'Ở': 'O', 'Ỡ': 'O',
        'Ù': 'U', 'Ú': 'U', 'Ụ': 'U', 'Ủ': 'U', 'Ũ': 'U',
        'Ư': 'U', 'Ừ': 'U', 'Ứ': 'U', 'Ự': 'U', 'Ử': 'U', 'Ữ': 'U',
        'Ỳ': 'Y', 'Ý': 'Y', 'Ỵ': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y',
        'Đ': 'D',
    };
    
    // Hàm chuyển đổi tiếng Việt sang slug
    function vietnameseSlugify(text) {
        // Loại bỏ dấu tiếng Việt
        let result = text;
        for (let [viet, eng] of Object.entries(vietnameseMap)) {
            result = result.replace(new RegExp(viet, 'g'), eng);
        }
        
        // Chuyển thành lowercase và thay thế ký tự không phải chữ/số bằng dấu gạch ngang
        result = result.toLowerCase()
            .replace(/[^a-z0-9]/g, '-')
            .replace(/-+/g, '-')
            .replace(/^-|-$/g, '');
        
        return result;
    }
    
    // Hàm khởi tạo slug generator
    function initCustomSlugGenerator() {
        const titleField = document.getElementById('id_title');
        const slugField = document.getElementById('id_slug');
        
        if (!titleField || !slugField) {
            return;
        }
        
        // Biến để theo dõi trạng thái slug có được edit thủ công không
        let slugManuallyEdited = false;
        
        // Kiểm tra nếu slug đã có giá trị (editing existing page)
        if (slugField.value.trim() !== '') {
            slugManuallyEdited = true;
        }
        
        // Event listener cho slug field để detect manual editing
        slugField.addEventListener('input', function() {
            if (this.value.trim() !== '') {
                slugManuallyEdited = true;
            }
        });
        
        // Event listener cho title field để auto-generate slug
        titleField.addEventListener('input', function() {
            if (!slugManuallyEdited) {
                const newSlug = vietnameseSlugify(this.value);
                slugField.value = newSlug;
                
                // Trigger change event để các component khác nhận biết
                const changeEvent = new Event('change', { bubbles: true });
                slugField.dispatchEvent(changeEvent);
            }
        });
        
        // Thêm nút reset slug
        const slugWrapper = slugField.closest('.field');
        if (slugWrapper) {
            const resetButton = document.createElement('button');
            resetButton.type = 'button';
            resetButton.className = 'button button-small';
            resetButton.textContent = 'Reset từ Title';
            resetButton.style.marginLeft = '10px';
            
            resetButton.addEventListener('click', function(e) {
                e.preventDefault();
                const newSlug = vietnameseSlugify(titleField.value);
                slugField.value = newSlug;
                slugManuallyEdited = false;
                
                // Trigger change event
                const changeEvent = new Event('change', { bubbles: true });
                slugField.dispatchEvent(changeEvent);
            });
            
            const slugFieldContainer = slugField.parentNode;
            slugFieldContainer.appendChild(resetButton);
        }
    }
    
    // Khởi tạo khi DOM ready
    document.addEventListener('DOMContentLoaded', function() {
        initCustomSlugGenerator();
    });
    
    // Khởi tạo lại khi Wagtail admin load content qua AJAX
    document.addEventListener('wagtail:tab-changed', function() {
        initCustomSlugGenerator();
    });
    
    // Expose function globally nếu cần
    window.vietnameseSlugify = vietnameseSlugify;
})();